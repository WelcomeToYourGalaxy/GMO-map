# -*- coding: utf-8 -*-
"""Industry entries, part 44. The layer everything buys from, and three edges.

From the audited additions list, in the order argued there.

TOOLS AND REAGENTS. The tier every other facet purchases from, and the thinnest
on this map relative to its weight. A company that supplies the enzyme, the kit
or the cell line is upstream of every approval anyone argues about.

ENZYMATIC SYNTHESIS. Where biosecurity policy actually attaches. Screening
applies to companies that make DNA to order; a benchtop printer in somebody's
laboratory is a different problem, and it is the direction the field is moving.

IN VITRO GAMETOGENESIS AND GERMLINE VENTURES. Eggs made from stem cells would
remove the limiting resource in human reproduction, and there are now companies
stating an intention to edit heritably. Both were absent.

ANIMAL TRADE STANDARDS. WOAH sets the rules by which a genetically altered
animal crosses a border, which is the practical constraint on where edited
livestock can be sold.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND44 = {}

# ============================================= TOOLS, REAGENTS, KITS ==========
IND44["USA"] = [
 e("Agilent Technologies",
   "https://www.agilent.com/",
   "One of the largest manufacturers of synthetic oligonucleotides in the world, "
   "alongside arrays and the mass spectrometry instruments used to characterise "
   "what an engineered organism actually produces. Oligo supply at this scale means "
   "the company is a screening chokepoint whether or not it is treated as one.",
   ["synthesis:synth", "synthesis:reagents", "synthesis:seq"]),
 e("Revvity \u2014 Horizon Discovery",
   "https://www.revvity.com/",
   "Supplies edited cell lines and CRISPR screening libraries to laboratories that "
   "do not make their own. Buying an engineered human cell line off a catalogue is "
   "ordinary practice and involves no biosafety filing by the purchaser, which is "
   "where a great deal of editing work actually begins.",
   ["editing:platform", "synthesis:reagents", "animals:models"]),
 e("Promega",
   "https://www.promega.com/",
   "Makes the enzymes and assay systems that molecular biology runs on, and the forensic DNA kits used by police laboratories. The same catalogue serves a university bench and a criminal investigation, and the company is privately held with a founder-set structure that has kept it out of the consolidation that took most of its peers.",
   ["synthesis:reagents", "synthesis:seq"]),
 e("Repligen",
   "https://www.repligen.com/",
   "Supplies the filtration and chromatography hardware that biologics and viral vectors are purified with. It is a genuine bottleneck: when this equipment is constrained, gene therapy manufacturing slows regardless of how many approvals have been granted, and the constraint is invisible in every account of the sector's progress.",
   ["synthesis:reagents", "cro:cdmo", "clinical:vectors"]),
 e("10x Genomics",
   "https://www.10xgenomics.com/",
   "Single-cell and spatial platforms that let researchers read what individual "
   "cells are doing rather than an average across a tissue. It is how the effects "
   "of an edit are now assessed, and it has been in continuous patent litigation "
   "with its competitors over who may sell that capability.",
   ["synthesis:seq", "synthesis:reagents", "rules:ip"]),
]

IND44["DEU"] = [
 e("Qiagen",
   "https://www.qiagen.com/",
   "Sample preparation and nucleic acid extraction kits, used before nearly every "
   "sequencing run, plus a forensic genomics line. Extraction is the invisible step "
   "on which every result downstream depends, and two or three companies supply "
   "almost all of it.",
   ["synthesis:reagents", "synthesis:seq"]),
]

IND44["JPN"] = [
 e("Takara Bio",
   "https://www.takarabio.com/",
   "Enzymes, cloning systems and single-cell reagents, and one of the few suppliers of this tier headquartered outside Europe and the United States. It also manufactures viral vectors for cell and gene therapy in Japan, and it descends from a sake brewer — which is less incidental than it sounds, since industrial fermentation expertise is what this whole layer was built on.",
   ["synthesis:reagents", "clinical:vectors", "cro:cdmo"]),
]

# ================================================= ENZYMATIC SYNTHESIS ========
IND44["FRA"] = [
 e("DNA Script",
   "https://www.dnascript.com/",
   "Sells a benchtop machine that prints DNA enzymatically, in a laboratory, "
   "without ordering anything. Synthesis screening works because orders pass "
   "through a manufacturer who can check them; a printer on a bench has no order to "
   "screen, and no country has written a rule for that.",
   ["synthesis:synth", "editing:platform", "wild:microbes"]),
]

IND44["USA"] += [
 e("Ansa Biotechnologies",
   "https://ansabio.com/",
   "Uses enzymatic synthesis to build unusually long DNA sequences, holding records "
   "for single-run length. Longer synthetic constructs mean whole genes and "
   "eventually whole genomes can be ordered rather than assembled, which changes "
   "what a screening system has to recognise.",
   ["synthesis:synth", "editing:synbio"]),
 e("Genome Project-write",
   "https://engineeringbiologycenter.org/",
   "An international consortium working toward synthesising whole genomes, "
   "including eventually a human one. It was announced at a closed meeting in 2016, "
   "which caused an immediate argument about whether a project of that kind should "
   "be discussed privately at all, and its ethics programme dates from that "
   "reaction.",
   ["synthesis:synth", "editing:synbio", "rules:standards"], base=BODY),
]

IND44["GBR"] = [
 e("Evonetix",
   "https://www.evonetix.com/",
   "Synthesises DNA in parallel on a silicon chip, each reaction site individually temperature-controlled. Applying semiconductor manufacturing to DNA is how synthesis cost falls by orders of magnitude rather than by increments — and cheap synthesis is simultaneously the precondition for most of the useful work in this field and for the thing biosecurity screening exists to prevent.",
   ["synthesis:synth", "editing:platform"]),
]

# ========================================= IN VITRO GAMETOGENESIS =============
IND44["USA"] += [
 e("Gameto",
   "https://www.gametogen.com/",
   "Uses stem-cell-derived support cells to mature human eggs outside the body, "
   "with the aim of removing the hormonal stimulation cycle that IVF currently "
   "requires. If eggs stop being scarce, every argument about embryo screening and "
   "selection changes scale, because the limiting resource was never the "
   "technology.",
   ["repro:clinics", "clinical:germline", "editing:platform"]),
 e("Conception Biosciences",
   "https://www.conception.bio/",
   "Working to make human eggs from stem cells. In vitro gametogenesis would allow "
   "an unlimited number of embryos to be produced and screened, which is the "
   "practical precondition for selection at scale \u2014 and it requires no editing "
   "at all, so no editing rule touches it.",
   ["repro:clinics", "clinical:germline"]),
 e("Preventive",
   "https://www.preventive.com/",
   "One of a small number of ventures openly working toward heritable human genome "
   "editing, funded privately and stating that intention. Germline editing is "
   "prohibited in most of the world and the prohibitions are national, so a company "
   "can be lawful somewhere while its work is a crime elsewhere.",
   ["clinical:germline", "repro:screening", "editing:platform"]),
]

IND44["ISR"] = [
 e("Renewal Bio",
   "https://www.renewal.bio/",
   "The commercial arm of the stem-cell embryo model work, proposing to grow "
   "embryo-like structures as a source of tissue. Because these are not made by "
   "fertilisation they fall outside every embryo research law, and the company is "
   "the first to build a business on that gap.",
   ["clinical:germline", "clinical:therapy", "repro:screening"]),
]

# ================================================ FERTILITY DRUG SUPPLY =======
IND44["CHE"] = [
 e("Ferring Pharmaceuticals",
   "https://www.ferring.com/",
   "One of the main suppliers of the gonadotropins that make IVF possible, several "
   "of them recombinant proteins made in engineered cell lines. The drugs are the "
   "least discussed part of the fertility industry and the part without which none "
   "of the rest of it runs.",
   ["repro:clinics", "clinical:therapy", "editing:synbio"]),
]

# ================================================= ANIMAL TRADE STANDARDS =====
IND44["FRA"] += [
 e("World Organisation for Animal Health (WOAH)",
   "https://www.woah.org/",
   "Sets the international animal health standards that decide whether an animal or "
   "its products may cross a border, including for genetically altered animals. "
   "Approval to sell an edited pig at home is worth little if no importing country "
   "will accept it, and this is where that is settled.",
   ["livestock:livestock", "rules:standards", "rules:regulators"], base=BODY),
]

IND44["CHE"] += [
 e("World Intellectual Property Organization",
   "https://www.wipo.int/",
   "Administers the treaties under which patents are filed internationally, "
   "including the Patent Cooperation Treaty route used for nearly every "
   "biotechnology application. It also hosts the long-running negotiation on "
   "genetic resources and traditional knowledge, where the question of whether a "
   "patent must disclose where its biological material came from has been open for "
   "over twenty years.",
   ["rules:ip", "editing:patents", "rules:standards"], base=BODY),
]
