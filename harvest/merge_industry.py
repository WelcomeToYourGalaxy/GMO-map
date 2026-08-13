#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge ind1.py-ind24.py into harvest/industry_source.json.

This step used to be an ad-hoc snippet, and it deduplicated on URL silently. Six
entries lost that way and nobody noticed for months, including the Jesse
Gelsinger entry - the 1999 trial death that stalled gene therapy for a decade.
Each had been written, reviewed and committed, and simply never appeared.

So the merge is a script now, and it refuses to drop anything. Two entries
sharing a URL is a mistake in the modules, not something to resolve quietly at
build time: either they are the same entry written twice, or they are different
entries and one of them needs its own source. The script says which entries
collide and on what, and writes nothing until they are fixed.

Run from the repository root:

    python3 harvest/merge_industry.py
    python3 harvest/merge_industry.py --dry-run
"""

import io, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "industry_source.json"
MODULES = 25


def load_all():
    sys.path.insert(0, str(ROOT))
    parts = []
    for i in range(1, MODULES + 1):
        name = "ind%d" % i
        try:
            mod = __import__(name)
        except ImportError:
            sys.exit("%s.py not found. The modules live in the repository root, "
                     "beside index.html, because they import from each other." % name)
        found = [getattr(mod, a) for a in dir(mod) if a.startswith("IND")]
        if not found:
            sys.exit("%s.py defines no IND dict" % name)
        parts.append((name, found[0]))
    return parts


def main():
    dry = "--dry-run" in sys.argv
    parts = load_all()

    by_url, by_name, order = {}, {}, []
    total = 0
    for modname, part in parts:
        for iso, entries in part.items():
            for x in entries:
                total += 1
                by_url.setdefault(x["url"], []).append((modname, x["name"]))
                by_name.setdefault(x["name"], []).append((modname, x["name"]))
                order.append(x)

    dup_url = {u: v for u, v in by_url.items() if len(v) > 1}
    dup_name = {n: v for n, v in by_name.items() if len(v) > 1}

    if dup_url or dup_name:
        sys.stderr.write("\nMERGE REFUSED. Entries collide, and dropping one "
                         "silently is how six entries went missing before.\n\n")
        for u, rows in sorted(dup_url.items()):
            sys.stderr.write("  same URL: %s\n" % u)
            for m, n in rows:
                sys.stderr.write("      %-8s %s\n" % (m, n))
            sys.stderr.write("      -> if these are different things, give each its own "
                             "source page.\n\n")
        for n, rows in sorted(dup_name.items()):
            sys.stderr.write("  same name: %s\n" % n)
            for m, _ in rows:
                sys.stderr.write("      %s\n" % m)
            sys.stderr.write("\n")
        sys.stderr.write("Nothing written. %s unchanged.\n" % OUT.name)
        sys.exit(1)

    print("  %d entries across %d modules, no collisions" % (total, MODULES))
    if dry:
        print("  dry run - nothing written")
        return
    OUT.write_text(json.dumps(order, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  wrote %s: %d entries" % (OUT.name, len(order)))
    print("  now run harvest/build_industry_points.py to rebuild the points")


if __name__ == "__main__":
    main()
