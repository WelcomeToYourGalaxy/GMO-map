# -*- coding: utf-8 -*-
"""Industry entries, part 24.

Chosen by influence rather than by filling gaps evenly. Each of these is either
one of a very small number of companies controlling something everyone else
depends on, or the first instance of something the whole field now does.

The clearest case is poultry: two companies supply essentially every broiler
chicken raised on Earth, and neither was on this map.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND24 = {}

# ================================================= ANIMAL GENETICS ============
IND24["USA"] = [
 e("Cobb-Vantress (Tyson Foods)", "https://www.cobbgenetics.com/",
   "One of two companies supplying the breeding stock behind essentially every broiler "
   "chicken raised on Earth, owned by the largest US meat processor. Roughly 70 billion "
   "chickens are slaughtered worldwide each year and the genetics of almost all of them "
   "trace to Cobb or Aviagen. That is a tighter concentration than seed, medicine or any "
   "other facet on this map, and it attracts a fraction of the attention: a breeding "
   "decision made in Arkansas reaches nearly every commercial flock in the world within a "
   "few generations, and there is no alternative supplier to switch to.",
   ["livestock:livestock", "seed:majors"]),
 e("Marshall BioResources", "https://www.marshallbio.com/",
   "The principal supplier of purpose-bred beagles and ferrets for research worldwide. "
   "Beagles are used because they are docile and uniform, which is a sentence worth "
   "sitting with. Dogs are covered by the US Animal Welfare Act, so unlike mice the "
   "numbers and the inspection reports are public \u2014 the transparency exists here and "
   "not for the animals used in far greater numbers.",
   ["animals:breeders", "animals:services"]),
 e("Kite Pharma (Gilead)", "https://www.kitepharma.com/",
   "Sells CAR-T cell therapies, in which a patient\u2019s own immune cells are removed, "
   "genetically rewritten to attack their cancer, and returned. It is the treatment that "
   "made engineered cell therapy an industry rather than a research programme, and the "
   "manufacturing runs one patient at a time \u2014 which is why the price sits in the "
   "hundreds of thousands and why capacity, not science, decides who is treated.",
   ["clinical:therapy", "cro:cdmo"]),
 e("Spark Therapeutics (Roche)", "https://sparktx.com/",
   "Luxturna, approved in 2017, was the first gene therapy for an inherited disease "
   "cleared in the United States \u2014 a one-time injection restoring some sight in a rare "
   "form of blindness, at $850,000 for two eyes. Every pricing argument since has been "
   "conducted in the shadow of that number, and Roche bought the company shortly after "
   "the approval.",
   ["clinical:therapy", "clinical:vectors"]),
 e("OrbiMed", "https://www.orbimed.com/",
   "The largest investment firm dedicated solely to healthcare, holding positions across "
   "therapeutics, devices and diagnostics worldwide. A fund of this size and focus shapes "
   "which diseases attract company formation at all \u2014 and a condition with few patients "
   "in wealthy countries does not attract it, however many people it affects elsewhere.",
   ["money:vc", "money:markets"]),
 e("Bunge", "https://www.bunge.com/",
   "One of the four traders \u2014 with Cargill, ADM and Louis Dreyfus \u2014 that move most of the "
   "world\u2019s grain and oilseeds. These four decide what is worth growing more directly "
   "than any seed company: a variety nobody will buy does not get planted whatever its "
   "traits. Three of the four are private or family-controlled and disclose far less than "
   "any listed seed company on this map.",
   ["seed:distribution", "money:markets"]),
]

# ============================================== EDITING & SUPPLY ==============
IND24["USA"] = IND24["USA"] + [
 e("Caribou Biosciences", "https://cariboubio.com/",
   "Founded by Jennifer Doudna, and the company through which the Berkeley side of the "
   "CRISPR patent dispute licensed its intellectual property. It holds a foundational "
   "position and lost the interference proceedings, which is why the licensing estate "
   "everyone else pays into sits with the Broad instead \u2014 the science was shared, the "
   "rights were not.",
   ["editing:platform", "editing:patents", "clinical:therapy"]),
 e("Sartorius", "https://www.sartorius.com/",
   "Supplies the bioreactors, filters and single-use bags that biologics and cell therapy "
   "manufacturing runs on. Equipment is the quiet constraint on genetic medicine: a "
   "therapy cannot be made faster than the vessels it is grown in can be built, and a "
   "handful of suppliers set that pace for the entire industry.",
   ["cro:cdmo", "synthesis:reagents"]),
]

IND24["DEU"] = [
 e("Merck KGaA / MilliporeSigma", "https://www.merckgroup.com/",
   "Holds CRISPR patents granted in Europe, Canada and elsewhere while the American "
   "dispute ran, and supplies a large share of the reagents laboratories buy daily. The "
   "same technique therefore has different owners in different jurisdictions, so where an "
   "experiment happens decides who is owed for it \u2014 a fact about patent law rather than "
   "about biology.",
   ["editing:patents", "synthesis:reagents", "cro:cdmo"]),
 e("EW Group", "https://www.ew-group.de/",
   "A private German holding company that owns Aviagen \u2014 the other of the two broiler "
   "genetics companies \u2014 alongside layer, turkey and aquaculture genetics businesses. It "
   "is one of the most consequential animal-breeding groups in the world and among the "
   "least visible, because being family-owned it publishes almost nothing.",
   ["livestock:livestock", "seed:majors"]),
]

IND24["NLD"] = [
 e("uniQure", "https://www.uniquregroup.com/",
   "Produced Glybera, approved in Europe in 2012 as the first gene therapy licensed "
   "anywhere in the Western world. It was withdrawn in 2017 having been used by a handful "
   "of patients \u2014 priced at around a million dollars, for a condition too rare to sustain "
   "it. The first approval and the first commercial failure are the same product.",
   ["clinical:therapy", "clinical:vectors"]),
]

IND24["SWE"] = [
 e("Vitrolife", "https://www.vitrolife.com/",
   "Supplies much of the culture media, equipment and consumables that IVF laboratories "
   "worldwide depend on. An embryo develops in this company\u2019s media, and the 2024 "
   "recall by a competitor showed what a supplier failure destroys \u2014 something "
   "irreplaceable, in a market regulated as devices rather than as the environment an "
   "embryo grows in.",
   ["repro:clinics", "synthesis:reagents"]),
]

# ================================================ TRADE & STATE ===============
IND24["CHN"] = [
 e("COFCO International", "https://www.cofcointernational.com/",
   "China\u2019s state-owned grain trader, built deliberately to reduce dependence on the "
   "four Western traders. It buys soy and maize at a scale that moves world prices, and "
   "because the buyer is a state pursuing food security rather than a company pursuing "
   "margin, its purchasing decisions follow a different logic from the rest of this "
   "facet \u2014 and reach the same farmers.",
   ["seed:distribution", "money:public", "money:markets"]),
]

IND24["SGP"] = [
 e("Wilmar International", "https://www.wilmar-international.com/",
   "The largest palm oil processor in the world. Palm is the highest-yielding oil crop by "
   "far and the one most associated with deforestation, and engineered and edited palm is "
   "under development to raise yields further. Whether that reduces land pressure or "
   "increases the return on clearing more is the question, and it will be settled by "
   "companies at this end of the chain rather than by the breeders.",
   ["seed:distribution", "money:markets"]),
]

# ==================================================== GOVERNANCE ==============
IND24["CAN"] = [
 e("Secretariat of the Convention on Biological Diversity",
   "https://www.cbd.int/",
   "Runs the Cartagena Protocol and the Biosafety Clearing-House \u2014 the register this map "
   "draws its national decisions from. It is also where gene drives are argued over at "
   "treaty level, and where a moratorium on them has been proposed and rejected more than "
   "once. Almost every country is a party. The United States is not, and has never "
   "ratified the Convention itself.",
   ["rules:regulators", "rules:standards"], base=BODY),
]
