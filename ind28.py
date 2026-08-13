# -*- coding: utf-8 -*-
"""Industry entries, part 28.

Breadth, in the places a single entry per country was standing in for a whole
national system: Latin America outside Brazil and Argentina, southeast Asia, and
the Gulf states now buying their way into food security.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND28 = {}

# ================================================== LATIN AMERICA =============
IND28["ARG"] = [
 e("INTA \u2014 Instituto Nacional de Tecnolog\u00eda Agropecuaria",
   "https://www.argentina.gob.ar/inta",
   "Argentina\u2019s public agricultural research institute, which developed the "
   "drought-tolerant wheat trait Bioceres commercialised. The trait was made with public "
   "money at a public institute and is sold by a private company under licence \u2014 the "
   "standard arrangement in this field, and the public share of the return is a matter "
   "of contract rather than of principle.",
   ["seed:traits", "seed:germplasm"], base=BODY),
 e("Bolsa de Cereales / grain trade associations",
   "https://www.bolsadecereales.com/",
   "The Buenos Aires grain exchange, which publishes the planting and harvest estimates "
   "the trade runs on. Argentina is among the largest exporters of soy and maize in the "
   "world, and what its exchange reports moves prices everywhere \u2014 including for farmers "
   "who have never heard of it.",
   ["seed:distribution", "money:markets"], base=ASSN),
]

IND28["BRA"] = [
 e("Agropalma / palm and tropical oils", "https://www.agropalma.com.br/",
   "Brazilian palm oil production in the Amazon basin, certified and audited against "
   "deforestation criteria. Palm expansion in South America is far smaller than in "
   "southeast Asia and growing, and it is the case where certification is being applied "
   "from the start rather than retrofitted after the clearing.",
   ["trees", "seed:distribution"]),
 e("Fiocruz \u2014 Oswaldo Cruz Foundation", "https://portal.fiocruz.br/",
   "Brazil\u2019s public health research foundation, which manufactures vaccines at scale and "
   "ran the local partnership for Wolbachia mosquito releases against dengue. It is the "
   "clearest example in the Americas of a public institution holding both the research "
   "and the manufacturing, so what it develops it can also make and give away.",
   ["clinical:therapy", "wild:insects"], base=BODY),
]

IND28["CHL"] = [
 e("ANASAC / Chilean seed multiplication", "https://www.anasac.cl/",
   "Counter-season seed multiplication for northern hemisphere breeders, which is a large "
   "and little-discussed part of the world seed system. Chile grows engineered seed for "
   "export that its own farmers may not plant, so the country carries the agronomic risk "
   "of a crop it has not approved for itself.",
   ["seed:distribution", "seed:germplasm"]),
]

IND28["CRI"] = [
 e("CATIE \u2014 tropical agricultural research and genebank",
   "https://www.catie.ac.cr/",
   "Holds the world\u2019s most important coffee and cacao collections, in Costa Rica. Both "
   "crops are grown by millions of smallholders and both face diseases conventional "
   "breeding has struggled with, so what is in this collection sets the limits of what "
   "either crop can become.",
   ["seed:germplasm", "trees"], base=BODY),
]

IND28["CUB"] = [
 e("Instituto Nacional de Ciencias Agr\u00edcolas", "https://www.inca.edu.cu/",
   "Cuba\u2019s agricultural research institute, in a country that turned to low-input and "
   "biological methods after Soviet fertiliser and fuel supplies ended in 1990. That "
   "transition is the largest involuntary experiment in low-input agriculture anyone has "
   "run, and its results are argued over by both sides of this debate.",
   ["seed:traits", "wild:microbes"], base=BODY),
]

# ================================================== SOUTHEAST ASIA ============
IND28["IDN"] = [
 e("Indonesian Agency for Agricultural Research and Development",
   "https://www.litbang.pertanian.go.id/",
   "Indonesia\u2019s agricultural research agency, for a country of 280 million that is a "
   "centre of diversity for rice, banana and spices and the world\u2019s largest palm oil "
   "producer. Decisions taken here affect more people and more land than most of the "
   "national bodies on this map, and reach English-language discussion almost never.",
   ["seed:traits", "trees"], base=BODY),
]

IND28["PHL"] = [
 e("Philippine Rice Research Institute", "https://www.philrice.gov.ph/",
   "The national rice institute, which worked on Golden Rice alongside IRRI and holds the "
   "Philippine rice collections. When a court cancelled the Golden Rice permit in 2024 it "
   "cancelled a public institute\u2019s product, not a company\u2019s \u2014 which is why that case "
   "does not fit the usual account of who wants what.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]

IND28["VNM"] = [
 e("Vietnam Academy of Agricultural Sciences", "https://vaas.vn/",
   "Vietnam\u2019s agricultural research system, in one of the largest rice-exporting "
   "countries in the world. Rice is where the food-security argument for engineering is "
   "strongest and where adoption has been slowest, because the export market has been "
   "the constraint rather than the science.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]

IND28["THA"] = [
 e("BIOTEC \u2014 National Center for Genetic Engineering and Biotechnology",
   "https://www.biotec.or.th/",
   "Thailand\u2019s national biotechnology centre, working on rice, shrimp and cassava. "
   "Thailand permits no commercial GM cultivation while conducting substantial research, "
   "which is a common arrangement and one that leaves a national capability with nowhere "
   "domestic to go.",
   ["seed:traits", "livestock:aqua"], base=BODY),
]

# ======================================================= THE GULF ============
IND28["ARE"] = [
 e("Silal / UAE food security investment", "https://www.silal.ae/",
   "An Abu Dhabi state food company buying and building agricultural capacity at home and "
   "abroad. Gulf states import most of what they eat and have responded by acquiring "
   "farmland and food technology overseas \u2014 so a country with almost no agriculture is "
   "now a significant owner of other countries\u2019 agriculture.",
   ["money:public", "seed:distribution"]),
]

IND28["SAU"] = [
 e("King Abdullah University of Science and Technology \u2014 desert agriculture",
   "https://www.kaust.edu.sa/",
   "Research on crops for saline water and extreme heat, funded at a scale few public "
   "institutions match. Salinity and heat tolerance affect an enormous and growing area "
   "of farmland worldwide and attract a fraction of the investment that herbicide "
   "tolerance does, so where this work is funded at all is worth knowing.",
   ["seed:traits", "editing:agtech"], base=BODY),
]
