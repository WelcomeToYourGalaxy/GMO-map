# -*- coding: utf-8 -*-
"""Industry entries, part 47. Finishing the additions list.

The remaining tiers, chosen so that each stands for something the others do not:
the cultivated-meat and precision-fermentation producers being regulated, the
service sequencing providers that do the reading for everyone else, the
diagnostics tier, and the last of the livestock genetics cooperatives.

After this the audited list is worked through. What it leaves behind is a
different kind of gap - not missing subjects, but entries whose descriptions are
thinner than the thing they describe. That is the next job and it is editing
rather than adding.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND47 = {}

# ================================================ CULTIVATED MEAT =============
IND47["ISR"] = [
 e("Aleph Farms",
   "https://www.aleph-farms.com/",
   "Received the first regulatory approval anywhere for cultivated beef, in Israel "
   "in 2024, and has applied in Switzerland, the UK and Thailand. Beef matters more "
   "than chicken here: it is the meat with the largest land and methane footprint, "
   "so it is the one the environmental argument for this technology rests on.",
   ["editing:agtech", "livestock:livestock"]),
 e("Believer Meats",
   "https://believermeats.com/",
   "Building what it describes as the largest cultivated meat plant in the world, in North Carolina, having originated in Israel. Capacity rather than approval is now the constraint in this sector, and plants of this size are being built ahead of any market able to absorb them — which is either conviction or the same mistake the biofuel sector made.",
   ["editing:agtech", "livestock:livestock", "cro:cdmo"]),
]

IND47["USA"] = [
 e("Wildtype",
   "https://www.wildtypefoods.com/",
   "Cultivated salmon, cleared by the FDA in 2025. Fish sidestep two objections aimed at cultivated red meat: the environmental case is about overfishing rather than land, and the product is eaten raw in sushi, where the texture problem that defeats a cultivated steak barely arises.",
   ["editing:agtech", "livestock:aqua"]),
 e("The EVERY Company",
   "https://www.theeveryco.com/",
   "Makes egg proteins by fermenting engineered yeast, sold into food manufacturing "
   "rather than to consumers. Precision fermentation reaches people mostly as an "
   "ingredient inside something else, which is why it has grown quickly with almost "
   "none of the argument attached to engineered crops.",
   ["editing:synbio", "wild:microbes"]),
]

IND47["DEU"] = [
 e("Formo",
   "https://www.formo.bio/",
   "Produces dairy proteins by fermentation without a cow, and secured EU novel "
   "food clearance for a fungal protein product. Doing this in Germany matters "
   "because it is among the most sceptical markets for engineered food in the "
   "world, and the route taken was the novel-food one rather than the GMO one.",
   ["editing:synbio", "wild:microbes", "livestock:livestock"]),
]

IND47["FIN"] = [
 e("Onego Bio",
   "https://onegobio.com/",
   "Ferments engineered fungi to make egg white protein, with US regulatory "
   "clearance in 2025. Finland and Denmark have become a centre for this because "
   "the fermentation infrastructure was already there for industrial enzymes, which "
   "is a good illustration of how this industry grows out of the one before it.",
   ["editing:synbio", "wild:microbes"]),
]

# ============================================ SERVICE SEQUENCING ==============
IND47["CHN"] = [
 e("Novogene",
   "https://www.novogene.com/",
   "One of the highest-volume sequencing service providers in the world, reading "
   "samples sent from laboratories that do not own machines. Service sequencing "
   "means a great deal of the world's genetic data is generated in a handful of "
   "facilities in a small number of countries, whatever the sample's origin.",
   ["synthesis:seq", "cro:cro"]),
]

IND47["KOR"] = [
 e("Macrogen",
   "https://www.macrogen.com/en/",
   "A large service sequencing provider across Asia, and one of the operators "
   "behind national genome projects in the region. Regional providers are how "
   "countries without their own capacity get sequencing done, and they inherit the "
   "question of where the resulting data sits.",
   ["synthesis:seq", "cro:cro"]),
]

IND47["USA"] += [
 e("Azenta Life Sciences \u2014 GENEWIZ",
   "https://www.azenta.com/",
   "Sequencing, synthesis and biological sample storage in one company. Storage is "
   "the overlooked half: millions of samples held in commercial freezers under "
   "contracts that outlast the studies they were collected for, and nobody's rules "
   "say what happens to them at the end.",
   ["synthesis:seq", "synthesis:synth", "synthesis:repos"]),
]

# ================================================== DIAGNOSTICS ===============
IND47["USA"] += [
 e("Myriad Genetics",
   "https://myriad.com/",
   "Held patents on the BRCA1 and BRCA2 genes and charged accordingly, until the US "
   "Supreme Court ruled unanimously in 2013 that naturally occurring DNA cannot be "
   "patented. That case set the boundary of what can be owned in this field, and it "
   "was decided against this company.",
   ["repro:screening", "rules:ip", "synthesis:seq"]),
 e("GeneDx",
   "https://www.genedx.com/",
   "Sequences exomes and genomes at scale for rare disease diagnosis, largely in "
   "children. Rare disease is where sequencing has the clearest benefit and the "
   "least argument attached, and it is also how a very large paediatric genomic "
   "database gets assembled.",
   ["synthesis:seq", "repro:screening", "clinical:trials"]),
]

# ============================================== LIVESTOCK GENETICS ============
IND47["FRA"] = [
 e("Groupe Grimaud",
   "https://www.grimaud.com/",
   "The second largest multi-species animal genetics company in the world, breeding "
   "ducks, rabbits, pigeons and laboratory animals, and also owning vaccine "
   "businesses. Multi-species breeders are unusual: most of this industry "
   "specialises in one animal, and holding several means holding the genetics of "
   "entire minor sectors.",
   ["livestock:livestock", "animals:breeders", "seed:germplasm"]),
]

IND47["NLD"] = [
 e("CRV",
   "https://www.crv4all.com/",
   "A Dutch-Flemish dairy cattle breeding cooperative, farmer-owned, running "
   "genomic selection across a large share of European dairy herds. Cooperative "
   "ownership is the counter-model to the corporate genetics companies, and it "
   "produces the same concentration of genetics by a different route.",
   ["livestock:livestock", "animals:breeders"]),
]

IND47["FRA"] += [
 e("InnovaFeed",
   "https://innovafeed.com/en/",
   "Farms black soldier fly larvae at industrial scale for aquaculture and poultry "
   "feed, co-located with starch plants so it eats their by-products. Insect "
   "protein is regulated as agriculture, so selective breeding of an undomesticated "
   "species proceeds with very little oversight of any kind.",
   ["livestock:livestock", "livestock:aqua"]),
]
