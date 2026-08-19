# -*- coding: utf-8 -*-
"""Industry entries, part 65. Going over the regulator's head.

Guide 2 ends by telling a reader to go up one level if nothing happens, and
does not say what is up there. Four things are, and none of them is a court.

  Ombudsman          reviews how a body treated you, not whether it was right
  Parliamentary petition and committee
                     puts a question a minister has to answer in public
  State attorney general
                     the one office that can sue on behalf of residents
  ISDS               the reason a government may say a ban is impossible

The last is included for a reason that runs against the grain of this set: it
is not a route anybody can use. It is a route used against them, and knowing it
exists explains a refusal that otherwise looks like reluctance.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND65 = {}

# ================================================ HOW YOU WERE TREATED =======
# ============================================= SOMEONE WHO CAN SUE ===========
IND65["USA"] = [
 e("State attorneys general",
   "https://www.naag.org/",
   "The one public office that can bring a case on behalf of residents rather than "
   "waiting for a resident to bring one. They have sued over pesticide labelling, "
   "consumer claims and environmental damage, and they take complaints from the "
   "public through consumer protection divisions that are used to hearing from "
   "ordinary people. Where a single person\u2019s loss is too small to litigate but "
   "the same thing happened to hundreds, this is the office that can act on the "
   "pattern.",
   ["rules:regulators", "rules:ip", "rules:influence"], base=BODY),
]

# ========================================= WHY A GOVERNMENT SAYS NO ==========
