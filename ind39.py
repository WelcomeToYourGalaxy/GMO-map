# -*- coding: utf-8 -*-
"""Industry entries, part 39. The design layer, and the people underneath it.

Probing turned up two clusters with nothing in them, at opposite ends.

THE DESIGN LAYER. AI protein design, cloud laboratories, public biofoundries and
DNA data storage. These change who can make an organism and how fast. A protein
designed by a model and built by a robot in a rented facility involves nobody
who has handled a pipette, and the biosecurity arrangements on this map assume
somebody has.

THE PEOPLE UNDERNEATH. Farmworker chemical exposure, crop insurance, and
university technology transfer. The first is who bears the cost of the spraying
that herbicide-tolerant crops were designed around. The second decides which
varieties a farmer can afford to plant. The third is where most of this
technology legally begins, since almost every platform here started in a
publicly funded laboratory and left it through a licensing office.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND39 = {}

# ===================================================== AI PROTEIN DESIGN ======
IND39["USA"] = [
 e("Institute for Protein Design",
   "https://www.ipd.uw.edu/",
   "Designs proteins that do not exist in nature using deep learning, including "
   "binders, enzymes and vaccine scaffolds, and has spun out a series of companies. "
   "Its director co-authored the 2024 call for voluntary commitments on AI protein "
   "design, which is the field asking for rules on itself in the absence of any.",
   ["editing:platform", "editing:synbio", "clinical:therapy"], base=BODY),
 e("Generate Biomedicines",
   "https://generatebiomedicines.com/",
   "Uses generative models to design therapeutic proteins from scratch rather than "
   "screening existing ones. When a molecule is designed rather than found, the "
   "regulatory question of what it is derived from has no answer, because it is not "
   "derived from anything.",
   ["editing:platform", "clinical:therapy"]),
]

IND39["GBR"] = [
 e("Google DeepMind \u2014 AlphaFold",
   "https://deepmind.google/science/alphafold/",
   "Predicted the structures of essentially all known proteins and released them "
   "publicly. It removed the single largest practical barrier to designing "
   "biological molecules, for everyone at once, and there was no mechanism by which "
   "that release could have been conditioned on anything.",
   ["editing:platform", "synthesis:seq"], base=BODY),
]

# ======================================================= CLOUD LABORATORIES ===
IND39["USA"] += [
 e("Emerald Cloud Lab",
   "https://www.emeraldcloudlab.com/",
   "Runs biological experiments by remote instruction: a customer writes a "
   "protocol, robots execute it, and nobody involved needs a laboratory or the "
   "skill to use one. Institutional biosafety oversight attaches to a person at a "
   "bench, and there is no person at the bench.",
   ["cro:preclinical", "editing:platform", "cro:cro"]),
]

# ======================================================= DNA DATA STORAGE =====
IND39["USA"] += [
 e("Twist Bioscience \u2014 DNA data storage",
   "https://www.twistbioscience.com/products/storage",
   "Writes digital data into synthesised DNA for archival storage, in a partnership "
   "including Microsoft and Illumina. Synthesis capacity built for data storage is "
   "the same capacity that makes genes, so a market with no biological purpose "
   "expands the infrastructure that biosecurity screening exists to watch.",
   ["synthesis:synth", "synthesis:repos"]),
]

# ======================================================= PUBLIC FOUNDRIES =====
IND39["GBR"] += [
 e("Global Biofoundry Alliance",
   "https://biofoundries.org/",
   "Links around thirty public biofoundries across four continents, most of them "
   "state-funded, sharing protocols and capacity. Public foundries put organism "
   "engineering inside universities and national laboratories rather than inside "
   "companies, which changes who is accountable for what comes out.",
   ["editing:synbio", "money:public", "rules:associations"], base=ASSN),
]

# ================================================ FARMWORKER EXPOSURE =========
IND39["USA"] += [
 e("Farmworker Justice",
   "https://www.farmworkerjustice.org/",
   "Represents US farmworkers on pesticide exposure, including the herbicides that "
   "tolerant engineered crops are grown to be sprayed with. The people applying "
   "those chemicals are the group with the highest exposure and the least standing "
   "in any approval process, and no biosafety assessment covers them.",
   ["rules:influence", "rules:associations"], base=ASSN),
]

IND39["CHE"] = [
 e("Pesticide Action Network International",
   "https://pan-international.org/",
   "Tracks pesticide poisoning and campaigns on highly hazardous pesticides "
   "worldwide, with the largest published estimates of unintentional poisonings. "
   "Herbicide-tolerant crops and herbicide volume are the same subject, and this is "
   "the organisation that counts the human cost of the second.",
   ["rules:influence", "rules:associations"], base=ASSN),
]

# ======================================================= CROP INSURANCE =======
IND39["USA"] += [
 e("USDA Risk Management Agency \u2014 federal crop insurance",
   "https://www.rma.usda.gov/",
   "Underwrites most US crop insurance, and its rules on which practices and "
   "varieties are covered shape what a farmer can afford to plant. Insurance "
   "coverage is a stronger determinant of what actually goes in the ground than any "
   "approval, and it is set by an agency nobody thinks of as a biotechnology "
   "regulator.",
   ["money:public", "rules:regulators", "seed:distribution"], base=BODY),
]

# ================================================= UNIVERSITY TECH TRANSFER ===
IND39["USA"] += [
 e("Wisconsin Alumni Research Foundation",
   "https://www.warf.org/",
   "The oldest university technology transfer office in the United States, holder "
   "of the foundational human embryonic stem cell patents, which it licensed on "
   "terms that shaped who could work on them for a decade. Almost every platform on "
   "this map began in a publicly funded laboratory and left it through an office "
   "like this one.",
   ["rules:ip", "editing:patents", "money:public"], base=BODY),
 e("AUTM",
   "https://autm.net/",
   "The association of university technology transfer offices, which sets the norms "
   "for how publicly funded research is licensed to companies. The Bayh-Dole Act of "
   "1980 let universities patent federally funded inventions, and this is the body "
   "that turned that into standard practice.",
   ["rules:ip", "rules:associations", "money:public"], base=ASSN),
]

