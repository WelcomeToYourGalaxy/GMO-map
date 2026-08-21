# -*- coding: utf-8 -*-
"""Industry entries, part 72. Three gaps found by probing rather than assuming.

I said there was nothing left worth adding. That was an assertion, not a check,
and probing the 773 entries against forty categories found three real absences.

  Plant variety offices    who grants the right that decides what a farmer may
                           do with a harvest - and there was no office for it
                           on a map that repeatedly says seed law is where this
                           industry meets most of the world's farmers
  Crop Trust               who pays for the genebanks the map already names
  Science advice bodies    who a government asks before deciding, which is a
                           different question from who assesses the dossier

The pattern in what was missing: institutions that decide the FRAME rather than
a case. Easy to overlook, and the map's own text keeps pointing at them.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND72 = {}

# ============================================ WHO GRANTS THE RIGHT ===========
IND72["FRA"] = [
 e("Community Plant Variety Office (CPVO)",
   "https://cpvo.europa.eu/",
   "Grants a single plant variety right valid across the whole European Union, "
   "and holds the register of them. A right granted here reaches 27 countries "
   "at once, which makes it the most concentrated seed-ownership decision "
   "anywhere: one office, one application, and what a farmer in any member state "
   "may do with a harvest changes. Its register is public and searchable by "
   "species, which is how to find out who owns a variety being grown near you.",
   ["rules:ip", "seed:germplasm", "rules:regulators"], base=BODY),
]

IND72["CHE"] = [
 e("UPOV \u2014 the office behind the convention",
   "https://www.upov.int/portal/index.html.en",
   "Administers the plant variety convention that 80 members and 99 countries "
   "are bound by, and advises governments drafting national seed laws \u2014 which "
   "is the quieter and more consequential half of what it does. A country "
   "acceding to the 1991 act typically works from UPOV's own model provisions, "
   "so the text that criminalises seed exchange in one country is recognisably "
   "the text used in another.",
   ["rules:ip", "rules:standards", "seed:germplasm"], base=BODY),
]

IND72["USA"] = [
 e("USDA Plant Variety Protection Office",
   "https://www.ams.usda.gov/services/plant-variety-protection",
   "Grants US plant variety certificates, which sit alongside utility patents on "
   "the same crops \u2014 and the two carry different rules. A variety certificate "
   "preserves a farmer's right to save seed for their own use; a utility patent "
   "does not, which is what Bowman v. Monsanto turned on. Which instrument "
   "covers a variety therefore decides what a grower may lawfully do, and the "
   "register says which.",
   ["rules:ip", "seed:germplasm", "rules:regulators"], base=BODY),
]

# ============================================ WHO PAYS FOR THE SEED ==========
IND72["DEU"] = [
 e("Crop Trust",
   "https://www.croptrust.org/",
   "An endowment that funds the world's crop collections in perpetuity, "
   "including the Svalbard vault and the CGIAR genebanks. It exists because "
   "genebanks are funded in three-year grants and seed collections die in the "
   "gaps: a collection missed for one regeneration cycle is lost, and cannot be "
   "reconstituted from anywhere. It is the answer to who pays for the material "
   "every argument on this map about landraces and wild relatives depends on.",
   ["seed:germplasm", "money:philanthropy", "rules:associations"], base=ASSN),
]

# ============================================ WHO GOVERNMENTS ASK ============
IND72["GBR"] = [
 e("National academies of science \u2014 advice to governments",
   "https://royalsociety.org/",
   "Academies are asked by governments for a position before a law is drafted, "
   "which is earlier and less visible than the regulatory assessment of any "
   "single application. Their reports are published and their working groups "
   "are named, so it is possible to see who advised and on what basis \u2014 and "
   "several national academies have taken positions on gene editing that their "
   "own regulators had not yet reached.",
   ["rules:influence", "rules:standards", "rules:associations"], base=ASSN),
]

IND72["BEL"] = [
 e("EU Group of Chief Scientific Advisors",
   "https://research-and-innovation.ec.europa.eu/strategy/support-policy-making/scientific-support-eu-policies/group-chief-scientific-advisors_en",
   "Advises the European Commission before a proposal is written. Its 2018 "
   "opinion on new genomic techniques, published after the Court held that "
   "editing falls under the GMO directive, is the document the Commission's "
   "subsequent legislative proposal rests on. Reading it explains where that "
   "proposal came from better than the proposal does.",
   ["rules:influence", "rules:standards", "editing:agtech"], base=BODY),
]
