# -*- coding: utf-8 -*-
"""Industry entries, part 43. From the audited additions list.

Every name below was checked against the 612 already present. Chosen from that
list on consequence rather than on completing sections, so several sections are
represented by their strongest one or two rather than in full.

The largest single hole it closes is the Oviedo Convention: the only binding
multilateral instrument anywhere that prohibits heritable modification of the
human genome. The map held the guidelines, the professional bodies and the
national bans, and not the one treaty.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND43 = {}

# =================================================== BINDING GERMLINE LAW =====
IND43["FRA"] = [
 e("Council of Europe \u2014 Oviedo Convention, Article 13",
   "https://www.coe.int/en/web/bioethics/oviedo-convention",
   "The only binding multilateral instrument that prohibits modifying the human "
   "genome in a way that can be inherited. Ratified by 29 European states, and "
   "conspicuously not by the United Kingdom, Germany or Russia. Everywhere else the "
   "germline is governed by national law, professional guidelines or nothing, so "
   "this single article carries more weight than any other text on the subject.",
   ["clinical:germline", "rules:regulators", "rules:standards"], base=BODY),
 e("INRAE",
   "https://www.inrae.fr/en",
   "The largest agricultural research organisation in Europe, formed in 2020, "
   "running plant, animal and microbial genetics across France. Public breeding at "
   "this scale is the counterweight to company-held traits, and it is the body that "
   "would carry an EU deregulation into practice if the proposed regulation passes.",
   ["seed:germplasm", "seed:traits", "money:public"], base=BODY),
]

# ============================================ PRE-CRISPR EDITING PLATFORMS ====
IND43["USA"] = [
 e("Sangamo Therapeutics",
   "https://www.sangamo.com/",
   "The first genome-editing company, working with zinc-finger nucleases from the "
   "1990s and in clinical trials years before CRISPR existed. Its history is the "
   "standing answer to the claim that genome editing is new and therefore "
   "unregulated by anything written earlier: the tools changed, the practice did "
   "not begin with them.",
   ["editing:platform", "clinical:therapy", "editing:patents"]),
 e("Precision BioSciences",
   "https://precisionbiosciences.com/",
   "Uses ARCUS meganucleases, a third editing chemistry distinct from both zinc "
   "fingers and CRISPR, in gene therapy and in engineered crops. Its existence "
   "matters to the carve-out argument: rules written around one molecular tool do "
   "not obviously cover organisms made with another.",
   ["editing:platform", "clinical:therapy", "editing:agtech"]),
]

IND43["FRA"] += [
 e("Cellectis",
   "https://www.cellectis.com/en/",
   "Pioneered TALEN editing and treated the first patient ever given an allogeneic "
   "CAR-T \u2014 cells taken from a donor rather than the patient, edited to avoid "
   "rejection, given as an off-the-shelf product. An engineered cell line "
   "manufactured in advance for whoever needs it is a different regulatory object "
   "from a therapy made from one person's own cells.",
   ["editing:platform", "clinical:therapy"]),
]

IND43["IRL"] = [
 e("ERS Genomics",
   "https://ersgenomics.com/",
   "Holds and licenses Emmanuelle Charpentier's share of the foundational CRISPR "
   "patents, and has signed hundreds of licences with companies and institutions. A "
   "cleaner illustration of enclosure than the Broad and Berkeley dispute, because "
   "nothing about it is contested: one licensing vehicle stands between the basic "
   "technique and most of the people using it.",
   ["editing:patents", "rules:ip", "editing:platform"]),
]

# ================================================= POPULATION GENOMICS ========
IND43["USA"] += [
 e("All of Us Research Program",
   "https://allofus.nih.gov/",
   "An NIH programme enrolling a million Americans, deliberately weighted toward "
   "groups underrepresented in genomic research. It is the largest attempt anywhere "
   "to correct the fact that reference genomes are overwhelmingly European, which "
   "is a scientific problem and a fairness problem at once: a risk score built on "
   "the wrong population is wrong for the person reading it.",
   ["synthesis:seq", "money:public", "clinical:trials"], base=BODY),
]

IND43["ISL"] = [
 e("deCODE genetics (Amgen)",
   "https://www.decode.com/",
   "Holds genotype and health data covering a very large share of the Icelandic "
   "population, and has been owned by a US pharmaceutical company since 2012. A "
   "whole nation's genetics under one corporate owner is the arrangement every "
   "later biobank has had to define itself against.",
   ["synthesis:seq", "money:markets", "clinical:trials"]),
]

IND43["ZAF"] = [
 e("H3Africa",
   "https://h3africa.org/",
   "A continent-wide genomics network built explicitly so that African samples are "
   "studied in African institutions rather than shipped out. It exists because the "
   "previous arrangement \u2014 samples collected in Africa, sequenced and patented "
   "elsewhere \u2014 was the normal one, and its data-sharing terms are now cited "
   "as a model in benefit-sharing arguments.",
   ["synthesis:seq", "money:public", "rules:standards"], base=BODY),
]

# ================================================== CULTIVATED MEAT ===========
IND43["USA"] += [
 e("Upside Foods",
   "https://upsidefoods.com/",
   "Received the first US clearance to sell meat grown from animal cells, in 2023. "
   "Its Emeryville plant is among the largest cultivated-meat facilities built, and "
   "the gap between that capacity and actual sales is the sector's central fact: "
   "approval was the easier problem.",
   ["editing:agtech", "livestock:livestock", "editing:synbio"]),
 e("Eat Just / GOOD Meat",
   "https://www.goodmeat.co/",
   "The first company to sell cultivated meat anywhere, in Singapore in 2020, and "
   "later cleared in the United States. Singapore approved it because a city-state "
   "importing most of its food has reasons a farming country does not \u2014 which "
   "is why the first approval was never going to come from a large agricultural "
   "producer.",
   ["editing:agtech", "livestock:livestock"]),
]

IND43["NLD"] = [
 e("Mosa Meat",
   "https://mosameat.com/",
   "Grew out of the Maastricht laboratory that made the first cultivated burger in "
   "2013, and filed the first EU novel-food application for cultivated beef in "
   "2025. The EU application is the test case: approval there would be the first in "
   "a jurisdiction that regulates novel food strictly and where several member "
   "states are actively hostile.",
   ["editing:agtech", "livestock:livestock"]),
]

# ============================================== REGULATORS AND CASES ==========
IND43["ARG"] = [
 e("CONABIA \u2014 Argentine biotechnology advisory commission",
   "https://www.argentina.gob.ar/agricultura/alimentos-y-bioeconomia/conabia",
   "Wrote Resolution 173/2015, which decided that an edited organism carrying no "
   "foreign DNA is not a GMO and needs no biosafety approval. Chile, Brazil, "
   "Colombia, Paraguay and Honduras all adopted versions of it, and the drafting "
   "was done here. More countries follow this text than follow any other on the "
   "subject.",
   ["rules:regulators", "rules:standards", "editing:agtech"], base=BODY),
]

IND43["PHL"] = [
 e("Philippine Court of Appeals \u2014 writ of kalikasan",
   "https://sc.judiciary.gov.ph/",
   "Revoked the approvals for Golden Rice and Bt eggplant in 2024 on precautionary "
   "grounds, using a constitutional environmental remedy available to citizens. The "
   "only case anywhere of a court withdrawing an already-granted biosafety approval "
   "at the request of the public, in the country where Golden Rice had been "
   "approved first.",
   ["rules:regulators", "seed:traits", "rules:influence"], base=REGI),
]

# ============================================ TESTING AND DISTRIBUTION ========
IND43["LUX"] = [
 e("Eurofins Scientific",
   "https://www.eurofins.com/",
   "The largest food and feed testing network in the world, and the default "
   "commercial laboratory for GMO detection. Whether a shipment is found to contain "
   "engineered material usually depends on a test run here, which makes a private "
   "testing company the practical enforcement mechanism for labelling rules across "
   "Europe and beyond.",
   ["rules:standards", "seed:distribution", "synthesis:seq"]),
]

IND43["CAN"] = [
 e("Nutrien Ag Solutions",
   "https://www.nutrienagsolutions.com/",
   "The largest agricultural retail network in the world, selling seed, chemicals "
   "and agronomic advice directly to farmers across the Americas and Australia. "
   "This is where trait choice is actually presented to a grower, by a salesperson "
   "with an inventory, and no approval process examines that step.",
   ["seed:distribution", "seed:licensees", "money:markets"]),
]

# ==================================================== OPPOSITION ==============
IND43["NLD"] += [
 e("Greenpeace International",
   "https://www.greenpeace.org/international/",
   "The most-cited opponent of agricultural biotechnology for three decades, and "
   "the counterparty in the Golden Rice dispute, where 150 Nobel laureates signed a "
   "letter against its position in 2016. Whatever one concludes about that "
   "argument, the organisation is a principal in it and the map recorded the "
   "industry's side without it.",
   ["rules:influence", "rules:associations", "seed:traits"], base=ASSN),
]

IND43["CAN"] += [
 e("ETC Group",
   "https://www.etcgroup.org/",
   "Produces the concentration figures on seed, pesticide and livestock genetics "
   "that almost every account of this industry uses, including this map's. A small "
   "organisation supplying the numbers both sides argue with is worth naming rather "
   "than citing invisibly.",
   ["rules:influence", "money:markets", "rules:associations"], base=ASSN),
]

IND43["ZWE"] = [
 e("La V\u00eda Campesina",
   "https://viacampesina.org/en/",
   "The largest farmers' organisation in the world, representing around 200 million "
   "smallholders across 81 countries, and the origin of the term food sovereignty. "
   "Its position on seed law rather than on biosafety is what makes it a principal "
   "here: it argues about who may save and replant, which is where UPOV bites.",
   ["rules:influence", "rules:associations", "seed:germplasm"], base=ASSN),
]

# ================================================= LIVESTOCK GENETICS =========
IND43["GBR"] = [
 e("Aviagen",
   "https://www.aviagen.com/",
   "Supplies the broiler genetics behind a very large share of the chicken eaten "
   "worldwide, under EW Group ownership. Almost every commercial chicken descends "
   "from a handful of proprietary breeding lines held by two companies, which is "
   "the narrowest genetic bottleneck in any food animal and predates engineering "
   "entirely.",
   ["livestock:livestock", "animals:breeders", "seed:germplasm"]),
]
