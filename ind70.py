# -*- coding: utf-8 -*-
"""Industry entries, part 70. The cases, as their own category.

Three decisions came off the map with the mechanisms and should not have. A
court ruling is not a procedure - it is a specific, dated event with a named
subject, which is what the map holds everywhere else. StarLink and Gelsinger
are already here on that basis.

They are tagged rules:cases, a facet that did not exist, because a decision is
not a regulator and not a standard, and reading it under either loses what it
is: something that already happened, to somebody, with a result.

Between them they settle the three questions people actually ask about
liability: can I be liable for a plant I did not plant, can I be harmed by a
release on land I do not own, and can I keep seed from my own harvest.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND70 = {}

IND70["DEU"] = [
 e("Bablok v. Freistaat Bayern \u2014 pollen in honey",
   "https://curia.europa.eu/juris/liste.jsf?num=C-442/09",
   "A Bavarian beekeeper found engineered maize pollen in his honey from a trial "
   "planted several kilometres away, and in 2011 the European Court of Justice "
   "held that the honey could not lawfully be sold without an authorisation "
   "covering it. It is the clearest legal recognition anywhere that a person can "
   "be harmed by a release on land they neither own nor farm, and it gave "
   "beekeepers standing in consultations that neighbours often lack. The burden "
   "landed on the beekeeper rather than on the grower, which is the part usually "
   "left out of accounts of it.",
   ["rules:cases", "rules:ip", "wild:drives"], base=REGI),
]

IND70["CAN"] = [
 e("Monsanto v. Schmeiser \u2014 liable for a plant you did not buy",
   "https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/2147/index.do",
   "The Supreme Court of Canada held in 2004 that a farmer infringed a patent by "
   "having the patented plant in his field, whatever the route by which it "
   "arrived, though he owed no damages having gained no benefit from it. The "
   "finding that matters is the first half: presence is infringement, and how it "
   "got there does not answer the claim. Every argument about drift liability "
   "since has been conducted in the shadow of it.",
   ["rules:cases", "rules:ip", "seed:traits"], base=REGI),
]

IND70["USA"] = [
 e("Bowman v. Monsanto \u2014 planting saved seed is making a copy",
   "https://www.supremecourt.gov/opinions/12pdf/11-796_c07d.pdf",
   "The US Supreme Court held unanimously in 2013 that planting seed saved from a "
   "patented crop makes a new infringing copy rather than using a purchased one, "
   "so the usual rule that a patent is exhausted on first sale does not protect "
   "the grower. It is the decision that makes a seed patent effectively perpetual "
   "across generations of a self-replicating organism, and it is why the "
   "technology agreement a grower signs is enforceable rather than decorative.",
   ["rules:cases", "rules:ip", "seed:licensees"], base=REGI),
]
