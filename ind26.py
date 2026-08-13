# -*- coding: utf-8 -*-
"""Industry entries, part 26.

The remaining structural gaps: the certifiers and testing bodies that decide
whether a claim can be made at all, the insurers and standards bodies that price
and define the risk, and the parts of the chain between a laboratory and a field
that nobody thinks of as part of this industry.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND26 = {}

# =============================================== CERTIFIERS & TESTING =========
IND26["USA"] = [
 e("The Non-GMO Project", "https://www.nongmoproject.org/",
   "The largest GMO-avoidance certification in North America, verifying tens of "
   "thousands of products. A private label doing what a labelling law would do, funded "
   "by the companies seeking the label \u2014 which means the standard is set by the market "
   "for it rather than by a legislature, and it covers only what its members choose to "
   "submit. It is also the reason a great deal of American food carries a GMO statement "
   "at all.",
   ["rules:standards", "seed:distribution"], base=ASSN),
 e("USDA National Organic Program", "https://www.ams.usda.gov/about-ams/programs-offices/national-organic-program",
   "Organic certification prohibits engineered organisms, which makes the organic "
   "standard the largest binding GMO restriction in American agriculture \u2014 not by law "
   "but by contract, and enforced through inspection rather than a regulator. When "
   "engineered pollen reaches an organic field the grower carries the loss, because the "
   "standard tests the product and does not ask who caused the presence.",
   ["rules:regulators", "rules:standards"], base=REGI),
 e("Genetic ID / GMO testing laboratories", "https://www.genetic-id.com/",
   "Commercial laboratories that test grain, seed and food for engineered material, for "
   "exporters, certifiers and regulators. Whether unauthorised presence can be "
   "demonstrated at all depends on somebody buying a test, at a threshold somebody "
   "chose \u2014 so detection is a purchased service, and the countries that cannot afford "
   "it are the ones that find nothing.",
   ["rules:standards", "synthesis:seq"]),
 e("Munich Re / agricultural and biotechnology risk",
   "https://www.munichre.com/en/solutions/for-industry-clients/agro.html",
   "Reinsurers price agricultural and liability risk, including for engineered crops and "
   "for the contamination claims that follow a spread event. An insurer deciding a risk "
   "is uninsurable stops a technology more completely than a regulator refusing a "
   "licence, and it does so commercially, without a hearing, and without publishing the "
   "reasoning.",
   ["money:markets", "rules:influence"]),
]

# ============================================ BETWEEN LAB AND FIELD ===========
IND26["NLD"] = [
 e("Koppert Biological Systems", "https://www.koppert.com/",
   "Sells predatory insects, mites and microbes for pest control \u2014 living organisms "
   "released deliberately into greenhouses and fields at enormous volume, none of them "
   "engineered. It is the working comparison for every engineered release argument: "
   "biological control has been done at scale for decades, with its own escape and "
   "establishment record, and almost nobody calls it a release.",
   ["wild:insects", "wild:microbes"]),
 e("Bejo / Rijk Zwaan seed testing and ISTA certification",
   "https://www.seedtest.org/",
   "The International Seed Testing Association sets the methods by which a seed lot is "
   "declared pure, viable and free of unwanted material. Those methods decide what "
   "counts as contamination in a trade dispute, so a technical committee most people "
   "have never heard of is where the threshold between clean and not is actually set.",
   ["rules:standards", "seed:germplasm"], base=ASSN),
]

IND26["CHE"] = [
 e("SGS \u2014 inspection and certification", "https://www.sgs.com/",
   "One of the largest inspection and certification companies in the world, testing and "
   "certifying agricultural cargoes at ports. A shipment is accepted or rejected on the "
   "strength of a private company\u2019s certificate, which means a commercial testing firm "
   "sits between every exporting country and every import rule on this map.",
   ["rules:standards", "seed:distribution"]),
]

IND26["DEU"] = [
 e("Bundessortenamt \u2014 variety registration",
   "https://www.bundessortenamt.de/",
   "Before a variety can be sold in the EU it must be registered as distinct, uniform "
   "and stable. Uniformity is the requirement that quietly excludes the diverse "
   "populations smallholders and organic growers prefer, so a technical seed-marketing "
   "rule written for industrial agriculture decides what may lawfully be sold, entirely "
   "separately from any biosafety question.",
   ["rules:regulators", "seed:germplasm"], base=REGI),
]

# ================================================== PUBLIC INTEREST ===========
IND26["GBR"] = [
 e("GeneWatch UK", "https://www.genewatch.org/",
   "Tracks genetic technologies and their governance, including gene drives, genetic "
   "databases and the claims made for agricultural biotechnology. Small organisations "
   "doing technical scrutiny are a tiny fraction of the money in this field, and their "
   "submissions are most of the independent expert comment that reaches regulators.",
   ["rules:influence", "rules:associations"], base=BODY),
]

IND26["FRA"] = [
 e("Confédération paysanne / farmer seed movements",
   "https://www.confederationpaysanne.fr/",
   "A French smallholder farmers\u2019 union that has fought seed marketing rules and "
   "conducted crop destructions, with members prosecuted for both. It is the sharpest "
   "European example of the seed argument being about who may lawfully grow and "
   "exchange what, rather than about whether an engineered plant is safe to eat.",
   ["rules:associations", "seed:germplasm"], base=ASSN),
]

IND26["ETH"] = [
 e("African Biodiversity Network / farmer seed systems",
   "https://africanbiodiversity.org/",
   "Works on farmer-managed seed systems across east and southern Africa, where most "
   "seed still moves through exchange rather than purchase. Every seed law reform on "
   "this continent is a decision about whether that remains lawful, and the people it "
   "affects most are the least represented in the drafting.",
   ["seed:germplasm", "rules:influence"], base=BODY),
]

IND26["IND"] = [
 e("Navdanya / seed sovereignty movement", "https://www.navdanya.org/",
   "Runs community seed banks and campaigns against seed patenting in India. It is the "
   "longest-running organised opposition to this industry anywhere, and its central "
   "claim \u2014 that seed saving is a right rather than an infringement \u2014 is the one UPOV 91 "
   "was written to settle the other way.",
   ["seed:germplasm", "rules:influence"], base=BODY),
]
