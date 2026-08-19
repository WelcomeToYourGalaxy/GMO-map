# -*- coding: utf-8 -*-
"""Industry entries, part 69. After the trial ends.

An entire phase of this subject is missing from the map, and it is the phase a
neighbour actually lives with. A field trial runs for a season or two. The
obligations attached to it run for years afterwards, and almost nobody -
including the people living beside the site - knows what they are or who holds
them.

  Post-harvest monitoring   the years of watching after the crop comes off
  Reporting an incident     the duty that exists and is almost never used
  Emergency measures        withdrawing an organism already approved
  Financial assurance       who pays if the holder is gone

The last is the gap. A permit holder can dissolve, be bought, or go bankrupt,
and in most jurisdictions no bond was ever required against the obligation. A
trial site whose holder no longer exists is nobody's responsibility, and the
map has no way to count them.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND69 = {}

# =========================================== THE YEARS AFTER THE HARVEST =====
IND69["USA"] = [
 e("Post-harvest monitoring \u2014 the obligation that outlasts the trial",
   "https://www.aphis.usda.gov/biotechnology/permits-notifications-petitions/permits",
   "A release permit does not end at harvest. It typically requires the site to be "
   "monitored for volunteers for one to several seasons afterwards, with the land "
   "left fallow or planted to something that makes volunteers visible, and the "
   "results reported. This is the part of a trial a neighbour lives beside, and it "
   "is knowable: the permit states the monitoring period, and the permit is "
   "public. If a site was cropped normally the season after a trial, that is a "
   "specific and checkable question to ask.",
   ["rules:regulators", "rules:standards"], base=BODY),
 e("Reporting an incident \u2014 the duty on the permit holder",
   "https://www.aphis.usda.gov/biotechnology/compliance-and-inspections/incident",
   "Permit conditions require the holder to notify the regulator when something "
   "goes wrong \u2014 material found outside the site, a containment failure, a "
   "mislabelled shipment \u2014 usually within days. It is self-reporting, which "
   "means it works when the holder tells and not otherwise. Most of the "
   "unauthorised releases on record were found by somebody else and reported "
   "afterwards, which is the argument for the monitoring in Guide 1 rather than an "
   "argument about anyone's honesty.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

# ============================================ TAKING SOMETHING BACK ==========
IND69["BEL"] = [
 e("Emergency measures \u2014 withdrawing an approved organism",
   "https://food.ec.europa.eu/plants/genetically-modified-organisms/gmo-authorisation_en",
   "A member state can suspend or prohibit an already-authorised organism on its "
   "territory where new information indicates a risk, and must notify the "
   "Commission with its reasons. It has been used, and the safeguard clause "
   "invoked this way is what eventually produced the EU opt-out. Two things make "
   "it hard: it needs new information rather than a change of mind, and the burden "
   "of assembling that information falls on the state invoking it \u2014 which is "
   "where independent published work matters more than correspondence.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

# ========================================== WHEN THE HOLDER IS GONE ==========
IND69["USA"] += [
 e("Financial assurance \u2014 the bond nobody required",
   "https://www.epa.gov/enforcement/financial-responsibility",
   "Mining, landfill and oil operations must post a bond so that clean-up is "
   "funded if the operator disappears. Biotechnology releases generally do not. A "
   "permit holder can be dissolved, sold or made bankrupt while the monitoring "
   "obligation still has years to run, and in most jurisdictions no money was set "
   "aside against it. Where an obligation has no funded successor it becomes "
   "nobody's, and there is no register anywhere that counts how many sites are in "
   "that position.",
   ["rules:regulators", "money:markets", "rules:standards"], base=BODY),
 e("Who inherits the obligation",
   "https://www.sec.gov/edgar/searchedgar/companysearch",
   "Companies in this field are bought, renamed and merged constantly, and the "
   "permits go with them \u2014 the obligation transfers to the successor, which is "
   "why an old trial may now be the responsibility of a company that never applied "
   "for it. Corporate filings are how that chain is traced, and it is worth "
   "tracing before writing to anybody, because a letter to a company that no "
   "longer holds the permit gets no answer and costs a season.",
   ["money:markets", "rules:regulators", "rules:ip"], base=BODY),
]
