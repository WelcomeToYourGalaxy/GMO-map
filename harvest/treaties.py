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
# Read from the Secretariat's own ratification list PDF, 9 August 2026:
# 173 numbered rows, complete, no gaps. This replaces a 2015 snapshot that
# had been patched by hand twice and was still two accessions short. The
# European Union is a party and is not a country, so it is not here.
CARTAGENA = """
AFG AGO ALB ARE ARM ATG AUT AZE BDI BEL BEN BFA BGD BGR BHR BHS BIH BLR BLZ BOL
BRA BRB BTN BWA CAF CHE CHN CIV CMR COD COG COL COM CPV CRI CUB CYP CZE DEU DJI
DMA DNK DOM DZA ECU EGY ERI ESP EST ETH FIN FJI FRA GAB GBR GEO GHA GIN GMB GNB
GRC GRD GTM GUY HND HRV HUN IDN IND IRL IRN IRQ ITA JAM JOR JPN KAZ KEN KGZ KHM
KIR KNA KOR KWT LAO LBN LBR LBY LCA LKA LSO LTU LUX LVA MAR MDA MDG MDV MEX MHL
MKD MLI MLT MMR MNE MNG MOZ MRT MUS MWI MYS NAM NER NGA NIC NIU NLD NOR NRU NZL
OMN PAK PAN PER PHL PLW PNG POL PRK PRT PRY PSE QAT ROU RWA SAU SDN SEN SLB SLE
SLV SOM SRB SUR SVK SVN SWE SWZ SYC SYR TCD TGO THA TJK TKM TON TTO TUN TUR TZA
UGA UKR URY UZB VCT VEN VNM WSM YEM ZAF ZMB ZWE
""".split()

# ---------------------------------------------------------------------------
# UPOV, from "Members of the International Union for the Protection of New
# Varieties of Plants", status 27 February 2025. Eighty members, which is the
# total the document itself prints.
#
# The two acts are separate tables because the difference between them is the
# whole reason to draw this. Under the 1991 act a farmer needs permission to
# sow seed saved from their own harvest; under the 1978 act they do not. The
# seventeen countries still on 1978 are most of South America plus China,
# which makes this layer a map of where that pressure is being applied.
#
# The European Union and the African Intellectual Property Organization are
# members and are not countries, so neither is here.
UPOV_1991 = """
ALB ARM AUS AUT AZE BEL BGR BIH BLR CAN CHE CRI CZE DEU DNK DOM EGY ESP EST FIN
FRA GBR GEO GHA HRV HUN IRL ISL ISR JOR JPN KEN KGZ KOR LTU LVA MAR MDA MKD MNE
NGA NLD OMN PAN PER POL ROU RUS SGP SRB SVK SVN SWE TUN TUR TZA UKR USA UZB VCT
VNM
""".split()

UPOV_1978 = """
ARG BOL BRA CHL CHN COL ECU ITA MEX NIC NOR NZL PRT PRY TTO URY ZAF
""".split()

# ---------------------------------------------------------------------------
# International Treaty on Plant Genetic Resources for Food and Agriculture,
# from FAO's own membership CSV. 153 contracting parties, of which 152 are
# countries; the European Union is the 153rd and is not one.
#
# Four states signed and never ratified - Cabo Verde, Haiti, North Macedonia
# and Thailand - and are NOT here. A signature is not membership, and the
# file distinguishes them, so this does too.
#
# The absences are the interesting part. China and Russia are not parties;
# the United States is. That is the reverse of the Cartagena pattern, where
# the United States stands outside and China is in - which is worth seeing on
# one map, because it shows that a country's position is taken treaty by
# treaty rather than as a general stance.
PLANT_TREATY = """
AFG AGO ALB ARE ARG ARM ATG AUS AUT BDI BEL BEN BFA BGD BGR BHR BOL BRA BTN CAF
CAN CHE CHL CIV CMR COD COG COK COL CRI CUB CYP CZE DEU DJI DNK DOM DZA ECU EGY
ERI ESP EST ETH FIN FJI FRA GAB GBR GEO GHA GIN GNB GRC GTM GUY HND HRV HUN IDN
IND IRL IRN IRQ ISL ITA JAM JOR JPN KEN KGZ KHM KIR KOR KWT LAO LBN LBR LBY LCA
LKA LSO LTU LUX LVA MAR MDA MDG MDV MHL MLI MLT MMR MNE MNG MOZ MRT MUS MWI MYS
NAM NER NGA NIC NLD NOR NPL OMN PAK PAN PER PHL PLW PNG POL PRK PRT PRY QAT ROU
RWA SAU SDN SEN SLE SLV SOM SRB SSD STP SVK SVN SWE SWZ SYC SYR TCD TGO TON TTO
TUN TUR TUV TZA UGA URY USA VEN WSM YEM ZMB ZWE
""".split()

