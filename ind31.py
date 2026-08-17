# -*- coding: utf-8 -*-
"""Industry entries, part 31. The biggest, and the three facets that were absent.

Chosen on influence, not on geography and not to fill a quota. Two kinds of gap
were found by counting rather than by looking:

FACETS ENTIRELY MISSING. Three, checked by searching every existing description:
xenotransplantation, human enhancement, and gain-of-function research. Each is
small in company count and none is small in consequence. A map of this industry
without the organisations engineering pig organs for human bodies, or the ones
enhancing human performance, or the laboratories that make pathogens more
transmissible on purpose, is missing the parts most people would say they came
to see.

LARGEST PLAYERS ABSENT. The contract research sector had two entries for a
business that runs most of the studies regulators read. The enzyme and
fermentation industry had almost nothing, though it is where most industrial
engineered organisms actually work - in vats, making things, at a scale no field
trial approaches.

Nothing here is included for balance. Each is here because leaving it out made
the map wrong about what this industry is and who runs it.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND31 = {}

# =============================================== XENOTRANSPLANTATION ==========
# Absent entirely. Engineered pig organs have now been put into living people.
IND31["USA"] = [
 e("United Therapeutics \u2014 Revivicor",
   "https://www.unither.com/",
   "Breeds pigs carrying ten genetic edits so their organs are less violently "
   "rejected by human bodies, and supplied the heart used in the first pig-to-human "
   "transplant in 2022 and the kidneys used since. The animals are raised in "
   "designated pathogen-free facilities that are closer to a semiconductor plant "
   "than a farm. This is the point where engineered livestock and human medicine "
   "stop being separate subjects.",
   ["livestock:livestock", "clinical:therapy", "animals:breeders"]),
 e("eGenesis",
   "https://egenesis.com/",
   "Uses editing to remove porcine retroviruses from the pig genome as well as to "
   "reduce rejection \u2014 the retrovirus problem being the one that stalled "
   "xenotransplantation for decades, because a virus crossing with the organ would "
   "arrive inside a patient whose immune system had been deliberately suppressed.",
   ["livestock:livestock", "clinical:therapy", "editing:platform"]),
 e("Makana Therapeutics (Recombinetics)",
   "https://recombinetics.com/",
   "Engineers pigs for organ and islet-cell transplantation, from a company whose "
   "hornless-cattle work produced the case that changed US policy: FDA found "
   "bacterial DNA in the edited cattle that the developers had not detected, which "
   "became the standard argument for why edited animals should stay inside "
   "regulation.",
   ["livestock:livestock", "livestock:cloning", "clinical:therapy"]),
]

# =============================================== HUMAN ENHANCEMENT ============
# Absent entirely. Small in revenue, and the subject that most of the public
# argument about this technology is actually about.
IND31["USA"] += [
 e("Minicircle",
   "https://minicircle.io/",
   "Sells a follistatin gene therapy intended to increase muscle mass, offered in "
   "Hondura\u0301s at Pr\u00f3spera, a special economic zone chosen because it "
   "regulates medicine on its own terms. Not approved anywhere with a conventional "
   "regulator. It is the clearest existing case of enhancement rather than "
   "treatment, sold to people who are not ill, in a jurisdiction selected for "
   "permitting it.",
   ["clinical:therapy", "clinical:germline"]),
 e("DARPA Biological Technologies Office",
   "https://www.darpa.mil/about-us/offices/bto",
   "Funds work on protecting and extending what a human body can do under stress "
   "\u2014 including rapid antibody production, temporary immunity, and control of "
   "the body\u2019s own genetic machinery. Its stated purpose is defensive and its "
   "output is dual-use by construction: a method for making a soldier resistant to "
   "something is a method for changing a person.",
   ["money:defence", "clinical:therapy", "editing:platform"], base=BODY),
]

IND31["CHN"] = [
 e("Southern University of Science and Technology \u2014 He Jiankui affair",
   "https://www.sustech.edu.cn/en/",
   "Where He Jiankui was employed when he edited the embryos that became the first "
   "gene-edited babies, announced in 2018. He was jailed, the university disowned "
   "the work, and China wrote germline editing into its criminal law. It is on this "
   "map because it is the only place where a human germline edit is known to have "
   "been carried to birth, and because the response to it set the rules everywhere "
   "else.",
   ["clinical:germline", "repro:screening"], base=BODY),
]

# =============================================== GAIN OF FUNCTION =============
IND31["NLD"] = [
 e("Erasmus MC \u2014 Fouchier laboratory",
   "https://www.erasmusmc.nl/en/",
   "Made H5N1 avian influenza transmissible between ferrets by air in 2011, work "
   "that triggered the first global argument about whether some results should be "
   "published at all. The US paused funding for this class of research for three "
   "years afterwards. Nothing else on this map is a case of an organism being made "
   "more dangerous on purpose and the reasoning being that you cannot defend "
   "against what you have not built.",
   ["wild:microbes", "rules:standards"], base=BODY),
]

IND31["GBR"] = [
 e("Global BioLabs",
   "https://www.globalbiolabs.org/",
   "Maps the world's BSL4 and BSL3+ laboratories and scores national biorisk governance, from King's College London and the Schar School. There is no international register of high-containment laboratories and no obligation to declare one, so a research project is the only global account of where the most dangerous work is done: 69 BSL4 labs across 27 countries, 51 of them operational and 18 planned or under construction, plus 57 BSL3+ labs. Its scorecards find an asymmetry worth stating plainly — of those 27 countries, 21 score high on biosafety governance, 12 on biosecurity, and exactly one on oversight of dual-use research. States are competent at preventing accidents, weaker at preventing theft, and almost entirely without rules on whether dangerous research should be done at all.",
   ["rules:standards", "wild:microbes"], base=BODY),
]

# =============================================== CONTRACT RESEARCH ============
# Two entries for the sector that runs most of the studies a regulator reads.
# =============================================== FERMENTATION & ENZYMES =======
# Where most industrial engineered organisms actually work.
IND31["USA"] += [
 e("International Flavors & Fragrances \u2014 Health & Biosciences",
   "https://www.iff.com/",
   "Engineered microbes producing enzymes, cultures and food ingredients at "
   "industrial scale, after absorbing DuPont\u2019s nutrition and biosciences "
   "division in 2021. Between this company and Novonesis, most of the world\u2019s "
   "industrial fermentation capacity sits in two sets of hands.",
   ["editing:synbio", "wild:microbes"]),
]
