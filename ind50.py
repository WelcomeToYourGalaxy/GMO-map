# -*- coding: utf-8 -*-
"""Industry entries, part 50. What a person can actually do, and where.

Every entry here passed one test: can an ordinary person use it, and has it
produced something. Bodies that exist but have never acted, and rights that can
only be exercised through some other body, were left out.

TESTING FIRST, because nothing else works without it. A drift complaint with no
laboratory result is an assertion; with one it is evidence, and every
enforcement action and court case on this map rests on a test somebody paid for.

THEN COMPLAINTS, because a report to the wrong body is the commonest way an
account of harm disappears. Each entry says what that body will and will not
act on.

An honest caveat carried in the entries themselves: a single complaint rarely
stops anything. What it reliably does is create a record, and the enforcement
actions and litigation elsewhere on this map were all built on records made
that way.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND50 = {}

# ===================================================== TESTING ================
IND50["USA"] = [
 e("Genetic ID / Eurofins \u2014 public GMO testing",
   "https://www.eurofinsus.com/food-testing/",
   "Accepts samples from anyone, not only from commercial clients. A PCR test on "
   "seed, grain or leaf tissue costs on the order of a hundred to a few hundred "
   "dollars and returns whether engineered material is present and often which "
   "event it is. That result is the difference between saying a neighbour\u2019s "
   "crop reached your field and being able to show it. Ask for the event "
   "identification rather than a presence-or-absence screen: knowing WHICH trait "
   "is what ties the material to a particular seed and a particular grower.",
   ["rules:standards", "synthesis:seq", "seed:distribution"]),
 e("State seed laboratories \u2014 sample submission",
   "https://www.aosaseed.com/",
   "Most US states run an official seed testing laboratory, and the Association of "
   "Official Seed Analysts lists them. Charges are modest and a result from an "
   "official laboratory carries weight with a state agriculture department that a "
   "private test may not. If a formal complaint is intended, test here first \u2014 "
   "the enforcement body is more likely to act on a laboratory it already "
   "recognises.",
   ["rules:standards", "rules:regulators", "seed:germplasm"], base=BODY),
]

IND50["DEU"] = [
 e("Accredited GMO laboratories \u2014 European Network of GMO Laboratories",
   "https://gmo-crl.jrc.ec.europa.eu/ENGL/",
   "The EU reference network for GMO detection, which publishes the validated "
   "methods national laboratories use and lists them by country. A result from an "
   "ENGL laboratory is the standard evidence in an EU enforcement action, so this "
   "is where to start in Europe rather than a general food laboratory.",
   ["rules:standards", "rules:regulators"], base=BODY),
]

# ============================================== COMPLAINT CHANNELS ============
IND50["USA"] += [
 e("USDA APHIS \u2014 biotechnology compliance complaints",
   "https://www.aphis.usda.gov/aphis/ourfocus/biotechnology/compliance-and-inspections",
   "Takes reports that a permit holder has broken the conditions of a release: "
   "planting outside the authorised area, failing to maintain isolation distances, "
   "leaving volunteers standing after harvest. It has an inspection service and it "
   "publishes enforcement actions, so a report can end in a penalty. What it will "
   "not do is reconsider whether the release should have been approved \u2014 for "
   "that the window was the comment period. Quote the permit number; without it a "
   "report is hard to route and easy to lose.",
   ["rules:regulators"], base=BODY),
 e("EPA \u2014 pesticide misuse and drift reporting",
   "https://www.epa.gov/pesticide-incidents",
   "Herbicide drift is the commonest real-world harm attached to engineered crops, "
   "because tolerance traits exist to be sprayed. Reports go first to the state "
   "lead agency, usually the department of agriculture, which inspects and can "
   "fine; the EPA holds the national incident record. Report while the damage is "
   "fresh: symptoms fade, and residue on foliage is detectable for a limited "
   "period.",
   ["rules:regulators"], base=BODY),
 e("State departments of agriculture \u2014 the body that actually inspects",
   "https://www.nasda.org/about/member-directory/",
   "Almost every enforceable complaint about a crop in the United States is "
   "handled by a state department of agriculture rather than by a federal agency. "
   "They employ the inspectors, they can enter a field, and they issue the "
   "penalties. Sending a report to Washington first is the commonest reason an "
   "account of harm goes nowhere.",
   ["rules:regulators"], base=BODY),
 e("OSHA \u2014 pesticide exposure at work",
   "https://www.osha.gov/workers/file-complaint",
   "A worker exposed while applying or working around these chemicals can file, "
   "and the complaint can be made anonymously. Retaliation for filing is itself "
   "unlawful and separately actionable. Farmworkers have the highest exposure of "
   "anyone in this system and the least standing in any approval process, so this "
   "is one of the few routes that reaches them directly.",
   ["rules:regulators", "rules:influence"], base=BODY),
]

IND50["GBR"] = [
 e("Health and Safety Executive \u2014 GMO contained use notifications",
   "https://www.hse.gov.uk/biosafety/gmo/",
   "Holds the notifications for every laboratory in Britain working with "
   "genetically modified organisms, and investigates complaints about how that "
   "work is contained. It is one of the few places anywhere that contained "
   "laboratory use is reportable by the public at all \u2014 most countries publish "
   "nothing about it and take no reports.",
   ["rules:regulators", "wild:microbes"], base=BODY),
]

IND50["CHE"] = [
 e("Biosafety Clearing-House \u2014 national focal points",
   "https://bch.cbd.int/about/contacts",
   "Every party to the Cartagena Protocol must name a national focal point, and "
   "the list is public. That office is the correspondent for biosafety in its "
   "country: it receives notifications, it files decisions, and it is the address "
   "for a question about a release that nobody else will answer. For most of the "
   "world it is the only named biosafety contact that exists.",
   ["rules:regulators", "rules:standards"], base=BODY),
]
