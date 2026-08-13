# -*- coding: utf-8 -*-
"""Industry entries, part 8."""
from ind1 import e, CO, BODY, REGI, ASSN

IND8 = {}

# ============================================================= PAKISTAN =======
IND8["PAK"] = [
 e("National Biosafety Centre \u2014 Ministry of Climate Change", "https://mocc.gov.pk/",
   "Pakistan’s biosafety body, in a country where Bt cotton spread widely before any formal approval process was functioning. The seed moved through informal channels ahead of the regulator, which is the sequence several countries have followed and which no register captures.",
   ["rules:regulators","seed:distribution","seed:traits"], base=REGI)]

# ============================================================ BANGLADESH ======
IND8["BGD"] = [
 e("Bangladesh Agricultural Research Institute \u2014 Bt brinjal", "http://www.bari.gov.bd/",
   "Bt brinjal was approved and grown in Bangladesh after being blocked in India, developed publicly and distributed to smallholders. It is the clearest case of an engineered crop reaching poor farmers as a public-sector product, and the reporting on whether it has helped them is contested by both sides.",
   ["seed:traits","money:philanthropy","rules:regulators"], base=BODY)]

# ============================================================ ETHIOPIA ========
IND8["ETH"] = [
 e("Ethiopian Environment Protection Authority \u2014 biosafety", "https://epa.gov.et/",
   "Ethiopia rewrote a restrictive biosafety law to permit engineered cotton and maize trials. Law reform preceding approval is the standard sequence across Africa, and the pressure for it typically comes from a combination of donor programmes and neighbouring states’ decisions.",
   ["rules:regulators","seed:germplasm"], base=REGI)]

# ============================================================== GHANA =========
IND8["GHA"] = [
 e("National Biosafety Authority Ghana", "https://nba.gov.gh/",
   "Ghana’s regulator, approving Bt cowpea after a long court challenge from domestic opponents. The litigation is as much a part of the record as the approval: opposition in West Africa is organised and legal, not simply absent as it is sometimes portrayed.",
   ["rules:regulators","rules:ip","seed:traits"], base=REGI)]

# ============================================================= URUGUAY ========
IND8["URY"] = [
 e("Gabinete Nacional de Bioseguridad", "https://www.gub.uy/ministerio-ganaderia-agricultura-pesca/",
   "Uruguay’s biosafety cabinet, approving engineered soy and maize in a country whose agriculture is heavily export-oriented. Small exporting countries adopt what their buyers will accept, so approval decisions here follow demand in China and Europe more closely than domestic debate.",
   ["rules:regulators","livestock:livestock","seed:distribution"], base=REGI)]

# ============================================================= PARAGUAY =======
IND8["PRY"] = [
 e("SENAVE \u2014 seed and plant health service", "https://www.senave.gov.py/",
   "Paraguay’s seed authority. Engineered soy reached Paraguay through unapproved cross-border planting from Brazil and Argentina before being legalised retroactively — approval following the fact rather than preceding it, which happened in Brazil too.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================== CHILE =========
IND8["CHL"] = [
 e("SAG \u2014 Servicio Agr\u00edcola y Ganadero", "https://www.sag.gob.cl/",
   "Chile permits engineered crops to be grown for seed export but not for domestic sale, making it a significant producer of engineered seed that its own farmers cannot plant. Counter-season seed multiplication for northern hemisphere companies is a large and little-discussed part of the world seed system.",
   ["rules:regulators","seed:distribution","seed:germplasm"], base=REGI)]

# ============================================================== SPAIN =========
IND8["ESP"] = [
 e("Ministerio de Agricultura \u2014 GM cultivation register", "https://www.mapa.gob.es/",
   "Spain grows nearly all of the European Union’s engineered maize — one country accounting for almost the entire cultivated area of a bloc usually described as GM-free. The register of planted area by province is public, and it is the only place the EU’s actual cultivation footprint can be seen.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================ PORTUGAL ========
IND8["PRT"] = [
 e("Direção-Geral de Alimentação e Veterinária", "https://www.dgav.pt/",
   "Portugal’s agriculture authority, overseeing the EU’s second and much smaller area of engineered maize. Portugal and Spain together are essentially the whole of EU cultivation, and both require coexistence measures and public registers of planted fields.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================= ROMANIA ========
IND8["ROU"] = [
 e("Ministry of Agriculture \u2014 biotechnology", "https://www.madr.ro/",
   "Romania grew engineered soy before joining the EU and had to stop on accession, and it is the clearest example of enlargement reversing an agricultural technology decision. Farmers who had adopted it lost access, and the argument about whether they should regain it is still live.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================== EGYPT =========
IND8["EGY"] = [
 e("Agricultural Genetic Engineering Research Institute", "https://ageri.arc.sci.eg/",
   "Egypt’s public genetic engineering institute, in a country that has approved and then suspended engineered maize cultivation. Egypt is the largest wheat importer in the world, which makes its position on engineered grain consequential well beyond its own fields.",
   ["editing:agtech","money:public"], base=BODY)]

# ============================================================== CANADA ========
IND8["CAN"] = [
 e("Nuseed / Nufarm omega-3 canola", "https://www.nuseed.com/",
   "Canola engineered to produce long-chain omega-3 oils previously obtained from fish, grown in Australia, the United States and Canada. It substitutes a crop for a wild-capture fishery, which is one of the few cases on this map where an engineered organism reduces pressure on a wild population rather than adding to it.",
   ["seed:traits","livestock:aqua"]),
 e("Health Canada \u2014 novel food decisions", "https://www.canada.ca/en/health-canada/services/food-nutrition/genetically-modified-foods-other-novel-foods.html",
   "Canada assesses foods by novelty of the trait rather than by method, so an edited food and a conventionally bred one with the same trait are treated alike. Decisions are published with the reasoning, which makes this one of the more legible novel-food registers, and it is also where the deregulated class becomes hardest to follow across borders.",
   ["rules:regulators","rules:standards"], base=REGI)]

# =============================================== SYNTHESIS & INSTRUMENTS ======
IND8["USA"] = [
 e("Aldevron (Danaher)", "https://www.aldevron.com/",
   "A manufacturer of plasmid DNA and mRNA for gene therapy and vaccine producers, now inside Danaher. Plasmid supply is a bottleneck for genetic medicine, and it sits with the same conglomerate that owns much of the reagent and instrument supply chain.",
   ["synthesis:synth","cro:cdmo","clinical:vectors"]),
 e("Pacific Biosciences", "https://www.pacb.com/",
   "Long-read sequencing, which reads DNA in longer continuous stretches than short-read platforms and so detects structural changes that short reads miss — including unintended insertions at an edit site. The verification capability and the editing capability come from the same industry.",
   ["synthesis:seq"]),
 e("Bio-Rad Laboratories", "https://www.bio-rad.com/",
   "A supplier of laboratory instruments and reagents, including droplet digital PCR used to detect and quantify engineered sequences in food and seed. Testing for unauthorised GM presence at low concentrations depends on this class of instrument, so the ability to find engineered material is itself a purchased product.",
   ["synthesis:reagents","rules:standards"])]
