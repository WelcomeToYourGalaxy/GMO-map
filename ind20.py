# -*- coding: utf-8 -*-
"""Industry entries, part 20."""
from ind1 import e, CO, BODY, REGI, ASSN

IND20 = {}

# ========================================================== SEED & TRAITS =====
IND20["USA"] = [
 e("S&W Seed Company", "https://swseedco.com/",
   "A US forage and sorghum seed company, and one of the few places alfalfa breeding sits. Forage crops receive almost no attention in the engineered-crop argument despite alfalfa being one of the few perennial engineered crops approved — it is pollinated by bees over long distances and cut rather than harvested for seed, so gene flow behaves differently from an annual grain and coexistence is a harder problem than for maize.",
   ["seed:traits","seed:licensees","wild:insects"]),
 e("Simplot \u2014 Innate potatoes", "https://www.simplot.com/food/innate",
   "Innate potatoes bruise less and produce less acrylamide when fried, achieved using only potato genes silenced rather than genes added from elsewhere. That distinction was the point: a plant containing nothing foreign was the industry's attempt to make an engineered crop that felt different to the public. It was developed for processors rather than growers or eaters, and McDonald's declining to buy it mattered more than any approval.",
   ["seed:traits","editing:agtech"]),
 e("J.R. Simplot / McCain \u2014 processor specification", "https://www.mccain.com/",
   "The two largest potato processors, whose purchasing specifications decide which varieties are grown across North America. Simplot developed and sells its own engineered Innate potatoes, so the same company breeds the variety, commercialises it and buys the crop. What actually limited their spread was McDonald's declining to use them — a buyer decision doing what no regulator did.",
   ["seed:distribution","livestock:livestock"])]

IND20["FRA"] = [
 e("Euralis / Lidea", "https://www.lidea-seeds.com/",
   "A French agricultural cooperative with seed and food businesses, operating in a country where growing engineered crops is prohibited and importing engineered feed is routine. Cooperatives sit between the trait owners and the farm and are owned by the farmers, which makes their position on this technology a vote by the people who would plant it.",
   ["seed:licensees","seed:germplasm"])]

IND20["BRA"] = [
 e("TMG \u2014 Tropical Melhoramento & Gen\u00e9tica", "https://www.tmg.agr.br/",
   "A Brazilian soy breeding foundation funded by the farmers who use its varieties, licensing traits from the majors and putting them into cultivars bred for Brazilian soils and daylength. It is the arrangement that made Brazilian soy competitive: the trait comes from abroad and the adaptation is done at home, which is also why trait licensing revenue leaves the country while the breeding value stays.",
   ["seed:licensees","seed:germplasm"])]

# =========================================== EDITING & SYNTHETIC BIOLOGY ======
IND20["USA"] = IND20["USA"] + [
 e("Perfect Day", "https://perfectday.com/",
   "Makes dairy proteins by fermenting engineered fungi, sold in products that require no GMO labelling because the organism is not in the final food. It is a substantial route by which engineering enters food while staying outside every labelling argument.",
   ["editing:synbio","cro:cdmo","livestock:livestock"]),
 e("Impossible Foods \u2014 soy leghemoglobin", "https://impossiblefoods.com/",
   "The heme protein that makes its burger taste of meat is produced by engineered yeast, and it is the ingredient the company had to defend. The FDA cleared it after the company sought a second review it was not required to seek, and it remains unapproved for retail sale in the EU. A plant-based product marketed to people avoiding industrial agriculture depends on a genetically engineered organism, which the company states openly and much of its market did not expect.",
   ["editing:synbio","seed:traits"]),
 e("Conagen", "https://www.conagen.com/",
   "Produces flavour, fragrance and sweetener compounds by fermenting engineered microbes instead of extracting them from plants. A vanilla or stevia molecule made this way is chemically identical to the plant-derived one and can often be labelled natural, which means the substitution reaches a shelf with nothing to distinguish it — and the farmers who grew the original crop lose the market without any decision being announced.",
   ["editing:synbio","cro:cdmo"])]

# ===================================================== LABORATORY ANIMALS =====
IND20["USA"] = IND20["USA"] + [
 e("Institutional Animal Care and Use Committees \u2014 OLAW", "https://olaw.nih.gov/",
   "The US committees that approve animal research protocols at each institution, composed largely of that institution's own scientists plus a veterinarian and at least one member from outside. Self-regulation of this kind is the entire approval layer for most animal work in the United States — the Office of Laboratory Animal Welfare oversees the system rather than the protocols — and committee records are not public unless a request forces them out.",
   ["animals:models","rules:regulators"], base=REGI)]

