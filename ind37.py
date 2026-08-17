# -*- coding: utf-8 -*-
"""Industry entries, part 37. Five empty subjects, and the licensing layer.

The five were found by probing: biosensors, controlled-environment agriculture,
tobacco, rubber and latex, and biofertiliser. Each is a real use of engineered
organisms with no entry.

The licensing layer is the other half. Nearly every trait on this map is used
under licence from somebody who does not grow anything, and that layer is thin
here. Who owns a patent decides who may plant a seed, and none of it appears in
a release register.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND37 = {}

# ========================================================== BIOSENSORS ========
IND37["USA"] = [
 e("Aanika Biosciences",
   "https://www.aanikabio.com/",
   "Sprays engineered spores onto crops as a traceable tag, so contaminated produce "
   "can be traced back to a field during an outbreak. It is a deliberate release of "
   "an engineered organism onto food, done for the purpose of surveillance rather "
   "than agronomy, and the release rules were not written with that use in mind.",
   ["wild:microbes", "editing:synbio", "seed:distribution"]),
 e("Sandia National Laboratories \u2014 biodetection",
   "https://www.sandia.gov/",
   "Builds engineered biological sensors for detecting pathogens and chemical "
   "agents, under nuclear-weapons-laboratory management. A detector that works by "
   "using a living system is itself a modified organism, and defence laboratories "
   "are where most of that work is funded.",
   ["money:defence", "editing:synbio", "wild:microbes"], base=BODY),
]

# ========================================== CONTROLLED-ENVIRONMENT AG =========
IND37["USA"] += [
 e("Plenty",
   "https://www.plenty.ag/",
   "Grows produce indoors under lights, with breeding programmes aimed at varieties "
   "that suit an environment no field has. Indoor growing is the one setting where "
   "an engineered plant is genuinely contained \u2014 no pollen leaves the building "
   "\u2014 which is an argument the sector has not yet made loudly and probably "
   "will.",
   ["seed:germplasm", "editing:agtech"]),
]

IND37["JPN"] = [
 e("Spread Co.",
   "https://spread.co.jp/en/",
   "One of the largest vertical farms in the world, in Kyoto, producing lettuce at "
   "industrial scale under fully controlled conditions. Japan\u2019s carve-out for "
   "edited crops and its indoor-growing industry sit in the same country, which is "
   "where contained engineered produce is most likely to appear first.",
   ["seed:germplasm", "editing:agtech"]),
]

# ============================================================= TOBACCO ========
IND37["GBR"] = [
 e("British American Tobacco \u2014 Kentucky BioProcessing",
   "https://www.bat.com/",
   "Owns a plant-made pharmaceutical business that grows proteins and vaccine "
   "candidates in engineered tobacco, including a COVID-19 candidate. Tobacco is "
   "the most studied plant in molecular biology and the easiest to engineer, so the "
   "industry with the most to lose from smoking decline holds one of the most "
   "capable plant-manufacturing platforms.",
   ["editing:synbio", "clinical:therapy", "seed:traits"]),
]

IND37["USA"] += [
 e("22nd Century Group",
   "https://www.xxiicentury.com/",
   "Engineers tobacco with very low nicotine, authorised by the FDA as a modified "
   "risk tobacco product in 2021. An engineered plant approved specifically because "
   "it removes an addictive compound \u2014 the only case on this map of a "
   "modification whose purpose is to make a product less effective at what it does.",
   ["seed:traits", "editing:agtech", "rules:regulators"]),
]

# ==================================================== RUBBER AND LATEX ========
IND37["MYS"] = [
 e("Malaysian Rubber Board",
   "http://www.lgm.gov.my/",
   "Runs the breeding and biotechnology programme for natural rubber, a crop with "
   "no synthetic substitute for aircraft tyres and surgical gloves. Rubber trees "
   "take seven years to yield, so a breeding decision made now takes effect in the "
   "2030s, and almost all of the world supply comes from a narrow genetic base "
   "collected in the 1870s.",
   ["seed:germplasm", "seed:traits", "trees"], base=BODY),
]

IND37["USA"] += [
 e("Bridgestone \u2014 guayule programme, Arizona",
   "https://www.bridgestoneamericas.com/",
   "Develops guayule, a desert shrub, as a domestic rubber source, using genomic selection and editing to raise latex yield. Nearly all natural rubber comes from one tropical species descended from a narrow collection made in the 1870s, grown mostly in one region — so a second source in a different climate is a hedge against a single disease outbreak taking the supply for tyres and surgical gloves at once.",
   ["seed:traits", "editing:agtech", "seed:germplasm"]),
]

# ======================================================= BIOFERTILISER ========
IND37["IND"] = [
 e("National Centre of Organic and Natural Farming \u2014 biofertiliser standards",
   "https://naturalfarming.dac.gov.in/",
   "Sets the standards for microbial inoculants sold to Indian farmers, in a market "
   "of millions of smallholders where a bag of live bacteria is cheaper than "
   "fertiliser. Quality control on living products sold this widely is where "
   "biosafety and consumer protection turn out to be the same problem.",
   ["wild:microbes", "rules:standards", "seed:distribution"], base=BODY),
]

IND37["DEU"] = [
 e("BASF \u2014 functional crop care and inoculants",
   "https://agriculture.basf.com/",
   "Sells microbial inoculants and seed treatments alongside its chemical and seed "
   "businesses. Live organisms applied to seed are a release in every practical "
   "sense and are regulated as a crop input, which is a lighter route than the one "
   "an engineered plant takes.",
   ["wild:microbes", "seed:distribution", "seed:traits"]),
]

# ==================================================== LICENSING LAYER ========
IND37["USA"] += [
 e("MPEG LA / Avanci \u2014 CRISPR patent pool attempt",
   "https://www.avanci.com/",
   "Tried to assemble a one-stop CRISPR licence covering patents held by dozens of "
   "institutions, on the model used for video codecs. It has not taken hold, which "
   "is the finding: the editing patent estate is fragmented enough that even the "
   "patent-pooling industry could not consolidate it.",
   ["editing:patents", "rules:ip"]),
]
