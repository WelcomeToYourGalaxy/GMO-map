#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check every URL in the map and report what has rotted.

Reads trackerdata.json and the internationalBodies block inside index.html, then
requests each URL and reports the outcome. Also reports how old each entry's
`checked` date is, because a URL that still resolves is not the same as an entry
that is still accurate — a ministry can be reorganised without its domain moving.

    python3 harvest/check_links.py                 # check everything
    python3 harvest/check_links.py --stale-only    # skip the network, just ages
    python3 harvest/check_links.py --update-dates  # stamp today on entries that pass

Standard library only. Be considerate: it runs 8 at a time with a timeout.
"""
import io, json, re, sys, ssl, pathlib
from datetime import date, datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = pathlib.Path(__file__).resolve().parent.parent
TD = ROOT / "trackerdata.json"
INDEX = ROOT / "index.html"
TIMEOUT = 20
UA = ("Mozilla/5.0 (compatible; GMO-map link checker; "
      "+https://github.com/WelcomeToYourGalaxy/GMO-map)")

STALE_DAYS = 365
OLD_DAYS = 730


def load_entries():
    """Yield (where, entry_dict) for everything on the map."""
    out = []
    td = json.loads(TD.read_text(encoding="utf-8"))
    for iso, c in td.items():
        for t in c.get("trackers", []):
            out.append((iso, t))
        for rn, r in (c.get("sub") or {}).items():
            for t in r.get("trackers", []):
                out.append(("%s/%s" % (iso, rn), t))
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"^const internationalBodies =(\[.*?\]);$", src, re.S | re.M)
    if m:
        for b in json.loads(m.group(1)):
            for t in b.get("trackers", []):
                out.append(("INTL", t))
    return out


def age_days(d):
    if not d:
        return None
    try:
        return (date.today() - datetime.strptime(d, "%Y-%m-%d").date()).days
    except ValueError:
        return None


def check(item):
    where, t = item
    url = t.get("url", "")
    ctx = ssl.create_default_context()
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers={"User-Agent": UA})
            with urlopen(req, timeout=TIMEOUT, context=ctx) as r:
                return (where, t, r.status, "")
        except HTTPError as e:
            if e.code in (403, 405, 501) and method == "HEAD":
                continue                      # some servers refuse HEAD; retry as GET
            return (where, t, e.code, e.reason or "")
        except (URLError, TimeoutError, OSError, ValueError) as e:
            if method == "HEAD":
                continue
            return (where, t, 0, str(getattr(e, "reason", e))[:60])
    return (where, t, 0, "unreachable")


def main():
    entries = load_entries()
    print("%d entries on the map\n" % len(entries))

    # ------------------------------------------------------------ staleness --
    buckets = {"fresh": 0, "stale": 0, "old": 0, "undated": 0}
    aged = []
    for where, t in entries:
        d = age_days(t.get("checked"))
        if d is None:
            buckets["undated"] += 1
        elif d > OLD_DAYS:
            buckets["old"] += 1; aged.append((d, where, t))
        elif d > STALE_DAYS:
            buckets["stale"] += 1; aged.append((d, where, t))
        else:
            buckets["fresh"] += 1
    print("verification age:")
    print("  under a year   %d" % buckets["fresh"])
    print("  over a year    %d" % buckets["stale"])
    print("  over two years %d" % buckets["old"])
    print("  no date        %d" % buckets["undated"])
    if aged:
        print("\nre-verify first (oldest):")
        for d, where, t in sorted(aged, reverse=True)[:25]:
            print("  %4dd  %-14s %s" % (d, where, t["name"][:58]))
    if "--stale-only" in sys.argv:
        return

    # ----------------------------------------------------------- reachability --
    print("\nchecking %d URLs, 8 at a time\u2026" % len(entries))
    results = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(check, entries):
            results.append(r)

    ok = [r for r in results if 200 <= r[2] < 400]
    gone = [r for r in results if r[2] in (404, 410)]
    denied = [r for r in results if r[2] in (401, 403, 429)]
    server = [r for r in results if 500 <= r[2] < 600]
    dead = [r for r in results if r[2] == 0]
    other = [r for r in results
             if r not in ok and r not in gone and r not in denied
             and r not in server and r not in dead]

    print("\n  reachable        %d" % len(ok))
    print("  404 / 410 gone   %d" % len(gone))
    print("  blocked us       %d  (403/429 usually means a bot filter, not a dead link)" % len(denied))
    print("  server error     %d  (may be transient \u2014 re-run before acting)" % len(server))
    print("  no response      %d" % len(dead))
    if other:
        print("  other            %d" % len(other))

    for label, group in (("GONE", gone), ("NO RESPONSE", dead), ("SERVER ERROR", server)):
        if not group:
            continue
        print("\n%s:" % label)
        for where, t, code, why in group:
            print("  %-14s %-52s %s %s" % (where, t["name"][:52], code or "", why))

    if "--update-dates" in sys.argv:
        today = date.today().isoformat()
        good = {t["url"] for _, t, code, _ in results if 200 <= code < 400}
        td = json.loads(TD.read_text(encoding="utf-8"))
        n = 0
        def stamp(lst):
            nonlocal n
            for t in lst:
                if t.get("url") in good:
                    t["checked"] = today; n += 1
        for c in td.values():
            stamp(c.get("trackers", []))
            for r in (c.get("sub") or {}).values():
                stamp(r.get("trackers", []))
        TD.write_text(json.dumps(td, ensure_ascii=False, indent=1), encoding="utf-8")
        print("\nstamped %s on %d reachable entries in trackerdata.json" % (today, n))
        print("NOTE: a reachable URL is not a verified entry. This only records that "
              "the link resolved \u2014 whether the description is still true is a "
              "separate question, and the one that actually matters.")


if __name__ == "__main__":
    main()
