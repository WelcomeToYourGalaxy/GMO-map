# -*- coding: utf-8 -*-
"""Industry entries, part 49. The last three from the Global BioLabs report.

Part 48 already took the networks and standards. Probing the 696 entries against
the report again leaves three, and each is a mechanism rather than a body:

  - the BWC confidence-building measures, which are the only routine declaration
    any state makes about maximum-containment work;
  - the two declared smallpox repositories, the only laboratories anywhere
    inspected by an international body;
  - Interpol's bioterrorism programme, the one part of this field whose work can
    end in an arrest.

On the report itself: it names no individual laboratory and publishes no
coordinates, and the saved interactive map carries no data at all. So the 69
BSL4 laboratories it counts remain unmappable here. That is a fact about what is
published rather than about what exists, and the entries below say so.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND49 = {}

# ================================================ BWC DECLARATIONS ============
IND49["CHE"] = [
 e("BWC confidence-building measures \u2014 annual declarations",
   "https://bwc-ecbm.unog.ch/",
   "The only routine declaration any state makes about its maximum-containment "
   "laboratories: one form asks for information on BSL4 facilities, another on "
   "national biosafety legislation. Between 2017 and 2021 only 78 to 92 of the 185 "
   "states parties submitted anything at all, and roughly a third of those made the "
   "submission public. Of the twenty countries with operating BSL4 laboratories, "
   "nine publish these reports. The declarations are voluntary in practice, "
   "unverified in principle, and they are the whole of international transparency "
   "on this subject.",
   ["rules:standards", "wild:microbes", "money:defence"], base=BODY),
 e("WHO \u2014 variola virus repository inspections",
   "https://www.who.int/groups/advisory-committee-on-variola-virus-research",
   "Smallpox exists in two declared laboratories, one in the United States and one "
   "in Russia, and the WHO inspects both every two years. They are the only "
   "laboratories anywhere subject to international inspection of this kind, agreed "
   "because the virus was eradicated and the stocks kept deliberately. Every other "
   "maximum-containment facility on Earth is inspected by its own government or by "
   "nobody \u2014 which makes two laboratories the exception that shows the shape "
   "of the rule.",
   ["wild:microbes", "rules:regulators", "rules:standards"], base=BODY),
]

# ==================================================== ENFORCEMENT =============
IND49["FRA"] = [
 e("Interpol \u2014 bioterrorism prevention programme",
   "https://www.interpol.int/en/Crimes/Terrorism/Bioterrorism",
   "Trains police and customs services on detecting the misuse of biological "
   "material and coordinates investigations across borders. It is the only body in "
   "this field whose work can end in an arrest rather than a guideline. The Global "
   "BioLabs assessment places it among the international organisations that have "
   "the resources to act and put biorisk management low on their own list of "
   "priorities, which is that report's recurring finding about every large "
   "institution in this space.",
   ["rules:regulators", "money:defence", "wild:microbes"], base=BODY),
]
