# -*- coding: utf-8 -*-
"""Industry entries, part 53. Where an application is announced.

Guide 3 says the consultation window is the one point at which an objection has
to be answered, and that almost nobody hears about an application in time. These
are the places notice actually appears, so that sentence has somewhere to send
a reader.

Each says how long the window is where that is published, and each says what it
cannot do \u2014 because a comment filed in the wrong venue, or after the
deadline, does not have to be read at all.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND53 = {}

# =============================================== WHERE NOTICE APPEARS ========
IND53["USA"] = [
 e("Federal Register \u2014 biotechnology notices and comment periods",
   "https://www.federalregister.gov/",
   "Where US petitions for deregulation, permit notices and environmental "
   "assessments are announced, with a comment period usually of thirty to sixty "
   "days. Comments filed inside it are part of the record and the agency must "
   "address them; comments after it are correspondence. It offers email alerts "
   "filtered by subject, which is the practical answer to the fact that thirty "
   "days is short if you hear on day twenty-eight.",
   ["rules:regulators", "rules:standards"], base=BODY),
 e("Regulations.gov \u2014 filing a comment and reading the response",
   "https://www.regulations.gov/",
   "The portal where a US comment is actually submitted, and where every other "
   "comment on the same docket can be read. That second part is the useful one: "
   "the agency\u2019s response to comments is published here, so it is possible to "
   "see whether a point landed and how it was answered. Cite the docket number in "
   "the first line.",
   ["rules:regulators", "rules:influence"], base=BODY),
]

IND53["ITA"] = [
 e("EFSA \u2014 public consultations on GMO applications",
   "https://www.efsa.europa.eu/en/consultations",
   "Every European assessment is published in full, with the panel\u2019s "
   "reasoning, and opened for comment, typically for thirty days. It is the most "
   "detailed public record of regulatory assessment anywhere, which also makes it "
   "the easiest to comment on usefully: the document states what was assessed, so "
   "a comment can address what was not.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

IND53["AUS"] = [
 e("OGTR \u2014 consultation on licence applications",
   "https://www.ogtr.gov.au/",
   "Publishes each application, the risk assessment and risk management plan, and "
   "the proposed field sites, which few regulators publish before a decision, then invites "
   "comment for around thirty days. Knowing the sites before the decision is what "
   "makes a local objection possible at all, and few regulators provide it at "
   "that stage \u2014 though EU member states do publish trial locations under "
   "the deliberate release directive.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

IND53["CAN"] = [
 e("Biosafety Clearing-House \u2014 decisions and consultations",
   "https://bch.cbd.int/",
   "Every party to the Cartagena Protocol must file its decisions here, and for "
   "most first imports intended for release a public consultation is required "
   "before that decision is taken. For countries with no national notice venue of "
   "their own, this is the only place an application becomes visible in advance. "
   "It is also where to check what a neighbouring country has decided about the "
   "same organism.",
   ["rules:regulators", "rules:standards"], base=BODY),
]

# ========================================== WHEN THERE IS NO WINDOW ==========
