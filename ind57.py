# -*- coding: utf-8 -*-
"""Industry entries, part 57. Getting paid, without a regulator.

Every route so far ends in an inspection, a comment or a refusal. None of them
compensates anybody. These four do, and three of them do not involve a
biosafety authority at all \u2014 which matters, because a regulator can fine an
operator and the money goes to the state, not to the person whose crop was
affected.

The pattern: this is ordinary property law. Drift onto land you own or rent is
the same kind of wrong as any other substance arriving where it should not,
and it is handled by the same courts, mediators and insurers that handle
everything else. No special standing is needed and no scientific dispute has
to be won \u2014 only that something arrived and it cost you.

Left out after probing: coexistence compensation funds, which exist in a small
number of European countries and are hard to describe accurately across
jurisdictions without misleading somebody about whether one covers them.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND57 = {}

# ================================================== ORDINARY COURTS ==========
IND57["USA"] = [
 e("USDA Agricultural Mediation Program",
   "https://www.farmers.gov/working-with-us/mediation",
   "Free or nearly free mediation between farmers and neighbours, lenders and "
   "agencies, funded federally and run by the states. It is faster than a court, "
   "produces a written agreement, and does not require either side to be found at "
   "fault. For a dispute between neighbouring growers \u2014 which is what most "
   "drift is \u2014 it is usually the first thing to try, because a court case "
   "between people who will farm beside each other for thirty years has costs a "
   "judgment does not settle.",
   ["rules:regulators", "rules:influence"], base=BODY),
]

# ============================================== THE BUYER'S REJECTION ========
IND57["USA"] += [
 e("Grain elevators and handlers \u2014 rejection at delivery",
   "https://www.ngfa.org/",
   "The elevator tests a load with the same strip a person can buy, and rejects "
   "it on the spot if the result is wrong for the contract. That single decision "
   "does more to enforce separation than any regulator: it happens within "
   "minutes, it costs the grower the price difference or the whole load, and "
   "there is no appeal. If your crop was rejected on a test, the rejection record "
   "is evidence of what was in it and where it came from \u2014 ask for it in "
   "writing, because it is the strongest document most growers will ever hold "
   "about their own harvest.",
   ["seed:distribution", "rules:standards", "money:markets"], base=ASSN),
 e("Trading standards and consumer protection authorities",
   "https://www.ftc.gov/",
   "Where a product is labelled non-GM, organic or free of something and is not, "
   "that is a consumer protection matter rather than a biosafety one \u2014 and "
   "the bodies that handle it are far more used to acting on a complaint from a "
   "member of the public than any agriculture department. A false claim is easier "
   "to prove than harm, and the penalties attach to the seller who made it.",
   ["rules:regulators", "rules:standards"], base=BODY),
]
