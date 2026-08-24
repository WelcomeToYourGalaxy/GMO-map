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
import json, re, socket, sys, time, pathlib

# EVERY socket in this process gets a ceiling.
#
# A run printed "checking robots.txt for each candidate path" and then produced
# nothing for six minutes until `timeout` killed it. The next line it owed was
# the robots.txt status, so it hung inside the robots fetch - and the version
# running still called RobotFileParser.read(), which does urlopen(self.url)
# with NO timeout argument. urlopen's default is None, which means block
# forever. Behind a proxy that accepts the connection and never answers, that
# is a hang with no ceiling and no output.
#
# _robots() no longer calls rp.read() at all, so that specific path is gone.
# This line is the guard for the next one: an explicit timeout on a call is a
# promise the author remembered to make, and this file has now been bitten
# twice by a call where nobody did.
socket.setdefaulttimeout(60)
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
    rp = _robots()
    if rp is None:
        return False, ("could not read robots.txt. Treating that as a refusal "
                       "rather than a licence.")
    ok = rp.can_fetch(UA, url)
    if not ok and getattr(rp, "disallow_all", False):
        # NOT the same answer as a Disallow line, and it used to print as one.
        return False, ("robots.txt could not be READ (401/403), so every path "
                       "reads as disallowed. This is a block on the fetcher, "
                       "not the site's rule.")
    return ok, ("robots.txt permits %s" % url if ok else
                "robots.txt disallows %s" % url)


_ROBOTS = []


