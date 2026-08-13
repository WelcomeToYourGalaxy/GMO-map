# -*- coding: utf-8 -*-
"""Industry entries, part 18."""
from ind1 import e, CO, BODY, REGI, ASSN

IND18 = {}

# ============================================================ SEED & TRAITS ===
IND18["NLD"] = [
 e("Enza Zaden", "https://www.enzazaden.com/",
   "A Dutch vegetable breeder, family-owned, in the province that supplies a large share of the world’s vegetable seed. Because these firms are private and regional, their combined position appears in no national statistic and no merger review.",
   ["seed:germplasm","seed:licensees"]),
 e("Bejo Zaden", "https://www.bejo.com/",
   "Another Dutch vegetable breeder in the same cluster, specialising in brassicas, carrots and onions. A handful of firms in one small area breed much of what the world eats fresh.",
   ["seed:germplasm","seed:distribution"])]

IND18["USA"] = [
 e("Beck's Hybrids", "https://www.beckshybrids.com/",
   "The largest family-owned seed company in the United States, selling maize and soy against the majors. It licenses the same traits its competitors do, so independence in ownership does not mean independence in genetics.",
   ["seed:licensees","seed:distribution"]),
 e("Corteva \u2014 seed applied technologies", "https://www.corteva.com/products-and-solutions/seed-applied-technologies.html",
   "Coatings and treatments applied to seed before sale, including insecticides. Treated seed largely escapes pesticide-use reporting because nothing is sprayed, so the area treated is recorded nowhere.",
   ["seed:distribution","wild:microbes"])]

# ================================================== EDITING & SYNTHETIC BIO ===
IND18["USA"] = IND18["USA"] + [
 e("Verve Therapeutics", "https://www.vervetx.com/",
   "Base editing aimed at permanently lowering cholesterol with a single treatment, in adults with inherited risk. A one-time edit for a condition currently managed with daily pills changes the risk calculation entirely: the edit cannot be stopped if something is wrong.",
   ["clinical:therapy","editing:platform"]),
 e("Mammoth Biosciences", "https://mammoth.bio/",
   "Develops smaller CRISPR proteins that fit more easily into delivery vectors, and diagnostic tests using the same enzymes. The delivery problem, not the cutting, is what limits genetic medicine.",
   ["editing:platform","clinical:vectors"]),
 e("Colossal \u2014 Breaking spin-out and IP licensing", "https://colossal.com/technology/",
   "A spin-out applying the company’s enzyme engineering to plastic degradation. The de-extinction target raises the money and generates coverage; the spin-outs are the products with buyers.",
   ["deextinct:ventures","editing:platform","money:vc"], trust="medium")]

# =========================================================== LAB ANIMALS ======
IND18["USA"] = IND18["USA"] + [
 e("Alpha Genesis", "https://www.alphagenesisinc.com/",
   "A US primate breeding and research facility, subject to published inspection reports documenting escapes and welfare findings. Primates are covered by the Animal Welfare Act, so the record exists at all.",
   ["animals:primates","animals:breeders"]),
 e("Ace Animals / laboratory dog and cat supply", "https://www.aphis.usda.gov/aphis/ourfocus/animalwelfare",
   "Class A dealers breeding dogs and cats for research, licensed and inspected under the Animal Welfare Act. Their reports are public, specific and almost never read.",
   ["animals:breeders","rules:regulators"], base=REGI)]

# ===================================================== ASSISTED REPRODUCTION ==
IND18["USA"] = IND18["USA"] + [
 e("Fairfax Cryobank / California Cryobank \u2014 donor limits", "https://fairfaxcryobank.com/",
   "Two of the largest US sperm banks, with voluntary family limits that count families rather than children and are enforced per bank. Nothing counts across banks or borders.",
   ["repro:banks","repro:surrogacy"], trust="medium"),
 e("Donor Sibling Registry", "https://www.donorsiblingregistry.com/",
   "A voluntary registry through which donor-conceived people find genetic siblings, which has repeatedly surfaced sibling groups far larger than any bank’s stated limit. It exists because no official register does.",
   ["repro:banks","repro:clinics"], base=BODY)]

IND18["IND"] = [
 e("Indian Council of Medical Research \u2014 ART regulation", "https://www.icmr.gov.in/",
   "India regulates assisted reproduction and prohibited commercial surrogacy in 2021, after years as a major destination for it. The prohibition redirected the trade rather than ending it.",
   ["repro:surrogacy","repro:clinics","rules:regulators"], base=REGI)]

# ============================================================= RULES ==========
IND18["CHE"] = [
 e("UPOV \u2014 International Union for the Protection of New Varieties of Plants", "https://www.upov.int/",
   "The treaty system governing plant variety rights. Trade agreements push countries to adopt the 1991 version, which restricts saving and exchanging seed; Ghana’s implementing law carries a ten-year minimum sentence. A practice older than writing becomes an offence in countries that never had the concept.",
   ["rules:ip","rules:standards","seed:distribution"], base=BODY),
 e("Codex Alimentarius \u2014 foods derived from biotechnology", "https://www.fao.org/fao-who-codexalimentarius/",
   "The UN food standards body’s guidance on assessing engineered foods. Codex standards are the reference point in WTO trade disputes, so what is written here determines which national measures survive a challenge.",
   ["rules:standards","rules:regulators"], base=BODY)]

IND18["BEL"] = [
 e("European Food Safety Authority \u2014 GMO panel opinions", "https://www.efsa.europa.eu/en/topics/topic/gmo",
   "Every EU GMO assessment, published in full with the reasoning. It is the most detailed public record of regulatory assessment anywhere, and the substantive independent scientific comments in those files come from a handful of organisations.",
   ["rules:regulators","rules:standards"], base=REGI)]

# ======================================================== NEW TERRITORIES =====
IND18["VNM"] = [
 e("Vietnam \u2014 GM maize cultivation and feed imports", "https://www.mard.gov.vn/",
   "Vietnam grows engineered maize and imports much more for feed. Adoption in Southeast Asia is driven by livestock demand rather than by consumer or seed-company pressure.",
   ["rules:regulators","livestock:livestock","seed:distribution"], base=REGI)]

IND18["NGA"] = [
 e("Institute for Agricultural Research, Zaria \u2014 Bt cowpea", "https://iar.abu.edu.ng/",
   "The Nigerian institute that developed Bt cowpea, an engineered staple for African smallholders rather than an export commodity. It is one of the few cases where the crop in question is what poor farmers actually grow and eat.",
   ["seed:traits","money:philanthropy","rules:regulators"], base=BODY)]

IND18["EGY"] = [
 e("Egypt \u2014 wheat import tenders and GM specification", "https://www.gasc.gov.eg/",
   "Egypt is the largest wheat importer in the world, and its tender specifications determine what exporters can ship. A single buyer at this scale sets de facto standards for producers on other continents.",
   ["seed:distribution","rules:regulators"], base=REGI)]
