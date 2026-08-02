#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn the industry entries into geocoded points on the map.

Until now industry organisations sat in trackerdata.json, which the map renders
as a per-country resources box. They are now points: one marker per organisation,
clicked to open its own description. No resources box.

Coordinates are the organisation's headquarters or principal site, at city
level. Every record is marked `precise:false` because a corporate headquarters is
not where the work happens, and the map's dashed ring means exactly that: the
position is indicative, not a facility location.

    python3 harvest/build_industry_points.py
    python3 harvest/build_industry_points.py --dry-run

Writes harvest/industry_points.json, merged into projects.json by
aphis_releases.py alongside the release records and the escape record.
"""
import io, json, sys, pathlib
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "harvest" / "industry_points.json"
SRC = ROOT / "harvest" / "industry_source.json"

# City-level coordinates for each organisation's headquarters or principal site.
# Kept in one table so a wrong pin is a one-line fix rather than a hunt.
PLACES = {
 # --- seed & traits ---
 "Bayer Crop Science": (51.0333, 6.9833, "Leverkusen"),
 "Bayer \u2014 investor filings": (51.0333, 6.9833, "Leverkusen"),
 "Bayer \u2014 Climate FieldView & digital farming": (38.6270, -90.1994, "St Louis"),
 "Corteva Agriscience": (39.7684, -86.1581, "Indianapolis"),
 "Corteva \u2014 CRISPR licensing framework": (39.7684, -86.1581, "Indianapolis"),
 "Syngenta Group": (47.5596, 7.5886, "Basel"),
 "Syngenta \u2014 seedcare & seeds portfolio": (47.5596, 7.5886, "Basel"),
 "Syngenta Group China": (31.2304, 121.4737, "Shanghai"),
 "BASF Agricultural Solutions": (49.4875, 8.4660, "Ludwigshafen"),
 "Rijk Zwaan": (51.9917, 4.1500, "De Lier"),
 "Limagrain / Vilmorin": (45.7772, 3.0870, "Clermont-Ferrand"),
 "Benson Hill": (38.6270, -90.1994, "St Louis"),
 "Pairwise": (35.7796, -78.6382, "Durham NC"),
 "KeyGene": (51.9692, 5.6654, "Wageningen"),
 "Groupe Roullier / seed & input distribution": (48.6493, -2.0257, "Saint-Malo"),
 "Mahyco / Maharashtra Hybrid Seeds": (19.8762, 75.3433, "Jalna"),
 "Bioceres Crop Solutions": (-32.9468, -60.6393, "Rosario"),
 "Nufarm": (-37.8136, 144.9631, "Melbourne"),
 "Chinese Academy of Agricultural Sciences": (39.9042, 116.4074, "Beijing"),
 # --- editing & synthetic biology ---
 "Ginkgo Bioworks": (42.3601, -71.0589, "Boston"),
 "Ginkgo Bioworks \u2014 agricultural biologicals": (42.3601, -71.0589, "Boston"),
 "Inari Agriculture": (42.3601, -71.0589, "Cambridge MA"),
 "Broad Institute \u2014 CRISPR patent estate": (42.3629, -71.0865, "Cambridge MA"),
 "Synthego": (37.5485, -121.9886, "Redwood City"),
 "Amyris": (37.8716, -122.2727, "Emeryville"),
 "Evogene": (32.0853, 34.7818, "Rehovot"),
 "Toolgen": (37.5665, 126.9780, "Seoul"),
 "Sanatech Seed": (35.0116, 135.7681, "Kyoto"),
 "Corbion": (52.0907, 5.1214, "Amsterdam"),
 "Novonesis (Novozymes / Chr. Hansen)": (55.6761, 12.5683, "Copenhagen"),
 # --- synthesis & sequencing ---
 "Twist Bioscience": (37.8044, -122.2712, "South San Francisco"),
 "Integrated DNA Technologies (Danaher)": (41.6611, -91.5302, "Coralville"),
 "Illumina": (32.9027, -117.2003, "San Diego"),
 "Addgene": (42.3601, -71.0589, "Watertown MA"),
 "BGI Group": (22.5431, 114.0579, "Shenzhen"),
 "Oxford Nanopore Technologies": (51.7520, -1.2577, "Oxford"),
 "Thermo Fisher Scientific": (42.3601, -71.0589, "Waltham MA"),
 "GenScript": (32.0603, 118.7969, "Nanjing"),
 "ATCC": (38.8048, -77.0469, "Manassas"),
 # --- contract research & manufacturing ---
 "Charles River Laboratories": (42.3601, -71.0589, "Wilmington MA"),
 "Labcorp Drug Development (formerly Covance)": (35.9940, -78.8986, "Burlington NC"),
 "Oxford Biomedica": (51.7520, -1.2577, "Oxford"),
 "Lonza": (46.2044, 7.8722, "Basel / Visp"),
 "Evotec": (53.5511, 9.9937, "Hamburg"),
 # --- laboratory animals ---
 "The Jackson Laboratory": (44.3876, -68.2039, "Bar Harbor"),
 "Taconic Biosciences": (42.6526, -73.7562, "Rensselaer"),
 "Envigo / Inotiv": (39.1653, -86.5264, "West Lafayette"),
 "CLEA Japan / Japan SLC": (35.6762, 139.6503, "Tokyo"),
 "Janvier Labs": (48.0833, -0.7667, "Le Genest-Saint-Isle"),
 "Mutant Mouse Resource & Research Centers": (38.5449, -121.7405, "Davis"),
 # --- livestock, aquaculture, pets ---
 "Acceligen (Recombinetics)": (44.9778, -93.2650, "Eagan MN"),
 "AquaBounty Technologies": (41.5868, -87.8406, "Maynard MA"),
 "ViaGen Pets & Equine": (30.5083, -97.6789, "Cedar Park"),
 "Sooam Biotech": (37.5665, 126.9780, "Seoul"),
 "Genus / PIC": (52.4862, -1.8904, "Basingstoke"),
 "Genus \u2014 PRRS-resistant pig approval": (52.4862, -1.8904, "Basingstoke"),
 "AquaGen": (63.4305, 10.3951, "Trondheim"),
 "GloFish": (33.7490, -84.3880, "Austin / distributed"),
 "Trans Ova Genetics": (42.7411, -95.1372, "Sioux Center"),
 "Livestock Improvement Corporation": (-37.7870, 175.2793, "Hamilton NZ"),
 "Regional Fish Institute": (35.0116, 135.7681, "Kyoto"),
 # --- insects, microbes, open release ---
 "Oxitec": (51.7520, -1.2577, "Abingdon"),
 "Target Malaria": (51.4988, -0.1749, "London"),
 "Pivot Bio": (37.8716, -122.2727, "Berkeley"),
 "Agragene": (32.7157, -117.1611, "San Diego"),
 "Indigo Ag": (42.3601, -71.0589, "Boston"),
 "MosquitoMate": (38.0406, -84.5037, "Lexington KY"),
 "Elemental Enzymes / biologicals sector": (38.6270, -90.1994, "St Louis"),
 "Wolbachia \u2014 World Mosquito Program": (-27.4975, 153.0137, "Brisbane"),
 # --- de-extinction & conservation biotech ---
 "Colossal Biosciences": (32.7767, -96.7970, "Dallas"),
 "Colossal \u2014 Form Bio spin-out": (32.7767, -96.7970, "Dallas"),
 "Living Carbon": (37.7749, -122.4194, "San Francisco"),
 "Suzano / FuturaGene": (-23.5505, -46.6333, "S\u00e3o Paulo"),
 "Revive & Restore": (37.9735, -122.5311, "Sausalito"),
 "San Diego Zoo Wildlife Alliance \u2014 Frozen Zoo": (32.7353, -117.1490, "San Diego"),
 "American Chestnut Foundation \u2014 Darling 58": (43.0481, -76.1474, "Syracuse"),
 # --- human clinical ---
 "Novartis \u2014 gene therapy": (47.5596, 7.5886, "Basel"),
 "Vertex / CRISPR Therapeutics \u2014 Casgevy": (47.3769, 8.5417, "Zug"),
 "ClinicalTrials.gov": (38.9959, -77.1013, "Bethesda"),
 "Bluebird bio": (42.3601, -71.0589, "Somerville MA"),
 "BioNTech": (49.9929, 8.2473, "Mainz"),
 "National Medical Products Administration \u2014 gene therapy": (39.9042, 116.4074, "Beijing"),
 # --- assisted reproduction ---
 "HFEA \u2014 licensed clinic register": (51.5194, -0.1270, "London"),
 "IVIRMA Global": (39.4699, -0.3763, "Valencia"),
 "Orchid Health": (37.7749, -122.4194, "San Francisco"),
 "CDC ART clinic data": (33.7990, -84.3255, "Atlanta"),
 "Cooper Surgical \u2014 fertility": (41.3083, -72.9279, "Trumbull CT"),
 "California Cryobank / Generate Life Sciences": (34.0522, -118.2437, "Los Angeles"),
 "Progyny": (40.7128, -74.0060, "New York"),
 "Genomic Prediction / LifeView": (40.4862, -74.4518, "North Brunswick"),
 "Society for Assisted Reproductive Technology": (34.0489, -84.2400, "Birmingham AL"),
 "Eugin Group": (41.3874, 2.1686, "Barcelona"),
 "Cryos International": (56.1629, 10.2039, "Aarhus"),
 # --- money ---
 "Gates Foundation \u2014 committed grants database": (47.6205, -122.3493, "Seattle"),
 "DARPA \u2014 Biological Technologies Office": (38.8816, -77.1109, "Arlington"),
 "ARCH Venture Partners": (41.8781, -87.6298, "Chicago"),
 "Wellcome Trust": (51.5254, -0.1340, "London"),
 "Baillie Gifford / growth capital in biotech": (55.9533, -3.1883, "Edinburgh"),
 "Department of Biotechnology": (28.6139, 77.2090, "New Delhi"),
 # --- rules, records & advocacy ---
 "BIO \u2014 Biotechnology Innovation Organization": (38.9072, -77.0369, "Washington DC"),
 "ISAAA \u2014 GM approval database": (42.4440, -76.5019, "Ithaca"),
 "CropLife International": (50.8467, 4.3525, "Brussels"),
 "OECD BioTrack": (48.8566, 2.3522, "Paris"),
 "Embrapa": (-15.7939, -47.8828, "Bras\u00edlia"),
 "CTNBio \u2014 national biosafety commission": (-15.7939, -47.8828, "Bras\u00edlia"),
 "Office of the Gene Technology Regulator \u2014 GMO Record": (-35.2809, 149.1300, "Canberra"),
 "Canadian Food Inspection Agency \u2014 PNT decisions": (45.4215, -75.6972, "Ottawa"),
 "Singapore Food Agency \u2014 novel food approvals": (1.3521, 103.8198, "Singapore"),

 # --- round 46 additions ---
 "CIBIOGEM": (19.4326, -99.1332, "Mexico City"),
 "Grupo Bimbo": (19.4326, -99.1332, "Mexico City"),
 "Executive Council for GMOs \u2014 Department of Agriculture": (-25.7479, 28.2293, "Pretoria"),
 "Pannar Seed (Corteva)": (-29.1211, 29.5192, "Greytown"),
 "National Biosafety Management Agency": (9.0765, 7.3986, "Abuja"),
 "Kenya National Biosafety Authority": (-1.2921, 36.8219, "Nairobi"),
 "Illumina Italy / Ferrara sequencing hub": (44.8378, 11.6197, "Ferrara"),
 "Selvita": (50.0647, 19.9450, "Krak\u00f3w"),
 "Syngene International": (12.9716, 77.5946, "Bengaluru"),
 "Bharat Biotech": (17.3850, 78.4867, "Hyderabad"),
 "WuXi AppTec": (31.2304, 121.4737, "Shanghai"),
 "Dabeinong Biotechnology": (39.9042, 116.4074, "Beijing"),
 "Charoen Pokphand Group": (13.7563, 100.5018, "Bangkok"),
 "Nutreco / Skretting": (52.0907, 5.1214, "Amersfoort"),
 "JBS": (-23.5505, -46.6333, "S\u00e3o Paulo"),
 "Colossal \u2014 thylacine programme partners": (-37.8136, 144.9631, "Melbourne"),
 "Australian Frozen Zoo / CryoDiversity": (-37.7847, 144.9517, "Melbourne"),
 "Understanding Animal Research": (51.5074, -0.1278, "London"),
 "Home Office \u2014 animals in science statistics": (51.4995, -0.1248, "London"),

 # --- round 48 additions ---
 "Federal Research Center for Animal Husbandry": (55.7558, 37.6173, "Moscow region"),
 "Ministry of Agriculture and Forestry \u2014 biosafety board": (39.9334, 32.8597, "Ankara"),
 "Ministry of Agrarian Policy and Food": (50.4501, 30.5234, "Kyiv"),
 "PT Perkebunan Nusantara / sugarcane biotechnology": (-6.2088, 106.8456, "Jakarta"),
 "Ministry of Agriculture and Environment \u2014 biosafety": (21.0278, 105.8342, "Hanoi"),
 "ICA \u2014 Instituto Colombiano Agropecuario": (4.7110, -74.0721, "Bogot\u00e1"),
 "SLU \u2014 Swedish University of Agricultural Sciences": (59.8586, 17.6389, "Uppsala"),
 "Solar Foods": (60.1699, 24.9384, "Vantaa"),
 "Teagasc": (53.3498, -6.2603, "Dublin"),
 "Cyagen": (37.5485, -121.9886, "Santa Clara"),
 "National Primate Research Centers": (38.5449, -121.7405, "Davis"),
 "Bachem": (47.2500, 8.6000, "Bubendorf"),
 "Samsung Biologics": (37.3894, 126.6440, "Incheon"),
 "Virtus Health": (-33.8688, 151.2093, "Sydney"),
 "Israeli fertility system \u2014 Ministry of Health": (31.7683, 35.2137, "Jerusalem"),
 "Predator Free 2050 \u2014 genetic tools debate": (-41.2866, 174.7756, "Wellington"),
 "Sovereign wealth investment in agrifood technology": (24.4539, 54.3773, "Abu Dhabi"),
}

# Facet key -> the organism-type bucket the map's own classifier understands, so
# the release layer's type filter keeps working across both kinds of point.
FACET_TYPE = {
 "seed": "Seed & trait company", "editing": "Gene editing company",
 "synthesis": "DNA synthesis & sequencing", "cro": "Contract research & manufacturing",
 "animals": "Laboratory animal supplier", "livestock": "Livestock & aquaculture company",
 "wild": "Open release programme", "deextinct": "De-extinction & conservation biotech",
 "clinical": "Clinical & therapeutic company", "repro": "Assisted reproduction",
 "money": "Funder", "rules": "Regulator, register or trade body",
}


def main():
    if not SRC.exists():
        sys.exit("industry_source.json not found \u2014 it holds the entries this converts")
    entries = json.loads(SRC.read_text(encoding="utf-8"))

    points, missing = [], []
    for x in entries:
        place = PLACES.get(x["name"])
        if not place:
            missing.append(x["name"]); continue
        lat, lng, city = place
        facet = (x.get("tags") or ["seed:majors"])[0].split(":")[0]
        points.append({
            "name": x["name"],
            "source": "industry:" + facet,
            "type": FACET_TYPE.get(facet, "Industry organisation"),
            "lat": lat, "lng": lng,
            "state": city,
            "precise": False,
            "impact": 3,
            "company": x.get("company") or "",
            "size": "",
            "status": "Industry organisation",
            "phase": "post",
            "date": "",
            "url": x["url"],
            "desc": x["desc"],
            "checked": x.get("checked", ""),
        })

    print("industry points: %d" % len(points))
    if missing:
        print("  ! no coordinates for %d entries \u2014 add them to PLACES:" % len(missing))
        for m in missing:
            print("      %s" % m)

    if "--dry-run" in sys.argv:
        print("\ndry run \u2014 nothing written")
        return
    OUT.write_text(json.dumps({
        "note": ("Industry organisations as map points, one marker each. Coordinates are "
                 "headquarters or principal site at city level, so every record is "
                 "precise:false \u2014 a corporate headquarters is not where the work happens."),
        "generated": date.today().isoformat(),
        "projects": points,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nwrote %s" % OUT.name)


if __name__ == "__main__":
    main()
