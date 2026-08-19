# -*- coding: utf-8 -*-
"""Industry entries, part 4. New territories and the thinner facets."""
from ind1 import e, CO, BODY, REGI, ASSN

IND4 = {}

# ============================================================== INDIA =========
IND4["IND"] = [
 e("Mahyco / Maharashtra Hybrid Seeds", "https://www.mahyco.com/",
   "The Indian seed company that brought Bt cotton to India in partnership with Monsanto, and later developed Bt brinjal — an aubergine blocked by an Indian moratorium in 2010 and subsequently approved in Bangladesh. Bt cotton now covers the great majority of Indian cotton acreage, which makes this one of the largest adoptions of an engineered crop anywhere, and the country where the argument about farmer debt, seed price and suicide has been most bitterly fought. The scale and the dispute both run through this company.",
   ["seed:licensees","seed:traits","rules:ip"]),
 e("Department of Biotechnology", "https://dbtindia.gov.in/",
   "India’s national biotechnology funder and policy body, financing crop, medical and industrial work across a research system serving 1.4 billion people. Its decisions set the direction for a fifth of humanity and are made largely outside the English-language debate about this field, which tends to treat American and European regulators as though they were the whole picture.",
   ["money:public","editing:agtech"], base=REGI)]

# ============================================================== CHINA =========
IND4["CHN"] = [
 e("Syngenta Group China", "https://www.syngentagroup.cn/",
   "The Chinese arm of the state-owned Syngenta, and the vehicle through which seed sovereignty operates as industrial policy. China has moved from importing engineered soy and maize for feed to approving domestic cultivation, and the company positioned to supply it is one the state already owns. That is a different arrangement from four private corporations.",
   ["seed:majors","money:markets","rules:regulators"]),
 e("Chinese Academy of Agricultural Sciences", "https://www.caas.cn/en/",
   "The state agricultural research system, and one of the largest crop research organisations in the world by staff and output. Its gene-editing work in rice, wheat and maize is published in the same journals as everyone else’s, but its priorities are set by national policy rather than by what a market will pay for — which produces a different set of crops and traits from the ones private breeders pursue.",
   ["editing:agtech","seed:germplasm","money:public"], base=BODY)]

# ============================================================= BRAZIL =========
IND4["BRA"] = [
 e("Embrapa", "https://www.embrapa.br/",
   "Brazil’s public agricultural research corporation, which turned the cerrado into one of the world’s great grain regions and holds engineered varieties of its own, including a virus-resistant bean developed entirely in the public sector. It is the strongest example anywhere of a state research body competing with the majors on their own ground — and Brazil is still second only to the United States in engineered acreage, so what Embrapa releases reaches an enormous area.",
   ["editing:agtech","cro:cro","rules:standards"]),
 e("CTNBio \u2014 national biosafety commission", "https://ctnbio.mctic.gov.br/",
   "Brazil’s biosafety commission, which approves engineered organisms for a country planting more than fifty million hectares of them. Its decisions are published and its meetings minuted, making it one of the more legible regulators in the world. It has also approved essentially everything put in front of it, including engineered eucalyptus and, in 2018, the first engineered insect approved for unrestricted commercial release anywhere.",
   ["rules:regulators","rules:standards"], base=REGI)]

# ========================================================== ARGENTINA =========
IND4["ARG"] = [
 e("Bioceres Crop Solutions", "https://bioceres.com.ar/",
   "The Argentine company behind HB4 drought-tolerant wheat — the first engineered wheat approved for cultivation anywhere. Wheat had been left alone for twenty-five years, not for technical reasons but because millers and bakers in importing countries would not take it. Argentina approved it and then had to negotiate acceptance downstream, which is why this one product tells you more about who really decides what gets grown than any regulator’s file does.",
   ["seed:traits","seed:licensees","rules:regulators"])]

# ========================================================== GERMANY ===========
IND4["DEU"] = [
 e("BioNTech", "https://www.biontech.com/",
   "Known for the COVID vaccine, but the underlying business is a platform for making mRNA and cell therapies to order, now with manufacturing in Germany, Singapore and Rwanda. The Rwandan plant matters most: production capacity for genetic medicine has never existed in Africa before, and where a thing can be made determines who can get it far more reliably than where it was invented.",
   ["clinical:therapy","clinical:vectors","money:markets"]),
 e("Evotec", "https://www.evotec.com/",
   "A drug discovery and development contractor that runs research programmes for pharmaceutical clients, including gene and cell therapy work. It is the European end of the arrangement in which the evidence for approval is generated by companies the applicant hires — the same structure as the American contract laboratories, with the same dependency on repeat business.",
   ["cro:cro","clinical:trials"])]

