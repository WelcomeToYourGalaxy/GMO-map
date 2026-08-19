# -*- coding: utf-8 -*-
"""Industry entries, part 61. The contract, not the law.

Guide 3 now sends readers to buyers, insurers and contracts. These are the
entries behind that, and they share a feature worth naming: each is a term
somebody signs, and a term binds the moment it is signed. No regulator has to
agree, no window has to be open, and nothing has to be proved.

  Grower contracts     what a farmer signs away, usually without reading it
  Retail sourcing      where a supermarket's specification is actually written
  Farm lease terms     the landowner's veto over what happens on their ground
  Agricultural lenders the condition attached to the money

The one asymmetry to keep in view: three of these bind the farmer and one is
the farmer's own lever. Contract farming terms are the least visible thing in
this field and the most binding on the person with the least room to argue.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND61 = {}

# ================================================= WHAT A GROWER SIGNS =======
IND61["USA"] = [
 e("Agricultural lenders \u2014 conditions on the loan",
   "https://www.farmcreditnetwork.com/",
   "Most cropping is financed, and a lender can require particular practices as a "
   "condition of credit \u2014 including which crops, which insurance, and "
   "increasingly which environmental standards. It is a private decision made by "
   "a credit committee, and it decides what gets planted more directly than any "
   "approval does. Farm Credit institutions in the United States are cooperatively "
   "owned by their borrowers, which means the people bound by those conditions "
   "also elect the board that sets them.",
   ["money:markets", "seed:distribution"], base=CO),
]

# ============================================== WHERE THE BUYER DECIDES ======
# ================================================ THE LANDOWNER'S VETO =======
