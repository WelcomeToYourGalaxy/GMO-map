# -*- coding: utf-8 -*-
"""Industry entries, part 56. Where findings go, and two kinds of standing.

Guide 1 tells a reader that fifty dated observations are worth more than one,
and then does not say where to put them. That is the gap this closes first.

Then two forms of standing that outrank a comment period, because they are
rights rather than opportunities: free, prior and informed consent, which is a
requirement to obtain agreement rather than an invitation to object; and
protected-area management, where a manager can refuse a release on land they
are responsible for without any biosafety process at all.

Probed and left out: consumer boycotts, which are real and unmeasurable; farmer
field schools, which teach rather than decide; open-source laboratory equipment,
which is about making organisms rather than checking for them.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND56 = {}

# =========================================== WHERE FINDINGS GO ===============
IND56["USA"] = [
 e("iNaturalist \u2014 recording where a plant actually was",
   "https://www.inaturalist.org/",
   "A dated, located, photographed observation, held publicly and permanently by "
   "somebody other than you. That is what turns a volunteer plant in a ditch from "
   "a thing you saw into a record that can be cited, checked and counted with "
   "everybody else\u2019s. It cannot identify an engineered plant \u2014 nothing "
   "visual can \u2014 but it fixes the species, the place and the date, which is "
   "the part a strip test does not give you and the part a complaint needs. "
   "Photograph the plant, note the trait if you tested, and say so in the "
   "description.",
   ["wild:drives", "rules:standards"], base=ASSN),
 e("Cooperative extension and plant clinics",
   "https://www.nifa.usda.gov/about-nifa/how-we-work/extension",
   "Every US state runs an extension service with plant clinics that identify "
   "specimens, diagnose damage and answer questions, usually free or for a few "
   "dollars. They are the most underused resource in this whole field: staffed by "
   "people who know local cropping, obliged to help the public, and able to say "
   "whether damage to your plants looks like herbicide drift \u2014 which is the "
   "question most people cannot answer alone. Equivalent services exist in most "
   "countries under agriculture ministries.",
   ["rules:regulators", "seed:germplasm", "money:public"], base=BODY),
]

# ============================================== CONSENT AS A RIGHT ===========
# ============================================ PROTECTED LAND ================
# ============================================== INDEPENDENT SCIENCE =========
IND56["DEU"] = [
 e("ENSSER \u2014 independent scientific review",
   "https://ensser.org/",
   "A network of scientists who publish assessments of engineered organisms "
   "independently of applicants and regulators. Useful to a person for one "
   "specific purpose: a comment in a consultation carries further if it cites "
   "published work rather than only local observation, and this is where to look "
   "for a scientific counter-argument that has been through review. Its members "
   "have also acted as expert witnesses, which is the other place it matters.",
   ["rules:influence", "rules:associations"], base=ASSN),
]
