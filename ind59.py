# -*- coding: utf-8 -*-
"""Industry entries, part 59. Schemes that collect what individuals find.

Guide 1 says fifty dated observations are worth more than one. Several
countries already run the machinery for exactly that, and almost nobody uses
it, because these schemes were built for pesticide poisoning and nobody
advertises them.

  Wildlife incident schemes    a dead animal is collected and tested, free
  Bee kill reporting           the incident type most likely to be investigated
  Animal facility inspections  a request that triggers a visit
  Certifier complaints         the fastest consequence available anywhere

The common feature: each takes a report from a member of the public, and each
produces a laboratory result or an inspection at public expense rather than
yours. Where such a scheme exists it is a better first call than a general
complaint line, because the response is defined in advance.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND59 = {}

# ============================================= WILDLIFE AND POLLINATORS ======
IND59["GBR"] = [
 e("Wildlife Incident Investigation Scheme",
   "https://www.hse.gov.uk/pesticides/reducing-environmental-impact/wildlife.htm",
   "Report a dead wild animal, pet or bee colony you believe was poisoned by "
   "pesticide, and the state collects the carcass and pays for the analysis. "
   "Results are published annually and feed into whether an approval is kept. It "
   "is one of very few schemes anywhere where a member of the public triggers a "
   "laboratory test at public expense rather than their own, and the reason it "
   "matters here is that herbicide-tolerant crops exist to be sprayed \u2014 the "
   "spraying is the part with a body count.",
   ["rules:regulators", "wild:drives"], base=BODY),
]

IND59["USA"] = [
 e("Bee kill incident reporting",
   "https://www.epa.gov/pollinator-protection/report-bee-kill-or-bee-kill-incident",
   "A reported bee kill is among the incident types most likely to be "
   "investigated, because the loss is visible, datable and belongs to somebody "
   "who can be identified. State agriculture departments hold registers of hive "
   "locations and can match a kill to applications nearby. For anyone trying to "
   "establish what is being sprayed in an area, a hive is both the evidence and "
   "the standing.",
   ["rules:regulators", "livestock:livestock"], base=BODY),
]

# ============================================== THE CERTIFIER ROUTE ==========
