#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the context overlays from geometry and data already in the repo.

Two of the eight overlays can be built honestly from what is here:

  trials.geojson   aggregated from projects.json, drawn on the real US state
                   polygons embedded in index.html as SUBGEO
  regime.geojson   each country classified by how it decides what counts as a
                   regulated organism, drawn on the same embedded geometry,
                   dissolved from admin-1 units to one shape per country

The other six need geometry this repo does not contain. They are listed at the
bottom of overlays/README.md with a source and a build route each; this script
does not invent them.

    python3 harvest/build_overlays.py            # write both
    python3 harvest/build_overlays.py --dry-run  # report, write nothing

Standard library only.
"""
import io, json, re, sys, pathlib
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
PROJECTS = ROOT / "projects.json"
HERE = ROOT / "harvest"
OUT = ROOT / "overlays"

# ---------------------------------------------------------------------------
# How each country decides what counts as a regulated organism. Three classes,
# because that distinction is what makes the map look different in different
# places - and it decides whether an absence of dots means nothing is happening
# or that the law stopped requiring a record.
#
# Sourced from the national frameworks described in the map's own entries. Only
# countries whose position is documented there are classified; the rest are
# left out rather than guessed at, so an unshaded country means "not classified
# here", never "no rules".
REGIME = {
    # Technique-based: an organism is regulated because of how it was made.
    # Gene-edited organisms generally stay inside the scheme.
    "technique": {
        "label": "Technique-based \u2014 regulated by how it was made",
        "iso": ["NZL", "NOR", "CHE", "AUT", "HUN", "SRB", "TUR", "IND", "MEX",
                "PER", "ECU", "BOL", "VEN", "EGY", "TUN", "DZA", "MAR", "SAU",
                "RUS", "UKR", "BLR", "KAZ", "IRN", "IRQ", "SYR", "LBN", "JOR"],
        "note": ("The organism is regulated because of the technique used to make it. "
                 "A gene-edited plant generally stays inside the scheme, so it generates "
                 "an application, an assessment and a register entry like any other."),
    },
    # Trait-based: regulated because of what it is, not how it was made.
    "trait": {
        "label": "Trait-based \u2014 regulated by what it is",
        "iso": ["CAN", "USA"],
        "note": ("Regulation attaches to the novelty of the trait rather than the "
                 "technique. Canada is the clearest case: transgenic events and "
                 "products of mutagenesis or gene editing sit in the same register, "
                 "which makes it the one place the second group stays visible."),
    },
    # Carve-out: a class of engineered organism has been moved outside the
    # registration scheme, so it generates no public record at all.
    "carveout": {
        "label": "Carve-out \u2014 a class moved outside registration",
        "iso": ["ARG", "BRA", "CHL", "PRY", "URY", "COL", "AUS", "JPN", "PHL",
                "THA", "ISR", "GBR", "NGA", "KEN", "GHA", "ZAF", "CHN",
                "DEU", "FRA", "ESP", "ITA", "NLD", "BEL", "PRT", "IRL", "POL",
                "CZE", "SVK", "SVN", "HRV", "ROU", "BGR", "GRC", "SWE", "DNK",
                "FIN", "EST", "LVA", "LTU", "CYP", "LUX", "MLT"],
        "note": ("At least one class of engineered organism has been placed outside "
                 "the registration scheme, so it produces no application, no "
                 "assessment and no register entry. In the European Union this is "
                 "Regulation (EU) 2026/1388, which puts NGT-1 plants outside the "
                 "authorisation and labelling regime from 2028. An absence of dots "
                 "in these countries can mean deregulation rather than absence."),
    },
}


def load_subgeo():
    """Pull the SUBGEO admin-1 geometry embedded in index.html."""
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"^const SUBGEO = (\{.*\});$", src, re.M)
    if not m:
        sys.exit("SUBGEO not found in index.html")
    return json.loads(m.group(1))


def dissolve(features):
    """Crude dissolve: collect every ring into one MultiPolygon. Adequate for a
    shaded country layer, and it keeps holes and island parts rather than
    replacing a country with its bounding box."""
    parts = []
    for f in features:
        g = f.get("geometry") or {}
        t, c = g.get("type"), g.get("coordinates")
        if t == "Polygon":
            parts.append(c)
        elif t == "MultiPolygon":
            parts.extend(c)
    return {"type": "MultiPolygon", "coordinates": parts} if parts else None


def build_trials(subgeo):
    """Release-authorisation density on real US state polygons."""
    try:
        projects = json.loads(PROJECTS.read_text(encoding="utf-8")).get("projects", [])
    except Exception as e:
        print("  ! could not read projects.json: %s" % e, file=sys.stderr)
        return None
    counts = {}
    for p in projects:
        for st in re.split(r"[,\s]+", str(p.get("state") or "")):
            st = st.strip()
            if len(st) == 2 and st.isalpha() and st.isupper():
                counts[st] = counts.get(st, 0) + 1
    if not counts:
        print("  ! no state-coded records in projects.json \u2014 skipping trials overlay",
              file=sys.stderr)
        return None

    # SUBGEO carries full state names; map the two-letter codes onto them.
    ABBR = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California",
     "CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia",
     "HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas",
     "KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts",
     "MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana",
     "NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico",
     "NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
     "OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
     "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont",
     "VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming",
     "DC":"District of Columbia","PR":"Puerto Rico"}
    by_name = {}
    for code, n in counts.items():
        nm = ABBR.get(code)
        if nm:
            by_name[nm] = by_name.get(nm, 0) + n

    feats = []
    for f in (subgeo.get("USA") or {}).get("features", []):
        nm = (f.get("properties") or {}).get("name")
        n = by_name.get(nm)
        if not n:
            continue
        feats.append({"type": "Feature",
                      "properties": {"name": "%s \u2014 %d release authorisation%s"
                                             % (nm, n, "" if n == 1 else "s"),
                                     "count": n},
                      "geometry": f["geometry"]})
    if not feats:
        return None
    return {"type": "FeatureCollection",
            "properties": {"note": ("Release authorisations per state, counted from "
                                    "projects.json. United States only, because that is "
                                    "the only jurisdiction whose register publishes "
                                    "release locations at state level. Regenerated "
                                    "whenever the release harvester runs.")},
            "features": feats}


def build_regime(subgeo):
    """One shape per classified country, dissolved from admin-1 units."""
    feats, missing = [], []
    for cls, spec in REGIME.items():
        for iso in spec["iso"]:
            country = subgeo.get(iso)
            if not country or not country.get("features"):
                missing.append(iso)
                continue
            geom = dissolve(country["features"])
            if not geom:
                missing.append(iso); continue
            feats.append({"type": "Feature",
                          "properties": {"name": "%s \u2014 %s" % (iso, spec["label"]),
                                         "regime": cls,
                                         "note": spec["note"]},
                          "geometry": geom})
    return {"type": "FeatureCollection",
            "properties": {"note": ("Each country classified by how it decides what "
                                    "counts as a regulated organism. Countries with no "
                                    "shape here are not classified in this build \u2014 that "
                                    "is not a statement that they have no rules.")},
            "features": feats}, missing


ISO3 = {"austria":"AUT","france":"FRA","italy":"ITA","germany":"DEU","greece":"GRC","poland":"POL","spain":"ESP","switzerland":"CHE","belgium":"BEL","united kingdom":"GBR","croatia":"HRV","hungary":"HUN","bulgaria":"BGR","brazil":"BRA","argentina":"ARG","india":"IND","china":"CHN","japan":"JPN","united states":"USA","canada":"CAN","australia":"AUS","south africa":"ZAF","philippines":"PHL","vietnam":"VNM","mexico":"MEX","nigeria":"NGA","kenya":"KEN"}


def main():
    subgeo = load_subgeo()
    print("SUBGEO carries admin-1 geometry for %d countries" % len(subgeo))
    OUT.mkdir(exist_ok=True)

    trials = build_trials(subgeo)
    regime, missing = build_regime(subgeo)

    if trials:
        print("  trials.geojson  %3d states with at least one authorisation" % len(trials["features"]))
    print("  regime.geojson  %3d countries classified, %d had no geometry here"
          % (len(regime["features"]), len(missing)))
    if missing:
        print("    no geometry for: %s" % " ".join(sorted(set(missing))))
        print("    (SUBGEO covers 46 countries; the rest need a world boundary file)")

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written")
        return
    if trials:
        (OUT / "trials.geojson").write_text(json.dumps(trials), encoding="utf-8")
    (OUT / "regime.geojson").write_text(json.dumps(regime), encoding="utf-8")

    # --- cultivation and gmo-free -------------------------------------------
    # These two were registered in the map for weeks with no file behind them,
    # because their harvesters write records and nothing turned records into
    # geometry. Both are area claims about whole countries or regions, so they
    # use the same admin-1 polygons the rest of this script does.
    sub = load_subgeo()
    by_iso = {}
    by_name = {}
    for iso, fc in sub.items():
        for f in fc.get("features", []):
            nm = ((f.get("properties") or {}).get("name") or "").strip()
            by_iso.setdefault(iso, []).append(f)
            if nm:
                by_name[nm.lower()] = (iso, f)

    def area_layer(src_file, key, note, pick):
        fp = HERE / src_file
        if not fp.exists():
            print("  %-22s no harvest yet (%s)" % (key, src_file))
            return
        try:
            rows = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print("  %-22s unreadable: %s" % (key, e)); return
        rows = rows.get("reports") or rows.get("zones") or rows.get("projects") or []
        feats, placed, missed = [], set(), 0
        for r in rows:
            where, val = pick(r)
            if not where:
                missed += 1; continue
            k = str(where).strip()
            hit = by_name.get(k.lower())
            if hit:
                iso, f = hit
                kk = iso + "|" + k.lower()
                if kk not in placed:
                    placed.add(kk)
                    feats.append({"type": "Feature", "geometry": f["geometry"],
                                  "properties": {"name": k, "iso": iso, "value": val,
                                                 "note": r.get("note", ""),
                                                 "src": r.get("url", "")}})
                continue
            iso = ISO3.get(k.lower()) or (k.upper() if k.upper() in by_iso else None)
            if iso and iso in by_iso:
                for f in by_iso[iso]:
                    nm = ((f.get("properties") or {}).get("name") or iso)
                    kk = iso + "|" + nm.lower()
                    if kk in placed:
                        continue
                    placed.add(kk)
                    feats.append({"type": "Feature", "geometry": f["geometry"],
                                  "properties": {"name": nm, "iso": iso, "value": val,
                                                 "note": r.get("note", ""),
                                                 "src": r.get("url", "")}})
            else:
                missed += 1
        if not feats:
            print("  %-22s harvest present but nothing placeable" % key); return
        (OUT / (key + ".geojson")).write_text(json.dumps(
            {"type": "FeatureCollection", "note": note, "features": feats}), encoding="utf-8")
        print("  %-22s %d polygons, %d rows unplaced" % (key, len(feats), missed))

    area_layer("fas_biotech.json", "cultivation",
               "Hectares of engineered crops by country. Source is the USDA FAS Agricultural "
               "Biotechnology Annual where it can be reached, and the ISAAA Global Status brief "
               "otherwise - ISAAA is an industry body and its framing is promotional, but the "
               "hectarage is the figure everyone including its critics cites, and each record "
               "names which source it came from. Country level: neither source gives a field.",
               lambda r: (r.get("country"), r.get("area_candidates")))
    area_layer("gmofree_zones.json", "gmofree",
               "Regions and municipalities that have declared themselves GMO-free, from the GMO "
               "Free Regions network. Where the declaration is municipal the whole country is "
               "shaded, because the source names no region this map holds geometry for.",
               lambda r: (r.get("region") or r.get("country"), r.get("country")))

    print("\nwrote overlays/, %s" % date.today().isoformat())
    print("The other six overlays need geometry this repo does not hold. "
          "See overlays/README.md for a source and route for each.")


if __name__ == "__main__":
    main()
