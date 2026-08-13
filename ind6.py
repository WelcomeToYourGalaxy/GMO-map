# -*- coding: utf-8 -*-
"""Industry entries, part 6. New territories, and the facets still thinnest:
contract research, laboratory animals, de-extinction."""
from ind1 import e, CO, BODY, REGI, ASSN

IND6 = {}

# ============================================================== MEXICO ========
IND6["MEX"] = [
 e("CIBIOGEM", "https://www.conahcyt.mx/cibiogem/",
   "Mexico’s biosafety commission, which sits over the most consequential dispute in this field: Mexico is where maize was domesticated, and engineered maize found in Oaxacan landraces is not contamination of a crop but of the reservoir every commercial maize variety on Earth was ultimately bred from. Mexico’s decree restricting GM maize for human consumption was challenged by the United States under the USMCA trade agreement, which is where a country’s biosafety decision gets tested against its trade obligations.",
   ["rules:regulators","seed:germplasm"], base=REGI),
 e("Grupo Bimbo", "https://www.grupobimbo.com/en",
   "The largest bakery company in the world, buying wheat and maize at a scale that makes its procurement policy a de facto regulation. A miller or baker of this size deciding not to accept an engineered grain closes the market for it more effectively than any regulator — which is why engineered wheat went unapproved for twenty-five years while the science sat ready.",
   ["seed:distribution","rules:influence"])]

# ========================================================= SOUTH AFRICA =======
IND6["ZAF"] = [
 e("Executive Council for GMOs \u2014 Department of Agriculture", "https://www.dalrrd.gov.za/",
   "South Africa’s GMO decision body, in the country that grows more engineered maize than anywhere else in Africa and where white maize — the staple people eat directly, not livestock feed — is largely engineered. Most engineered maize worldwide goes to animals. Here it is dinner, which makes South Africa the place where the food-safety argument is least abstract.",
   ["rules:regulators","seed:distribution"], base=REGI),
 e("Pannar Seed (Corteva)", "https://www.pannar.com/",
   "A South African seed company acquired by what is now Corteva after a competition fight that went to the country’s appeal court, which initially blocked the deal on concentration grounds. It is one of the few times a national competition authority tried to stop consolidation in seed and had to be overruled to let it through — the reasoning on both sides is public.",
   ["seed:licensees","seed:distribution","seed:majors"])]

# ============================================================= NIGERIA ========
IND6["NGA"] = [
 e("National Biosafety Management Agency", "https://nbma.gov.ng/",
   "Nigeria’s biosafety regulator, which has approved Bt cowpea — an engineered staple developed for African smallholders rather than for export commodity production. Nigeria is the largest market in West Africa, so approvals here shape what neighbouring regulators do next, and this is one of the few cases where the crop in question is what poor farmers actually grow and eat.",
   ["rules:regulators","seed:traits"], base=REGI)]

# ============================================================== KENYA =========
IND6["KEN"] = [
 e("Kenya National Biosafety Authority", "https://www.biosafetykenya.go.ke/",
   "Kenya lifted its ten-year ban on GM crops in 2022, and the decision was immediately challenged in court. The episode is the clearest example of the pattern this map keeps finding in Africa: approval arrives through a mix of donor funding, trade pressure and domestic politics, and the public argument happens after the decision rather than before it.",
   ["rules:regulators"], base=REGI)]

# ============================================================== ITALY =========
IND6["ITA"] = [
 e("Illumina Italy / Ferrara sequencing hub", "https://www.illumina.com/company/about-us/global-locations.html",
   "A large European sequencing operation, and part of how genomic capacity spread beyond a handful of national centres. Where sequencing can be done cheaply determines who can check things — what is in a seed lot, a food shipment, a wild population — which makes distributed capacity one of the few developments on this map that helps the people doing the checking.",
   ["synthesis:seq","synthesis:reagents"])]

# ============================================================== POLAND ========
IND6["POL"] = [
 e("Selvita", "https://selvita.com/",
   "A Polish contract research organisation running drug discovery programmes for international clients. Central and Eastern Europe now hosts a substantial share of the trials and preclinical work that Western regulators read, so the evidence base for approvals in one jurisdiction is increasingly produced in another, under a different oversight system.",
   ["cro:cro","animals:services"])]

