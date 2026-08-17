# -*- coding: utf-8 -*-
"""Industry entries, part 46. Who pays, who buys, and the last two production gaps.

PUBLIC FUNDERS AND INSTITUTES. Most of what this industry sells began in a
publicly funded laboratory. The map held the databases those funders publish and
not the funders, which recorded the output and lost the decision.

NAMED FINANCE. The passive-ownership entry was generic. Naming the three index
managers makes it checkable, because they are the largest shareholders in nearly
every listed company on this map at once - which is a different kind of
concentration from the four-companies-hold-the-seed kind, and a less discussed
one.

THE BUYER ROW. Retail and food-manufacturer specifications moved more European
acreage than any law did. A buyer saying it will not accept engineered material
is not regulation and works faster.

FORESTRY, AQUACULTURE AND INDUSTRIAL. Three production gaps left from the
additions list.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND46 = {}

# ===================================================== PUBLIC FUNDERS =========
IND46["USA"] = [
 e("ARPA-H",
   "https://arpa-h.gov/",
   "A US health research agency created in 2022 on the DARPA model, funding "
   "high-risk biomedical programmes on fixed timelines. Agencies built this way "
   "choose directions rather than reviewing proposals, which concentrates a great "
   "deal of influence over what gets attempted in a small number of programme "
   "managers.",
   ["money:public", "clinical:therapy", "editing:platform"], base=BODY),
 e("Cold Spring Harbor Laboratory",
   "https://www.cshl.edu/",
   "Where the 1975 Asilomar-era conversations about recombinant DNA were shaped and "
   "where a great deal of foundational molecular biology was done. It is also the "
   "institution whose earlier history included the Eugenics Record Office, which is "
   "part of the same building's record and part of why arguments about human "
   "genetics carry the weight they do.",
   ["editing:platform", "money:public", "clinical:germline"], base=BODY),
 e("Chan Zuckerberg Initiative",
   "https://chanzuckerberg.com/",
   "Funds cell atlases, imaging and open software for biology at a scale comparable "
   "to a national agency, with no public accountability attached. Philanthropy on "
   "this map has been Gates-dominated; this is the second source large enough to "
   "set direction on its own.",
   ["money:philanthropy", "synthesis:seq", "editing:platform"], base=BODY),
]

IND46["BEL"] = [
 e("European Research Council",
   "https://erc.europa.eu/",
   "Funds investigator-led research across the EU on scientific merit alone, and is "
   "the main European source for the basic work that later becomes a platform. "
   "Emmanuelle Charpentier's CRISPR work was ERC-funded, which is why a European "
   "public grant sits behind a patent estate now licensed worldwide.",
   ["money:public", "editing:platform"], base=BODY),
]

IND46["DEU"] = [
 e("Max Planck Society",
   "https://www.mpg.de/en",
   "Germany's principal basic research organisation, and where Charpentier ran the "
   "unit that produced her share of the CRISPR patents. Institutes of this kind "
   "hold the intellectual property their researchers generate, so a public research "
   "body becomes a licensor whether or not it set out to be one.",
   ["money:public", "editing:patents", "editing:platform"], base=BODY),
 e("EMBL \u2014 European Molecular Biology Laboratory",
   "https://www.embl.org/",
   "An intergovernmental research organisation funded by 28 member states, running "
   "the European Nucleotide Archive and the sequence databases most of this field "
   "depends on. Open sequence data is a deliberate arrangement paid for by "
   "governments, and it is also what makes any pathogen genome a synthesis "
   "template.",
   ["synthesis:repos", "synthesis:seq", "money:public"], base=BODY),
]

IND46["FRA"] = [
 e("Institut Pasteur",
   "https://www.pasteur.fr/en",
   "A private foundation doing public work on infectious disease, with a network of "
   "institutes across thirty countries, many in places with no other high-capacity "
   "laboratory. That network is where a great deal of pathogen sequencing actually "
   "happens, and it long predates any international arrangement for it.",
   ["wild:microbes", "money:philanthropy", "synthesis:seq"], base=BODY),
]

# ======================================================== NAMED FINANCE =======
IND46["USA"] += [
 e("BlackRock",
   "https://www.blackrock.com/",
   "The largest asset manager in the world and, through index funds, among the "
   "largest shareholders in Bayer, Corteva, Thermo Fisher, Illumina and most other "
   "listed companies on this map at once. Common ownership of competitors by the "
   "same few managers is a form of concentration that no merger review examines, "
   "because no merger occurred.",
   ["money:markets", "rules:influence"]),
 e("Alexandria Real Estate Equities",
   "https://www.are.com/",
   "Owns and leases much of the purpose-built laboratory space in Cambridge, South "
   "San Francisco and San Diego. Biological work needs containment-rated buildings "
   "that take years to construct, so a landlord holding the supply in three "
   "clusters has a quiet say in which companies can exist at all.",
   ["money:markets", "cro:cdmo"]),
]

IND46["NLD"] = [
 e("Rabobank",
   "https://www.rabobank.com/",
   "The largest agricultural lender in the world, financing farms, traders and "
   "processors across dozens of countries, and publishing the sector analysis the "
   "industry plans against. Credit decides which farms can carry the cost of a "
   "seed-and-chemical package, which is a stronger filter on adoption than approval "
   "is.",
   ["money:markets", "seed:distribution"]),
]

# ============================================================ BUYERS ==========
IND46["CHE"] = [
 e("Nestl\u00e9",
   "https://www.nestle.com/",
   "The largest food company in the world, and a buyer whose sourcing "
   "specifications reach millions of hectares. When a manufacturer of this size "
   "says it will not accept engineered ingredients in a market, growers in that "
   "supply chain stop planting them \u2014 a decision taken commercially, with no "
   "consultation and no appeal.",
   ["seed:distribution", "rules:influence", "money:markets"]),
]

IND46["GBR"] = [
 e("Unilever",
   "https://www.unilever.com/",
   "Sets ingredient specifications across food and household products in most "
   "countries, including on engineered material and on the palm and soy it buys. "
   "Buyer specifications are the mechanism that moved European acreage away from "
   "engineered crops, and they are written by companies rather than parliaments.",
   ["seed:distribution", "rules:influence", "editing:synbio"]),
]

IND46["USA"] += [
 e("Walmart",
   "https://corporate.walmart.com/",
   "The largest grocery retailer in the world. Its sourcing standards travel "
   "upstream through suppliers who cannot afford to lose the account, which makes a "
   "retail purchasing policy one of the few instruments that changes agricultural "
   "practice across borders without any legal force at all.",
   ["seed:distribution", "rules:influence"]),
]

# =================================================== FORESTRY AND AQUA ========
IND46["USA"] += [
 e("ArborGen",
   "https://www.arborgen.com/",
   "The largest supplier of forest tree seedlings in the world, and the developer "
   "of engineered eucalyptus and loblolly pine programmes. A tree planted now is "
   "harvested in twenty to forty years, so an engineered forest is a decision that "
   "cannot be revisited on any normal regulatory timescale.",
   ["trees", "seed:traits", "seed:germplasm"]),
]

IND46["NOR"] = [
 e("Benchmark Genetics",
   "https://www.benchmarkgenetics.com/",
   "Breeds salmon, shrimp and tilapia for aquaculture worldwide, using genomic "
   "selection and disease-resistance programmes. Farmed salmon is among the most "
   "intensively bred animals on Earth, and escapes into wild rivers make that "
   "breeding an environmental question rather than an agricultural one.",
   ["livestock:aqua", "animals:breeders", "seed:germplasm"]),
]

# ================================================= INDUSTRIAL BIOTECH =========
IND46["USA"] += [
 e("LanzaTech",
   "https://lanzatech.com/",
   "Ferments engineered bacteria on industrial waste gas, turning steel-mill "
   "emissions into ethanol and chemicals at commercial plants in China, Belgium and "
   "India. Carbon capture performed by a modified organism is regulated as "
   "industrial processing rather than as biotechnology, which is why almost nobody "
   "counts it.",
   ["editing:synbio", "wild:microbes", "money:markets"]),
 e("Genomatica",
   "https://www.genomatica.com/",
   "Engineers microbes to make chemical intermediates \u2014 nylon precursors, "
   "solvents, plasticisers \u2014 that are otherwise made from oil. The organisms "
   "never leave the tank and the product carries no label, so an engineered "
   "manufacturing route reaches consumers with no disclosure of any kind.",
   ["editing:synbio", "wild:microbes"]),
]
