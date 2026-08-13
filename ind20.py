# -*- coding: utf-8 -*-
"""Industry entries, part 20."""
from ind1 import e, CO, BODY, REGI, ASSN

IND20 = {}

# ========================================================== SEED & TRAITS =====
IND20["USA"] = [
 e("S&W Seed Company", "https://swseedco.com/",
   "A US forage and sorghum seed company. Forage crops receive almost no attention in this debate and cover enormous areas, largely because what feeds livestock is discussed less than what feeds people.",
   ["seed:traits","seed:licensees","wild:insects"]),
 e("Simplot \u2014 Innate potatoes", "https://www.simplot.com/food/innate",
   "Innate potatoes are engineered to bruise less and produce less acrylamide when fried, using only potato genes. They were developed for processors rather than for growers or eaters, which is who the trait actually serves.",
   ["seed:traits","editing:agtech"]),
 e("J.R. Simplot / McCain \u2014 processor specification", "https://www.mccain.com/",
   "The processors’ purchasing specifications decide which potato varieties get planted. A specification from a buyer of this size is a more effective rule than most regulations.",
   ["seed:distribution","livestock:livestock"])]

IND20["FRA"] = [
 e("Euralis / Lidea", "https://www.lidea-seeds.com/",
   "A French agricultural cooperative with seed and food businesses. Cooperative structures still hold a large share of European agriculture, which is why concentration figures calculated globally do not describe Europe well.",
   ["seed:licensees","seed:germplasm"])]

IND20["BRA"] = [
 e("TMG \u2014 Tropical Melhoramento & Gen\u00e9tica", "https://www.tmg.agr.br/",
   "A Brazilian soy breeding foundation, farmer-funded, licensing traits from the majors into varieties adapted to Brazilian conditions. Local adaptation is what makes a trait usable, and it is done by organisations the trait owners do not control.",
   ["seed:licensees","seed:germplasm"])]

# =========================================== EDITING & SYNTHETIC BIOLOGY ======
IND20["USA"] = IND20["USA"] + [
 e("Perfect Day", "https://perfectday.com/",
   "Makes dairy proteins by fermenting engineered fungi, sold in products that require no GMO labelling because the organism is not in the final food. It is a substantial route by which engineering enters food while staying outside every labelling argument.",
   ["editing:synbio","cro:cdmo","livestock:livestock"]),
 e("Impossible Foods \u2014 soy leghemoglobin", "https://impossiblefoods.com/",
   "The heme protein that makes its burger taste of meat is produced by engineered yeast, and the company sought and won FDA affirmation for it. It is one of the few cases where a company chose the slower regulatory route when a faster one was arguable.",
   ["editing:synbio","seed:traits"]),
 e("Conagen", "https://www.conagen.com/",
   "Produces flavour, fragrance and sweetener compounds by fermentation with engineered microbes, replacing plant extraction. Ingredients arriving this way are rarely identified as engineered at any point in the supply chain.",
   ["editing:synbio","cro:cdmo"])]

# ===================================================== LABORATORY ANIMALS =====
IND20["USA"] = IND20["USA"] + [
 e("Charles River \u2014 horseshoe crab and LAL supply", "https://www.criver.com/products-services/qc-microbial-solutions",
   "Horseshoe crab blood is used to test injectable drugs and devices for bacterial contamination, and the animals are bled and returned to the sea with a proportion dying. A recombinant substitute exists, works, and is in the US pharmacopoeia; adoption has been slow because the old test is what everyone is used to.",
   ["animals:services","synthesis:reagents","editing:synbio"]),
 e("Institutional Animal Care and Use Committees \u2014 OLAW", "https://olaw.nih.gov/",
   "US committees that approve animal research at each institution, composed largely of staff of that institution. Their records are not generally public, so the main approval step for most animal research in the United States leaves no external trace.",
   ["animals:models","rules:regulators"], base=REGI)]

