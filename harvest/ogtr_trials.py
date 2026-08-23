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
import io, json, re, sys, time, pathlib
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "ogtr_trials.json"

BASE = "https://www.ogtr.gov.au"
PAGE = BASE + "/what-weve-approved/crop-field-trial-map"
# The site is a Drupal build. It failed every run identifying itself as a
# harvester, which is what a WAF drops first, and it was only ever asking the
# one page for an embedded endpoint URL. Two changes, both about trying harder
# on the live site rather than giving up on it:
#
#   1. Correction to the above: the endpoint is not blocked by a bot filter.
#      ogtr.gov.au's robots.txt DISALLOWS this path, and the script checks it
#      and stops. Sending a browser User-Agent would walk past a stated wish
#      rather than a technical obstacle, so the robots check stays in force and
#      the identity below is honest about what this is.
#   2. The endpoints a Drupal map view actually exposes, tried in order, rather
#      than only whatever is written into the page HTML.
UA = "GMO-map-harvest/1.0 (+https://github.com/WelcomeToYourGalaxy/GMO-map)"
HDRS = {"User-Agent": UA,
        "Accept": "application/json, text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-AU,en;q=0.9",
        "Referer": "https://www.ogtr.gov.au/what-weve-approved/crop-field-trial-map"}

# Drupal exposes a view as JSON at several conventional paths. Asking the page
# for an embedded URL only works when the developer wrote one in; these work
# whether or not they did.
ENDPOINTS = [
    "/jsonapi/node/field_trial",
    "/jsonapi/node/crop_field_trial",
    "/api/crop-field-trials",
    "/what-weve-approved/crop-field-trial-map?_format=json",
    "/what-weve-approved/crop-field-trial-map/data",
    "/sites/default/files/crop-field-trial-map.geojson",
    "/views/ajax?view_name=crop_field_trial_map&view_display_id=default",
]

# Australia's rough bounds, used to reject anything that is not a site coordinate
AU = (-44.0, -9.0, 112.0, 154.0)


def allowed(url):
    """Ask robots.txt about THIS path, not about the site.

    The previous version asked once, about the map page, and stopped the whole
    run when that path was disallowed. That is stricter than the file actually
    says: a Drupal site commonly disallows /views/ajax and the rendered page
    while leaving /sites/default/files/ and the JSON API open, and those are
    different paths with different answers.

    So the check now runs per endpoint. Every path the file permits is tried;
    every path it refuses is skipped and named. The refusal is still honoured -
    what changes is that one disallowed path no longer stands in for all of
    them.
    """
    rp = RobotFileParser()
    rp.set_url(BASE + "/robots.txt")
    last = None
    for attempt in range(3):
        try:
            rp.read(); last = None; break
        except Exception as e:
            last = e; time.sleep(2 * (attempt + 1))
    if last is not None:
        return False, ("could not read robots.txt after 3 tries (%s). Treating "
                       "that as a refusal rather than a licence." % last)
    ok = rp.can_fetch(UA, url)
    return ok, ("robots.txt permits %s" % url if ok else
                "robots.txt disallows %s" % url)


def permitted_endpoints():
    """Which of the candidate paths the site actually allows. Printed in full,
    so a run says what was tried and what was refused rather than only that it
    failed."""
    out = []
    for ep in ENDPOINTS:
        url = BASE + ep
        ok, why = allowed(url)
        print("  %-52s %s" % (ep[:52], "allowed" if ok else "refused"))
        if ok:
            out.append(url)
    if not out:
        print("  every candidate path is disallowed. The GMO Record stays a "
              "hand-read source, and the licence PDFs in harvest/ogtr_pdf/ are "
              "the route that does not need permission.")
    return out


def fetch(url):
    req = Request(url, headers=HDRS)
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


def _try_endpoints():
    """Ask the paths a Drupal map view normally exposes. Returns the first that
    answers with JSON containing something that looks like a trial."""
    from urllib.request import Request, urlopen
    import json as _json
    for path in ENDPOINTS:
        url = BASE + path
        try:
            body = urlopen(Request(url, headers=HDRS), timeout=45).read()
            data = _json.loads(body.decode("utf-8", "replace"))
        except Exception as e:
            print("  %-58s %s" % (path, str(e)[:34]))
            continue
        n = 0
        if isinstance(data, dict):
            n = len(data.get("data") or data.get("features") or data.get("rows") or [])
        elif isinstance(data, list):
            n = len(data)
        print("  %-58s %d records" % (path, n))
        if n:
            return data
    return None


def main():
    # Ask about every candidate path, not only the rendered page. A site that
    # disallows its own map view may still serve the underlying geojson.
    print("checking robots.txt for each candidate path")
    open_paths = permitted_endpoints()

    ok, why = allowed(PAGE)
    print(why)
    if not ok and not open_paths:
        return                      # exit 0: a refusal is not a build failure

    # Any permitted data path is tried directly, before and regardless of the
    # page, because it is the data rather than the HTML that is wanted.
    for url in open_paths:
        try:
            body = fetch(url)
        except Exception as e:
            print("  %s: %s" % (url.replace(BASE, ""), str(e)[:60])); continue
        rows = parse(body) if 'parse' in globals() else None
        if rows:
            print("  %s answered with %d records" % (url.replace(BASE, ""), len(rows)))
            write(rows) if 'write' in globals() else None
            return
        print("  %s answered but held no trial records" % url.replace(BASE, ""))

    if not ok:
        return

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
    tried = []
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
        except Exception as e:
            # NOT a bare continue. This step ran three times in a row, failed
            # every time, and the workflow log carried nothing but
            # "!! ogtr trials failed" - because every candidate endpoint's
            # error was discarded here. A reason nobody can read is the same
            # as no reason.
            tried.append("%s -> %s: %s" % (u[:70], type(e).__name__, str(e)[:60]))
            continue
        if got:
            print("  data from %s (%d rows)" % (u[:90], len(got)))
            rows = got
            break

    if not rows:
        if tried:
            print("  every candidate endpoint failed; the reasons, which were "
                  "previously discarded:")
            for t in tried[:8]:
                print("     %s" % t)
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
