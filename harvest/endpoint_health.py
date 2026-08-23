#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Endpoint health check for the harvesters.

THE PROBLEM THIS SOLVES

44 harvester scripts fetch from perhaps a hundred endpoints. When one dies the
run still succeeds: the script prints a line, returns nothing, and the commit
goes through. The 2026-08-23 runs show six dead endpoints reported that way —
ePing, EFSA, the CDC ART clinics, the EU GMO register landing page, ALURES and
the Canadian animal-use statistics — and the only reason anyone noticed was
that a panel on the map looked empty.

A harvester failing silently is the same fault as a resource row with a stale
link, and it needs the same answer: something that checks and says so.

WHAT IT DOES

Reads every harvest/*.py, extracts the URLs assigned to module-level constants,
probes each one, and writes a report. Run it in CI on a schedule, or before a
release. It changes no data and touches no harvester.

    python3 harvest/endpoint_health.py            # human-readable
    python3 harvest/endpoint_health.py --json      # machine-readable
    python3 harvest/endpoint_health.py --fail-on-dead   # exit 1 if any 404/DNS

WHY IT IS SEPARATE FROM THE HARVESTERS

A harvester should not stop the run when one of its sources is down — a partial
harvest is better than none, and the workflows are deliberately written so a
failure leaves the previous file in place. But that design means nothing ever
fails loudly. This is where the noise belongs.
"""

import argparse, ast, json, pathlib, re, ssl, socket, sys, urllib.request, urllib.error

HERE = pathlib.Path(__file__).resolve().parent
UA = "GMO-map-endpoint-health/1.0 (public research map)"
TIMEOUT = 20
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

# A URL that must 404. If it does not, the network is behind a filtering proxy
# and every result would be a false negative — the same guard as linkcheck.py.
CANARY = "https://example.com/a-page-that-cannot-exist-canary"


def urls_in(path):
    """Module-level NAME = "http..." assignments, and f-string/format bases.

    Deliberately conservative: it reads the source with ast rather than
    regexing for anything http-shaped, so a URL inside a docstring or a comment
    is not probed. Constants are what harvesters break on.
    """
    out = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [("(unparsed)", str(e)[:60])]
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
            continue
        val = node.value.value
        if not val.startswith("http"):
            continue
        for t in node.targets:
            if isinstance(t, ast.Name):
                out.append((t.id, val))
    return out


def probe(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as r:
                return r.status, ""
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 406) and method == "HEAD":
                continue
            return e.code, ""
        except (socket.timeout, TimeoutError):
            return None, "timeout"
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            if "Name or service not known" in reason or "nodename nor servname" in reason:
                return None, "dns"
            return None, reason[:60]
        except Exception as e:
            return None, str(e)[:60]
    return None, "refused HEAD and GET"


def verdict(status, note):
    """Same three-way split as linkcheck.py, and for the same reason.

    A 403 is not death — Cloudflare and several government sites refuse unknown
    clients. But note that the CDC ART clinics harvester ALSO reports 403, and
    there it does mean the harvest yields nothing. So 403 is reported in its own
    class: not dead, but worth a human look, because a harvester cannot read a
    page a browser can.
    """
    if status and 200 <= status < 400:
        return "ok"
    if status in (404, 410) or note == "dns":
        return "DEAD"
    if status in (401, 403):
        return "blocked (a browser may still see it; the harvester will not)"
    return "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fail-on-dead", action="store_true")
    ap.add_argument("--dir", default=str(HERE))
    args = ap.parse_args()

    st, note = probe(CANARY)
    if not (st in (404, 410) or note == "dns"):
        print("ABORTING: a URL that must 404 did not. This network filters "
              "outbound requests, so every result would be a false negative.",
              file=sys.stderr)
        return 2

    seen, rows = {}, []
    for py in sorted(pathlib.Path(args.dir).glob("*.py")):
        if py.name == pathlib.Path(__file__).name:
            continue
        for name, url in urls_in(py):
            if url.startswith("http") is False:
                continue
            if url not in seen:
                seen[url] = verdict(*probe(url))
            rows.append({"script": py.name, "const": name, "url": url,
                         "verdict": seen[url]})

    dead = [r for r in rows if r["verdict"] == "DEAD"]
    if args.json:
        print(json.dumps({"checked": len(rows), "distinct": len(seen),
                          "rows": rows}, indent=1))
    else:
        by = {}
        for r in rows:
            by.setdefault(r["verdict"], []).append(r)
        print("%d constants across %d scripts, %d distinct URLs\n"
              % (len(rows), len({r["script"] for r in rows}), len(seen)))
        for v in ("DEAD", "blocked (a browser may still see it; the harvester will not)",
                  "unknown", "ok"):
            group = by.get(v, [])
            if not group:
                continue
            print("== %s (%d)" % (v, len(group)))
            if v == "ok":
                print("   (not listed)")
            else:
                for r in group:
                    print("   %-26s %-16s %s" % (r["script"], r["const"], r["url"][:70]))
            print()
    return 1 if (args.fail_on_dead and dead) else 0


if __name__ == "__main__":
    sys.exit(main())
