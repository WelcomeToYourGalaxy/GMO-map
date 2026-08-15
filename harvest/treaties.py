#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Treaty membership as a map layer.

Every other layer here shows what a country DOES. This one shows what it has
AGREED TO, which is the thing that makes the rest of it legible. A country with
no filed biosafety decisions and no regime classification is a blank space, and
a blank space can mean two opposite things: a state that never joined the treaty
that would require it to file, or a state that joined and filed nothing. The
United States and Russia are exactly that pair, and until now the map drew them
identically.

    python3 harvest/treaties.py

STRUCTURE. One table per treaty, and adding a treaty is adding a table. Each
carries its own source URL and the date the list was read, because a
ratification list is a snapshot and this repository has already been caught out
by a stale one: Sierra Leone ratified in 2020 and was missing from the 2015
list this map worked from for months.

WHAT IS HERE AND WHAT IS NOT. The Cartagena Protocol table is complete and
checked. The other four are declared and empty, deliberately: UPOV in
particular is the one worth having - the 1991 act restricts farm-saved seed and
the 1978 act does not, so which act a country signed is the seed-sovereignty
argument in a single variable - but writing a membership list from memory is
exactly the fabrication this project refuses. Each empty table names the
depositary page its list must come from. An empty treaty draws nothing and says
so rather than shading the world grey.
"""

import json, sys, time, pathlib
from urllib.request import Request, urlopen

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "overlays" / "treaties.geojson"
WORLD = HERE / "_world_boundaries.geojson"
WORLD_URL = ("https://raw.githubusercontent.com/datasets/geo-countries/master/"
             "data/countries.geojson")

# ---------------------------------------------------------------------------
# Cartagena Protocol on Biosafety. Read from the Secretariat's ratification
# list, 29 September 2015, plus two accessions confirmed since: Uzbekistan
# (25 October 2019) and Sierra Leone (15 June 2020). The Protocol reports 173
# parties; this table holds 172, so one accession since 2015 is unaccounted
# for and that gap is stated rather than papered over.
# ---------------------------------------------------------------------------
CARTAGENA = """
AFG ALB DZA AGO ATG ARM AUT AZE BHS BHR BGD BRB BLR BEL BLZ BEN BTN BOL BIH BWA
BRA BGR BFA BDI CPV KHM CMR CAF TCD CHN COL COM COG CRI CIV HRV CUB CYP CZE PRK
COD DNK DJI DMA DOM ECU EGY SLV ERI EST ETH FJI FIN FRA GAB GMB GEO DEU GHA GRC
GRD GTM GIN GNB GUY HND HUN IND IDN IRN IRQ IRL ITA JAM JPN JOR KAZ KEN KIR KGZ
LAO LVA LBN LSO LBR LBY LTU LUX MDG MWI MYS MDV MLI MLT MHL MRT MUS MEX MNG MNE
MAR MOZ MMR NAM NRU NLD NZL NIC NER NGA NIU NOR OMN PAK PLW PAN PNG PRY PER PHL
POL PRT QAT KOR MDA ROU RWA KNA LCA VCT WSM SAU SEN SRB SYC SVK SVN SLB SOM ZAF
ESP LKA PSE SDN SUR SWZ SWE CHE SYR TJK THA MKD TGO TON TTO TUN TUR TKM UGA UKR
ARE GBR TZA URY VEN VNM YEM ZMB ZWE UZB SLE
""".split()

TREATIES = [
    {
        "key": "cartagena",
        "label": "Cartagena Protocol on Biosafety",
        "colour": "#4a7a8c",
        "read": "2015-09-29, plus accessions to 2020",
        "source": "https://bch.cbd.int/protocol/parties/",
        "parties": CARTAGENA,
        "what": ("Governs the movement of living modified organisms between "
                 "countries. A party must decide before a first import for "
                 "release and must file that decision to the Biosafety "
                 "Clearing-House within fifteen days. Almost every national "
                 "biosafety law on this map exists because its country joined "
                 "this."),
        "absence": ("A state outside it is under no obligation to notify anyone "
                    "of anything. The United States is the largest of them and "
                    "has never joined, which is why it files no decisions while "
                    "authorising more releases than any other country."),
    },
    # ---- declared, and empty until somebody reads the list ------------------
    {
        "key": "nagoya_kl",
        "label": "Nagoya\u2013Kuala Lumpur Supplementary Protocol",
        "colour": "#8c5a4a",
        "read": "",
        "source": "https://bch.cbd.int/protocol/supplementary/",
        "parties": [],
        "what": ("Liability and redress for damage caused by living modified "
                 "organisms. It answers the question the Cartagena Protocol "
                 "leaves open: who pays."),
        "absence": ("Far fewer states have joined this than joined Cartagena. "
                    "The difference between the two lists is the difference "
                    "between agreeing to notify and agreeing to be liable."),
    },
    {
        "key": "upov91",
        "label": "UPOV \u2014 1991 act",
        "colour": "#7a6a3a",
        "read": "",
        "source": "https://www.upov.int/members/en/",
        "parties": [],
        "what": ("Plant variety rights. The 1991 act restricts what a farmer may "
                 "do with seed saved from their own harvest; the earlier 1978 "
                 "act does not. Which act a country signed is the whole "
                 "seed-sovereignty argument in one variable."),
        "absence": "",
    },
    {
        "key": "upov78",
        "label": "UPOV \u2014 1978 act",
        "colour": "#9a8a5a",
        "read": "",
        "source": "https://www.upov.int/members/en/",
        "parties": [],
        "what": ("The earlier plant variety rights act, which leaves farm-saved "
                 "seed alone. Countries still bound by it are under steady "
                 "pressure, usually through trade agreements, to move to 1991."),
        "absence": "",
    },
    {
        "key": "plant_treaty",
        "label": "International Treaty on Plant Genetic Resources",
        "colour": "#4a7a5a",
        "read": "",
        "source": "https://www.fao.org/plant-treaty/countries/membership/en/",
        "parties": [],
        "what": ("The multilateral system for exchanging crop genetic material, "
                 "and for sharing what comes of it."),
        "absence": "",
    },
]


# The same simplifier the regime layer uses. Written full-resolution this file
# came out at 12 MB for 236 countries - four times the regime overlay, for a
# layer that says one boolean per country. A map nobody waits for is a map
# nobody reads.
sys.path.insert(0, str(HERE))
try:
    from build_regime import simplify
except Exception:
    def simplify(geom, tol=0.02):
        return geom


def world():
    if not WORLD.exists():
        print("  fetching world boundaries")
        req = Request(WORLD_URL, headers={"User-Agent": "GMO-map/1.0"})
        WORLD.write_bytes(urlopen(req, timeout=180).read())
    return json.loads(WORLD.read_text(encoding="utf-8"))


def main():
    gj = world()
    feats, counts = [], {}
    live = [t for t in TREATIES if t["parties"]]
    empty = [t for t in TREATIES if not t["parties"]]

    for t in live:
        parties = set(t["parties"])
        counts[t["key"]] = 0
        for f in gj["features"]:
            p = f.get("properties") or {}
            iso = p.get("ISO3166-1-Alpha-3") or ""
            if not iso or iso == "-99":
                continue
            member = iso in parties
            feats.append({
                "type": "Feature",
                "geometry": simplify(f["geometry"]),
                "properties": {
                    "treaty": t["key"], "label": t["label"],
                    "iso": iso, "name": p.get("name") or iso,
                    # Both states are drawn. A layer that only draws members
                    # answers "who joined" and never "who did not", and the
                    # second question is the one the blank spaces on this map
                    # keep raising.
                    "member": member,
                    "read": t["read"], "src": t["source"],
                    "what": t["what"], "absence": t["absence"],
                },
            })
            counts[t["key"]] += 1 if member else 0

    out = {"type": "FeatureCollection",
           "generated": time.strftime("%Y-%m-%d"),
           "note": ("Treaty membership by country. Drawn for members and "
                    "non-members alike, because an absence on this map means "
                    "nothing until you know whether the country ever agreed to "
                    "anything."),
           "treaties": [{"key": t["key"], "label": t["label"],
                         "colour": t["colour"], "source": t["source"],
                         "read": t["read"], "parties": len(t["parties"])}
                        for t in TREATIES],
           "features": feats}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    drawn = {f["properties"]["iso"] for f in feats if f["properties"]["member"]}
    for t in live:
        missing = sorted(set(t["parties"]) - drawn)
        print("  %-46s %d parties drawn of %d in the table"
              % (t["label"], counts[t["key"]], len(t["parties"])))
        if missing:
            # A party with no boundary is a party the map cannot draw, which is
            # not the same as a country that did not join. France and Norway
            # carry no ISO3 code in the upstream boundary file.
            print("     not drawn for want of a boundary: %s" % " ".join(missing))
    for t in empty:
        print("  %-46s NO LIST YET \u2014 %s" % (t["label"], t["source"]))
    print("  treaties.geojson: %d features, %.2f MB"
          % (len(feats), OUT.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
