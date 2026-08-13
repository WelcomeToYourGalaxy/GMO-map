#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build overlays/regime.geojson at full country coverage.

The old build was limited twice: 71 countries were classified by hand inside
build_overlays.py, and SUBGEO holds admin-1 geometry for only 46 countries, so
36 of the 71 ever drew. Both limits are gone. The classification lives in
regime_classification.py with a confidence rating per country, and the outlines
come from a world boundaries dataset.

Outlines are simplified before writing. A country shape at world zoom does not
need every inlet: unsimplified this file is 10 MB, and at 0.08 degrees it is
2.4 MB and looks identical at the zooms the layer is drawn.
"""

import io, json, sys, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "overlays" / "regime.geojson"
CACHE = ROOT / "harvest" / "_world_boundaries.geojson"

WORLD_URL = ("https://raw.githubusercontent.com/datasets/geo-countries/master/"
             "data/countries.geojson")

# The dataset writes -99 instead of an ISO code for a handful of countries.
BY_NAME = {"France": "FRA", "Norway": "NOR", "Kosovo": "XKX"}

SIMPLIFY_TOL = 0.08


def load_world():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    print("  fetching world boundaries")
    with urllib.request.urlopen(WORLD_URL, timeout=90) as r:
        raw = r.read().decode("utf-8")
    CACHE.write_text(raw, encoding="utf-8")
    return json.loads(raw)


def _thin_ring(ring, tol):
    if not ring:
        return ring
    out = [ring[0]]
    for pt in ring[1:-1]:
        if abs(pt[0] - out[-1][0]) > tol or abs(pt[1] - out[-1][1]) > tol:
            out.append(pt)
    if len(ring) > 1:
        out.append(ring[-1])
    return out if len(out) >= 4 else ring


def simplify(geom, tol=SIMPLIFY_TOL):
    t = geom.get("type")
    if t == "Polygon":
        rings = [r for r in (_thin_ring(r, tol) for r in geom["coordinates"])
                 if len(r) >= 4]
        return {"type": "Polygon", "coordinates": rings} if rings else None
    if t == "MultiPolygon":
        polys = []
        for poly in geom["coordinates"]:
            rings = [r for r in (_thin_ring(r, tol) for r in poly) if len(r) >= 4]
            if rings:
                polys.append(rings)
        return {"type": "MultiPolygon", "coordinates": polys} if polys else None
    return geom


def main():
    sys.path.insert(0, str(ROOT / "harvest"))
    from regime_classification import classified, CONF_NOTE, base_of

    cls = classified()
    world = load_world()

    feats, have = [], set()
    for f in world.get("features", []):
        props = f.get("properties") or {}
        iso = props.get("ISO3166-1-Alpha-3") or props.get("ISO_A3") or ""
        if iso in ("-99", ""):
            iso = BY_NAME.get(props.get("name", ""), "")
        if iso not in cls:
            continue
        geom = simplify(f.get("geometry") or {})
        if not geom:
            continue
        regime, conf = cls[iso]
        have.add(iso)
        feats.append({
            "type": "Feature", "geometry": geom,
            # name is what the popup prints as its title. It used to be the
            # ISO code, so a reader clicking France was told "FRA". iso is a
            # separate field because the popup matches a country's outline to
            # its shaded areas on it, and matching on a display name fails the
            # moment two datasets spell a country differently.
            "properties": {"name": props.get("name") or iso, "iso": iso,
                           "regime": regime,
                           # What the carve-out is cut out of. A country is not
                           # left without an approach by having an exemption.
                           "base": base_of(regime),
                           "confidence": conf, "conf_note": CONF_NOTE[conf]},
        })

    if not feats:
        sys.exit("no countries matched: the boundary dataset changed shape. "
                 "Writing nothing rather than an empty overlay, which would "
                 "read as a world with no biosafety law anywhere.")

    out = {"type": "FeatureCollection",
           "note": ("How each country decides what counts as a regulated "
                    "organism. Compiled from national biosafety statutes and "
                    "Cartagena Protocol country profiles; the classification is "
                    "a reading of each law, not a field anyone publishes. "
                    "Outlines are simplified for display."),
           "features": feats}
    txt = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(txt, encoding="utf-8")

    from collections import Counter
    print("  regime.geojson  %d of %d countries drawn, %.2f MB"
          % (len(feats), len(cls), len(txt) / 1024 / 1024))
    print("    by regime:   %s" % dict(Counter(f["properties"]["regime"] for f in feats)))
    print("    by evidence: %s" % dict(Counter(f["properties"]["confidence"] for f in feats)))
    missing = sorted(set(cls) - have)
    if missing:
        print("    no boundary found for: %s" % " ".join(missing))


if __name__ == "__main__":
    main()
