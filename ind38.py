# -*- coding: utf-8 -*-
"""Industry entries, part 38. Six empty subjects, all of them downstream.

Probed and found with nothing: consumer genetics, forensic DNA, antimicrobial
resistance, religious rulings, mass-tort litigation, and the communications
industry.

What they have in common is that none of them makes an organism. They decide
what happens to the results - who reads a genome, who is identified by one, what
counts as permitted food, who pays after harm, and what the public is told. A
map that holds only the laboratories describes the supply and not the
consequences.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND38 = {}

# ================================================= CONSUMER GENETICS ==========
IND38["USA"] = [
 e("23andMe",
   "https://www.23andme.com/",
   "Sold genetic testing direct to customers and built a database of around fifteen "
   "million genomes, then filed for bankruptcy in 2025 with that database as an "
   "asset in the sale. Several US states told customers to delete their data. The "
   "case established what happens to a population\u2019s genomes when the company "
   "holding them fails: they are property.",
   ["synthesis:seq", "repro:screening", "money:markets"]),
 e("Ancestry",
   "https://www.ancestry.com/",
   "Holds more consumer genetic profiles than any other company. Its matching "
   "service is how most people discover unrecorded parentage and undisclosed donor "
   "conception, which makes a commercial genealogy product the main practical "
   "check on anonymity promised by fertility clinics decades ago.",
   ["synthesis:seq", "repro:banks"]),
]

# ===================================================== FORENSIC DNA ===========
IND38["USA"] += [
 e("Parabon NanoLabs",
   "https://parabon-nanolabs.com/",
   "Sells forensic genetic genealogy and DNA phenotyping to police forces, "
   "predicting appearance and ancestry from crime-scene samples and matching them "
   "against consumer genealogy databases. It is the route by which a genome "
   "uploaded for family history becomes a police tool, without the person who "
   "uploaded it being a suspect in anything.",
   ["synthesis:seq", "rules:influence"]),
 e("FBI \u2014 CODIS",
   "https://www.fbi.gov/how-we-can-help-you/dna-fingerprint-act-of-2005-expungement-policy/codis-and-ndis-fact-sheet",
   "The US national DNA index, holding profiles from over twenty million people. "
   "Arrestee collection in many states means inclusion does not require conviction. "
   "The infrastructure for reading human genomes at population scale was built for "
   "law enforcement long before medicine had a use for it.",
   ["rules:regulators", "synthesis:seq"], base=BODY),
]

# ========================================== ANTIMICROBIAL RESISTANCE ==========
IND38["CHE"] = [
 e("WHO \u2014 antimicrobial resistance surveillance",
   "https://www.who.int/health-topics/antimicrobial-resistance",
   "Tracks resistant infections, now associated with over a million deaths a year. "
   "Resistance is what makes engineered alternatives \u2014 phages, engineered "
   "probiotics, novel antibiotics from engineered microbes \u2014 fundable at all, "
   "and it is also driven by antibiotic use in engineered-feed livestock systems. "
   "The same industry is on both sides of the problem.",
   ["wild:microbes", "rules:standards", "livestock:livestock"], base=BODY),
]


# ===================================================== RELIGIOUS RULINGS ======
IND38["MYS"] = [
 e("JAKIM \u2014 Malaysian halal certification",
   "https://www.halal.gov.my/",
   "Certifies halal status for food sold to around two billion people, and its "
   "rulings cover enzymes, gelatine and cultured products made with engineered "
   "organisms. Whether a protein made by a modified microbe carries the origin of "
   "the gene it came from is a question no food regulator answers and this one "
   "must.",
   ["rules:standards", "editing:synbio"], base=BODY),
]

IND38["ISR"] = [
 e("Chief Rabbinate \u2014 kashrut and cultivated meat",
   "https://www.gov.il/en/departments/the_chief_rabbinate_of_israel",
   "Ruled on whether cultivated meat grown from animal cells is meat, dairy or "
   "neither \u2014 a question with no precedent, in the country where cultivated "
   "meat was approved earliest. Religious authorities are making category decisions "
   "about engineered products before any secular regulator has settled the same "
   "question.",
   ["rules:standards", "editing:agtech"], base=BODY),
]

# ========================================================== LITIGATION ========
IND38["USA"] += [
 e("Bayer \u2014 Roundup litigation and reserves",
   "https://www.bayer.com/en/investors/glyphosate-litigation",
   "Has set aside and paid many billions over glyphosate claims since acquiring "
   "Monsanto, in the largest mass tort attached to an agricultural product. The "
   "herbicide is what herbicide-tolerant engineered crops are grown to be sprayed "
   "with, so the liability landed on the trait business through the chemistry it "
   "was designed around.",
   ["rules:ip", "money:markets", "seed:majors"], base=REGI),
 e("Baum Hedlund and the glyphosate plaintiffs\u2019 bar",
   "https://www.baumhedlundlaw.com/",
   "The plaintiffs\u2019 firms that brought the glyphosate cases and won the first "
   "verdicts. Litigation of this kind is the only mechanism that has extracted "
   "money from this industry at scale, and it runs on contingency fees rather than "
   "on any regulator\u2019s finding.",
   ["rules:influence", "rules:ip"]),
]

# ========================================================= COMMUNICATIONS =====
