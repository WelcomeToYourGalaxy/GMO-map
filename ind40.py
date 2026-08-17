# -*- coding: utf-8 -*-
"""Industry entries, part 40. What happens to people, and two adjacent fields.

Probing found ten subjects empty. Five are worth entries and are here; the rest
- grain elevators, commodity certification schemes, weather services, soil carbon
markets, irrigation - are real industries that touch engineered crops without
being about them, and adding them would make this a map of agriculture rather
than of genetic engineering.

The five kept all concern what happens to a person: who gets an organ, who is
treated by a clinic operating outside approval, who finds out how they were
conceived, and two fields where engineering is being applied to the brain and to
controlled substances.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND40 = {}

# ==================================================== ORGAN PROCUREMENT =======
IND40["USA"] = [
 e("United Network for Organ Sharing",
   "https://unos.org/",
   "Runs the US transplant waiting list, on which around a hundred thousand people "
   "sit and several thousand die each year. That queue is the argument for "
   "engineered pig organs, and it is also what will decide who receives the first "
   "of them \u2014 an allocation system built for human donors now has to rank "
   "patients for an organ from an animal.",
   ["clinical:therapy", "rules:regulators", "livestock:livestock"], base=BODY),
]

# =================================================== UNPROVEN CELL CLINICS ====
IND40["USA"] += [
 e("US Stem Cell Inc \u2014 FDA injunction",
   "https://www.fda.gov/news-events/press-announcements/",
   "Injected patients with cells derived from their own fat, including into eyes; "
   "three women were blinded. A federal court granted the FDA a permanent "
   "injunction in 2019. Hundreds of clinics were operating the same way, selling "
   "cell treatments as a service rather than a drug, and enforcement has been "
   "case-by-case ever since.",
   ["clinical:therapy", "rules:regulators"], base=REGI),
]

IND40["MEX"] = [
 e("Cross-border stem cell clinics",
   "https://www.isscr.org/patient-resources",
   "Clinics in Mexico, Panama, the Caribbean and parts of Asia sell unapproved cell "
   "treatments to patients who travel for them, often after exhausting options at "
   "home. Regulatory arbitrage in medicine works the same way as in agriculture: "
   "the jurisdiction is chosen, not the treatment.",
   ["clinical:therapy", "clinical:trials"], base=CO),
]

# ================================================ DONOR-CONCEIVED PEOPLE ======
IND40["USA"] += [
 e("US Donor Conceived Council",
   "https://www.usdcc.org/",
   "Advocates for people conceived from donated sperm or eggs, including on access "
   "to medical and identity information that clinics promised would stay sealed. "
   "Consumer DNA testing broke that promise permanently, and the people affected "
   "were not party to the arrangement that made it.",
   ["repro:banks", "repro:clinics", "rules:influence"], base=ASSN),
 e("Fertility fraud prosecutions",
   "https://www.congress.gov/",
   "Dozens of doctors have been found to have used their own sperm on patients "
   "without consent, discovered decades later through consumer DNA matching. Most "
   "faced no applicable criminal law until states began writing fertility fraud "
   "statutes from 2019. A crime that could not be detected was also a crime that "
   "had not been legislated.",
   ["repro:clinics", "rules:regulators"], base=REGI),
]

# ============================================================ NEUROTECH =======
IND40["USA"] += [
 e("Neuralink",
   "https://neuralink.com/",
   "Implants electrode arrays in the human brain, with the first patient in 2024. "
   "Adjacent to this map rather than inside it, until the point where the field "
   "uses engineered viruses to deliver light-sensitive proteins into neurons "
   "\u2014 which is gene therapy performed on the brain, and is where the two "
   "subjects meet.",
   ["clinical:therapy", "clinical:vectors"]),
 e("GenSight Biologics \u2014 optogenetic vision restoration",
   "https://www.gensight-biologics.com/",
   "Uses an engineered virus to put a light-sensitive algal protein into retinal "
   "cells, restoring partial vision in a blind patient in 2021. An organism\u2019s "
   "gene, delivered by another organism, changing what a human nervous system can "
   "detect \u2014 the clearest existing case of engineering a new sense rather than "
   "repairing an old one.",
   ["clinical:therapy", "clinical:vectors", "editing:platform"]),
]

# ============================================= ENGINEERED PSYCHOACTIVES =======
IND40["CAN"] = [
 e("Octarine Bio",
   "https://octarinebio.com/",
   "Engineers yeast to produce psilocybin and related compounds by fermentation "
   "rather than extraction from mushrooms. A controlled substance made by a "
   "modified organism sits under drug law and biosafety law at once, and neither "
   "was written with the other in mind.",
   ["editing:synbio", "wild:microbes", "clinical:therapy"]),
]

IND40["USA"] += [
 e("Cronos Group \u2014 fermented cannabinoids",
   "https://thecronosgroup.com/",
   "Produces rare cannabinoids using engineered yeast under a partnership with "
   "Ginkgo, instead of growing and extracting them. Where a plant-derived "
   "controlled substance can be brewed instead, the agricultural licensing that "
   "governs the plant stops applying.",
   ["editing:synbio", "wild:microbes"]),
]
