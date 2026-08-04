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

 # --- round 50 additions ---
 "National Biosafety Centre \u2014 Ministry of Climate Change": (33.6844, 73.0479, "Islamabad"),
 "Bangladesh Agricultural Research Institute \u2014 Bt brinjal": (23.9999, 90.4203, "Gazipur"),
 "Ethiopian Environment Protection Authority \u2014 biosafety": (9.0320, 38.7469, "Addis Ababa"),
 "National Biosafety Authority Ghana": (5.6037, -0.1870, "Accra"),
 "Gabinete Nacional de Bioseguridad": (-34.9011, -56.1645, "Montevideo"),
 "SENAVE \u2014 seed and plant health service": (-25.2637, -57.5759, "Asunci\u00f3n"),
 "SAG \u2014 Servicio Agr\u00edcola y Ganadero": (-33.4489, -70.6693, "Santiago"),
 "Ministerio de Agricultura \u2014 GM cultivation register": (40.4168, -3.7038, "Madrid"),
 "Dire\u00e7\u00e3o-Geral de Alimenta\u00e7\u00e3o e Veterin\u00e1ria": (38.7223, -9.1393, "Lisbon"),
 "Ministry of Agriculture \u2014 biotechnology": (44.4268, 26.1025, "Bucharest"),
 "Agricultural Genetic Engineering Research Institute": (30.0444, 31.2357, "Giza"),
 "Nuseed / Nufarm omega-3 canola": (49.8951, -97.1384, "Winnipeg"),
 "Health Canada \u2014 novel food decisions": (45.4215, -75.6972, "Ottawa"),
 "Aldevron (Danaher)": (46.8772, -96.7898, "Fargo"),
 "Pacific Biosciences": (37.4419, -122.1430, "Menlo Park"),
 "Bio-Rad Laboratories": (37.8716, -122.2727, "Hercules CA"),

 # --- round 51 additions ---
 "Intellia Therapeutics": (42.3601, -71.0589, "Cambridge MA"),
 "Sarepta Therapeutics": (42.3601, -71.0589, "Cambridge MA"),
 "FDA \u2014 cellular & gene therapy approvals": (39.0349, -76.9822, "Silver Spring"),
 "Alliance for Regenerative Medicine": (38.9072, -77.0369, "Washington DC"),
 "Genomics England": (51.5194, -0.1270, "London"),
 "Roche / Genentech": (47.5596, 7.5886, "Basel"),
 "Flagship Pioneering": (42.3601, -71.0589, "Cambridge MA"),
 "USDA NIFA \u2014 grant database": (38.8977, -77.0261, "Washington DC"),
 "Leaps by Bayer": (52.5200, 13.4050, "Berlin"),
 "Verily \u2014 Debug programme": (37.4419, -122.1430, "South San Francisco"),
 "Greenlight Biosciences": (42.3601, -71.0589, "Medford MA"),
 "Oxitec do Brasil": (-22.4149, -45.4527, "Campinas"),
 "WuXi Biologics Ireland": (53.9975, -6.4053, "Dundalk"),
 "Lonza Singapore / biologics cluster": (1.3521, 103.8198, "Singapore"),
 "Shanghai Model Organisms Center": (31.2304, 121.4737, "Shanghai"),
 "Chinese assisted reproduction sector \u2014 NHC licensing": (39.9042, 116.4074, "Beijing"),
 "National Biosafety Board Malaysia": (3.1390, 101.6869, "Putrajaya"),
 "Ministerio del Ambiente \u2014 moratoria GMO": (-12.0464, -77.0428, "Lima"),
 "AGES \u2014 Austrian Agency for Health and Food Safety": (48.2082, 16.3738, "Vienna"),
 "Ministry of the Environment \u2014 GMO register": (50.0755, 14.4378, "Prague"),
 # --- round 52 additions ---
 "Centro de Ingenier\u00eda Gen\u00e9tica y Biotecnolog\u00eda": (23.1136, -82.3666, "Havana"),
 "Comit\u00e9 Nacional de Bioseguridad": (-16.4897, -68.1193, "La Paz"),
 "Ministerio del Ambiente \u2014 bioseguridad": (-0.1807, -78.4678, "Quito"),
 "Comisi\u00f3n T\u00e9cnica Nacional de Bioseguridad": (9.9281, -84.0907, "San Jos\u00e9"),
 "National Environment Management Council": (-6.7924, 39.2083, "Dar es Salaam"),
 "National Biosafety Authority Zambia": (-15.3875, 28.3228, "Lusaka"),
 "Ministry of Rural Development and Food": (37.9838, 23.7275, "Athens"),
 "Ministry of Agriculture \u2014 GMO-free constitutional provision": (47.4979, 19.0402, "Budapest"),
 "Office National de S\u00e9curit\u00e9 Sanitaire des Produits Alimentaires": (34.0209, -6.8416, "Rabat"),
 "Food and Drug Administration \u2014 GM food registration": (25.0330, 121.5654, "Taipei"),
 "Saudi Food and Drug Authority \u2014 GM food rules": (24.7136, 46.6753, "Riyadh"),
 "International Rice Research Institute \u2014 Golden Rice": (14.1699, 121.2422, "Los Ba\u00f1os"),
 "Norwegian Biotechnology Advisory Board": (59.9139, 10.7522, "Oslo"),
 "Rewriting Extinction / genetic biocontrol programmes": (38.5449, -121.7405, "Davis"),
 "Nature Conservancy \u2014 biotechnology in conservation": (38.8816, -77.1109, "Arlington"),
 "Wellcome Leap": (51.5254, -0.1340, "London"),
 "China National Seed Group (Syngenta / Sinochem)": (39.9042, 116.4074, "Beijing"),
 "European Bioinformatics Institute \u2014 model organism databases": (52.0798, 0.1846, "Hinxton"),
 # --- round 62: animal experimentation facilities ---
 "USDA APHIS \u2014 annual research facility reports": (38.8977, -77.0261, "Washington DC"),
 "Charles River \u2014 global site network": (42.5470, -71.1730, "Wilmington MA"),
 "Jackson Laboratory \u2014 Bar Harbor": (44.3876, -68.2039, "Bar Harbor"),
 "Wisconsin National Primate Research Center": (43.0731, -89.4012, "Madison"),
 "Inotiv \u2014 facility network": (40.4259, -86.9081, "West Lafayette"),
 "Home Office \u2014 licensed establishments": (51.4995, -0.1248, "London"),
 "The Francis Crick Institute \u2014 animal research": (51.5316, -0.1284, "London"),
 "German Primate Center (DPZ)": (51.5413, 9.9158, "G\u00f6ttingen"),
 "Biomedical Primate Research Centre": (52.0355, 4.3266, "Rijswijk"),
 "Charles River / Janvier \u2014 European breeding sites": (48.0833, -0.7667, "Le Genest-Saint-Isle"),
 "Guangdong / Hainan primate breeding sector": (23.1291, 113.2644, "Guangzhou"),
 "Cyagen \u2014 Suzhou and Santa Clara facilities": (31.2989, 120.5853, "Suzhou"),
 "RIKEN BioResource Research Center": (36.0839, 140.0764, "Tsukuba"),
 "Committee for Control and Supervision of Experiments on Animals": (28.6139, 77.2090, "New Delhi"),
 "European Commission \u2014 ALURES animal use database": (50.8467, 4.3525, "Brussels"),
 # --- round 63: law firms, lobbying, named individuals ---
 "Arnold & Porter \u2014 agricultural biotechnology practice": (38.9007, -77.0500, "Washington DC"),
 "Covington & Burling \u2014 food and drug regulatory": (38.9007, -77.0180, "Washington DC"),
 "US Patent and Trademark Office \u2014 patent full-text search": (38.8462, -77.0563, "Alexandria"),
 "Patent Trial and Appeal Board": (38.8462, -77.0563, "Alexandria"),
 "European Patent Office \u2014 opposition register": (48.1351, 11.5820, "Munich"),
 "No Patents on Seeds": (48.1351, 11.5820, "Munich"),
 "EU Transparency Register \u2014 biotechnology lobbying": (50.8467, 4.3525, "Brussels"),
 "Euroseeds": (50.8467, 4.3525, "Brussels"),
 "Bayer Crop Science \u2014 divisional leadership": (38.6270, -90.1994, "St Louis"),
 "Broad Institute \u2014 CRISPR inventors and the patent record": (42.3629, -71.0865, "Cambridge MA"),
 "Innovative Genomics Institute \u2014 Jennifer Doudna": (37.8719, -122.2585, "Berkeley"),
 "Colossal Biosciences \u2014 founders and scientific advisers": (32.7767, -96.7970, "Dallas"),
 "He Jiankui \u2014 the germline case and its aftermath": (22.5431, 114.0579, "Shenzhen"),
 "Rothamsted Research": (51.8094, -0.3560, "Harpenden"),
 "Syngenta \u2014 sustainability and regulatory reporting": (47.5596, 7.5886, "Basel"),
 "OECD \u2014 Working Party on Biotechnology": (48.8566, 2.3522, "Paris"),
 "FAO \u2014 biotechnology and biosafety": (41.9028, 12.4964, "Rome"),
 # --- round 65: contract research and assisted reproduction ---
 "IQVIA": (40.0583, -74.4057, "Durham / Parsippany"),
 "Parexel": (42.3370, -71.2092, "Newton MA"),
 "Catalent": (40.5187, -74.4121, "Somerset NJ"),
 "ICON plc \u2014 site and patient networks": (53.3498, -6.2603, "Dublin"),
 "Fujifilm Diosynth Biotechnologies": (35.9940, -78.8986, "Research Triangle Park"),
 "ClinicalTrials.gov \u2014 sponsor and site search": (38.9959, -77.1013, "Bethesda"),
 "Pharmaron": (39.9042, 116.4074, "Beijing"),
 "BGI Genomics \u2014 clinical and prenatal testing": (22.5431, 114.0579, "Shenzhen"),
 "Celltrion": (37.3894, 126.6440, "Incheon"),
 "Serum Institute of India": (18.5204, 73.8567, "Pune"),
 "US Fertility": (38.9847, -77.0947, "Rockville"),
 "Kindbody": (40.7128, -74.0060, "New York"),
 "Cooper Surgical \u2014 culture media recall": (39.0349, -76.9822, "Silver Spring"),
 "Society for Reproductive Endocrinology and Infertility": (34.0489, -84.2400, "Birmingham AL"),
 "HFEA \u2014 treatment add-ons ratings": (51.5194, -0.1270, "London"),
 "Care Fertility": (52.9548, -1.1581, "Nottingham"),
 "Spanish Fertility Society \u2014 national registry": (40.4168, -3.7038, "Madrid"),
 "Cross-border surrogacy and gamete brokerage": (31.7683, 35.2137, "Jerusalem"),
 "Monash IVF": (-37.8136, 144.9631, "Melbourne"),
 # --- round 66: money, open release, clinical, livestock, synthesis ---
 "Blackstone Life Sciences": (40.7639, -73.9740, "New York"),
 "Novo Holdings": (55.7558, 12.5150, "Hellerup"),
 "SEC EDGAR \u2014 full-text search": (38.8977, -77.0261, "Washington DC"),
 "Open Philanthropy \u2014 biosecurity and science funding": (37.7749, -122.4194, "San Francisco"),
 "Wellcome Sanger Institute": (52.0798, 0.1846, "Hinxton"),
 "Sterile Insect Technique programmes \u2014 IAEA and national partners": (48.2340, 16.4166, "Vienna"),
 "Bayer / Ginkgo \u2014 Joyn Bio nitrogen fixation": (42.3601, -71.0589, "Boston"),
 "EPA \u2014 biopesticide and plant-incorporated protectant registrations": (38.8944, -77.0227, "Washington DC"),
 "Moscamed Brasil": (-12.2664, -38.9663, "Juazeiro"),
 "Recombinant DNA Advisory Committee \u2014 archive": (38.9959, -77.1013, "Bethesda"),
 "Jesse Gelsinger and the 1999 trial death \u2014 FDA record": (39.0349, -76.9822, "Silver Spring"),
 "Alnylam Pharmaceuticals": (42.3601, -71.0589, "Cambridge MA"),
 "FDA \u2014 intentional genomic alterations in animals": (39.0349, -76.9822, "Rockville"),
 "Hendrix Genetics": (52.6500, 5.0500, "Boxmeer"),
 "Topigs Norsvin": (52.0907, 5.1214, "Helvoirt"),
 "Mowi": (60.3913, 5.3221, "Bergen"),
 "International Gene Synthesis Consortium": (38.9072, -77.0369, "Washington DC"),
 "Benchling": (37.7749, -122.4194, "San Francisco"),
 "Codex DNA / Telesis Bio": (32.9027, -117.2003, "San Diego"),
 "Australian Frozen Zoo \u2014 threatened species cryobanking": (-37.7847, 144.9517, "Melbourne"),
 "Nature's SAFE": (52.7000, -2.7500, "Shropshire"),
 # --- round 67 ---
 "KWS SAAT": (52.1561, 9.9578, "Einbeck"),
 "DLF Seeds": (55.4038, 10.4024, "Roskilde"),
 "Groupe Florimond Desprez": (50.5167, 3.2500, "Cappelle-en-P\u00e9v\u00e8le"),
 "Sakata Seed": (35.4437, 139.6380, "Yokohama"),
 "Bucher / agricultural machinery and data": (47.4979, 8.7280, "Niederweningen"),
 "Beam Therapeutics": (42.3601, -71.0589, "Cambridge MA"),
 "Prime Medicine": (42.3601, -71.0589, "Cambridge MA"),
 "Arcadia Biosciences": (38.5449, -121.7405, "Davis"),
 "Zymergen / Ginkgo \u2014 the collapse and absorption": (37.8716, -122.2727, "Emeryville"),
 "Tropic Biosciences": (52.6220, 1.2214, "Norwich"),
 "Element Biosciences": (32.9027, -117.2003, "San Diego"),
 "Ultima Genomics": (37.5485, -121.9886, "Fremont"),
 "New England Biolabs": (42.5806, -70.8828, "Ipswich MA"),
 "WHO \u2014 human genome editing governance framework": (46.2324, 6.1370, "Geneva"),
 "African Union \u2014 continental biosafety and biotechnology policy": (9.0320, 38.7469, "Addis Ababa"),
 "Ministry of Agriculture \u2014 GMO prohibition": (44.7866, 20.4489, "Belgrade"),
 "Ministry of Environment and Water \u2014 GMO register": (42.6977, 23.3219, "Sofia"),
 "Sri Lanka \u2014 food labelling and import control": (6.9271, 79.8612, "Colombo"),
 "SEARCA \u2014 regional biotechnology information": (14.1699, 121.2422, "Los Ba\u00f1os"),
 # --- round 68 ---
 "Regeneron Genetics Center": (41.1220, -73.7949, "Tarrytown"),
 "bluebird bio \u2014 the insertional oncogenesis cases": (39.0349, -76.9822, "Silver Spring"),
 "Moderna": (42.3601, -71.0589, "Cambridge MA"),
 "Institute for Clinical and Economic Review": (42.3601, -71.0589, "Boston"),
 "CRISPR Therapeutics": (47.1662, 8.5155, "Zug"),
 "a16z Bio + Health": (37.4419, -122.1430, "Menlo Park"),
 "NIH RePORTER": (38.9959, -77.1013, "Bethesda"),
 "BARDA \u2014 Biomedical Advanced Research and Development Authority": (38.8977, -77.0261, "Washington DC"),
 "Temasek \u2014 agri-food and life sciences": (1.3521, 103.8198, "Singapore"),
 "Alliance for Science / Cornell \u2014 agricultural biotechnology communications": (42.4440, -76.5019, "Ithaca"),
 "Zoetis": (40.4406, -74.4057, "Parsippany"),
 "Neogen": (42.7325, -84.5555, "Lansing"),
 "Fonterra": (-36.8485, 174.7633, "Auckland"),
 "Revive & Restore \u2014 black-footed ferret cloning": (37.9735, -122.5311, "Sausalito"),
 "Oxitec \u2014 US releases and EPA experimental use permits": (24.5551, -81.7800, "Florida Keys"),
 "Guangzhou Wolbaki \u2014 mosquito production": (23.1291, 113.2644, "Guangzhou"),
 "African Centre for Biodiversity \u2014 corporate research": (-26.2041, 28.0473, "Johannesburg"),
 "Grain SA and the commercial maize sector": (-26.7145, 27.0972, "Potchefstroom"),
 "INASE \u2014 seed royalties and farm-saved seed": (-34.6037, -58.3816, "Buenos Aires"),
 "Federation of Seed Industry of India": (28.6139, 77.2090, "New Delhi"),
 "CONAHCYT \u2014 native maize and public research": (19.4326, -99.1332, "Mexico City"),
 # --- round 69 ---
 "IUCN \u2014 synthetic biology and biodiversity conservation": (46.4312, 6.2100, "Gland"),
 "American Chestnut Research and Restoration Project \u2014 SUNY ESF": (43.0481, -76.1474, "Syracuse"),
 "Colossal Foundation": (32.7767, -96.7970, "Dallas"),
 "Frozen Ark Project": (52.9548, -1.1581, "Nottingham"),
 "Target Malaria \u2014 Imperial College programme record": (51.4988, -0.1749, "London"),
 "Cibus": (32.9027, -117.2003, "San Diego"),
 "Bayer \u2014 Crop Science product safety summaries": (51.0333, 6.9833, "Leverkusen"),
 "Center for Food Safety \u2014 animal biotechnology litigation": (38.9072, -77.0369, "Washington DC"),
 "Genus \u2014 PRRS pig commercialisation record": (52.4862, -1.8904, "Basingstoke"),
 "AquaChile / Agrosuper": (-41.4693, -72.9424, "Puerto Montt"),
 "Norwegian Institute of Marine Research \u2014 escape monitoring": (60.3913, 5.3221, "Bergen"),
 "Novartis \u2014 Zolgensma outcomes-based agreements": (47.5596, 7.5886, "Basel"),
 "Cure Rare Disease and the 2022 trial death": (39.0349, -76.9822, "Silver Spring"),
 "Alliance for Regenerative Medicine \u2014 sector data": (38.9072, -77.0369, "Washington DC"),
 "MHRA \u2014 Innovative Licensing and Access Pathway": (51.4995, -0.1248, "London"),
 "Thermo Fisher \u2014 Patheon and clinical services": (35.9940, -78.8986, "Durham NC"),
 "Advarra": (39.0840, -77.1528, "Columbia MD"),
 "BGI \u2014 MGI Tech instruments": (22.5431, 114.0579, "Shenzhen"),
 "Syncona": (51.5194, -0.1270, "London"),
 "European Investment Bank \u2014 life sciences lending": (49.6116, 6.1319, "Luxembourg"),
 # --- round 70 ---
 "Enza Zaden": (52.7167, 4.7500, "Enkhuizen"),
 "Bejo Zaden": (52.6500, 4.7833, "Warmenhuizen"),
 "Beck's Hybrids": (39.9784, -86.0086, "Atlanta, Indiana"),
 "Corteva \u2014 seed applied technologies": (39.7684, -86.1581, "Indianapolis"),
 "Verve Therapeutics": (42.3601, -71.0589, "Boston"),
 "Mammoth Biosciences": (37.8044, -122.2712, "Brisbane CA"),
 "Colossal \u2014 Breaking spin-out and IP licensing": (32.7767, -96.7970, "Dallas"),
 "Alpha Genesis": (32.6935, -80.8534, "Yemassee SC"),
 "Ace Animals / laboratory dog and cat supply": (38.8977, -77.0261, "Washington DC"),
 "Fairfax Cryobank / California Cryobank \u2014 donor limits": (38.8462, -77.3064, "Fairfax VA"),
 "Donor Sibling Registry": (39.7392, -104.9903, "Denver"),
 "Indian Council of Medical Research \u2014 ART regulation": (28.6139, 77.2090, "New Delhi"),
 "UPOV \u2014 International Union for the Protection of New Varieties of Plants": (46.2324, 6.1370, "Geneva"),
 "Codex Alimentarius \u2014 foods derived from biotechnology": (41.9028, 12.4964, "Rome"),
 "European Food Safety Authority \u2014 GMO panel opinions": (44.8378, 11.6197, "Parma"),
 "Vietnam \u2014 GM maize cultivation and feed imports": (21.0278, 105.8342, "Hanoi"),
 "Institute for Agricultural Research, Zaria \u2014 Bt cowpea": (11.1113, 7.7227, "Zaria"),
 "Egypt \u2014 wheat import tenders and GM specification": (30.0444, 31.2357, "Cairo"),
 # --- round 71 ---
 "Pivot Bio \u2014 PROVEN product record": (37.8716, -122.2727, "Berkeley"),
 "Marrone / Pro Farm Group": (38.5449, -121.7405, "Davis"),
 "USDA APHIS \u2014 biotechnology regulatory notices": (38.8977, -77.0261, "Washington DC"),
 "Rothamsted \u2014 GM aphid-repellent wheat trial": (51.8094, -0.3560, "Harpenden"),
 "CSIRO \u2014 agricultural biotechnology": (-35.2809, 149.1300, "Canberra"),
 "ViaGen \u2014 Przewalski's horse and endangered species cloning": (30.5083, -97.6789, "Cedar Park"),
 "Wildlife Conservation Society \u2014 biotechnology position": (40.8506, -73.8770, "Bronx NY"),
 "Rhino and wildlife biobanking \u2014 BioRescue partners": (-1.2921, 36.8219, "Ol Pejeta / Nairobi"),
 "Vertex Pharmaceuticals": (42.3601, -71.0589, "Boston"),
 "National Marrow Donor Program / NMDP \u2014 cell therapy infrastructure": (44.9778, -93.2650, "Minneapolis"),
 "Sickle Cell Disease Association of America": (39.2904, -76.6122, "Hanover MD"),
 "PMDA \u2014 regenerative medicine conditional approval": (35.6762, 139.6503, "Tokyo"),
 "Fidelity and index funds \u2014 passive ownership of the sector": (38.8977, -77.0261, "Washington DC"),
 "Bill & Melinda Gates Agricultural Innovations (Gates Ag One)": (38.6270, -90.1994, "St Louis"),
 "Chinese state agricultural investment \u2014 seed industry revitalisation": (39.9042, 116.4074, "Beijing"),
 "Aurigene / Dr Reddy's discovery services": (12.9716, 77.5946, "Bengaluru"),
 "SK pharmteco": (37.5665, 126.9780, "Seoul"),
 "Ministry of Agriculture \u2014 GMO cultivation prohibition": (52.2297, 21.0122, "Warsaw"),
 "Malaysian Palm Oil Board \u2014 genome programme": (3.1390, 101.6869, "Kajang"),
 # --- round 72 ---
 "S&W Seed Company": (36.7378, -119.7871, "Fresno"),
 "Simplot \u2014 Innate potatoes": (43.6150, -116.2023, "Boise"),
 "J.R. Simplot / McCain \u2014 processor specification": (46.1351, -67.0837, "Florenceville"),
 "Euralis / Lidea": (43.2951, -0.3708, "Pau"),
 "TMG \u2014 Tropical Melhoramento & Gen\u00e9tica": (-23.3103, -51.1628, "Londrina"),
 "Perfect Day": (37.5485, -121.9886, "Berkeley"),
 "Impossible Foods \u2014 soy leghemoglobin": (37.4419, -122.1430, "Redwood City"),
 "Conagen": (42.3601, -71.0589, "Bedford MA"),
 "Charles River \u2014 horseshoe crab and LAL supply": (32.7765, -79.9311, "Charleston SC"),
 "Institutional Animal Care and Use Committees \u2014 OLAW": (38.9959, -77.1013, "Bethesda"),
 "Editas Medicine": (42.3601, -71.0589, "Cambridge MA"),
 "Orchard Therapeutics": (51.5194, -0.1270, "London"),
 "European Sperm Bank": (55.6761, 12.5683, "Copenhagen"),
 "Greek cross-border fertility sector": (37.9838, 23.7275, "Athens"),
 "WTO \u2014 SPS Committee and biotechnology notifications": (46.2244, 6.1432, "Geneva"),
 "ISO \u2014 biotechnology standards committee": (46.2324, 6.1370, "Geneva"),
 "COMESA \u2014 regional biosafety policy": (-15.3875, 28.3228, "Lusaka"),
 "Volcani Center \u2014 Agricultural Research Organization": (32.0104, 34.8199, "Rishon LeZion"),
 "International Center for Biosaline Agriculture": (25.0968, 55.3900, "Dubai"),
 "International Potato Center (CIP)": (-12.0782, -76.9450, "Lima"),
 "Ethiopian Biodiversity Institute": (9.0320, 38.7469, "Addis Ababa"),
 # --- round 73 ---
 "Corteva \u2014 hybrid wheat programme": (39.7684, -86.1581, "Indianapolis"),
 "Bayer \u2014 short-stature corn": (38.6270, -90.1994, "St Louis"),
 "Corteva \u2014 Enlist herbicide system": (39.7684, -86.1581, "Indianapolis"),
 "Ohalo Genetics": (37.5485, -121.9886, "Aptos CA"),
 "Inari \u2014 SEEDesign platform": (42.3601, -71.0589, "Cambridge MA"),
 "Syngenta \u2014 biologicals and Valagro": (47.5596, 7.5886, "Basel"),
 "BASF \u2014 enzymes and industrial biotechnology": (49.4875, 8.4660, "Ludwigshafen"),
 "dsm-firmenich": (52.0907, 5.1214, "Maastricht / Kaiseraugst"),
 "Novo Nordisk \u2014 recombinant insulin manufacture": (55.7558, 12.5150, "Bagsv\u00e6rd"),
 "Biocon \u2014 biosimilar insulin": (12.9716, 77.5946, "Bengaluru"),
 "Oxford Nanopore \u2014 field sequencing": (51.7520, -1.2577, "Oxford"),
 "Roslin Institute": (55.9533, -3.1883, "Midlothian"),
 "Yuan Longping High-Tech Agriculture": (28.2282, 112.9388, "Changsha"),
 "Bioceres / Moolec \u2014 molecular farming": (-32.9468, -60.6393, "Rosario"),
 "ISAAA AfriCenter": (-1.2921, 36.8219, "Nairobi"),
 "Kenya Plant Health Inspectorate Service": (-1.2921, 36.8219, "Nairobi"),
 "CIMMYT \u2014 maize and wheat genebank": (19.5304, -98.8464, "Texcoco"),
 "MASIPAG": (14.1699, 121.2422, "Los Ba\u00f1os"),
 # --- round 79 ---
 "American Seed Trade Association": (38.8816, -77.1109, "Alexandria VA"),
 "Seed Savers Exchange": (43.3045, -91.7960, "Decorah"),
 "Organic Seed Alliance": (48.1171, -123.4307, "Port Townsend"),
 "Scribe Therapeutics": (37.8716, -122.2727, "Alameda"),
 "Tome Biosciences / large-payload integration": (42.3601, -71.0589, "Watertown MA"),
 "iGEM Foundation": (42.3601, -71.0589, "Paris / Boston"),
 "Cyagen / knockout mouse repositories \u2014 IMPC": (52.0798, 0.1846, "Hinxton"),
 "Physicians Committee / animal testing policy": (38.9072, -77.0369, "Washington DC"),
 "Cargill": (44.9778, -93.2650, "Minnetonka"),
 "Archer Daniels Midland": (41.8781, -87.6298, "Chicago"),
 "Nuffield Council on Bioethics": (51.5194, -0.1270, "London"),
 "UK Biobank": (53.4808, -2.2426, "Stockport"),
 "Nucleus Genomics": (40.7128, -74.0060, "New York"),
 "Society for Assisted Reproductive Technology \u2014 clinic outcome reports": (34.0489, -84.2400, "Birmingham AL"),
 "Foundation for Food & Agriculture Research": (38.9072, -77.0369, "Washington DC"),
 "Norwegian Government Pension Fund Global \u2014 ethics exclusions": (59.9139, 10.7522, "Oslo"),
 "Swiss GMO moratorium \u2014 Federal Office for the Environment": (46.9480, 7.4474, "Bern"),
 "Global 2000 / Friends of the Earth Austria": (48.2082, 16.3738, "Vienna"),
 "Wageningen University & Research": (51.9692, 5.6654, "Wageningen"),
}


