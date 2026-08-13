# -*- coding: utf-8 -*-
"""Industry entries, part 25.

Continuing by influence. This batch is weighted to the places where one body or
one company sits at a chokepoint nothing else routes around: the seed treaty
almost every country signed, the two remaining broiler-adjacent breeders, the
biggest missing state actors, and the people who have to be paid before any
sequence becomes a product.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND25 = {}

# ==================================================== GOVERNANCE ==============
IND25["ITA"] = [
 e("International Treaty on Plant Genetic Resources (Plant Treaty)",
   "https://www.fao.org/plant-treaty/en/",
   "The treaty governing access to the crop diversity everyone breeds from, and the "
   "multilateral system through which a breeder can take material from a genebank in "
   "one country and use it in another. It also carries the clause recognising farmers\u2019 "
   "rights to save and exchange seed \u2014 which sits directly against what UPOV 91 "
   "requires, and countries have signed both. The contradiction is not an oversight; "
   "it is what happens when the same governments negotiate in two rooms.",
   ["rules:regulators", "rules:standards", "seed:germplasm"], base=BODY),
]

IND25["NOR"] = [
 e("Svalbard Global Seed Vault", "https://www.seedvault.no/",
   "The backup of last resort: duplicate samples from genebanks worldwide, stored in "
   "permafrost inside a mountain. It has been withdrawn from once, by Syria\u2019s ICARDA "
   "collection after the war destroyed its Aleppo store \u2014 which is the only "
   "demonstration anyone needed that the thing works and that it is needed. It holds "
   "seeds, not the living collections that maintain them, so it is insurance rather "
   "than a substitute for the genebanks this map documents.",
   ["seed:germplasm", "deextinct:biobank"], base=BODY),
]

# ================================================== SEED & GENETICS ===========
IND25["FRA"] = [
 e("Groupe Danone / dairy and ferment supply", "https://www.danone.com/",
   "One of the largest dairy and plant-based food companies in the world, and a very "
   "large buyer of the engineered cultures and enzymes that dairy processing runs on. "
   "A buyer at this scale sets what is acceptable upstream: its supplier standards "
   "reach more farms than most national rules, and they are commercial documents that "
   "nobody votes on.",
   ["livestock:livestock", "seed:distribution"]),
]

IND25["USA"] = [
 e("Corteva \u2014 Pioneer seed production network",
   "https://www.pioneer.com/us/agronomy/production.html",
   "The plants and contract growers that multiply hybrid seed before it reaches "
   "farmers. Seed production is the physical bottleneck the whole trait business rests "
   "on: a licensed trait is worth nothing until somebody has grown, dried, treated and "
   "bagged enough seed to plant a country, and the capacity to do that at scale belongs "
   "to a handful of companies.",
   ["seed:majors", "seed:distribution"]),
 e("Elanco Animal Health", "https://www.elanco.com/",
   "One of the largest animal health companies in the world, spun out of Eli Lilly. It "
   "sells the medicines that make dense livestock production possible, which puts it in "
   "the same position as the edited disease-resistance work on this map \u2014 both make the "
   "conditions survivable rather than changing them, and both are sold to the same "
   "producers.",
   ["livestock:livestock", "clinical:therapy"]),
 e("Ohio State / land-grant agricultural extension",
   "https://extension.osu.edu/",
   "The US land-grant extension system is how public agricultural research reaches "
   "farmers as advice rather than as a sales call. Its funding has fallen for decades "
   "while input companies have expanded their own agronomy services, so the advice a "
   "farmer receives now comes increasingly from whoever is selling the input. That "
   "shift is quiet, documented in budget lines, and shapes adoption more than any "
   "regulator does.",
   ["rules:regulators", "seed:distribution"], base=BODY),
 e("American Farm Bureau Federation", "https://www.fb.org/",
   "The largest US farm organisation, and a consistent supporter of agricultural "
   "biotechnology in legislative and trade fights. Farm organisations are where "
   "adoption is argued out among the people who actually plant, and their positions "
   "carry weight that no company\u2019s does \u2014 which is also why membership organisations "
   "of this size are worth lobbying.",
   ["rules:associations", "rules:influence"], base=ASSN),
]

# ================================================ STATE & FINANCE =============
IND25["IND"] = [
 e("National Seed Association of India", "https://nsai.co.in/",
   "The Indian seed industry\u2019s association, at the centre of the fight over Bt cotton "
   "trait fees after several state governments capped seed prices by law. India is one "
   "of the few places a government has directly set what a trait may be sold for, and "
   "the argument over whether that is price control or the correction of a monopoly has "
   "run for over a decade.",
   ["rules:associations", "seed:licensees"], base=ASSN),
]

IND25["BRA"] = [
 e("BNDES \u2014 Brazilian Development Bank", "https://www.bndes.gov.br/",
   "The state development bank that financed much of Brazil\u2019s agricultural expansion "
   "and its meatpacking consolidation, including the growth of JBS into the largest "
   "meat processor in the world. Public credit built the private concentration, which "
   "is a different route to the same outcome and one that rarely appears in accounts of "
   "how these companies got so large.",
   ["money:public", "money:markets"], base=BODY),
]

IND25["JPN"] = [
 e("Ajinomoto", "https://www.ajinomoto.com/",
   "Produces amino acids by microbial fermentation at industrial scale, for food, feed "
   "and pharmaceuticals. Fermentation-derived amino acids are in most animal feed "
   "worldwide and in a great deal of processed food, made by engineered microbes, and "
   "labelled nowhere \u2014 the organism is not in the product, so the rules do not reach it.",
   ["synthesis:synth", "livestock:livestock"]),
]

IND25["KOR"] = [
 e("CJ CheilJedang \u2014 fermentation and feed", "https://www.cj.co.kr/en/",
   "A major producer of fermentation-derived feed additives and food ingredients, "
   "competing directly with Ajinomoto. Two or three companies supply most of the world\u2019s "
   "fermented amino acids, which is a concentration comparable to seed and attracts none "
   "of the same attention because the product is an ingredient nobody sees.",
   ["synthesis:synth", "livestock:livestock"]),
]

IND25["CHE"] = [
 e("Firmenich / flavour and fragrance biotechnology",
   "https://www.dsm-firmenich.com/en/businesses/taste-texture-health.html",
   "Flavour compounds once extracted from plants are increasingly brewed by engineered "
   "microbes instead \u2014 vanillin being the clearest case. That displaces the farmers who "
   "grew the plant, in countries with no say in the decision, and the substitution "
   "happens inside a supply chain rather than through any policy anyone can object to.",
   ["synthesis:synth", "seed:distribution"]),
]

IND25["GBR"] = [
 e("Nuffield Farming Scholarships / farmer knowledge networks",
   "https://www.nuffieldscholar.org/",
   "Farmer-to-farmer study and exchange, independent of input suppliers. Where public "
   "extension has been cut back, networks like this are one of the few remaining routes "
   "by which a farmer hears about a practice from someone with nothing to sell them.",
   ["rules:associations", "seed:germplasm"], base=BODY),
]
