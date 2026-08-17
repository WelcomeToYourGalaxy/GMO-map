# -*- coding: utf-8 -*-
"""Industry entries, part 45. Population genomics, China's working companies,
and the testing tier that enforces every labelling rule.

POPULATION GENOMICS. National sequencing programmes, each with a different
answer to who owns the result. Iceland's went to a company, Finland's runs
through a public-private consortium, Estonia's is a state biobank, and the Gulf
programmes are sovereign. The comparison is the point.

CHINA'S WORKING COMPANIES. The Chinese entries on this map were state bodies and
multinationals. The firms that actually do the editing were missing, which made
the largest state programme in the world look like policy without practitioners.

TESTING AND CERTIFICATION. A labelling rule is enforced by a laboratory finding
something, and by a certifier withdrawing a mark. Both are private, and between
them they decide what a positive result costs.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND45 = {}

# =================================================== POPULATION GENOMICS ======
IND45["FIN"] = [
 e("FinnGen",
   "https://www.finngen.fi/en",
   "Links genetic data from around half a million Finns to a national health "
   "register going back decades, in a partnership between Finnish universities and "
   "a group of pharmaceutical companies. Finland's population history makes rare "
   "variants unusually common there, so the country is scientifically valuable in a "
   "way that created the arrangement rather than the other way round.",
   ["synthesis:seq", "money:markets", "clinical:trials"], base=BODY),
]

IND45["EST"] = [
 e("Estonian Biobank",
   "https://genomics.ut.ee/en/content/estonian-biobank",
   "Holds genetic data on roughly a fifth of the adult Estonian population, run by "
   "the state, with results returned to participants through the national health "
   "system. It is the clearest working example of a national genomic programme "
   "operated as public infrastructure rather than as a research asset or a company "
   "holding.",
   ["synthesis:seq", "money:public", "repro:screening"], base=BODY),
]

IND45["ARE"] = [
 e("Emirati Genome Programme",
   "https://mohap.gov.ae/",
   "Sequencing the entire Emirati population, with the data held by the state and "
   "used in preventive health and in newborn screening. Sovereign genomic "
   "programmes of this kind are being built across the Gulf, and they answer the "
   "ownership question by not asking it: the state holds everything.",
   ["synthesis:seq", "money:public", "repro:screening"], base=BODY),
]

IND45["CHN"] = [
 e("China Kadoorie Biobank",
   "https://www.ckbiobank.org/",
   "Half a million adults across ten regions of China, followed for two decades in "
   "a collaboration with Oxford. One of the largest prospective cohorts in "
   "existence, and the main source of evidence on how genetic risk plays out in a "
   "non-European population.",
   ["synthesis:seq", "money:public", "clinical:trials"], base=BODY),
]

# ============================================ CHINA'S WORKING COMPANIES =======
IND45["CHN"] += [
 e("Qi Biodesign",
   "https://www.qibiodesign.com/",
   "Develops its own editing tools rather than licensing Western ones, and works on "
   "edited crops for the Chinese market. Chinese groups building an editing "
   "toolchain outside the CRISPR patent estate is the practical answer to a "
   "licensing regime that would otherwise decide who may commercialise an edited "
   "crop.",
   ["editing:platform", "editing:agtech", "editing:patents"]),
 e("EdiGene",
   "https://www.edigene.com/",
   "Runs gene-editing therapy programmes in China, including for blood disorders, "
   "under a domestic approval route rather than the FDA or EMA. China has "
   "authorised cell and gene therapies its Western counterparts have not, and this "
   "is one of the companies working through that difference.",
   ["editing:platform", "clinical:therapy", "clinical:trials"]),
 e("Origin Agritech",
   "https://www.originagritech.com/",
   "Held the first biosafety certificate granted in China for an engineered maize "
   "trait, phytase corn, in 2009 \u2014 and then watched food-crop approvals stop "
   "for a decade. Its history is the record of that pause, which was policy rather "
   "than science.",
   ["seed:traits", "seed:licensees", "rules:regulators"]),
 e("Yazhou Bay Seed Laboratory, Hainan",
   "http://www.hainan.gov.cn/",
   "A state seed-breeding complex on Hainan, where the climate allows several "
   "generations a year and where much of China's crop breeding is accelerated. "
   "Concentrating national breeding capacity in one place is a deliberate "
   "industrial policy, and there is no equivalent elsewhere.",
   ["seed:germplasm", "seed:traits", "money:public"], base=BODY),
]

# ============================================ TESTING AND CERTIFICATION =======
IND45["CHE"] = [
]

IND45["GBR"] = [
 e("Intertek",
   "https://www.intertek.com/",
   "Tests food and feed for engineered content alongside SGS and Eurofins. Three "
   "companies between them run most of the world's commercial GMO testing, so a "
   "labelling threshold set by a parliament is applied in practice by three private "
   "laboratory networks.",
   ["rules:standards", "seed:distribution"]),
 e("Soil Association",
   "https://www.soilassociation.org/",
   "Certifies organic production in the United Kingdom, and organic standards "
   "exclude engineered material outright. A grower whose crop tests positive loses "
   "the certification and the price premium with it, which is a sharper consequence "
   "than any regulator imposes for the same finding.",
   ["rules:standards", "rules:associations", "seed:distribution"], base=ASSN),
]

IND45["DEU"] = [
 e("IFOAM \u2014 Organics International",
   "https://www.ifoam.bio/",
   "The global umbrella for organic standards, which exclude genetic engineering by "
   "definition in every member scheme. It is the largest coordinated market "
   "structure anywhere built around the absence of this technology, and it sets the "
   "terms on which coexistence is argued.",
   ["rules:standards", "rules:associations", "rules:influence"], base=ASSN),
 e("Demeter International",
   "https://demeter.net/",
   "Certifies biodynamic production to standards stricter than organic, including on seed: varieties bred by methods it rejects cannot be used at all, and that includes cell fusion techniques the organic rules permit. Where organic excludes engineered material from the field, this excludes it from the breeding history of the variety.",
   ["rules:standards", "seed:germplasm", "rules:associations"], base=ASSN),
]

# ================================================ TRADE AND DISTRIBUTION ======
IND45["NLD"] = [
 e("Louis Dreyfus Company",
   "https://www.ldc.com/",
   "The D in the ABCD group that moves most of the world's traded grain and "
   "oilseed. Traders decide which cargoes are segregated and which are commingled, "
   "and that decision is what makes identity preservation possible or impossible "
   "for everyone downstream.",
   ["seed:distribution", "money:markets"]),
]

IND45["ISR"] = [
 e("ADAMA",
   "https://www.adama.com/",
   "A large off-patent crop protection company, Chinese-owned through ChemChina, "
   "selling the generics that follow once a herbicide's patent expires. Generic "
   "competition is what makes a tolerance trait cheap to use, so it shapes adoption "
   "as much as the trait's own licensing does.",
   ["seed:distribution", "money:markets", "seed:licensees"]),
]

IND45["THA"] = [
 e("East-West Seed",
   "https://www.eastwestseed.com/",
   "Breeds vegetable varieties for smallholders across Asia and Africa, selling "
   "small packets rather than bulk seed. It works almost entirely outside the "
   "engineered-trait business, which makes it a useful measure of what a large seed "
   "company looks like when engineering is not part of the model.",
   ["seed:germplasm", "seed:distribution", "seed:majors"]),
]
