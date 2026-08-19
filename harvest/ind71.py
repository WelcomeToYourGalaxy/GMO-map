# -*- coding: utf-8 -*-
"""Industry entries, part 71. The rest of the case law.

rules:cases had three entries. These are the remaining decisions that settled
something and are still the answer, worldwide.

Chosen on one test: a later argument cannot be had without reference to it.
That excludes most litigation and includes six rulings, on three continents,
across forty-five years.

  Chakrabarty 1980        whether a living organism can be patented at all
  EC-Biotech 2006         whether caution is a trade barrier
  AMP v. Myriad 2013      whether a gene as found in nature can be owned
  Johnson v. Monsanto 2018 what a jury does with the safety evidence
  Nuziveedu 2019          whether a seed patent binds an Indian farmer
  Conf\u00e9d\u00e9ration paysanne 2018
                          whether editing counts as genetic modification
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND71 = {}

IND71["USA"] = [
 e("Diamond v. Chakrabarty \u2014 a living organism can be patented",
   "https://supreme.justia.com/cases/federal/us/447/303/",
   "The US Supreme Court held in 1980, by five to four, that an engineered "
   "bacterium was patentable subject matter: anything under the sun made by man. "
   "Everything else in this field rests on it. Without that ruling there is no "
   "seed patent, no technology agreement, no licensing estate and no reason for "
   "a company to fund the work. It is the single most consequential decision on "
   "this map and it was decided by one vote.",
   ["rules:cases", "rules:ip", "editing:patents"], base=REGI),
 e("Association for Molecular Pathology v. Myriad \u2014 a gene as found cannot be",
   "https://www.supremecourt.gov/opinions/12pdf/12-398_1b7d.pdf",
   "The US Supreme Court held unanimously in 2013 that a naturally occurring DNA "
   "sequence is a product of nature and not patentable merely because it has "
   "been isolated, while cDNA made in a laboratory remains patentable. It ended "
   "Myriad\u2019s monopoly on BRCA testing and the price that came with it, and it "
   "drew the line the whole synthetic biology industry now works against: what "
   "you find is not yours, what you build is.",
   ["rules:cases", "rules:ip", "repro:screening"], base=REGI),
 e("Johnson v. Monsanto \u2014 the first glyphosate verdict",
   "https://www.courts.ca.gov/",
   "A California jury found in 2018 that glyphosate had contributed to a school "
   "groundskeeper\u2019s cancer and that the manufacturer had failed to warn, and "
   "awarded damages later reduced on appeal. Thousands of claims followed and "
   "the reserves run to billions. Whatever one concludes about the science, the "
   "verdict is the reason herbicide-tolerance traits are now a financial "
   "exposure as well as a product, and the reason the industry is seeking "
   "statutory protection it lost in court.",
   ["rules:cases", "rules:ip", "seed:majors"], base=REGI),
]

IND71["FRA"] = [
 e("Conf\u00e9d\u00e9ration paysanne \u2014 editing is genetic modification",
   "https://curia.europa.eu/juris/liste.jsf?num=C-528/16",
   "The European Court of Justice held in 2018 that organisms produced by newer "
   "mutagenesis techniques are genetically modified organisms within the "
   "directive, and are not covered by the exemption for conventional mutagenesis. "
   "It is why edited crops are regulated in the EU and unregulated in most of the "
   "Americas, and why the Commission has since proposed legislation to reverse "
   "it. Every argument about whether editing counts refers back to this.",
   ["rules:cases", "rules:regulators", "editing:agtech"], base=REGI),
]

IND71["CHE"] = [
 e("EC \u2014 Biotech \u2014 caution as a trade barrier",
   "https://www.wto.org/english/tratop_e/dispu_e/cases_e/ds291_e.htm",
   "The United States, Canada and Argentina brought a WTO complaint against the "
   "EU\u2019s de facto moratorium on approvals, and the panel found in 2006 that "
   "the delays breached the agreement on sanitary measures. It did not rule on "
   "whether engineered crops are safe. What it established is that a slow "
   "approval process is itself actionable in trade law, which is why a country "
   "weighing a restriction is also weighing a dispute.",
   ["rules:cases", "rules:standards", "rules:ip"], base=REGI),
]

IND71["IND"] = [
 e("Monsanto v. Nuziveedu \u2014 a seed patent in India",
   "https://main.sci.gov.in/",
   "The Indian Supreme Court restored in 2019 the patent claim over Bt cotton "
   "technology that the High Court had struck down, sending the substantive "
   "question back for trial. The dispute matters beyond India because Indian law "
   "excludes plants and seeds from patentability while allowing patents on the "
   "genetic construct, and the argument over where that line falls governs "
   "whether a seed patent means anything in the country with the most cotton "
   "farmers.",
   ["rules:cases", "rules:ip", "seed:traits"], base=REGI),
]
