# -*- coding: utf-8 -*-
"""Industry entries, part 41. Screening at both ends of a life, and two controls.

Probing found eight empty. Seven are here. School and museum education is
dropped: it is real and it is not an actor in this industry.

Two clusters again.

THE CONTROLS. The US Select Agent Program and the dual-use research policy are
the only two mechanisms anywhere that decide, in advance, that a specific piece
of biological work may not be done or may not be published. Everything else on
this map regulates release, sale or safety after the fact.

SCREENING AT BOTH ENDS. Prenatal testing, newborn screening, egg markets and
disputes over frozen embryos. This is where genetic technology reaches ordinary
people who never sought it out, at the largest scale of anything here: nearly
every baby born in a wealthy country is screened, and increasingly so is every
pregnancy.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND41 = {}

# ====================================================== SELECT AGENTS =========
IND41["USA"] = [
 e("Federal Select Agent Program",
   "https://www.selectagents.gov/",
   "Registers every US laboratory permitted to hold the pathogens and toxins judged "
   "most dangerous, inspects them, and can bar individuals from access. It is one "
   "of very few mechanisms in the world that decides in advance that particular "
   "biological work may not be done \u2014 and its list is where the boundary is "
   "actually drawn between research and a weapon.",
   ["rules:regulators", "wild:microbes", "money:defence"], base=BODY),
 e("NIH \u2014 dual use research of concern policy",
   "https://osp.od.nih.gov/policies/biosecurity-and-biosafety-policy/",
   "The US policy requiring review of research that could be misapplied, revised in "
   "2024 to cover more pathogen work. Compliance is a condition of federal funding "
   "rather than a law, so it reaches the funded and no one else, and privately "
   "financed work of the same kind falls outside it entirely.",
   ["rules:standards", "rules:regulators", "wild:microbes"], base=BODY),
]

# ================================================ PRENATAL SCREENING ==========
IND41["USA"] += [
 e("Natera",
   "https://www.natera.com/",
   "Sells non-invasive prenatal testing, reading fetal DNA from a pregnant "
   "woman\u2019s blood. Millions of tests a year, and expansion into rare "
   "microdeletions where a positive result is more often wrong than right \u2014 a "
   "screening industry selling certainty about conditions it cannot reliably "
   "detect.",
   ["repro:screening", "synthesis:seq", "clinical:trials"]),
]

# ================================================= NEWBORN SCREENING ==========
IND41["GBR"] = [
 e("Genomics England \u2014 Generation Study",
   "https://www.genomicsengland.co.uk/initiatives/newborns",
   "Sequencing the genomes of 100,000 newborns to look for treatable conditions, "
   "with the data retained for research. The largest deliberate collection of "
   "infant genomes anywhere, gathered with parental consent for a person who cannot "
   "give it and will live with the consequences.",
   ["synthesis:seq", "repro:screening", "money:public"], base=BODY),
]

IND41["USA"] += [
 e("Newborn screening and residual dried blood spots",
   "https://newbornscreening.hrsa.gov/",
   "Nearly every baby born in the United States has blood taken for screening, and "
   "the leftover cards have been retained by state laboratories for years \u2014 "
   "used for research, and in some cases subpoenaed. Texas and Michigan were both "
   "sued over it. A universal public health programme is also the largest "
   "unconsented biobank in existence.",
   ["repro:screening", "synthesis:seq", "rules:regulators"], base=REGI),
]

# ====================================================== EGG MARKETS ===========
IND41["ESP"] = [
 e("Spanish egg donation market",
   "https://www.registronacional.com/",
   "Spain performs more donor-egg cycles than any other European country, with "
   "donation anonymous and compensated, drawing patients from countries where it is "
   "not. Where donation is anonymous the resulting person cannot trace their own "
   "genetic origin \u2014 except now through consumer DNA testing, which no law "
   "anticipated.",
   ["repro:banks", "repro:clinics", "repro:surrogacy"], base=REGI),
]

# =============================================== EMBRYO DISPOSITION ===========
IND41["USA"] += [
 e("Frozen embryo disputes and personhood rulings",
   "https://www.supremecourt.gov/",
   "Around a million embryos are in storage in the United States. Courts have had "
   "to decide what they are when a couple separates, and in 2024 the Alabama "
   "Supreme Court held that frozen embryos are children, halting IVF in the state "
   "until the legislature intervened. The legal status of an embryo outside a body "
   "is unsettled in the country with the most of them.",
   ["repro:clinics", "rules:regulators", "clinical:germline"], base=REGI),
]

# ==================================================== RETAIL POLICY ===========
