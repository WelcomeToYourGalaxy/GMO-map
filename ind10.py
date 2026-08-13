# -*- coding: utf-8 -*-
"""Industry entries, part 10."""
from ind1 import e, CO, BODY, REGI, ASSN

IND10 = {}

# =============================================================== CUBA =========
IND10["CUB"] = [
 e("Centro de Ingenier\u00eda Gen\u00e9tica y Biotecnolog\u00eda", "https://cigb.edu.cu/",
   "Cuba’s state genetic engineering centre, which developed and manufactured its own COVID vaccines and exports biotechnology products. A small embargoed country built a vaccine industry from public investment, which is the sharpest available counter-argument to the claim that only private capital can do this work.",
   ["seed:traits","clinical:therapy","money:public"], base=BODY)]

# ============================================================= BOLIVIA ========
IND10["BOL"] = [
 e("Comit\u00e9 Nacional de Bioseguridad", "https://www.medioambiente.gob.bo/",
   "Bolivia’s biosafety committee, in a country that permits engineered soy but has resisted expanding approvals under pressure from both agribusiness and indigenous organisations. The dispute is unusually explicit about whose land and whose seed is at stake.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================= ECUADOR ========
IND10["ECU"] = [
 e("Ministerio del Ambiente \u2014 bioseguridad", "https://www.ambiente.gob.ec/",
   "Ecuador wrote a prohibition on engineered seeds and crops into its constitution in 2008, then amended the position for research purposes. A constitutional ban is the strongest legal form this opposition has taken anywhere, and its subsequent softening shows what that form does and does not withstand.",
   ["rules:regulators","seed:germplasm"], base=REGI)]

# ========================================================== COSTA RICA ========
IND10["CRI"] = [
 e("Comisi\u00f3n T\u00e9cnica Nacional de Bioseguridad", "https://www.protecnet.go.cr/",
   "Costa Rica permits engineered crops to be grown for seed export while restricting domestic cultivation — the same arrangement as Chile. Several countries have settled on producing engineered seed for others to plant without planting it themselves.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================ TANZANIA ========
IND10["TZA"] = [
 e("National Environment Management Council", "https://www.nemc.or.tz/",
   "Tanzania halted its engineered crop trials in 2018 and ordered the material destroyed, after having permitted them. Reversal after approval is rare enough that this case is cited by both sides, and the trials were publicly funded research rather than a company’s.",
   ["rules:regulators"], base=REGI)]

# ============================================================== ZAMBIA ========
IND10["ZMB"] = [
 e("National Biosafety Authority Zambia", "https://www.nba.co.zm/",
   "Zambia refused engineered food aid during the 2002 famine, on the grounds that accepting grain would put engineered genes into its seed stock and close its European market. The decision is still argued over, and it established that a country might weigh trade access against immediate need.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================== GREECE ========
IND10["GRC"] = [
 e("Ministry of Rural Development and Food", "https://www.minagric.gr/",
   "Greece prohibits the cultivation of engineered crops and has used EU opt-outs to maintain it. Greece is also a centre of diversity for several Mediterranean crops, which is the stated basis for the position.",
   ["rules:regulators"], base=REGI)]

# ============================================================= HUNGARY ========
IND10["HUN"] = [
 e("Ministry of Agriculture \u2014 GMO-free constitutional provision", "https://kormany.hu/",
   "Hungary wrote GMO-free agriculture into its constitution in 2011, the only EU member to do so. The clause has held through changes of government, which is more than most agricultural policy positions manage.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================ MOROCCO =========
IND10["MAR"] = [
 e("Office National de S\u00e9curit\u00e9 Sanitaire des Produits Alimentaires", "https://www.onssa.gov.ma/",
   "Morocco’s food safety authority, in a country that imports engineered feed without permitting cultivation. North African import policy determines what North American and South American exporters plant, at a scale rarely credited to the importing countries.",
   ["seed:distribution","rules:regulators"], base=REGI)]

# ============================================================= TAIWAN =========
IND10["TWN"] = [
 e("Food and Drug Administration \u2014 GM food registration", "https://www.fda.gov.tw/ENG/",
   "Taiwan requires registration and labelling of engineered foods and maintains a public register of approved events. Its labelling threshold is stricter than the American approach and looser than the European one, which places it in the middle of a global argument usually described as two-sided.",
   ["rules:regulators","rules:standards"], base=REGI)]

# ======================================================== SAUDI ARABIA ========
IND10["SAU"] = [
 e("Saudi Food and Drug Authority \u2014 GM food rules", "https://www.sfda.gov.sa/en",
   "Saudi Arabia requires labelling of engineered foods and approves specific events for import. A large food importer with mandatory labelling shapes what exporters are willing to ship, and does so without growing anything itself.",
   ["rules:regulators","seed:distribution"], base=REGI)]

# ============================================================ PHILIPPINES =====
IND10["PHL"] = [
 e("International Rice Research Institute \u2014 Golden Rice", "https://www.irri.org/golden-rice",
   "The public institute that developed Golden Rice, the vitamin-A rice held up for twenty-five years as the thing objectors are denying to children. In that time it has not reduced deficiency anywhere, partly because it was never finished into varieties farmers grow and eat. A Philippine court cancelled its commercial permit in April 2024 and declined to reverse itself.",
   ["seed:traits","money:philanthropy","rules:regulators"], base=BODY)]

# ============================================================== NORWAY ========
IND10["NOR"] = [
 e("Norwegian Biotechnology Advisory Board", "https://www.bioteknologiradet.no/english/",
   "Norway’s public advisory body on biotechnology, which runs open consultations and publishes reasoned positions including on gene drives and germline editing. It is the clearest working example of a country building deliberation into biotechnology policy rather than adding it afterwards.",
   ["rules:regulators","clinical:germline","repro:screening"], base=BODY)]

# ================================================= DE-EXTINCTION & RESCUE =====
IND10["USA"] = [
 e("Rewriting Extinction / genetic biocontrol programmes", "https://www.geneticbiocontrol.org/",
   "Research toward using engineered organisms for conservation — suppressing invasive species, rescuing populations too small to recover. The conservation case is the strongest argument for deliberate release, and it is being made by people with no commercial interest in the outcome.",
   ["deextinct:rescue","wild:drives","wild:insects"], base=BODY),
 e("Nature Conservancy \u2014 biotechnology in conservation", "https://www.nature.org/",
   "One of the largest conservation organisations in the world, which has engaged with rather than opposed biotechnology in conservation. Its position splits the environmental movement, and the split is substantive rather than tactical.",
   ["deextinct:rescue","rules:associations"], base=BODY)]

# ============================================================= MONEY ==========
IND10["GBR"] = [
 e("Wellcome Leap", "https://wellcomeleap.org/",
   "A programme funding high-risk biomedical work on short timelines, including in genetic medicine. It is an attempt to buy speed with philanthropic money rather than venture money, and the difference in what gets attempted is visible in its portfolio.",
   ["money:philanthropy","clinical:therapy","repro:screening"], base=BODY)]

IND10["CHN"] = [
 e("China National Seed Group (Syngenta / Sinochem)", "https://www.sinochem.com/en/",
   "China’s largest seed company, inside the state-owned group that also owns Syngenta. The combination gives one state-controlled entity a position in both domestic and international seed markets that no private company holds.",
   ["seed:majors","seed:distribution","money:public"])]

# ============================================================= ANIMALS ========
IND10["DEU"] = [
 e("European Bioinformatics Institute \u2014 model organism databases", "https://www.ebi.ac.uk/",
   "The public databases holding genome and model-organism data that biology worldwide depends on, funded by European states. Almost every entry on this map relies on this infrastructure, and none of it is owned by anyone who charges for it.",
   ["animals:models","synthesis:repos"], base=BODY)]
