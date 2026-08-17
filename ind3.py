# -*- coding: utf-8 -*-
"""Industry entries, part 3."""
from ind1 import e, CO, BODY, REGI, ASSN

IND3 = {}

# =========================================================== SEED & TRAITS ====
IND3["USA"] = [
 e("Benson Hill", "https://bensonhill.com/",
   "Used computational breeding and editing to design soy for protein content, raised heavily on that promise, and went bankrupt in 2025. The technology worked well enough, and the company still could not build a business between the four majors and the commodity buyers. It is the clearest recent evidence that the concentration on this map is not only about patents — the distribution and processing chain is closed too.",
   ["seed:traits","editing:agtech","money:vc"]),
 e("Pairwise", "https://www.pairwise.com/",
   "A gene-editing company backed by Bayer and Corteva together, developing consumer-facing produce — seedless blackberries, less bitter greens. The joint backing matters more than the products: the two largest competitors in world agriculture are co-funding the same editing platform, which tells you they expect to license rather than compete on the underlying technique.",
   ["editing:agtech","seed:traits"])]

IND3["NLD"] = [
 e("KeyGene", "https://www.keygene.com/",
   "A Dutch crop research company that develops breeding and editing technologies and licenses them to seed companies rather than selling seed itself. It is the layer beneath the visible market — the traits and techniques in other companies’ varieties often originate here, so the concentration measured by counting seed brands understates how few sources the underlying technology has.",
   ["editing:agtech","cro:cro","seed:germplasm"])]

IND3["FRA"] = [
 e("Groupe Roullier / seed & input distribution", "https://www.roullier.com/",
   "A large French group in fertiliser, animal nutrition and seed distribution, privately held and little discussed outside the sector. Distribution is where a farmer’s actual choice is made: whatever is bred anywhere, what reaches a field is what the local distributor stocks, and that decision is taken by companies almost nobody outside farming can name.",
   ["seed:distribution","seed:licensees"])]

# ======================================= EDITING & SYNTHETIC BIOLOGY ==========
IND3["USA"] = IND3["USA"] + [
 e("Broad Institute \u2014 CRISPR patent estate", "https://www.broadinstitute.org/",
   "Holds the CRISPR patents that prevailed in the long US interference proceedings against Berkeley, covering use in plant and animal cells — which is to say, essentially every commercial application. The public money that funded the underlying work bought the public no rights in the result. Either side would have held the same estate had it won, and both sides built on publicly funded work.",
   ["editing:patents","money:public","seed:traits"], base=BODY),
 e("Synthego", "https://www.synthego.com/",
   "Sells synthetic guide RNAs and edited cell lines by catalogue, which is what turned genome editing from a technique into a purchase order. Its position is upstream of everything: a laboratory anywhere with an institutional account can order the exact reagents for a specific edit and have them in days. There is no screening regime covering who may buy them.",
   ["editing:platform","synthesis:reagents"]),
 e("Amyris", "https://amyris.com/",
   "Engineered yeast to brew squalane, sweeteners and fragrance compounds previously extracted from plants or animals, and went bankrupt in 2023 having burned through billions. Its rise and fall follows the pattern of precision fermentation as a business: the chemistry works, the scale-up economics rarely do, and the compounds it displaced were grown by farmers who had no forum in which to raise it.",
   ["editing:synbio","cro:cdmo"])]

# ===================================== SYNTHESIS, SEQUENCING & REAGENTS =======
IND3["USA"] = IND3["USA"] + [
 e("Thermo Fisher Scientific", "https://www.thermofisher.com/",
   "The largest life-sciences supplier in the world by revenue, selling the instruments, reagents and cell-culture media that nearly every laboratory on this map depends on daily. Through Patheon it also manufactures drugs for other companies, and through PPD it runs their clinical trials, so the same firm can supply the materials, make the product and test it in people. Almost no engineered organism anywhere is made without something from this company, which makes it infrastructure rather than a participant — and infrastructure is rarely regulated as an actor. It is also the company that sold DNA collection kits used in Xinjiang, which it withdrew after sustained pressure.",
   ["synthesis:reagents", "synthesis:seq", "cro:cdmo", "cro:cro", "clinical:trials", "animals:services"]),
 e("GenScript", "https://www.genscript.com/",
   "One of the largest gene synthesis and CRISPR services companies, China-based with global operations. It is a member of the voluntary screening consortium, which is the whole point: the most consequential control on what sequences get made is a trade association code that firms join by choice, and roughly a fifth of world capacity belongs to companies that have not.",
   ["synthesis:synth","cro:cdmo","clinical:vectors"]),
 e("ATCC", "https://www.atcc.org/",
   "The American Type Culture Collection holds and distributes cell lines, microbes and viruses — the standard reference material biology is calibrated against. Its catalogue is the reason results from two laboratories can be compared at all. Access requires institutional credentials, so like Addgene it is simultaneously the infrastructure of open science and a gate that decides who may practise it.",
   ["synthesis:repos","animals:models"], base=BODY)]

# ============================================ CONTRACT RESEARCH & MANUFACTURE =
IND3["GBR"] = [
 e("Oxford Biomedica", "https://www.oxb.com/",
   "Manufactures the viral vectors that gene therapies are delivered in, for clients rather than under its own name. Delivery, not editing, is the real constraint on genetic medicine, so a handful of contract manufacturers effectively decide which therapies can be made at all — and during a shortage, which get made first is a commercial negotiation nobody appoints or oversees.",
   ["cro:cdmo","clinical:vectors"])]

IND3["CHE"] = IND3.get("CHE", []) + [
 e("Lonza", "https://www.lonza.com/",
   "The largest contract manufacturer of biologics in the world, making other companies’ medicines including at pandemic scale. Which products get made, and when, is decided in commercial negotiations between a contractor and its clients. During a shortage that is a rationing decision, taken privately, by a company no health authority appoints or oversees.",
   ["cro:cdmo","clinical:vectors","cro:cro"])]

