# -*- coding: utf-8 -*-
"""Industry entries, part 66. The other permissions a release needs.

A biosafety approval is not the only permission an environmental release
requires, and the others are frequently easier to reach. Each of these is a
separate consent, granted by a different body, under a law written for a
different purpose \u2014 and any one of them can stop a release that biosafety
law would allow.

  Wildlife agencies      permit what may be put into a wild population
  Endangered species     a mandatory consultation with a hard trigger
  Tribal consultation    a required step with its own standing
  Transboundary notice   the neighbouring country's right to be told

The practical point running through all four: a person objecting on biosafety
grounds is arguing against a scientific assessment. A person objecting on
endangered species or heritage grounds is invoking a duty the agency already
has, which is a much shorter argument.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND66 = {}

# ================================================ WILDLIFE PERMITS ===========
IND66["USA"] = [
 e("Fish and Wildlife Service \u2014 permits for releases into wild populations",
   "https://www.fws.gov/service/permits",
   "Putting an animal into a wild population needs a permit from the wildlife "
   "agency, separate from anything a biosafety regulator says. That covers "
   "engineered insects intended to suppress a wild population, and anything "
   "proposed for conservation \u2014 an engineered chestnut, a resistant ferret, a "
   "drive against island predators. The agency\u2019s question is about the wild "
   "population rather than about the technology, and it is a question local "
   "knowledge can answer.",
   ["wild:drives", "deextinct:rescue", "rules:regulators"], base=BODY),
]

# ============================================== ACROSS THE BORDER ============
