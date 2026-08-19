# -*- coding: utf-8 -*-
"""Industry entries, part 58. The human side, from the patient's end.

Everything so far has been about land. Roughly a third of this map is not: gene
therapies, fertility clinics, embryo screening, genomic databases. A person
affected by that side has a different set of routes, and none of the previous
entries reaches them.

Four here, and the useful thing they have in common is that each is a right the
person already holds rather than a process they have to be admitted to.

  Adverse event reporting   anyone can file, including a patient
  Ethics committees         must include lay members, and take correspondence
  Data protection           a right of access and deletion over your own genome
  Being sued over seed      the one place a person is the defendant

Left out: donor-conceived registries, already on the map; hospital complaint
procedures, which vary too much to describe usefully across countries.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND58 = {}

# ============================================ REPORTING WHAT HAPPENED ========
IND58["USA"] = [
 e("FDA MedWatch \u2014 reporting an adverse event yourself",
   "https://www.fda.gov/safety/medwatch-fda-safety-information-and-adverse-event-reporting-program",
   "A patient, a relative or a carer can file a report directly, without a doctor "
   "and without permission. This matters more for gene and cell therapies than "
   "for ordinary medicines, because so few people have received any one of them: "
   "with a few hundred patients treated worldwide, a single well-described report "
   "is a measurable fraction of everything known about that product. The "
   "equivalents are the Yellow Card scheme in the UK and EudraVigilance in the "
   "EU. Reports are public in aggregate, so it is also where to look before "
   "consenting to something.",
   ["clinical:therapy", "rules:regulators"], base=BODY),
]

IND58["GBR"] = [
 e("Research ethics committees \u2014 lay membership and correspondence",
   "https://www.hra.nhs.uk/about-us/committees-and-services/res-and-recs/",
   "Every clinical trial must be approved by an ethics committee, and those "
   "committees are required to include lay members \u2014 people from outside "
   "medicine and science, appointed as members of the public. Vacancies are "
   "advertised and the role is open to anyone. A committee will also accept "
   "correspondence about a study it approved. It is the only body in the medical "
   "half of this map with a seat reserved for someone with no professional "
   "interest in the answer.",
   ["clinical:trials", "rules:regulators", "rules:standards"], base=BODY),
]

# ================================================ YOUR OWN GENOME ============
IND58["BEL"] = [
 e("Data protection authorities \u2014 rights over your own genetic data",
   "https://edpb.europa.eu/about-edpb/about-edpb/members_en",
   "Under the GDPR and comparable laws elsewhere, genetic data is a special "
   "category: you can demand a copy of what an organisation holds about you, "
   "require it to be corrected, and in most circumstances require it to be "
   "deleted \u2014 and complain to a regulator that can fine, without going to "
   "court. This is the strongest right an ordinary person has anywhere on this "
   "map, and it applies to consumer testing companies, biobanks and clinics "
   "alike. It became concrete when a company holding fifteen million genomes "
   "filed for bankruptcy and its database was listed as a saleable asset.",
   ["synthesis:seq", "repro:screening", "rules:regulators"], base=BODY),
]

# ============================================== WHEN YOU ARE SUED ============
IND58["CAN"] = [
 e("Being sued over seed \u2014 Schmeiser and Bowman",
   "https://scc-csc.lexum.com/",
   "Two decisions define what a patent on a self-replicating organism means for "
   "the person growing it. In Canada, Monsanto v. Schmeiser held in 2004 that a "
   "farmer infringed by having the patented plant in his field, whatever the "
   "route by which it arrived, though he owed no damages having gained no "
   "benefit. In the United States, Bowman v. Monsanto held in 2013 that planting "
   "saved seed is making a new copy, not using a purchased one. Together they "
   "mean a grower can be liable for a plant they did not buy and did not want. "
   "It is the one place in this whole field where an ordinary person is the "
   "defendant, and worth knowing before it happens rather than after.",
   ["rules:ip", "seed:traits", "editing:patents"], base=REGI),
]
