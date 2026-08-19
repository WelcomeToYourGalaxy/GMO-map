# -*- coding: utf-8 -*-
"""Industry entries, part 60. Food rules that reach back to the field.

Four routes where a decision about food determines what may be planted, and
none of them runs through a biosafety regulator.

The strongest is the least obvious. A geographical indication \u2014 the rule
behind Champagne, Parmigiano Reggiano and several hundred lesser-known names
\u2014 specifies which varieties may be grown inside a defined boundary. It is
enforceable across the whole European Union, it is permanent, and the people
who write it are the producers in that place. It is the only mechanism on this
map where a defined area\u2019s cultivation rules are set by the growers there
and backed by trade law.

Then the feed declaration, which reaches further than any food label: most
engineered material is eaten by animals, and the label that follows it through
a cow exists in only a few countries.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND60 = {}

# ================================================ GEOGRAPHICAL NAMES ========
IND60["DEU"] = [
 e("Ohne Gentechnik \u2014 the feed declaration",
   "https://www.ohnegentechnik.org/",
   "Most engineered material is eaten by animals, and no label follows it through "
   "a cow: milk, meat and eggs from animals fed engineered soy are labelled "
   "nowhere in the world as a matter of law. This German scheme is the largest of "
   "the few private answers to that, certifying that livestock were fed without "
   "it, and it covers a substantial share of German dairy. It reaches the part of "
   "the supply chain that consumer labelling law does not touch at all, which is "
   "where most of the volume actually is.",
   ["rules:standards", "livestock:livestock", "seed:distribution"], base=ASSN),
]

# ================================================== NEAR THE GROWER =========