def _robots():
    """Fetch robots.txt ONCE and say what came back.

    RobotFileParser.read() SWALLOWS 401 and 403: it sets disallow_all and
    raises nothing. So a Cloudflare challenge or a WAF on the runner's IP
    produced a parser that refuses every path, printed by the caller as
    "refused" - the same word as a real Disallow line - while the script's own
    "could not read robots.txt after 3 tries" message never fired, because
    nothing was ever raised. A run could report that the whole site is closed
    when the truth was that the fetcher was blocked from reading the rules.

    Fetching the file directly first gives the status code, which is the thing
    that distinguishes those two. Called once and cached: it was being
    re-fetched for every candidate endpoint.
    """
    if _ROBOTS:
        return _ROBOTS[0]
    url = BASE + "/robots.txt"
    # ONE request, and the parser is fed from ITS body.
    # RobotFileParser.read() calls urlopen(self.url) with NO headers, so it goes
    # out as Python-urllib while the probe above went out as HDRS. A WAF
    # filtering on user-agent answers those two differently, and the line could
    # print "HTTP 200 | disallow_all=True" - visibly contradictory, but only
    # because the status described a different request from the one that shaped
    # the parser. Fetch once, parse that body, and set disallow_all here.
    code, note, body = None, "", None
    for attempt in range(3):
        try:
            r = urlopen(Request(url, headers=HDRS), timeout=30)
            code, note = r.getcode(), ""
            body = r.read().decode("utf-8", "replace")
            break
        except Exception as e:
            code = getattr(e, "code", None)
            note = "%s: %s" % (type(e).__name__, str(e)[:70])
            if code in (401, 403):
                break                      # a block, not a transient failure
            time.sleep(2 * (attempt + 1))
    rp = RobotFileParser()
    rp.set_url(url)
    if body is not None:
        try:
            rp.parse(body.splitlines())
        except Exception as e:
            print("  robots.txt: HTTP %s but parsing it raised %s"
                  % (code, str(e)[:60]))
            _ROBOTS.append(None)
            return None
    elif code in (401, 403):
        rp.disallow_all = True             # same rule the stdlib applies
    elif code is not None and 400 <= code < 500:
        rp.allow_all = True                # ditto: a 404 is not a refusal
    else:
        # Nothing is known: no status, no body. This is the case that used to
        # print least, because the reason was suppressed when code was None.
        print("  robots.txt: no response after 3 tries (%s)" % (note or "no reason recorded"))
        _ROBOTS.append(None)
        return None
    print("  robots.txt: HTTP %s%s | disallow_all=%s allow_all=%s"
          % (code if code is not None else "no response",
             (" (%s)" % note) if note else "",
             getattr(rp, "disallow_all", False), getattr(rp, "allow_all", False)))
    if getattr(rp, "disallow_all", False):
        print("     ^ 401/403 on robots.txt. Every path below will read as "
              "refused. That is this runner being blocked, NOT the site "
              "publishing a rule against these paths.")
    _ROBOTS.append(rp)
    return rp


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
        rp = _robots()
        # rp is None when robots.txt could not be reached AT ALL - no status, no
        # body. That is not "disallowed by a rule" either, and the first version
        # of this branch printed it as one: the same lie, one case over.
        if rp is None or getattr(rp, "disallow_all", False):
            # The refusal came from a 401/403 on robots.txt, not from a rule.
            # The old unconditional closer told a reader to abandon the route
            # because the runner had been firewalled - the sentence they skim
            # to, contradicting the warning four lines above it.
            print("  NOTHING WAS LEARNED about this site's rules. robots.txt "
                  "was not read (blocked, or unreachable - see the status "
                  "line above), so every path reads as refused. This run does "
                  "NOT show the route is closed; repeat it from an unblocked "
                  "network before concluding anything.")
        else:
            print("  every candidate path is disallowed by a rule in "
                  "robots.txt. The GMO Record stays a hand-read source, and "
                  "the licence PDFs in harvest/ogtr_pdf/ are the route that "
                  "does not need permission.")
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
    """First value whose KEY contains one of these names as a whole word.

    It used to be a bare substring test, and every Drupal jsonapi node carries
    `revision_translation_affected` - "translation" contains "lat". Asked for a
    latitude, pick returned True, float() rejected it, coords() returned
    (None, None), and to_record() dropped the row. It would do that to EVERY
    row, so a jsonapi endpoint answering correctly with forty trials would
    report "0 of 40 usable" and be thrown away.

    Four more sat on the same trap: `site` matched website, `state` matched
    real_estate, `size` matched filesize, `dir` matched director.

    So a name must start at a non-letter boundary and run on only into more
    letters - `field_latitude` and `_lat` hit, `translation` misses. `dir`
    still matches `director`; it is tried after `licence` and `license`, so it
    only bites on a payload with a director key and no licence key.
    """
    for n in names:
        pat = re.compile(r"(?:^|[^a-z])" + re.escape(n.lstrip("_")) + r"(?![a-z])")
        for k, v in row.items():
            if not k or v in (None, ""):
                continue
            key = str(k).lower()
            if n.startswith("_"):
                if n not in key:            # internal keys we set ourselves
                    continue
            elif not pat.search(key):
                continue
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


def _phase(status):
    """'post' only where the status actually says the trial is over."""
    t = (status or "").lower()
    if any(w in t for w in ("complet", "expired", "surrender", "revoked",
                            "finish", "closed", "ceased", "monitor")):
        return "post"
    if any(w in t for w in ("current", "active", "approv", "licens", "issued",
                            "in progress", "ongoing")):
        return "live"
    return ""


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
        # NOT hardcoded "post" any more. Every record used to claim the trial
        # was finished, while `status` is read from the data and the register
        # covers current trials as well as post-harvest monitoring. Derived
        # where the status says so, and left EMPTY where it does not, rather
        # than asserting a stage the source never stated.
        "phase": _phase(status),
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