# ======================================================= HUMAN CLINICAL =======
IND20["USA"] = IND20["USA"] + [
 e("Editas Medicine", "https://www.editasmedicine.com/",
   "One of the original CRISPR therapeutics companies, founded around the Broad Institute's patents with Feng Zhang among its founders. It ran the first trial of CRISPR editing performed inside the human body rather than on cells removed and returned — injecting the editing machinery directly into the eye to treat an inherited blindness. That trial was discontinued for insufficient benefit, which is worth recording: in-body editing is the harder problem, and the first serious attempt at it did not work.",
   ["clinical:therapy","editing:platform","clinical:trials"]),
 e("Orchard Therapeutics", "https://www.orchard-tx.com/",
   "Gene therapies for rare inherited disorders, several of them approved and at least one withdrawn from a market for commercial reasons rather than safety ones. That is the recurring problem in ultra-rare disease: a therapy can work, be approved, and still be withdrawn because too few patients exist to pay for manufacturing it.",
   ["clinical:therapy","money:markets"])]

# ======================================================= ASSISTED REPRO =======
IND20["DNK"] = [
 e("European Sperm Bank", "https://www.europeanspermbank.com/",
   "A large Danish sperm bank shipping internationally, and one of a small number of suppliers serving much of Europe. Family limits are set per country and applied by the bank rather than by any regulator with sight of the whole picture, so a donor legal in one jurisdiction may already have exceeded another's limit. Consumer DNA testing has since made the resulting sibling networks discoverable by the people in them, which no arrangement anticipated.",
   ["repro:banks","repro:clinics"])]

IND20["GRC"] = [
 e("Greek cross-border fertility sector", "https://www.moh.gov.gr/",
   "Greece receives large numbers of patients from countries with tighter rules, offering donor egg treatment with compensation and age limits that differ from those at home. Cross-border fertility care is a market created entirely by legal difference: the medicine is the same everywhere and the law is not.",
   ["repro:clinics","repro:surrogacy","rules:regulators"], base=REGI)]

# =============================================================== RULES ========
IND20["CHE"] = [
 e("WTO \u2014 SPS Committee and biotechnology notifications", "https://www.wto.org/english/tratop_e/sps_e/sps_e.htm",
   "Where countries raise objections to each other's biotechnology measures, under the agreement requiring health and safety restrictions to be scientifically justified. The 2003 case against the EU's approval moratorium was decided here in substance, and the standing threat of a complaint shapes what a country writes into its rules well before any dispute is filed.",
   ["rules:regulators","rules:influence","rules:standards"], base=REGI),
 e("ISO \u2014 biotechnology standards committee", "https://www.iso.org/committee/4514241.html",
   "Writes the international standards for biotechnology methods, terminology and biobanking, through technical committee 276. Standards of this kind are written by industry participants and adopted by reference into national regulation, so a committee with no public accountability supplies the definitions a law then enforces — including, in several cases, what counts as a genetically modified organism for testing purposes.",
   ["rules:standards","synthesis:repos"], base=BODY)]

IND20["KEN"] = [
 e("COMESA \u2014 regional biosafety policy", "https://www.comesa.int/",
   "A regional biosafety policy covering nineteen African states, intended to let countries rely on a single assessment rather than each conducting its own. Regional harmonisation is how a country with no biosafety capacity gets a functioning system, and it is also how one country's decision becomes eighteen others' without a separate debate in any of them.",
   ["rules:standards","rules:regulators"], base=BODY)]

# ======================================================== NEW TERRITORIES =====
IND20["ISR"] = [
 e("Volcani Center \u2014 Agricultural Research Organization", "https://www.agri.gov.il/en/",
   "Israel's national agricultural research organisation, working on crops for arid and saline conditions and on gene editing in fruit and vegetables. Countries with little water and less arable land have driven a disproportionate share of agricultural biotechnology, because the constraint is severe enough to justify the cost — and the resulting varieties are then useful in places facing the same conditions later.",
   ["editing:agtech","money:public","seed:germplasm"], base=BODY)]

IND20["ARE"] = [
 e("International Center for Biosaline Agriculture", "https://www.biosaline.org/",
   "Research on crops that grow in saline soils and can be irrigated with brackish water, based in the UAE. Salinity already affects a large share of irrigated land and is spreading as aquifers are drawn down and seawater intrudes. Breeding for salt tolerance is the least glamorous adaptation work and among the most consequential, and almost none of it involves engineering.",
   ["editing:agtech","money:philanthropy","seed:germplasm"], base=BODY)]

IND20["PER"] = [
 e("International Potato Center (CIP)", "https://cipotato.org/",
   "Holds one of the world's largest potato and sweetpotato collections, in Peru, inside the crop's centre of origin. It developed engineered late-blight-resistant potato for African conditions, and it works in a country whose farmers maintain thousands of native varieties — so the collection, the engineering and the living diversity are all in one place.",
   ["seed:germplasm","money:philanthropy","editing:agtech"], base=BODY)]

IND20["ETH"] = [
 e("Ethiopian Biodiversity Institute", "https://www.ebi.gov.et/",
   "Ethiopia’s national genebank, holding landraces of coffee, teff and other crops from a major centre of diversity. Material held here underpins breeding worldwide, and the terms on which it leaves are governed by treaties most people have never heard of.",
   ["seed:germplasm","rules:ip","money:public"], base=BODY)]
