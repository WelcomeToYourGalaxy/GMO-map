# -*- coding: utf-8 -*-
"""Industry entries, part 67. Finding out who is actually behind it.

An application arrives from a company nobody has heard of. A committee approves
it and the members are named but not their other roles. These are the free,
public lookups that answer both, and they take minutes rather than a request.

  Corporate registries        who owns the applicant, and who they file with
  Political donations         what was given, to whom, and when
  Revolving door records      who worked at the regulator before the company
  Conflict declarations       what a committee member had to disclose

None of this is investigation in any dramatic sense. It is four websites, and
the reason it belongs on a map about engineered organisms is that an
application is judged on its merits by people whose other commitments are a
matter of public record and almost never looked up.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND67 = {}

# ============================================== WHO OWNS THE APPLICANT =======
IND67["GBR"] = [
 e("Corporate registries \u2014 tracing an applicant",
   "https://find-and-update.company-information.service.gov.uk/",
   "An application often arrives from a name with no history. A corporate registry "
   "gives the directors, the registered address, the accounts and, in many "
   "countries, the ultimate owner \u2014 free, immediately, no request needed. The "
   "UK register is fully open; most European ones are; the United States files at "
   "state level, so start with the state named on the application. The useful "
   "detail is usually the shared address or the shared director rather than the "
   "ownership chain, because a subsidiary set up for one trial tends to share both "
   "with its parent.",
   ["money:markets", "rules:standards"], base=BODY),
 e("OpenCorporates \u2014 across jurisdictions at once",
   "https://opencorporates.com/",
   "The same lookup across dozens of national registers in one search, which is "
   "what you need when a company operates under different names in different "
   "countries \u2014 the normal arrangement in this industry. It is also the "
   "practical answer to a change of name, which otherwise breaks a trail "
   "entirely.",
   ["money:markets", "rules:standards"], base=ASSN),
]

# ============================================== WHO GAVE WHAT TO WHOM ========
IND67["USA"] = [
 e("Lobbying and political donation records",
   "https://www.opensecrets.org/",
   "In the United States, lobbying spending and political donations are filed "
   "quarterly and published, searchable by company and by recipient \u2014 "
   "including which specific bills were lobbied on. The EU transparency register "
   "does the equivalent for Brussels, and most national parliaments keep one. It "
   "is a lookup rather than an accusation: what it establishes is who was in the "
   "room and what they were asking for, before a rule changed.",
   ["rules:influence", "money:markets"], base=ASSN),
 e("Revolving door records",
   "https://www.opensecrets.org/revolving-door/",
   "Tracks people who moved between a regulator and the industry it regulates, in "
   "both directions, from public filings. It matters here for a specific reason: "
   "the decisions on this map are made by small committees in small fields where "
   "the people qualified to assess an application are frequently the people who "
   "have worked on one. That is not itself wrongdoing, and it is the sort of thing "
   "a reader is entitled to know before weighing an assessment.",
   ["rules:influence", "rules:regulators"], base=ASSN),
]

# =========================================== WHAT A MEMBER DECLARED ==========
IND67["ITA"] = [
 e("Declarations of interest \u2014 the people on the panel",
   "https://open.efsa.europa.eu/",
   "Every member of a scientific panel assessing an application must file a "
   "declaration of interests, and in the EU those declarations are published "
   "alongside the panel\u2019s opinion, naming past employers, funding and "
   "consultancies. Most regulators worldwide have an equivalent requirement and a "
   "good many publish it. It is the most direct answer to \u2018who decided this "
   "and what else are they involved in\u2019, and it sits one click from the "
   "assessment itself.",
   ["rules:regulators", "rules:standards", "rules:influence"], base=BODY),
]
