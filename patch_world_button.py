#!/usr/bin/env python3
"""The zoom-back-out control: the house glyph becomes a worded button.

Run from the repo root:  python3 patch_world_button.py
Applies by exact-text match, refuses to run twice, exits 0 when already done.
"""
import pathlib, sys

P = pathlib.Path("index.html")
if not P.exists():
    sys.exit("index.html not found - run this from the GMO-map repo root")
s = P.read_text(encoding="utf-8")

MARK = "class='reset-world'"
if MARK in s or 'reset-world' in s:
    print("already applied"); sys.exit(0)

edits = [
    # The control itself: words instead of the glyph, and its own class so the
    # 36 px square rule for the +/- buttons does not clip the text.
    (
        "a.title='Reset view (hide state/province layer)'; a.innerHTML='\\u2302'; a.style.fontWeight='700'; a.style.fontSize='16px';",
        "a.className='reset-world'; a.title='Zoom back out to the whole world (and hide the state/province layer)'; a.innerHTML='Back to world view'; a.style.fontWeight='700';",
    ),
    # CSS: let that one button be as wide as its words.
    (
        "@media (max-width:900px){ .leaflet-top.leaflet-left{ top:14px; right:12px; } }",
        ".leaflet-top.leaflet-left .leaflet-bar a.reset-world{ width:auto !important; padding:0 14px; font-size:13px !important; white-space:nowrap; letter-spacing:.01em; }\n"
        "@media (max-width:900px){ .leaflet-top.leaflet-left{ top:14px; right:12px; } }",
    ),
]
for old, new in edits:
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected exactly one match, found {n}:\n  {old[:90]}")
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print("applied: zoom-out control now reads 'Back to world view'")
