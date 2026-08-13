# -*- coding: utf-8 -*-
"""Industry entries, part 7."""
from ind1 import e, CO, BODY, REGI, ASSN

IND7 = {}

# ============================================================== RUSSIA ========
IND7["RUS"] = [
 e("Federal Research Center for Animal Husbandry", "https://www.vij.ru/",
   "Russia’s principal livestock genetics institute. Russia bans the cultivation of engineered crops while importing engineered feed, and its editing research continues regardless of the cultivation ban — a combination that appears in no simple account of which countries are for or against.",
   ["livestock:livestock","editing:agtech","money:public"], base=BODY)]

# ============================================================== TURKEY ========
IND7["TUR"] = [
 e("Ministry of Agriculture and Forestry \u2014 biosafety board", "https://www.tarimorman.gov.tr/",
   "Turkey prohibits the cultivation of engineered crops and permits their import for animal feed, with a biosafety board approving specific events for that purpose. The prohibition and the imports coexist because the political objection attaches to growing rather than to eating, which is a distinction most national debates end up making somewhere.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================== UKRAINE =======
IND7["UKR"] = [
 e("Ministry of Agrarian Policy and Food", "https://minagro.gov.ua/",
   "Ukraine has no functioning approval system for engineered crops and substantial evidence they are grown anyway, unregistered, on a large share of soy and maize area. A country with no register does not thereby have no engineered crops; it has no record of them, and the war has made the gap wider.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================= INDONESIA ======
IND7["IDN"] = [
 e("PT Perkebunan Nusantara / sugarcane biotechnology", "https://ptpn.co.id/",
   "Indonesia’s state plantation company, which grew engineered drought-tolerant sugarcane developed domestically — one of the few engineered crops anywhere developed by a public body for a national crop rather than by a multinational for an export commodity.",
   ["seed:traits","seed:distribution","money:public"])]

# ============================================================ VIET NAM ========
IND7["VNM"] = [
 e("Ministry of Agriculture and Environment \u2014 biosafety", "https://monre.gov.vn/",
   "Vietnam approved engineered maize for cultivation and has expanded the area since. Adoption in Southeast Asia runs through feed demand: the maize is grown for animals, and the pressure comes from livestock producers rather than from consumers or seed companies.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================= COLOMBIA =======
IND7["COL"] = [
 e("ICA \u2014 Instituto Colombiano Agropecuario", "https://www.ica.gov.co/",
   "Colombia’s agricultural regulator, approving engineered cotton and maize. Colombia is also a centre of diversity for several crops, which puts approval decisions and centre-of-origin concerns in the hands of the same body — an arrangement Mexico has fought publicly over and Colombia has not.",
   ["rules:regulators","rules:ip"], base=REGI)]

# ============================================================== SWEDEN ========
IND7["SWE"] = [
 e("SLU \u2014 Swedish University of Agricultural Sciences", "https://www.slu.se/en/",
   "A Swedish research university whose gene-editing work in crops sits under EU rules that treat edited organisms as GMOs following the 2018 Court of Justice ruling. European public-sector plant research has largely relocated its field trials or stopped doing them, and this is one of the institutions where that decision was taken.",
   ["editing:agtech","deextinct:trees","money:public"], base=BODY)]

# ============================================================== FINLAND =======
IND7["FIN"] = [
 e("Solar Foods", "https://solarfoods.com/",
   "A Finnish company producing protein from engineered microbes fed on hydrogen and carbon dioxide rather than on crops, approved for sale in Singapore. It is one of the few products here that would reduce agricultural land use rather than intensify it, and it reached market in the jurisdiction most willing to approve novel foods first.",
   ["editing:synbio","cro:cdmo"])]

# ============================================================== IRELAND =======
IND7["IRL"] = [
 e("Teagasc", "https://www.teagasc.ie/",
   "Ireland’s state agriculture and food development authority, running research and advisory services for a livestock-dominated agriculture. State advisory bodies decide what reaches farmers as recommendation rather than as sales pitch, and in countries that still have them, they are the main counterweight to the input suppliers’ own agronomists.",
   ["livestock:livestock","money:public"], base=BODY)]

# ================================================= LABORATORY ANIMALS =========
IND7["USA"] = [
 e("Cyagen", "https://www.cyagen.com/",
   "A contract company producing custom engineered mice and cell lines to order, with operations in the United States and China. The service model means a laboratory anywhere can commission an animal without holding the capability itself — the animals exist, the work is contracted, and the resulting lines often appear in no public catalogue.",
   ["animals:services","animals:models","cro:cro"]),
 e("National Primate Research Centers", "https://www.nprcresearch.org/",
   "The US network of federally funded primate research facilities, holding thousands of monkeys for biomedical research including genetic modification. Primates are covered by the Animal Welfare Act, so unlike mice they are counted, and the numbers, procedures and inspection reports are public.",
   ["animals:primates","animals:breeders","money:public"], base=BODY)]

# ================================================= CONTRACT RESEARCH ==========
IND7["CHE"] = [
 e("Bachem", "https://www.bachem.com/",
   "A Swiss manufacturer of peptides and oligonucleotides, supplying the active ingredients for genetic medicines to pharmaceutical clients. Oligonucleotide manufacturing capacity is a hard limit on how many genetic therapies can exist at once, and it is held by a small number of specialist firms.",
   ["cro:cdmo","synthesis:synth","clinical:vectors"])]

IND7["KOR"] = [
 e("Samsung Biologics", "https://samsungbiologics.com/",
   "One of the largest contract biologics manufacturers in the world, built by a Korean conglomerate in under two decades. Manufacturing capacity of this scale gives its owner a position in global medicine supply that no regulator granted and none oversees.",
   ["cro:cdmo","clinical:vectors"])]

# ================================================= ASSISTED REPRODUCTION ======
IND7["AUS"] = [
 e("Virtus Health", "https://www.virtushealth.com.au/",
   "One of Australia’s largest fertility groups, listed and then taken private by an investment firm. Private equity ownership of fertility clinics is spreading across several countries, and the return expectations of that ownership sit behind decisions about cycle pricing, add-on offerings and which patients are accepted.",
   ["repro:clinics","money:vc"])]

IND7["ISR"] = [
 e("Israeli fertility system \u2014 Ministry of Health", "https://www.gov.il/en/departments/ministry_of_health",
   "Israel funds IVF more generously than any other country, with state-covered cycles up to two children and among the highest per-capita treatment rates in the world. It is the closest thing to a natural experiment in what happens when cost stops being the constraint on assisted reproduction.",
   ["repro:clinics","rules:regulators","repro:screening"], base=REGI)]

# =========================================================== DE-EXTINCTION ====
IND7["NZL"] = [
 e("Predator Free 2050 \u2014 genetic tools debate", "https://pf2050.co.nz/",
   "New Zealand’s programme to eradicate introduced rats, possums and stoats, and the public argument about whether gene drives should be among the tools. The government funded research and a national conversation before deciding rather than after — which is rare enough in this field to be worth recording either way.",
   ["deextinct:rescue","wild:drives","rules:regulators"], base=BODY)]

# ================================================================ MONEY =======
IND7["ARE"] = [
 e("Sovereign wealth investment in agrifood technology", "https://www.mubadala.com/",
   "Gulf state funds have taken large positions in agricultural and food technology, including engineered crops and cultivated protein, driven by import dependence rather than by returns alone. State capital with a food-security motive behaves differently from venture capital with a fund clock, and it is becoming a significant share of the money in this field.",
   ["money:vc","money:public","editing:synbio"])]
