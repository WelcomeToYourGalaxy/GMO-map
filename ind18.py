# -*- coding: utf-8 -*-
"""Industry entries, part 18."""
from ind1 import e, CO, BODY, REGI, ASSN

IND18 = {}

# ============================================================ SEED & TRAITS ===
IND18["NLD"] = [
 e("Enza Zaden", "https://www.enzazaden.com/",
   "A Dutch vegetable breeder, family-owned, in the cluster of firms that dominate world vegetable seed. It has used editing in research while the EU treats edited plants as GMOs, which for a European breeder means the technique is available in the laboratory and not in the market — the position the proposed EU regulation would change.",
   ["seed:germplasm","seed:licensees"]),
 e("Bejo Zaden", "https://www.bejo.com/",
   "A Dutch vegetable breeder specialising in brassicas, carrots and onions, family owned and among the larger vegetable seed houses in the world. It works by conventional and marker-assisted breeding rather than transgenics, which is the norm in vegetables: the crops are too many, the markets too fragmented and the approval costs too high for engineered varieties to pay. Vegetable seed is where the concentration argument looks different from the commodity crops — a handful of European family firms rather than four multinationals.",
   ["seed:germplasm","seed:distribution"])]

IND18["USA"] = [
 e("Beck's Hybrids", "https://www.beckshybrids.com/",
   "The largest family-owned seed company in the United States, selling maize and soy against the majors. It licenses the traits it sells rather than owning them, which is the ordinary position for an independent: the seed genetics are its own, the trait inside them belongs to somebody else, and the licence terms determine what it can offer. Independents like this are the measure of how much of the market the four majors do not directly hold.",
   ["seed:licensees","seed:distribution"])]

# ================================================== EDITING & SYNTHETIC BIO ===
IND18["USA"] = IND18["USA"] + [
 e("Verve Therapeutics", "https://www.vervetx.com/",
   "Base editing aimed at permanently lowering cholesterol with a single treatment, in adults with inherited risk. A one-time edit for a condition currently managed with daily pills changes the risk calculation entirely: the edit cannot be stopped if something is wrong.",
   ["clinical:therapy","editing:platform"]),
 e("Mammoth Biosciences", "https://mammoth.bio/",
   "Develops ultra-compact CRISPR proteins, also founded by Jennifer Doudna. The constraint it works against is delivery: the adeno-associated viruses used to carry editing machinery into a body have a small fixed cargo capacity, and standard Cas9 nearly fills it. A smaller enzyme leaves room for the guide and the control sequences, which is the difference between a therapy that can be given as an injection and one that requires cells to be removed, edited and returned in hospital.",
   ["editing:platform","clinical:vectors"]),
 e("Colossal \u2014 Breaking spin-out and IP licensing", "https://colossal.com/technology/",
   "A spin-out applying the de-extinction company's enzyme engineering to plastic degradation. It is the pattern worth noting rather than the product: a venture raised on returning extinct animals generates conventional industrial biotechnology as a by-product, and the by-product is what has a market.",
   ["deextinct:ventures","editing:platform","money:vc"], trust="medium")]

# =========================================================== LAB ANIMALS ======
IND18["USA"] = IND18["USA"] + [
 e("Alpha Genesis", "https://www.alphagenesisinc.com/",
   "A US primate breeding and research facility, subject to published USDA inspection reports and, in 2016, to escapes that drew national attention. Primate supply is the tightest constraint in biomedical research: demand rose sharply during the pandemic, China stopped exporting macaques, and prices multiplied — so a small number of breeding colonies now determine what research is physically possible.",
   ["animals:primates","animals:breeders"]),
 e("Ace Animals / laboratory dog and cat supply", "https://www.aphis.usda.gov/aphis/ourfocus/animalwelfare",
   "A Class A dealer breeding dogs and cats for research, licensed and inspected by USDA APHIS. Purpose-bred beagles are the standard dog in toxicology because regulators require a non-rodent species for most safety studies, so the requirement itself creates the market. Class B dealers, who bought animals from random sources including pounds, were phased out of live-animal supply after sustained investigation; Class A breeding replaced them, which resolved the provenance question and not the underlying one.",
   ["animals:breeders","rules:regulators"], base=REGI)]

