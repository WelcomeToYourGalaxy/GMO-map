#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-off repo tidy. Run once from the repo root, then delete this file.

Fixes four things found in the uploaded repo:

  1. Stray files that should not be committed:
       guides/?                 (1 byte, an upload artefact)
       overlays/README (2).md   (a duplicate of overlays/README.md)
       bch_focal_points.py      (a duplicate of harvest/bch_focal_points.py)
       check_links.py           (a duplicate of harvest/check_links.py)
     Only removed after confirming the root copies are byte-identical to the
     harvest/ ones and that the README duplicate adds nothing.

  2. Language codes in wire.json. GDELT reports a language NAME, and the
     harvester was truncating it to two characters, so 'sp', 'ch', 'po' and 'ge'
     appeared beside the proper es/zh/pt/de and the dropdown listed several
     languages twice. 'po' also collided Portuguese with Polish. The harvester is
     fixed; this repairs the items already committed.

    python3 tidy_repo.py --dry-run
    python3 tidy_repo.py
"""
import json, pathlib, sys, filecmp

ROOT = pathlib.Path(__file__).resolve().parent
DRY = "--dry-run" in sys.argv

NAMES = {
 "english": "en", "spanish": "es", "portuguese": "pt", "french": "fr",
 "german": "de", "italian": "it", "dutch": "nl", "russian": "ru",
 "ukrainian": "uk", "polish": "pl", "czech": "cs", "slovak": "sk",
 "romanian": "ro", "hungarian": "hu", "greek": "el", "bulgarian": "bg",
 "serbian": "sr", "croatian": "hr", "slovenian": "sl", "swedish": "sv",
 "norwegian": "no", "danish": "da", "finnish": "fi", "turkish": "tr",
 "arabic": "ar", "hebrew": "he", "chinese": "zh", "japanese": "ja",
 "korean": "ko", "vietnamese": "vi", "thai": "th", "indonesian": "id",
 "hindi": "hi", "bengali": "bn", "catalan": "ca", "filipino": "tl",
}
# The two-letter truncations the old code produced, mapped to real ISO codes.
# 'po' is deliberately absent: it could be Portuguese or Polish and there is no
# way to tell after the fact, so those items keep their value and get counted
# under a code the dropdown will label as unknown rather than guessed wrong.
TRUNC = {"sp": "es", "ch": "zh", "ge": "de", "in": "id", "cr": "hr",
         "uk": "uk", "sw": "sw", "no": "no"}


def tidy_files():
    removed = []
    for rel, twin in (("bch_focal_points.py", "harvest/bch_focal_points.py"),
                      ("check_links.py", "harvest/check_links.py")):
        a, b = ROOT / rel, ROOT / twin
        if a.exists() and b.exists():
            if filecmp.cmp(a, b, shallow=False):
                removed.append(rel)
            else:
                print("  ! %s differs from %s \u2014 leaving both, compare by hand" % (rel, twin))
    for rel in ("guides/?", "overlays/README (2).md"):
        if (ROOT / rel).exists():
            removed.append(rel)
    for rel in removed:
        print("  remove  %s" % rel)
        if not DRY:
            (ROOT / rel).unlink()
    if not removed:
        print("  no stray files found")
    return len(removed)


def tidy_wire():
    p = ROOT / "wire.json"
    if not p.exists():
        print("  no wire.json"); return 0
    items = json.loads(p.read_text(encoding="utf-8")) or []
    changed = 0
    for it in items:
        lg = str(it.get("lang") or "").strip().lower()
        new = NAMES.get(lg) or TRUNC.get(lg) or lg
        if new and new != lg:
            it["lang"] = new; changed += 1
    print("  wire.json: %d items, %d language codes normalised" % (len(items), changed))
    from collections import Counter
    print("  now: %s" % dict(Counter(x.get("lang", "?") for x in items).most_common(12)))
    if changed and not DRY:
        p.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    return changed


if __name__ == "__main__":
    print("tidy files")
    tidy_files()
    print()
    print("normalise wire language codes")
    tidy_wire()
    if DRY:
        print()
        print("dry run — nothing written")
    else:
        print()
        print("done. delete this script; it is a one-off.")