# _try_endpoints() WAS HERE AND HAS BEEN DELETED.
#
# It was defined and never called, and it fetched all seven candidate paths
# UNCONDITIONALLY - no robots check at all. That is the one thing this script
# exists to not do: permitted_endpoints() asks robots.txt about each path
# precisely so a refusal is honoured per path. A dead function that walks past
# that check is a loaded gun for whoever next wires it up looking for something
# that "already works".
#
# Anything it did that was worth keeping is in permitted_endpoints() plus the
# loop in main(), which asks first and then fetches.


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
        # THIS USED TO CALL parse() AND write(), NEITHER OF WHICH EXISTS IN
        # THIS FILE. Both calls were wrapped in `if 'name' in globals()`, so
        # they evaluated to None instead of raising NameError: `rows` was
        # ALWAYS None, every permitted path printed "answered but held no trial
        # records" whatever came back, and a full FeatureCollection would have
        # been discarded. Five runs survived it because the guard turned a
        # crash into a lie. The real parser is harvest_rows(); the real writer
        # is _emit() below, which is what the page-scraping path already uses.
        try:
            rows = harvest_rows(body)
        except Exception as e:
            print("  %s: could not be parsed (%s)"
                  % (url.replace(BASE, ""), str(e)[:50])); continue
        if rows:
            print("  %s answered with %d records" % (url.replace(BASE, ""), len(rows)))
            if _emit(rows, "robots-permitted endpoint %s" % url.replace(BASE, "")):
                return
            # else: it parsed, but nothing usable came out of it. Keep going -
            # another permitted path, or the page scrape, may still carry the
            # coordinates this one lacked.
        print("  %s answered, and held no trial records" % url.replace(BASE, ""))

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
    # 8 candidates x a 45s socket timeout x 3 retries each is 18 minutes of
    # probing inside a step the workflow kills at 6. The run was terminated
    # BEFORE the reporting below could say which endpoints were tried, which is
    # why three runs produced the single line "!! ogtr trials failed" and
    # nothing else. Give this function its own budget, well inside the step's,
    # and report what it got through.
    BUDGET = 240.0
    t0 = time.time()
    print("  %d candidate data endpoints, most likely first (%.0fs budget)"
          % (len(cands), BUDGET))
    for u in cands[:3]:
        print("     %s" % u[:100])
    rows = []
    for u in cands:
        left = BUDGET - (time.time() - t0)
        if left <= 10:
            tried.append("stopped after %d of %d candidates with %.0fs of the "
                         "budget used - the rest were not probed"
                         % (cands.index(u), len(cands), time.time() - t0))
            break
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

    _emit(rows, "page-scraped endpoint")


def _emit(rows, src):
    """The single writer. It used to be inline at the end of main(), which is
    why the permitted-path loop above had nothing real to call and reached for
    a write() that does not exist."""
    out = [r for r in (to_record(x) for x in rows) if r]
    print("  usable site records: %d of %d rows (from %s)" % (len(out), len(rows), src))
    if not out:
        # RETURNS FALSE, and the caller must act on it. The permitted-path loop
        # used to call _emit() and then `return` unconditionally, so an endpoint
        # that answered with rows carrying no usable coordinate ENDED THE RUN:
        # nothing written, and the page-scraping path that might have found the
        # geojson never tried. A jsonapi node listing is the likely shape for
        # that - it can carry the location in a nested relationship rather than
        # a flat lat/lng, so harvest_rows() finds rows and coords() finds
        # nothing in them.
        print("  every row was dropped by to_record(), so this endpoint gave "
              "nothing usable. Nothing written from it: an empty file reaches "
              "the map as 'OGTR licenses no trials', which is the opposite of "
              "true. Continuing to the next route.", file=sys.stderr)
        return False
    if "--dry-run" in sys.argv:
        # TRUE. A dry run that fell through here would go on to probe eight
        # more endpoints having already found what it came for.
        print("\ndry run \u2014 nothing written")
        return True
    OUT.write_text(json.dumps({
        "note": ("OGTR licensed crop field trial sites. The only release records on "
                 "this map with real coordinates, because OGTR is the only regulator "
                 "that publishes site locations."),
        "source": src,
        "projects": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)
    return True


if __name__ == "__main__":
    main()