# ===================================================== ASSISTED REPRODUCTION ==
IND18["USA"] = IND18["USA"] + [
 e("Fairfax Cryobank / California Cryobank \u2014 donor limits", "https://fairfaxcryobank.com/",
   "Two of the largest US sperm banks. Family limits in the United States are voluntary, set by professional guidance rather than law, and counted by the bank from reported pregnancies — a figure that depends on recipients choosing to report. Cases of donors with dozens of confirmed offspring have emerged through consumer DNA matching rather than through any register, which is the pattern throughout this part of the industry: the technology that broke anonymity is also the only thing auditing it.",
   ["repro:banks","repro:surrogacy"], trust="medium"),
 e("Donor Sibling Registry", "https://www.donorsiblingregistry.com/",
   "A voluntary registry through which donor-conceived people and their genetic half-siblings find each other, founded in 2000 by a mother and her donor-conceived son. It has matched tens of thousands of people and repeatedly revealed sibling groups far larger than any clinic disclosed — in some cases well over a hundred. It existed for years before consumer DNA testing made the same discovery unavoidable, and it is still the only place the resulting families are counted.",
   ["repro:banks","repro:clinics"], base=BODY)]

IND18["IND"] = [
 e("Indian Council of Medical Research \u2014 ART regulation", "https://www.icmr.gov.in/",
   "Wrote the guidelines that governed Indian assisted reproduction for two decades before the ART Act and the Surrogacy Act of 2021 replaced them with law. India had been the largest commercial surrogacy destination in the world; the 2021 acts prohibited commercial surrogacy and restricted altruistic arrangements to married Indian couples, which closed an international market by statute in a single step. The clinics remained and now number in the thousands.",
   ["repro:surrogacy","repro:clinics","rules:regulators"], base=REGI)]

# ============================================================= RULES ==========
IND18["CHE"] = [
 e("UPOV \u2014 International Union for the Protection of New Varieties of Plants", "https://www.upov.int/",
   "The treaty system governing plant variety rights. Trade agreements push countries to adopt the 1991 version, which restricts saving and exchanging seed; Ghana’s implementing law carries a ten-year minimum sentence. A practice older than writing becomes an offence in countries that never had the concept.",
   ["rules:ip","rules:standards","seed:distribution"], base=BODY),
 e("Codex Alimentarius \u2014 foods derived from biotechnology", "https://www.fao.org/fao-who-codexalimentarius/",
   "The UN food standards body's guidance on assessing engineered foods, agreed in 2003 after four years of negotiation. Codex texts are not binding, but the WTO treats them as the reference for whether a country's food safety measure is justified — so a voluntary standard becomes the test by which a trade restriction stands or falls, and that is where a national labelling rule is actually decided.",
   ["rules:standards","rules:regulators"], base=BODY)]

IND18["BEL"] = [
 e("European Food Safety Authority \u2014 GMO panel opinions", "https://www.efsa.europa.eu/en/topics/topic/gmo",
   "Every EU assessment of an engineered crop, published in full with the data and the panel's reasoning. It is the most transparent regulatory record in this field anywhere — and it has repeatedly issued favourable opinions on crops that member states then refused to allow, because the assessment is scientific and the decision is political and the two are deliberately separated.",
   ["rules:regulators","rules:standards"], base=REGI)]

# ======================================================== NEW TERRITORIES =====
IND18["VNM"] = [
 e("Vietnam \u2014 GM maize cultivation and feed imports", "https://www.mard.gov.vn/",
   "Vietnam approved engineered maize for cultivation in 2014 and grows a modest area, while importing several million tonnes of engineered maize and soy each year for animal feed. That combination is the normal position across Asia and is rarely described: a country can be cautious about growing engineered crops and still depend on them entirely, because the feed arrives regardless and no labelling follows it through a pig.",
   ["rules:regulators","livestock:livestock","seed:distribution"], base=REGI)]

IND18["NGA"] = [
 e("Institute for Agricultural Research, Zaria \u2014 Bt cowpea", "https://iar.abu.edu.ng/",
   "The Nigerian institute that developed Bt cowpea, approved in 2019 and the first engineered food crop released in sub-Saharan Africa. Cowpea is grown almost entirely by smallholders for domestic consumption rather than export, and the pod borer it resists can destroy most of a crop — so this is one of very few engineered crops developed by a public institute for a staple its own country eats.",
   ["seed:traits","money:philanthropy","rules:regulators"], base=BODY)]

IND18["EGY"] = [
 e("Egypt \u2014 wheat import tenders and GM specification", "https://www.gasc.gov.eg/",
   "The largest wheat importer in the world, buying through state tenders whose specifications set terms for exporters across several continents. Egypt has at times specified GM-free consignments and at times abandoned the requirement under supply pressure, and each shift moves what traders segregate. A tender document from one buyer of this size functions as regulation for everyone selling into it.",
   ["seed:distribution","rules:regulators"], base=REGI)]
