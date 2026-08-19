# -*- coding: utf-8 -*-
"""Industry entries, part 62. What a grower switches to.

Every route so far tells somebody how to object, complain or refuse. None of
them answers the question a farmer actually asks, which is what they plant
instead \u2014 and a declaration nobody can farm under does not hold.

Four things stand between a grower and that switch, and each has an answer
somewhere on this map now:

  Where does non-engineered seed come from?   independent breeders and OSSI
  Who cleans and stores it?                   the seed conditioner
  Whose varieties are they, if not a major's? public and participatory breeding
  How do I know they yield?                   independent variety trials

The last is the one that decides it. A grower will not switch on principle;
they will switch on a yield figure from somebody who did not sell them the
seed.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND62 = {}

# ================================================ SEED THAT IS NOT OWNED =====
IND62["USA"] = [
 e("Open Source Seed Initiative",
   "https://osseeds.org/",
   "Releases varieties under a pledge that they and anything bred from them stay "
   "free to use, save and breed with \u2014 the seed equivalent of an open source "
   "licence, and the direct counter to the technology agreement a patented seed "
   "comes with. Several hundred varieties are released this way. It is small "
   "against the commercial seed market and it is the only mechanism that puts a "
   "variety permanently beyond enclosure rather than merely outside it for now.",
   ["seed:germplasm", "rules:ip", "seed:distribution"], base=ASSN),
]

# ============================================= BREEDING SOMEBODY ELSE DOES ===
# ================================================ AGROECOLOGY ================
IND62["ITA"] = [
 e("FAO agroecology programme",
   "https://www.fao.org/agroecology/en/",
   "The UN food agency\u2019s work on farming systems built around biological "
   "processes rather than purchased inputs. Its relevance here is narrow and "
   "real: most engineered traits exist to make an input work better, so a system "
   "that uses fewer inputs has less use for them. It is the only body at that "
   "level treating this as an agronomic question rather than a regulatory one.",
   ["seed:germplasm", "money:public", "rules:standards"], base=BODY),
]