# --- organisation type -------------------------------------------------------
# The facets say what part of the industry something works in. They do not say
# what KIND of body it is, and a ministry, a committee, a company and a campaign
# group are not the same thing to argue with. Type is derived from the entry's
# own name and its base record rather than hand-tagged, so it stays consistent
# across 420 entries and can be re-derived when entries change.
_TYPE_WORDS = (
 ("igo",       ("united nations", "oecd", "fao", "who ", "wto", "unep", "cbd",
                "european commission", "european food safety", "european patent",
                "european investment", "codex", "iaea", "upov", "world bank",
                "african union", "comesa", "iucn", "cgiar", "searca", "iso ")),
 ("ministry",  ("ministry", "ministerio", "minist\u00e8re", "department of",
                "administration", "authority", "agency", "inspectorate",
                "service", "office of", "usda", "aphis", "fda ", "epa ",
                "government", "federal", "national biosafety", "customs",
                "home office", "secretariat", "gasc", "kephis", "inase",
                "senave", "conahcyt", "cibiogem", "ages", "onssa", "sag ")),
 ("committee", ("committee", "commission", "council", "board", "panel",
                "ctnbio", "geac", "conabia", "advisory")),
 ("institute", ("institute", "university", "college", "academy", "centre",
                "center", "laboratory", "research", "cimmyt", "embrapa",
                "riken", "csiro", "rothamsted", "roslin", "sanger", "broad",
                "volcani", "iita", "irri", "zoo", "genebank", "biobank")),
 ("association",("association", "federation", "croplife", "euroseeds", "bio \u2014",
                "society for", "alliance for regenerative", "isaaa",
                "consortium", "grain sa", "seed trade")),
 ("ngo",       ("no patents on seeds", "greenpeace", "genewatch", "friends of the earth",
                "global 2000", "revive & restore", "nature conservancy",
                "wildlife conservation", "center for food safety", "masipag",
                "african centre for biodiversity", "seed savers", "organic seed",
                "donor sibling", "physicians committee", "sickle cell",
                "nature\u2019s safe", "nature's safe", "frozen ark", "understanding animal")),
 ("fund",      ("foundation", "trust", "capital", "ventures", "venture",
                "partners", "holdings", "investment", "philanthrop", "wellcome",
                "gates", "blackstone", "temasek", "syncona", "a16z", "flagship",
                "arch ", "pension fund", "leaps by", "reporter", "barda",
                "nifa", "index funds")),
 ("registry",  ("register", "registry", "database", "clinicaltrials", "edgar",
                "reporter", "search", "record", "statistics", "alures",
                "patentscope", "espacenet", "wiews", "genesys")),
)


def org_type(name, base_kind, skind):
    """One of nine types. Order matters: an igo that is also a 'commission'
    should read as an igo, and a company with 'research' in its name should not
    become an institute, so the company test runs on the base record first."""
    low = " " + name.lower() + " "
    for t, words in _TYPE_WORDS:
        if any(w in low for w in words):
            return t
    if base_kind == "structured" or skind == "database":
        return "registry"
    return "company"

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
            # Carried so the index and the lens/sub filters can work off the
            # points. Before this they read trackerData, which ships empty since
            # entries became map points - so the index was blank and every lens
            # button did nothing.
            "tags": x.get("tags", []),
            "kind": x.get("kind", "structured"),
            "voice": x.get("voice", "interpretive"),
            "trust": x.get("trust", "high"),
            "skind": x.get("skind", "other"),
            "company": x.get("company") or "",
            "otype": org_type(x["name"], x.get("kind", ""), x.get("skind", "")),
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