# ================================================= LABORATORY ANIMALS =========
IND3["FRA"] = IND3["FRA"] + [
 e("Janvier Labs", "https://janvier-labs.com/",
   "A major European supplier of laboratory rodents, serving research across the continent. Europe publishes animal-use statistics through ALURES, which makes it one of the few places where the scale of this trade is officially counted — and the count exists because the EU legislated for it, not because the industry offered it.",
   ["animals:breeders","animals:models"])]

IND3["USA"] = IND3["USA"] + [
 e("Mutant Mouse Resource & Research Centers", "https://www.mmrrc.org/",
   "The US public repository network that archives and distributes engineered mouse strains, funded by the NIH. It exists so that a line created once with public money is not recreated a hundred times, which is genuine stewardship. It is also a permanent archive of engineered animals maintained indefinitely, and the animals in it are excluded by statute from the count of animals used in US research.",
   ["animals:models","money:public"], base=REGI)]

# ================================================ LIVESTOCK & AQUACULTURE =====
IND3["GBR"] = IND3["GBR"] + [
 e("Genus / PIC", "https://www.genusplc.com/",
   "The world’s largest pig genetics company, supplying breeding stock across dozens of countries, and the developer of pigs edited to resist PRRS — a disease that spreads because pigs are kept in crowded conditions. Its position means an edit approved once propagates through a very large share of global pig production within a few generations. The crowding does not change; the animal is rewritten to tolerate it.",
   ["livestock:livestock","seed:germplasm"])]

IND3["NOR"] = [
 e("AquaGen", "https://aquagen.no/en/",
   "A Norwegian salmon breeding company supplying eggs to farms worldwide. Norway runs the only systematic long-term monitoring anywhere of farmed genetics introgressing into wild rivers, and it finds it in a large majority of assessed populations — with nothing engineered involved. Intensive selection alone, plus escapes, has already changed wild fish. That is the baseline any argument about engineered salmon has to start from.",
   ["livestock:aqua","seed:germplasm"])]

# ============================================= INSECTS, MICROBES & RELEASE ====
IND3["USA"] = IND3["USA"] + [
 e("Agragene", "https://agragene.com/",
   "Develops engineered insects for agricultural pest control, releasing sterile males to suppress wild populations. It sits in the small commercial end of a field otherwise dominated by public programmes, and it is the part of the map where a private company’s product is, by design, a release into an ecosystem it does not own.",
   ["wild:insects","seed:traits"]),
 e("Indigo Ag", "https://www.indigoag.com/",
   "Sells microbial seed treatments and runs a carbon-credit programme for farmers, valued in the billions and repeatedly restructured. The pairing is unusual: the same company sells an engineered input and certifies the environmental benefit claimed from using it, and the certification market has no independent verifier of comparable scale.",
   ["wild:microbes","seed:distribution"])]

# ====================================================== HUMAN CLINICAL ========
IND3["USA"] = IND3["USA"] + [
 e("Bluebird bio", "https://www.bluebirdbio.com/",
   "Approved gene therapies for beta-thalassemia and cerebral adrenoleukodystrophy, then withdrew from Europe entirely when governments would not meet its price, and later reported a quarter with no doses sold at all in the United States. Patients who could have had a working treatment simply cannot get one. It is the clearest demonstration that a cure existing and a cure being available are different facts.",
   ["clinical:therapy","money:markets"])]

IND3["CHN"] = [
 e("National Medical Products Administration \u2014 gene therapy", "https://www.nmpa.gov.cn/",
   "China’s medicines regulator, overseeing an approval pipeline for cell and gene therapies now comparable in size to the American one. Its decisions rarely enter English-language discussion of this field, which means the usual account of who is doing what in genetic medicine is missing one of its two largest actors.",
   ["clinical:trials","rules:regulators"], base=REGI)]

# ================================================= ASSISTED REPRODUCTION ======
IND3["USA"] = IND3["USA"] + [
 e("Cooper Surgical \u2014 fertility", "https://www.coopersurgical.com/fertility/",
   "Supplies much of the equipment and culture media that IVF laboratories run on, and recalled culture media in 2024 after embryos failed to develop, with lawsuits following from families whose cycles were lost. A supplier failure in this facet destroys something irreplaceable, and the regulatory framework treats the media as a device rather than as the environment an embryo develops in.",
   ["repro:clinics","repro:banks","synthesis:reagents"]),
 e("California Cryobank / Generate Life Sciences", "https://www.cryobank.com/",
   "One of the largest sperm banks in the world, with published family limits that cap how many families may use one donor. The limits are voluntary, self-enforced, count families rather than children, and nothing counts across banks or borders — which is why donor-conceived people keep finding sibling groups far larger than any published cap implies.",
   ["repro:banks","repro:surrogacy"])]

# ============================================================ MONEY ===========
IND3["USA"] = IND3["USA"] + [
 e("ARCH Venture Partners", "https://www.archventure.com/",
   "One of the most influential early-stage investors in biotechnology, founding and funding companies across this map from Illumina onward. Venture money sets the clock: a fund must return capital within a fixed period, which rewards moving fast and getting big long before any regulator sees a product. That deadline shapes what gets built more than any scientific judgement does.",
   ["money:vc","editing:platform"]),
 e("Wellcome Trust", "https://wellcome.org/",
   "One of the largest charitable research funders in the world, with an endowment in the tens of billions, funding a substantial share of UK and global genomics. It is research money that does not need an exit, does not need a product, and can fund a twenty-year question. Very little of the work on this map is funded that way.",
   ["money:philanthropy","clinical:trials"], base=BODY)]
