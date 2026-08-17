# -*- coding: utf-8 -*-
"""Industry entries, part 29.

Countries entirely absent from the map so far, chosen where something real is
happening rather than to tick a list. Mostly east and west Africa, where seed law
reform is being negotiated now, and the Maghreb, where the region's crop research
sits.

A country here is not on the map because it is a large player. It is on the map
because a decision is being taken there about crops millions of people eat, and
because leaving it blank makes the map look like nothing happens there.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND29 = {}

# ==================================================== EAST AFRICA =============
IND29["UGA"] = [
 e("National Agricultural Research Organisation \u2014 Uganda",
   "https://www.naro.go.ug/",
   "Developed disease-resistant banana and cassava, both staples eaten directly by "
   "tens of millions in the region. Uganda\u2019s biosafety bill passed parliament twice and "
   "was returned unsigned twice, so the research exists and the legal route to release "
   "it does not \u2014 the clearest case anywhere of a country having the product and not the "
   "permission.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]

IND29["RWA"] = [
 e("Rwanda Agriculture and Animal Resources Development Board",
   "https://www.rab.gov.rw/",
   "Runs seed certification and crop research for a country that has rebuilt its "
   "agricultural system from near nothing since 1994. Rwanda is frequently cited as a "
   "model for agricultural policy in the region, which means what it adopts tends to "
   "spread \u2014 and it has moved toward permitting engineered crops.",
   ["seed:traits", "livestock:livestock"], base=BODY),
]

IND29["MOZ"] = [
 e("Instituto de Investiga\u00e7\u00e3o Agr\u00e1ria de Mo\u00e7ambique",
   "https://www.iiam.gov.mz/",
   "Mozambique\u2019s agricultural research institute, which ran confined field trials of "
   "drought-tolerant and insect-resistant maize under the WEMA programme. Those trials "
   "were donor-funded and the varieties donor-developed, which is the pattern across the "
   "region: the research is African and the agenda mostly is not.",
   ["seed:traits"], base=BODY),
]

IND29["MWI"] = [
 e("Malawi Environmental Affairs Department \u2014 biosafety",
   "https://www.environment.gov.mw/",
   "Approved Bt cotton for commercial cultivation, one of the few African countries to "
   "reach commercial approval. Malawi is small, poor and landlocked, so its decision "
   "carries little weight commercially and considerable weight as precedent \u2014 which is "
   "roughly the reverse of how it is usually reported.",
   ["rules:regulators"], base=REGI),
]

IND29["TZA"] = [
 e("Tanzania Commission for Science and Technology",
   "https://www.costech.or.tz/",
   "Oversees research approvals in a country that halted its GM trials in 2018 and "
   "ordered the material destroyed. Reversal after approval is rare enough that this "
   "case is cited by both sides, and the trials were publicly funded research rather "
   "than a company\u2019s product.",
   ["rules:regulators", "seed:traits"], base=REGI),
]

# ==================================================== WEST AFRICA =============
IND29["BFA"] = [
 e("Institut de l\u2019Environnement et de Recherches Agricoles",
   "https://www.inera.bf/",
   "Burkina Faso grew Bt cotton commercially and then withdrew it, after the fibre came "
   "out shorter and buyers paid less. The trait worked against the pest and the crop lost "
   "value anyway \u2014 which is the clearest demonstration on this map that a trait doing "
   "what it says is not the same as a product that works.",
   ["fibre", "seed:traits"], base=BODY),
]

IND29["CIV"] = [
 e("Conseil du Caf\u00e9-Cacao", "https://www.conseilcafecacao.ci/",
   "C\u00f4te d\u2019Ivoire produces more cocoa than anywhere else, grown almost entirely by "
   "smallholders, and the crop faces a virus conventional breeding has not solved. What "
   "happens to cocoa genetics is decided between this board, the chocolate companies and "
   "the research collections \u2014 and the growers are the party with the least say and the "
   "most at stake.",
   ["trees", "seed:distribution"], base=BODY),
]

IND29["CMR"] = [
 e("Institut de Recherche Agricole pour le D\u00e9veloppement",
   "https://www.irad-cameroon.org/",
   "Cameroon's agricultural research institute, holding germplasm and running breeding for crops grown across central Africa. Institutes of this kind hold collections nobody else has, are chronically underfunded, and are the entities that benefit-sharing arrangements are written about — usually without their participation in the writing.",
   ["seed:germplasm", "seed:traits"], base=BODY),
]

# ======================================================= MAGHREB ==============
IND29["TUN"] = [
 e("Institut National de la Recherche Agronomique de Tunisie",
   "https://www.inrat.agrinet.tn/",
   "Works on durum wheat, olives and date palm for a warming, drying region. North "
   "Africa is where climate pressure on agriculture is arriving first and hardest, and "
   "the crops most affected are the ones with the least commercial breeding behind them.",
   ["seed:traits", "trees"], base=BODY),
]

IND29["DZA"] = [
 e("Institut National de la Recherche Agronomique d\u2019Alg\u00e9rie",
   "https://www.inraa.dz/",
   "Algeria imports most of its wheat and has among the highest per-capita cereal "
   "consumption in the world, which makes it one of the buyers whose specifications "
   "shape what exporting countries plant. Its own research is on adapting cereals to "
   "drought.",
   ["seed:traits"], base=BODY),
]

# ================================================== SOUTHEAST ASIA ============
IND29["KHM"] = [
 e("Cambodian Agricultural Research and Development Institute",
   "https://www.cardi.org.kh/",
   "Holds Cambodia\u2019s rice collections, including traditional varieties from a country "
   "whose agricultural knowledge was deliberately destroyed in the 1970s. Rebuilding a "
   "seed system after that is a different problem from developing one, and the "
   "collections are what made it possible at all.",
   ["seed:germplasm", "seed:traits"], base=BODY),
]

IND29["NPL"] = [
 e("Nepal Agricultural Research Council", "https://narc.gov.np/",
   "Nepal spans lowland plains to high mountains and holds landraces adapted across that "
   "whole range, which is an unusual concentration of climate adaptation in one small "
   "country. Its collections matter well beyond its borders for exactly that reason.",
   ["seed:germplasm", "seed:traits"], base=BODY),
]

# ==================================================== THE AMERICAS ============
IND29["GTM"] = [
 e("ICTA \u2014 Instituto de Ciencia y Tecnolog\u00eda Agr\u00edcolas",
   "https://icta.gob.gt/",
   "Guatemala sits inside the centre of origin for maize, where wild relatives and thousands of local varieties still grow. Gene flow from an engineered crop into that diversity is a different question from gene flow in a field in Iowa, and this is the institute that holds the collections and would have to answer it.",
   ["seed:germplasm", "food_crops"], base=BODY),
]