# ============================================================== INDIA =========
IND6["IND"] = [
 e("Syngene International", "https://www.syngeneintl.com/",
   "An Indian contract research and manufacturing company working for global pharmaceutical clients, part of the Biocon group. The scale of Indian contract research means a large fraction of the world’s preclinical data is generated here, and the regulator reading it is usually somewhere else entirely.",
   ["cro:cro","cro:cdmo","animals:services"]),
 e("Bharat Biotech", "https://www.bharatbiotech.com/",
   "An Indian vaccine manufacturer producing at a volume few companies anywhere match, including recombinant and viral-vector products. Manufacturing capacity in the global south changes who gets treated during a shortage far more than any patent pledge does — during the pandemic that distinction was the whole argument.",
   ["clinical:vectors","cro:cdmo"])]

# ============================================================== CHINA =========
IND6["CHN"] = [
 e("WuXi AppTec", "https://www.wuxiapptec.com/",
   "One of the largest contract research and manufacturing organisations in the world, China-based, working for a substantial share of the global pharmaceutical industry. US legislative attempts to restrict it revealed how central it had become: many Western drugs, including biologics, depend on it somewhere in the chain, and the companies opposing restriction were its clients.",
   ["cro:cro","cro:cdmo","clinical:vectors"]),
 e("Dabeinong Biotechnology", "https://www.dbn.com.cn/",
   "A Chinese agricultural biotechnology company holding domestic approvals for engineered maize and soy traits, positioned for the country’s shift from importing engineered feed to growing it. Chinese trait developers are approaching the position the four majors hold elsewhere, with the state as a deliberate partner rather than an arms-length regulator.",
   ["seed:traits","seed:majors","money:public"])]

# ============================================================ THAILAND ========
IND6["THA"] = [
 e("Charoen Pokphand Group", "https://www.cpgroupglobal.com/",
   "A Thai conglomerate that is one of the largest animal feed and livestock producers in the world, operating across Asia. Feed buyers of this size decide what gets grown: an engineered soy or maize variety succeeds or fails on whether the companies feeding hundreds of millions of animals will purchase it.",
   ["seed:distribution","livestock:livestock"])]

# ========================================================== NETHERLANDS =======
IND6["NLD"] = [
 e("Nutreco / Skretting", "https://www.nutreco.com/",
   "A major producer of animal and fish feed, including feeds using engineered algal oil as a substitute for wild-caught fish oil. It is one of the clearer cases where an engineered input reduces a documented pressure on wild populations, and the product reaches consumers entirely unlabelled because the engineered organism is not in the fish, only in what the fish ate.",
   ["seed:distribution","livestock:aqua","editing:synbio"])]

# ============================================================== BRAZIL ========
IND6["BRA"] = [
 e("JBS", "https://jbs.com.br/en/",
   "The largest meat processor in the world, buying livestock across several continents. Its purchasing standards function as private regulation for everything upstream — which cloned or edited animals are acceptable, which feed is, which traceability is required — decided commercially and applied across more producers than most national rules reach.",
   ["seed:distribution","livestock:livestock"])]

# ================================================= DE-EXTINCTION & RESCUE =====
IND6["AUS"] = [
 e("Colossal \u2014 thylacine programme partners", "https://tigrrlab.science.unimelb.edu.au/",
   "The Australian university partnership working on thylacine de-extinction, funded by Colossal. Australian marsupial genomics is genuinely advanced by this work, whatever one makes of the goal, which is the recurring bargain in this facet: a spectacular target funds unglamorous capability that would otherwise go unfunded.",
   ["deextinct:ventures","money:vc","deextinct:rescue"], base=BODY),
 e("Australian Frozen Zoo / CryoDiversity", "https://www.zoo.org.au/",
   "Australian biobanking of native species, in a country with a very high rate of endemic species and extinctions. What is banked now is the entire set of options anyone will have later, and the collecting is being done by a small number of underfunded programmes against a clock nobody controls.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]

# =============================================== LABORATORY ANIMALS ===========
IND6["GBR"] = [
 e("Understanding Animal Research", "https://www.understandinganimalresearch.org.uk/",
   "A UK organisation that publishes animal-use figures and runs the Concordat under which research institutions commit to openness about what they do. It is industry-funded advocacy and it is also the reason the UK has some of the most detailed public animal-use data anywhere — both facts are true, and the data is checkable regardless of who paid for the campaign.",
   ["animals:models","rules:associations"], base=ASSN),
 e("Home Office \u2014 animals in science statistics", "https://www.gov.uk/government/collections/statistics-of-scientific-procedures-on-living-animals",
   "The UK government’s annual count of animal procedures, published by species, severity and purpose. It is the most detailed national record of laboratory animal use in the world, and it exists because the UK legislated for it in 1986. Comparable data does not exist in the United States, where mice, rats and birds are excluded from the governing Act altogether.",
   ["animals:models","animals:breeders","rules:regulators"], base=REGI)]
