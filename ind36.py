# -*- coding: utf-8 -*-
"""Industry entries, part 36. Six more subjects with nothing in them.

Found the same way as part 35: probing every existing description for the terms
rather than looking. Six came back empty.

MIRROR LIFE. Organisms built from mirror-image molecules. Nothing that eats,
infects or degrades ordinary life could touch them, which is the appeal and the
reason a large group of scientists asked in 2024 that the work stop.

BIOCONTAINMENT. The engineering that is supposed to stop a released organism
surviving outside its intended setting. It is the answer to the escape question,
and it had no entries.

ENGINEERED PROBIOTICS. Live modified bacteria swallowed as medicine.

CORAL. Engineered and assisted-evolution corals for reefs, which would be a
deliberate release into open ocean.

ANTIBODY ANIMALS. Cattle carrying human genes, bled to produce human antibodies
against disease outbreaks.

MATERIALS. Engineered organisms making silk, leather and structural materials.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND36 = {}

# ======================================================== MIRROR LIFE =========
IND36["USA"] = [
 e("Mirror Biology Dialogues Fund",
   "https://www.mirrorbiology.org/",
   "Set up after a 2024 paper in which around forty scientists, several of whom had "
   "worked toward it, called for mirror bacteria not to be built. A mirror organism "
   "would be invisible to the enzymes and immune systems of ordinary life, so "
   "nothing could digest, infect or degrade it. This is the clearest case of a "
   "field asking to be stopped before the thing exists.",
   ["rules:standards", "editing:synbio", "wild:microbes"], base=ASSN),
 e("Scripps Research \u2014 expanded genetic alphabet",
   "https://www.scripps.edu/",
   "Built bacteria carrying a synthetic base pair beyond the natural four, and got "
   "them to copy it and make proteins from it. An organism using a genetic code no "
   "other living thing shares cannot exchange genes with anything, which is both a "
   "containment strategy and a step toward life that is not related to ours.",
   ["editing:synbio", "editing:platform"], base=BODY),
]

# ===================================================== BIOCONTAINMENT =========
IND36["USA"] += [
 e("Harvard Medical School \u2014 genetically recoded organisms",
   "https://hms.harvard.edu/",
   "Recoded the E. coli genome so the bacterium depends on a synthetic amino acid "
   "that does not exist in nature and dies without it, and cannot use genes taken "
   "from other organisms. This is what biocontainment actually looks like when it "
   "is engineered rather than assumed \u2014 and almost nothing released into a "
   "field carries anything of the kind.",
   ["editing:synbio", "wild:microbes", "rules:standards"], base=BODY),
 e("Synlogic",
   "https://www.synlogictx.com/",
   "Engineered bacteria taken as medicine, designed to break down compounds the "
   "patient cannot metabolise and built to die outside the gut. It wound down its "
   "lead programme in 2024 after trial results, which is worth recording: a living "
   "engineered medicine that reached patients and then did not work is part of the "
   "history of this field.",
   ["clinical:therapy", "editing:synbio", "wild:microbes"]),
]

# =============================================================== CORAL ========
IND36["AUS"] = [
 e("Australian Institute of Marine Science \u2014 coral assisted evolution",
   "https://www.aims.gov.au/",
   "Breeds and conditions corals and their symbiotic algae for heat tolerance, and "
   "works on engineered symbionts. Anything put on a reef is released into open "
   "water that connects to every other reef, so there is no containment available "
   "even in principle \u2014 and the alternative being weighed against it is the "
   "reef dying.",
   ["wild:microbes", "deextinct:rescue", "seed:germplasm"], base=BODY),
]

# ==================================================== ANTIBODY ANIMALS ========
IND36["USA"] += [
 e("SAB Biotherapeutics",
   "https://www.sab.bio/",
   "Keeps cattle carrying human chromosome fragments so they produce human "
   "antibodies, then bleeds them to make treatments against influenza, MERS and "
   "COVID-19. A herd of transchromosomic cows is a manufacturing plant that eats "
   "grass, and it is regulated as a drug facility rather than as livestock.",
   ["livestock:livestock", "clinical:therapy", "cro:cdmo"]),
]

# ======================================================== MATERIALS ==========
IND36["JPN"] = [
 e("Spiber",
   "https://www.spiber.inc/en/",
   "Ferments engineered microbes to make protein fibres based on spider silk, used "
   "in clothing sold by The North Face and others. Structural materials grown in a "
   "tank rather than drilled or farmed, and sold to consumers with no label "
   "describing how they were made.",
   ["editing:synbio", "wild:microbes"]),
]

IND36["USA"] += [
 e("Modern Meadow",
   "https://www.modernmeadow.com/",
   "Produces collagen by fermentation with engineered yeast for use in leather "
   "alternatives. Collagen is an animal protein made without an animal, which puts "
   "it outside both the agricultural rules and the medicines rules that would "
   "otherwise cover a protein of that kind.",
   ["editing:synbio", "wild:microbes"]),
]

# ============================================== BIODEFENCE PROCUREMENT ========
