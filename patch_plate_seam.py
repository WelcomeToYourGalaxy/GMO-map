#!/usr/bin/env python3
"""The painted chart's two edges, made to meet on the globe.

The same fix the Culprits atlas applied to its copy of this chart
(pipeline/plate/seam_fix.py in WelcomeToYourGalaxy/culprits), run on the chart
this map carries inside index.html (PLATE_IMG). On the globe the chart's east
and west edges meet in the Pacific and were never drawn to join: the compass
rose split across them sits out of line, a sea serpent and a cloud plume stop
dead at the edge, and the misty top and bottom edges reach different heights.
The rose is made one again, water and cloud within about forty pixels of the
join are drawn into the chart's own open water, painted land is left alone,
and the see-through edges are blended. Nothing else in the chart changes.

Run from the repo root:  python3 patch_plate_seam.py
Needs numpy, scipy and pillow. Refuses to run twice; exits 0 when done.
"""
import base64, io, pathlib, re, sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

P = pathlib.Path("index.html")
if not P.exists():
    sys.exit("index.html not found - run this from the GMO-map repo root")
s = P.read_text(encoding="utf-8")
found = re.findall(r'var PLATE_IMG = "data:image/webp;base64,([A-Za-z0-9+/=]+)"', s)
if len(found) != 1:
    sys.exit("expected the chart (PLATE_IMG) exactly once in index.html")
old_b64 = found[0]

im = np.array(Image.open(io.BytesIO(base64.b64decode(old_b64))).convert("RGBA")).astype(np.float64)
H, W = im.shape[:2]
if (W, H) != (1600, 1435):
    sys.exit(f"chart is {W}x{H}; the fix is measured for 1600x1435")
rgb, A = im[:, :, :3].copy(), im[:, :, 3].copy()

if np.abs(rgb[:, 0] - rgb[:, W - 1]).mean() < 6 and np.abs(A[:, 0] - A[:, W - 1]).mean() < 6:
    print("already applied - the chart's two edges already meet"); sys.exit(0)
print("edge difference before:", round(float(np.abs(rgb[:, 0] - rgb[:, W - 1]).mean()), 2), "colour")

ROSE = (640, 860)          # the rows the split compass rose sits in
ROSE_HALF = 90             # how far it reaches either side of the seam
VEIL = 45                  # how far the water is drawn together
FADE = 70                  # how far the see-through edges are blended

# 1. The rose: the western half becomes the mirror of the eastern half, so the
#    two halves are one rose again.
r0, r1 = ROSE
mirror = rgb[r0:r1, W - ROSE_HALF:][:, ::-1]
mirrorA = A[r0:r1, W - ROSE_HALF:][:, ::-1]
w = np.clip(1 - np.arange(ROSE_HALF) / ROSE_HALF, 0, 1) ** 0.7
rows = np.arange(r0, r1)
ends = np.clip(np.minimum(rows - r0, r1 - 1 - rows) / 25.0, 0, 1)[:, None]
weight = (w[None, :] * ends)[..., None]
rgb[r0:r1, :ROSE_HALF] = rgb[r0:r1, :ROSE_HALF] * (1 - weight) + mirror * weight
A[r0:r1, :ROSE_HALF] = A[r0:r1, :ROSE_HALF] * (1 - weight[..., 0]) + mirrorA * weight[..., 0]

# 2. Water and cloud near the seam are drawn into the plate's own open water,
#    so a serpent or a cloud fades out instead of being cut off. Painted land
#    keeps its own pixels: land does meet across the date line.
patch = rgb[650:720, 120:230]                       # open Pacific, no lines or creatures
tile = np.concatenate([patch, patch[:, ::-1]], axis=1)
tile = np.concatenate([tile, tile[::-1]], axis=0)
sea = np.tile(tile, (H // tile.shape[0] + 1, 1, 1))[:H, :2 * VEIL]
band = np.concatenate([rgb[:, W - VEIL:], rgb[:, :VEIL]], axis=1)
bandA = np.concatenate([A[:, W - VEIL:], A[:, :VEIL]], axis=1)
bright = band.mean(axis=2)
water = (band[..., 2] + band[..., 1] > band[..., 0] * 2.3) & (bright < 125)
# Everything but painted land is drawn together: water, the pale cloud plumes
# and the dark ones. Land is sand and green — warmer than it is blue.
land = (band[..., 0] > band[..., 2] + 6) & (bright > 105)
soft = gaussian_filter((~land).astype(float), 4)[..., None]
# The tile is toned to the water beside the seam, row by row.
near = band[:, VEIL - 12:VEIL + 12]
nearw = water[:, VEIL - 12:VEIL + 12]
tone = np.array([[np.median(near[r][nearw[r]][..., c]) if nearw[r].any() else np.nan
                  for c in range(3)] for r in range(H)])
for c in range(3):
    col = tone[:, c]
    good = ~np.isnan(col)
    tone[:, c] = np.interp(np.arange(H), np.arange(H)[good], col[good]) if good.any() else 40
tone = gaussian_filter(tone, (25, 0))
sea = sea - sea.reshape(-1, 3).mean(axis=0) + tone[:, None, :]
d = np.abs(np.arange(2 * VEIL) - (VEIL - 0.5))
veil = np.clip(1 - d / VEIL, 0, 1)[None, :, None] ** 0.8
rose_rows = np.zeros((H, 1, 1))
rose_rows[r0:r1] = 1
veil = veil * soft * (1 - rose_rows)                          # the rose is left as it is
band = band * (1 - veil) + sea * veil
rgb[:, W - VEIL:] = band[:, :VEIL]
rgb[:, :VEIL] = band[:, VEIL:]

# 2b. The last few pixels either side are mixed with their mirror across the
#     seam, so colour runs across the join with nothing left to see.
JOIN = 14
j = np.arange(JOIN)
tj = 0.5 * (1 - j / JOIN)
wj, ej = rgb[:, :JOIN].copy(), rgb[:, W - JOIN:].copy()
rgb[:, :JOIN] = wj * (1 - tj[None, :, None]) + ej[:, ::-1] * tj[None, :, None]
rgb[:, W - JOIN:] = ej * (1 - tj[::-1][None, :, None]) + wj[:, ::-1] * tj[::-1][None, :, None]

# 3. The see-through top and bottom edges: blended so the mist crosses the join
#    at the same height on both sides.
x = np.arange(FADE)
t = 0.5 * (1 - x / FADE)                                      # half and half at the seam
west, east = A[:, :FADE].copy(), A[:, W - FADE:].copy()
A[:, :FADE] = west * (1 - t) + east[:, ::-1] * t
A[:, W - FADE:] = east * (1 - t[::-1]) + west[:, ::-1] * t[::-1]

out = np.dstack([np.clip(rgb, 0, 255), np.clip(A, 0, 255)]).round().astype(np.uint8)
buf = io.BytesIO()
Image.fromarray(out).save(buf, "WEBP", quality=92, alpha_quality=100, method=6)
new_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
s = s.replace(old_b64, new_b64, 1)
P.write_text(s, encoding="utf-8")
print("edge difference now:", round(float(np.abs(out[:, 0, :3].astype(float) - out[:, W - 1, :3]).mean()), 2),
      "colour,", round(float(np.abs(out[:, 0, 3].astype(float) - out[:, W - 1, 3]).mean()), 2), "alpha")
