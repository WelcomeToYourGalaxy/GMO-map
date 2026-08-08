#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OGTR crop field trial sites — the one register that publishes locations.

Australia's Office of the Gene Technology Regulator runs an interactive map of
current and post-harvest-monitoring GMO crop field trials, carrying the licence,
the holder, the crop and trait, the area and the site location:

    https://www.ogtr.gov.au/what-weve-approved/crop-field-trial-map

An interactive map is driven by a data endpoint, so the data exists in a
machine-readable form even though no bulk download is advertised. This script
finds that endpoint rather than assuming a URL, for the same reason as the
contamination register: page structure moves, and a hard-coded path fails
silently a year later.

**It checks robots.txt first and stops if the path is disallowed.** That check is
the point of this script existing rather than a scraper: earlier rounds recorded
OGTR as off-limits on the strength of robots.txt, and the right way to act on
that is to ask the file every run rather than to remember an answer.

Why it is worth having: every other release record on this map is
`precise:false`, sitting at a country or state fallback because the register
published no location. **OGTR publishes real coordinates.** These are the only
release points on the map that sit where the thing actually is.

    python3 harvest/ogtr_trials.py --dry-run
    python3 harvest/ogtr_trials.py

Writes harvest/ogtr_trials.json, merged into projects.json by aphis_releases.py.
"""
import io, json, re, sys, pathlib
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "ogtr_trials.json"

BASE = "https://www.ogtr.gov.au"
PAGE = BASE + "/what-weve-approved/crop-field-trial-map"
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"

# Australia's rough bounds, used to reject anything that is not a site coordinate
AU = (-44.0, -9.0, 112.0, 154.0)


def allowed(url):
    """Ask robots.txt. Returns (bool, explanation)."""
    rp = RobotFileParser()
    rp.set_url(BASE + "/robots.txt")
    try:
        rp.read()
    except Exception as e:
        return False, ("could not read robots.txt (%s). Treating that as a refusal "
                       "rather than a licence." % e)
    ok = rp.can_fetch(UA, url)
    return ok, ("robots.txt permits %s" % url if ok else
                "robots.txt DISALLOWS %s for this agent. Stopping. The GMO Record "
                "stays a hand-read source." % url)


def fetch(url):
    req = Request(url, headers={"User-Agent": UA,
                                "Accept": "application/json, text/html;q=0.8"})
    with urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def find_endpoints(page):
    """Candidate data URLs referenced by the map page, most specific first."""
    out = []
    for pat in (r'["\'](/[^"\']*?(?:geojson|/api/|jsonapi|views/ajax|export)[^"\']*)["\']',
                r'["\'](https?://[^"\']*?(?:geojson|/api/|jsonapi)[^"\']*)["\']',
                r'data-[a-z-]*url=["\']([^"\']+)["\']'):
        for u in re.findall(pat, page, re.I):
            u = u if u.startswith("http") else BASE + u
            if u not in out:
                out.append(u)
    return out


def harvest_rows(payload):
    """Pull site rows out of whatever shape the endpoint returns."""
    try:
        data = json.loads(payload)
    except Exception:
        return []
    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        rows = []
        for f in data.get("features", []):
            g = (f.get("geometry") or {}).get("coordinates") or []
            p = dict(f.get("properties") or {})
            if len(g) >= 2:
                p["_lng"], p["_lat"] = g[0], g[1]
            rows.append(p)
        return rows
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    for k in ("rows", "data", "results", "items", "features"):
        v = data.get(k) if isinstance(data, dict) else None
        if isinstance(v, list):
            return [r for r in v if isinstance(r, dict)]
    return []


def pick(row, *names):
    for n in names:
        for k, v in row.items():
            if k and n in str(k).lower() and v not in (None, ""):
                return str(v).strip()
    return ""


def coords(row):
    la = pick(row, "_lat", "lat", "latitude")
    ln = pick(row, "_lng", "lon", "lng", "longitude")
    try:
        la, ln = float(la), float(ln)
    except Exception:
        return None, None
    if not (AU[0] <= la <= AU[1] and AU[2] <= ln <= AU[3]):
        return None, None       # not an Australian site coordinate
    return la, ln


def to_record(row):
    la, ln = coords(row)
    if la is None:
        return None
    lic = pick(row, "licence", "license", "dir", "permit")
    crop = pick(row, "crop", "species", "organism")
    trait = pick(row, "trait", "modification", "gm trait")
    holder = pick(row, "holder", "licensee", "organisation", "company")
    where = pick(row, "location", "site", "lga", "shire", "state", "region")
    status = pick(row, "status", "stage") or "Licensed field trial"
    area = pick(row, "area", "hectare", "size")
    return {
        "name": ("%s \u2014 %s field trial" % (lic or "OGTR licence", crop or "GM crop"))[:180],
        "source": "ogtr",
        "type": (crop or "Crop") + ", licensed field trial",
        "lat": la, "lng": ln,
        "state": where or "Australia",
        # The whole point of this source: a real site position, not a fallback.
        "precise": True,
        "impact": 3,
        "company": holder,
        "size": area,
        "status": status,
        "phase": "post",
        "date": "",
        "url": PAGE,
        "desc": ("WHAT. A licensed GMO crop field trial site%s%s. "
                 "WHERE IT SITS. Australia's OGTR is the only regulator in the world "
                 "that publishes the locations of active field trial sites, alongside "
                 "the full risk assessment and licence conditions for each. "
                 "WHY IT MATTERS. Every other release record on this map sits at a "
                 "country or state fallback because the register published no "
                 "location. These points sit where the trial actually is \u2014 which "
                 "proves that publishing site locations is possible, and removes the "
                 "usual argument against doing it everywhere else."
                 % ((", %s" % trait) if trait else "",
                    (", held by %s" % holder) if holder else "")),
        "checked": "",
    }


def main():
    ok, why = allowed(PAGE)
    print(why)
    if not ok:
        return                      # exit 0: a refusal is not a build failure

    try:
        page = fetch(PAGE)
    except Exception as e:
        print("could not fetch the map page: %s" % e, file=sys.stderr); return

    cands = find_endpoints(page)
    # Two runs timed out at 4 minutes probing endpoints in page order. The map
    # data is a geojson or an api route; a stylesheet or an analytics beacon is
    # not, and each dead probe costs a full timeout. Sort so the likely ones go
    # first and cap the number tried.
    def likely(u):
        u = u.lower()
        return (0 if "geojson" in u else 1 if "/api/" in u or "jsonapi" in u
                else 2 if "views/ajax" in u or "export" in u else 3)
    cands = sorted(set(cands), key=likely)[:8]
    print("  %d candidate data endpoints, most likely first" % len(cands))
    for u in cands[:3]:
        print("     %s" % u[:100])
    rows = []
    for u in cands:
        allowed_u, _ = allowed(u)
        if not allowed_u:
            continue
        try:
            got = harvest_rows(fetch(u))
        except Exception:
            continue
        if got:
            print("  data from %s (%d rows)" % (u[:90], len(got)))
            rows = got
            break

    if not rows:
        print("  no machine-readable site data found. The map may render from an "
              "endpoint this script does not recognise, or from markup. Open %s, "
              "look at the network tab, and add the URL to find_endpoints()." % PAGE,
              file=sys.stderr)
        return

    out = [r for r in (to_record(x) for x in rows) if r]
    print("  usable site records: %d of %d rows" % (len(out), len(rows)))
    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written"); return
    OUT.write_text(json.dumps({
        "note": ("OGTR licensed crop field trial sites. The only release records on "
                 "this map with real coordinates, because OGTR is the only regulator "
                 "that publishes site locations."),
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
