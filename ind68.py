# -*- coding: utf-8 -*-
"""Industry entries, part 68. The paper trail nobody thinks to follow.

Guide 1 tells a reader to check the register and warns that registers stop at
the state line. There are other registers, kept for other reasons, and several
are more precise about location than the biosafety one.

  EU field trial locations   published to the parcel, by law, since 2001
  Plant passports            follow consignments of plants inside the EU
  Water discharge permits    say what may be applied near water, and by whom
  Environmental assessment   longer than a biosafety file, and challengeable

The first matters most, and it corrects something this map says elsewhere.
Australia is described here as the only regulator publishing field trial sites.
For deliberate release trials the EU publishes locations too, and has since the
2001 Directive. Corrected below rather than quietly.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND68 = {}

# ============================================ LOCATIONS, PUBLISHED BY LAW ====
IND68["BEL"] = [
 e("EU deliberate release register \u2014 trial locations",
   "https://webgate.ec.europa.eu/fip/GMO_Registers/",
   "The EU directive on deliberate release requires member states to make the "
   "location of every field trial public, and the registers do \u2014 in several "
   "countries down to the municipality or the land parcel, which is more precise "
   "than the state-level information the United States publishes. Some member "
   "states publish an online map. Anyone in Europe asking whether a trial is near "
   "them has a better answer available than this map has previously suggested, "
   "and it is the national competent authority that holds it.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

# ============================================== NEAR WATER ==================