# ======================================================= HUMAN CLINICAL =======
IND20["USA"] = IND20["USA"] + [
 e("Editas Medicine", "https://www.editasmedicine.com/",
   "One of the original CRISPR therapeutics companies, founded around the Broad patents. Several such companies were built directly on institutional patent estates before any product existed.",
   ["clinical:therapy","editing:platform","clinical:trials"]),
 e("Orchard Therapeutics", "https://www.orchard-tx.com/",
   "Gene therapies for rare inherited disorders, several withdrawn or discontinued on commercial grounds after approval. A treatment can be approved, work, and still cease to exist because the patient population is too small to sustain it.",
   ["clinical:therapy","money:markets"])]

# ======================================================= ASSISTED REPRO =======
IND20["DNK"] = [
 e("European Sperm Bank", "https://www.europeanspermbank.com/",
   "A large Danish sperm bank shipping internationally. Family limits are set per country and enforced per bank, so a donor can reach limits in many jurisdictions at once with nobody counting the total.",
   ["repro:banks","repro:clinics"])]

IND20["GRC"] = [
 e("Greek cross-border fertility sector", "https://www.moh.gov.gr/",
   "Greece receives large numbers of patients from countries where treatments are restricted or unavailable. A national restriction becomes a travel decision, and the clinics on the receiving side are regulated only by their own country.",
   ["repro:clinics","repro:surrogacy","rules:regulators"], base=REGI)]

# =============================================================== RULES ========
IND20["CHE"] = [
 e("WTO \u2014 SPS Committee and biotechnology notifications", "https://www.wto.org/english/tratop_e/sps_e/sps_e.htm",
   "Where countries challenge each other’s biotechnology measures as trade barriers, including the US challenge to Mexico’s GM maize decree. A biosafety decision becomes a trade dispute, and the forum deciding it is a trade forum.",
   ["rules:regulators","rules:influence","rules:standards"], base=REGI),
 e("ISO \u2014 biotechnology standards committee", "https://www.iso.org/committee/4514241.html",
   "International standards for biotechnology methods and terminology. Standards decide what counts as detection, which determines whether unauthorised GM presence can be demonstrated in a legal dispute.",
   ["rules:standards","synthesis:repos"], base=BODY)]

IND20["KEN"] = [
 e("COMESA \u2014 regional biosafety policy", "https://www.comesa.int/",
   "A regional biosafety policy covering nineteen African states, allowing centralised approval decisions. Regional harmonisation means an approval in one process applies across many countries, which concentrates the decision considerably.",
   ["rules:standards","rules:regulators"], base=BODY)]

# ======================================================== NEW TERRITORIES =====
IND20["ISR"] = [
 e("Volcani Center \u2014 Agricultural Research Organization", "https://www.agri.gov.il/en/",
   "Israel’s national agricultural research organisation, working on crops for arid conditions. Drought and salinity work has an obvious case and almost none of it has reached farmers as an engineered product anywhere.",
   ["editing:agtech","money:public","seed:germplasm"], base=BODY)]

IND20["ARE"] = [
 e("International Center for Biosaline Agriculture", "https://www.biosaline.org/",
   "Research on crops for saline soils and water, based in the UAE. Salinity affects an enormous and growing area of farmland, and it attracts a fraction of the investment that herbicide tolerance does.",
   ["editing:agtech","money:philanthropy","seed:germplasm"], base=BODY)]

IND20["PER"] = [
 e("International Potato Center (CIP)", "https://cipotato.org/",
   "A public research centre holding one of the world’s largest potato and sweetpotato genebanks, based in Peru — the crop’s centre of origin. Peru’s moratorium on engineered crops and this genebank exist in the same country for the same reason.",
   ["seed:germplasm","money:philanthropy","editing:agtech"], base=BODY)]

IND20["ETH"] = [
 e("Ethiopian Biodiversity Institute", "https://www.ebi.gov.et/",
   "Ethiopia’s national genebank, holding landraces of coffee, teff and other crops from a major centre of diversity. Material held here underpins breeding worldwide, and the terms on which it leaves are governed by treaties most people have never heard of.",
   ["seed:germplasm","rules:ip","money:public"], base=BODY)]