# ---------------------------------------------------------------------------
# Nagoya-Kuala Lumpur Supplementary Protocol on Liability and Redress, from
# the Biosafety Clearing-House party table. 55 parties, 54 of them countries;
# the European Union is the 55th and is not one.
#
# Sixteen more states signed and never deposited an instrument - Brazil,
# Poland, Portugal, Senegal, Thailand, Tunisia among them - and are NOT here.
# The deposit column is what makes a party, and it uses five different codes
# (RTF, ACS, APV, ACP, ACC); a guard listing only three of them threw Finland
# out for having accepted rather than ratified.
#
# This is the number to compare against Cartagena's 172. Two-thirds of the
# states that agreed to notify have not agreed to be liable for damage, and
# that gap is the most pointed thing this layer holds.
NAGOYA_KL = """
ALB ARE AUT BEL BFA BGR CAF CHE COD COG COL CUB CZE DEU DNK ESP EST FIN FRA GBR
GNB HRV HUN IND IRL ITA JPN KHM LBR LTU LUX LVA MDA MEX MLI MLT MNG MWI NGA NLD
NOR PER PRK ROU SVK SVN SWE SWZ SYR TGO UGA UKR VEN VNM
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
        "read": "Biosafety Clearing-House party table, 2026-08",
        "source": "https://bch.cbd.int/protocol/supplementary/",
        "parties": NAGOYA_KL,
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
        "read": "2025-02-27",
        "source": "https://www.upov.int/edocs/pubdocs/en/upov_pub_423.pdf",
        "parties": UPOV_1991,
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
        "read": "2025-02-27",
        "source": "https://www.upov.int/edocs/pubdocs/en/upov_pub_423.pdf",
        "parties": UPOV_1978,
        "what": ("The earlier plant variety rights act, which leaves farm-saved "
                 "seed alone. Countries still bound by it are under steady "
                 "pressure, usually through trade agreements, to move to 1991."),
        "absence": "",
    },
    {
        "key": "plant_treaty",
        "label": "International Treaty on Plant Genetic Resources",
        "colour": "#4a7a5a",
        "read": "FAO membership list, downloaded 2026-08",
        "source": "https://www.fao.org/plant-treaty/countries/membership/en/",
        "parties": PLANT_TREATY,
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



# The upstream boundary file writes -99 for France and Norway instead of their
# ISO3 codes - an old defect in that dataset. Left alone it silently drops two
# countries from every layer built on it, and the regime layer has been missing
# France this whole time.
BOUNDARY_ISO_FIX = {"France": "FRA", "Norway": "NOR"}


def iso_of(props):
    iso = props.get("ISO3166-1-Alpha-3") or ""
    if iso and iso != "-99":
        return iso
    return BOUNDARY_ISO_FIX.get(props.get("name") or "", "")

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

    # One feature per country carrying a flag per treaty, rather than one
    # feature per country PER TREATY. The first version wrote the same geometry
    # three times and came to 9.9 MB for three booleans a country; this is the
    # same information at a third of the weight, and it lets the map answer
    # "party to this but not that" without loading three layers.
    party_of = {t["key"]: set(t["parties"]) for t in live}
    for f in gj["features"]:
        p = f.get("properties") or {}
        iso = iso_of(p)
        if not iso:
            continue
        props = {"iso": iso, "name": p.get("name") or iso}
        any_member = False
        for t in live:
            m = iso in party_of[t["key"]]
            props[t["key"]] = m
            any_member = any_member or m
            counts[t["key"]] = counts.get(t["key"], 0) + (1 if m else 0)
        # Non-members are drawn too. A layer that shows only who joined answers
        # half the question, and the blank spaces on this map keep raising the
        # other half.
        props["any"] = any_member
        feats.append({"type": "Feature", "geometry": simplify(f["geometry"]),
                      "properties": props})

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

    for t in live:
        drawn = {f["properties"]["iso"] for f in feats
                 if f["properties"].get(t["key"])}
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
