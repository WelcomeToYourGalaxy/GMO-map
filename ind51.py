# -*- coding: utf-8 -*-
"""Industry entries, part 51. Four things a person can look something up in.

Checked the country-by-country source document against the 721 entries. Almost
everything in it is already here: of 139 linked sources, 125 are on the map and
the other 14 are the harvest feeds themselves, which are recorded as sources
rather than as organisations.

Four of those fourteen are worth an entry in their own right, because they are
not feeds this project reads \u2014 they are tools a person can use directly, and
each answers a question the map otherwise leaves them holding.

  OECD BioTrack        what the identifier written on a record actually means
  FAO GM Foods Platform which countries have approved a given organism
  GMO Free Regions      how a region declares itself, from those that did it
  EPA plant-incorporated protectants
                        the category that makes a plant a pesticide
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND51 = {}

# ============================================== LOOKING SOMETHING UP =========
IND51["FRA"] = [
 e("OECD BioTrack \u2014 unique identifier database",
   "https://biotrack.oecd.org/",
   "Where the international serial number on an engineered organism can be looked "
   "up. This map repeatedly says to write that identifier down; this is what it is "
   "for. Enter it and the database returns the organism, the applicant, the trait "
   "and which countries have ruled on it \u2014 the single string that ties a "
   "decision in one jurisdiction to the same organism in another. It only covers "
   "organisms carrying an inserted gene, because that is what the numbering system "
   "was built around, so an edited organism will not be found here and that "
   "absence is itself the answer.",
   ["rules:standards", "rules:regulators", "seed:traits"], base=BODY),
]

IND51["ITA"] = [
 e("FAO GM Foods Platform",
   "https://www.fao.org/food/food-safety-quality/gm-foods-platform/en/",
   "Countries post their food safety approvals here voluntarily, so it is the "
   "closest thing to a single place to ask whether a given engineered organism has "
   "been cleared for food anywhere. Useful in the ordinary case of wanting to know "
   "whether something in the food supply has been assessed by anyone at all. "
   "Voluntary means incomplete: an absence here means no country chose to post it, "
   "not that no country approved it.",
   ["rules:standards", "rules:regulators"], base=BODY),
]

# ============================================ DECLARING A REGION FREE ========
IND51["AUT"] = [
 e("GMO Free Regions network",
   "https://www.gmo-free-regions.org/",
   "The network of European regions that have declared themselves free of "
   "engineered cultivation, and the practical route for anywhere considering it. "
   "It holds what the regions that succeeded actually did: which legal instrument "
   "they used, what the coexistence rules require, and how the voluntary grower "
   "agreements were written. Most of the roughly 200 declarations on this map came "
   "through this network rather than through national legislation, which makes it "
   "the working example of the mechanism rather than a description of it.",
   ["rules:associations", "rules:influence", "rules:standards"], base=ASSN),
]

# ========================================= WHEN A PLANT IS A PESTICIDE =======
IND51["USA"] = [
 e("EPA \u2014 plant-incorporated protectant registrations",
   "https://www.epa.gov/regulation-biotechnology-under-tsca-and-fifra/"
   "overview-plant-incorporated-protectants",
   "A plant engineered to produce its own insecticide is regulated by the EPA as a "
   "pesticide, not by USDA as a crop \u2014 the pesticide is the plant. That is why "
   "Bt maize carries a registration number and a label with use restrictions, and "
   "why resistance management requirements are enforceable against the grower. "
   "Anyone trying to find out what a specific engineered crop is permitted to do, "
   "or what a grower is obliged to do around it, will find more here than in the "
   "release permit.",
   ["rules:regulators", "seed:traits"], base=BODY),
]
