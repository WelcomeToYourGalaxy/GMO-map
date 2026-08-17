# -*- coding: utf-8 -*-
"""Industry entries, part 32. Four facets with nothing in them.

Checked by searching every existing description rather than by eye. Each of
these is small in company count and none is small in consequence, and between
them they cover the parts of this industry that decide what CAN be made, by
whom, and who pays when it goes wrong.

SCREENING. Anyone can order DNA. Whether the company making it checks the
sequence against a list of dangerous ones is voluntary almost everywhere.

COMMUNITY BIOLOGY. Where the enhancement argument actually happens in public,
and where the equipment stopped being expensive.

WEAPONS GOVERNANCE. The Biological Weapons Convention has no verification
protocol. There is no inspectorate, no declarations anyone checks, and no
equivalent of the nuclear or chemical machinery. That absence is a fact about
this industry and it had nowhere to sit on the map.

LIABILITY. Who pays if an engineered organism causes damage, and whether anyone
will insure it.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND32 = {}

# ================================================= SYNTHESIS SCREENING ========
IND32["CHE"] = [
 e("International Biosecurity and Biosafety Initiative for Science (IBBIS)",
   "https://ibbis.bio/",
   "Set up in Geneva to give DNA synthesis companies a common way to screen orders "
   "against sequences of concern, and to check that the customer is who they say "
   "they are. It exists because screening is voluntary nearly everywhere: a company "
   "that chooses not to check is breaking no rule in most countries, and the tools "
   "to do the checking were until recently proprietary.",
   ["synthesis:synth", "rules:standards", "wild:microbes"], base=BODY),
]

IND32["USA"] = [
 e("NTI | bio",
   "https://www.nti.org/about/programs-projects/project/biosecurity-innovation-and-risk-reduction/",
   "The biosecurity arm of the Nuclear Threat Initiative, which built the Global "
   "Health Security Index and pushed for an international entity to govern gene "
   "synthesis. A nuclear-security organisation moving into biology is itself the "
   "argument: the field is being treated as a proliferation problem rather than a "
   "public-health one.",
   ["rules:influence", "rules:standards", "money:philanthropy"], base=ASSN),
]

# ==================================================== COMMUNITY BIOLOGY =======
IND32["USA"] += [
 e("The ODIN",
   "http://www.the-odin.com/",
   "Sells gene-editing kits, engineered bacteria and frog-muscle-growth injections "
   "by post, to anyone. Its founder injected himself with a CRISPR construct on a "
   "livestream in 2017. California later required such kits to carry a warning that "
   "they are not for self-administration \u2014 a law that exists because of this "
   "one shop.",
   ["editing:platform", "clinical:therapy", "synthesis:reagents"]),
 e("Genspace",
   "https://www.genspace.org/",
   "The first community biology laboratory, in Brooklyn, offering benchwork to "
   "people with no institution behind them. Community labs are where the safety "
   "argument is most visible, because they have no institutional biosafety "
   "committee to answer to and have generally built their own instead.",
   ["editing:synbio", "rules:standards"], base=ASSN),
]

# ================================================= WEAPONS GOVERNANCE =========
IND32["CHE"] += [
 e("Biological Weapons Convention \u2014 Implementation Support Unit",
   "https://disarmament.unoda.org/biological-weapons/",
   "Three staff in Geneva support the treaty banning biological weapons, signed by "
   "188 states. The Convention has no verification protocol: negotiations for one "
   "collapsed in 2001 and have not restarted. There is no inspectorate, no "
   "declaration anybody checks and no laboratory network \u2014 nothing resembling "
   "the machinery that exists for nuclear or chemical weapons. The gap is the point "
   "of this entry.",
   ["rules:regulators", "rules:standards", "money:defence"], base=BODY),
 e("Australia Group",
   "https://www.dfat.gov.au/publications/minisite/theaustraliagroupnet/site/en/index.html",
   "An informal arrangement of 43 states that harmonises export controls on "
   "pathogens, toxins and the equipment to work with them. Informal is accurate: it "
   "has no treaty and no secretariat of its own, and it is the main practical brake "
   "on where dangerous biological material can be sent.",
   ["rules:standards", "rules:influence", "money:defence"], base=BODY),
]

# ======================================================= LIABILITY ============
IND32["DEU"] = [
 e("Munich Re \u2014 agricultural and biotechnology risk",
   "https://www.munichre.com/",
   "One of the reinsurers that decides whether an engineered-organism risk is "
   "insurable at all. If nobody will write the cover, the release does not happen "
   "regardless of what a regulator permits \u2014 which makes reinsurance a control "
   "on this industry that nobody voted for and few people notice.",
   ["money:markets", "rules:influence"]),
]

IND32["USA"] += [
 e("Farm liability and the StarLink settlement",
   "https://www.epa.gov/",
   "StarLink maize was approved for animal feed and not for people, then turned up "
   "in taco shells in 2000. The recall and the settlements that followed cost "
   "hundreds of millions and are still the reference case for who pays when an "
   "engineered organism ends up where it was not approved to be: the answer was the "
   "developer, after litigation, and only that once.",
   ["rules:ip", "money:markets", "seed:traits"], base=REGI),
]
