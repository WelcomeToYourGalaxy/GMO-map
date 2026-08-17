# -*- coding: utf-8 -*-
"""Industry entries, part 30. Rounding out, rather than adding.

The map had 519 entries and looked complete because every facet had at least
one. Counted, it was not: contract research regulatory was a single
organisation, primates were six worldwide, pets were four. And 70% of everything
sat in North America and Europe - a map of the industry as seen from there.

So this module is chosen against the two thinnest axes at once. Facets that were
being held up by one or two entries, and the regions that a Western reading
leaves out: China, India, Brazil, Argentina, and the contract-research sector
that runs the work everyone else commissions.

Nothing here is included for balance alone. Each is on the map because a
decision is taken there about an organism, and leaving it out made the map wrong
about where this industry is.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND30 = {}

# ================================================= CONTRACT RESEARCH ==========
# cro:regulatory was ONE entry for the whole sector. These are the firms that
# actually run the studies a regulator reads, for clients who never appear in
# the filing.
IND30["USA"] = [
 e("Labcorp Early Development (Covance)",
   "https://www.labcorp.com/drug-development",
   "One of the largest contract research organisations in the world, running "
   "toxicology and safety studies on behalf of clients whose names do not appear "
   "in the resulting submission. The regulator reads the study; the public reads "
   "the sponsor. Between those two sits a company most people have never heard "
   "of, holding the animals and the data.",
   ["cro:regulatory", "cro:preclinical", "animals:services"]),
]

# ============================================================ CHINA ===========
# The largest state agricultural-biotechnology programme in the world, and it
# was thinner on this map than Belgium.
IND30["CHN"] = [
 e("GemPharmatech",
   "https://www.gempharmatech.com/en/",
   "Builds and supplies genetically modified mice at very large scale, with a "
   "catalogue of thousands of knockout strains. Founded at Nanjing University and "
   "now selling internationally, it is the clearest sign that laboratory-animal "
   "supply is no longer a mostly American business.",
   ["animals:models", "animals:breeders"]),
 e("Hunan Yuan Longping High-Tech Agriculture",
   "https://www.lpht.com.cn/",
   "Named for the rice breeder whose hybrid varieties are credited with feeding a "
   "very large share of China, and now one of the country\u2019s biggest seed "
   "companies. A reminder that the seed business in Asia grew out of public "
   "breeding programmes rather than out of chemistry companies.",
   ["seed:majors", "seed:germplasm", "seed:distribution"]),
]

# ============================================================ INDIA ===========
IND30["IND"] = [
 e("Indian Council of Agricultural Research",
   "https://icar.org.in/",
   "Runs the public crop-breeding system across a country with more farmers than "
   "any other. Most Indian varieties in the ground came from a public institute "
   "rather than a company, which is the fact most often missing from arguments "
   "about seed ownership there.",
   ["seed:germplasm", "seed:traits"], base=BODY),
 e("Indira IVF",
   "https://www.indiraivf.com/",
   "The largest fertility chain in India by cycle count, operating over a hundred "
   "centres. India registered thousands of clinics under the ART Act 2021 after "
   "decades in which the sector was effectively unregulated, and a chain this size "
   "is what that market produced in the meantime.",
   ["repro:clinics"]),
]

# ======================================================= SOUTH AMERICA ========
IND30["BRA"] = [
 e("CTNBio \u2014 Comiss\u00e3o T\u00e9cnica Nacional de Biosseguran\u00e7a",
   "http://ctnbio.mctic.gov.br/",
   "Brazil\u2019s biosafety commission, which decides what may be released. It has "
   "approved more engineered events than any regulator outside the United States, "
   "and its 2018 resolution putting most gene-edited organisms outside the "
   "registration system is the carve-out this map records for Brazil.",
   ["rules:regulators"], base=BODY),
 e("Huntington Medicina Reprodutiva",
   "https://www.huntington.com.br/",
   "The largest fertility group in Brazil, with clinics in S\u00e3o Paulo, "
   "Bras\u00edlia and Campinas. It appears four times in the Latin American "
   "registry under slightly different names, which is what a chain looks like in "
   "a register that lists sites rather than owners.",
   ["repro:clinics"]),
]

# ================================================ THIN FACETS ELSEWHERE =======
IND30["GBR"] = [
 e("Human Fertilisation and Embryology Authority",
   "https://www.hfea.gov.uk/",
   "Licenses every fertility clinic and every piece of human embryo research in "
   "the United Kingdom, and publishes what it finds clinic by clinic. It is the "
   "only regulator in the world doing all three, which is why the UK is the one "
   "country where this sector can be read rather than estimated.",
   ["repro:clinics", "clinical:germline", "rules:regulators"], base=BODY),
]

IND30["KEN"] = [
 e("Kenya Agricultural and Livestock Research Organisation",
   "https://www.kalro.org/",
   "Runs the trials behind Kenya\u2019s engineered cassava and maize work, in a "
   "country that lifted a ten-year import ban on engineered crops in 2022 and then "
   "faced a court challenge over it. The research and the legal fight are "
   "happening at the same time, which is the usual position across the continent "
   "and rarely the one described.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]