# ============================================================ JAPAN ===========
IND4["JPN"] = [
 e("Sanatech Seed", "https://sanatech-seed.com/en/",
   "Sells a gene-edited tomato with raised GABA content directly to Japanese consumers, the first edited food marketed to the public anywhere. Japan classed it outside the GMO rules because no foreign DNA was inserted, so it required notification rather than approval. The product itself is unremarkable; what it established is that a country can move an edited food to market through a notification form.",
   ["editing:agtech","livestock:pets","rules:regulators"]),
 e("Regional Fish Institute", "https://regional.fish/en/",
   "A Kyoto University spin-out selling gene-edited red sea bream and tiger puffer with more edible flesh, cleared through Japan’s notification route. These are the first edited animals sold as food anywhere, and they reached consumers without the review AquaBounty’s salmon spent twenty-five years in — the same category of product, a different classification, and an entirely different regulatory life.",
   ["livestock:aqua","editing:agtech"])]

# ============================================================ ISRAEL ==========
IND4["ISR"] = [
 e("Evogene", "https://www.evogene.com/",
   "An Israeli company using computational biology to design traits, licensing them to seed companies rather than selling seed. Like KeyGene, it is a layer beneath the visible market: counting brands in a seed catalogue understates how few sources the underlying genetics has.",
   ["editing:platform","editing:agtech","clinical:therapy"])]

# ======================================================== SOUTH KOREA =========
IND4["KOR"] = [
 e("Toolgen", "https://www.toolgen.com/",
   "A South Korean gene-editing company holding CRISPR patents that were contested in the same interference proceedings as Broad and Berkeley. Its presence is a reminder that the patent estate everyone else licenses from is not purely American, and that a technique now central to world agriculture and medicine is owned in pieces by a handful of institutions across three continents.",
   ["editing:patents","editing:platform"])]

# ========================================================== SINGAPORE =========
IND4["SGP"] = [
 e("Singapore Food Agency \u2014 novel food approvals", "https://www.sfa.gov.sg/",
   "The first regulator in the world to approve cultivated meat for sale, and a jurisdiction that has deliberately positioned itself as the place novel foods can reach market first. A small state can set a global precedent by approving something before anyone else does, and the rest of the world then argues with a product that already exists rather than a proposal.",
   ["rules:regulators","editing:synbio","livestock:livestock"], base=REGI)]

# ========================================================= NETHERLANDS ========
IND4["NLD"] = [
 e("Corbion", "https://www.corbion.com/",
   "A Dutch company fermenting engineered algae and microbes into food ingredients, lactic acid and omega-3 oils. Products of fermentation are generally not labelled as engineered even when an engineered organism made them, because the organism is not in the final product — so this is a substantial route by which genetic engineering enters food while remaining outside every labelling debate.",
   ["editing:synbio","cro:cdmo"])]

# ============================================================= DENMARK ========
IND4["DNK"] = [
 e("Novonesis (Novozymes / Chr. Hansen)", "https://www.novonesis.com/",
   "The world’s largest industrial enzyme company, formed by merger, supplying engineered enzymes and cultures to baking, brewing, dairy, detergents and animal feed. Most enzymes in industrial food processing are made by engineered microbes, and almost none of it is labelled or discussed. By volume of engineered organisms actually working in production, this is one of the largest operations on the map and among the least visible.",
   ["editing:synbio","cro:cdmo","rules:regulators"])]

# ========================================================== AUSTRALIA =========
IND4["AUS"] = [
 e("Office of the Gene Technology Regulator \u2014 GMO Record", "https://www.ogtr.gov.au/what-weve-approved/gmo-record",
   "Australia’s regulator, and one of the few that publishes where field trials actually are — EU member states do too, under the deliberate release directive, in several countries down to the parcel. Every other release record on this map sits at a state or country centroid because the register gives no location; Australia gives coordinates, licence conditions and risk assessments. It shows that publishing sites is possible and that everyone else has chosen not to.",
   ["rules:regulators","rules:standards"], base=REGI),
 e("Nufarm", "https://nufarm.com/",
   "An Australian agrochemical company, and one of the largest generic producers of off-patent herbicides including glyphosate. Once a patent lapses the chemistry does not disappear — it gets cheaper, and generic manufacturers expand the market the original patent holder created. The traits engineered to survive these herbicides remain valuable long after the herbicide itself stops being anyone’s exclusive property.",
   ["seed:licensees","livestock:aqua","seed:traits"])]

# ============================================================= CANADA =========
IND4["CAN"] = [
 e("Canadian Food Inspection Agency \u2014 PNT decisions", "https://inspection.canada.ca/en/plant-varieties/plants-novel-traits",
   "Canada regulates by what a plant is rather than by how it was made, assessing anything with a novel trait whatever the method. Transgenic events and products of mutagenesis or editing sit in the same public register, which makes Canada the one country where the second group stays visible instead of disappearing into a carve-out. The register is also where the gap shows: the deregulated class carries no international identifier, so it cannot be tracked across borders.",
   ["rules:regulators","rules:standards","editing:agtech"], base=REGI)]
