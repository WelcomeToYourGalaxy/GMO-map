# -*- coding: utf-8 -*-
"""Industry entries, part 35. Four subjects with nothing in them.

Found by probing every existing description for the terms, not by eye. Each of
these is a real and growing use of engineered organisms and each had zero
entries:

PHAGE THERAPY. Engineered viruses given to patients to kill bacteria that
antibiotics cannot. Already used under compassionate-use rules.

EMBRYO MODELS. Structures grown from stem cells that develop like early human
embryos without being one. They fall outside every embryo research law, because
those laws define an embryo by fertilisation.

INSECT PROTEIN AND BIOMINING. Two industrial uses of engineered organisms at
large scale - one feeding animals, one extracting metal - that sit outside the
crop and medicine arguments entirely.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND35 = {}

# ============================================================ PHAGE ===========
IND35["USA"] = [
 e("Adaptive Phage Therapeutics (BiomX)",
   "https://www.biomx.com/",
   "Supplies bacteriophages, including engineered ones, matched to a patient\u2019s "
   "specific infection when antibiotics have failed. Treatment is often given under "
   "compassionate-use rules rather than an approval, so the therapy reaches people "
   "through the exception rather than the process \u2014 which means the record of "
   "who received what is held by hospitals rather than by a regulator.",
   ["clinical:therapy", "wild:microbes", "editing:platform"]),
 e("Locus Biosciences",
   "https://www.locus-bio.com/",
   "Engineers phages carrying a CRISPR system that cuts the bacterial genome from "
   "the inside, so the bacterium is killed by its own machinery. In trials for "
   "urinary tract infection. A deliberately released engineered virus that is "
   "intended to reproduce inside a patient is a category the medicines rules were "
   "not written for.",
   ["clinical:therapy", "editing:platform", "wild:microbes"]),
]

IND35["GEO"] = [
 e("Eliava Institute",
   "https://eliava-institute.org/",
   "Has treated patients with phages continuously in Tbilisi since 1923, through "
   "the period when the rest of the world abandoned the approach for antibiotics. "
   "Its collection and its clinical records are the longest-running body of "
   "experience anywhere, and they sit outside the regulatory framework every other "
   "country now applies.",
   ["clinical:therapy", "wild:microbes", "clinical:trials"], base=BODY),
]

# ======================================================= EMBRYO MODELS ========
IND35["ISR"] = [
 e("Weizmann Institute \u2014 stem-cell embryo models",
   "https://www.weizmann.ac.il/",
   "Grew structures from stem cells in 2023 that developed the features of a human "
   "embryo at fourteen days without egg, sperm or fertilisation. Every embryo "
   "research law in the world defines an embryo by fertilisation, so these fall "
   "outside all of them \u2014 including the fourteen-day limit that has governed "
   "the field since 1979.",
   ["clinical:germline", "repro:screening"], base=BODY),
]

IND35["GBR"] = [
 e("International Society for Stem Cell Research \u2014 guidelines",
   "https://www.isscr.org/",
   "Writes the guidelines the field actually follows on embryo models and on the "
   "fourteen-day limit, because in most countries no statute covers them. A "
   "professional body setting the rule where the law does not reach is the usual "
   "arrangement in this part of the sector, and it has no enforcement of any kind.",
   ["rules:standards", "rules:associations", "clinical:germline"], base=ASSN),
]

# ===================================================== INSECT PROTEIN =========
IND35["FRA"] = [
 e("\u1ef8nsect",
   "https://www.ynsect.com/",
   "Farms mealworms at industrial scale for animal feed and pet food, with "
   "selective breeding and genomic selection applied to the insects themselves. "
   "Insect farming is regulated as agriculture rather than as biotechnology, so "
   "breeding programmes on a species nobody has domesticated before proceed with "
   "very little oversight.",
   ["livestock:livestock", "seed:germplasm", "editing:agtech"]),
]

IND35["NLD"] = [
 e("Protix",
   "https://protix.eu/",
   "Breeds black soldier fly larvae for feed at commercial scale, supplying fish "
   "and poultry producers across Europe. The EU approved insect protein in "
   "aquaculture feed in 2017 and in poultry and pig feed in 2021, which is how a "
   "novel organism enters the food chain without ever being described as one.",
   ["livestock:livestock", "livestock:aqua"]),
]

# =========================================================== BIOMINING ========
IND35["CHL"] = [
 e("BioSigma",
   "http://www.biosigma.cl/",
   "A joint venture of Codelco, the Chilean state copper company, and JX Nippon, "
   "using engineered bacteria to leach copper from ore too poor to smelt. "
   "Bioleaching puts living organisms into mine waste at industrial scale, in a "
   "setting governed by mining law rather than by biosafety law.",
   ["wild:microbes", "editing:synbio", "money:public"]),
]

IND35["USA"] += [
 e("Cemvita",
   "https://www.cemvita.com/",
   "Engineers microbes to extract metals and to convert carbon dioxide in oil "
   "wells, working with mining and petroleum companies. Organisms designed to work "
   "underground in an existing well are released into a place nobody can survey "
   "afterwards, and no framework treats that as a release.",
   ["wild:microbes", "editing:synbio"]),
]
