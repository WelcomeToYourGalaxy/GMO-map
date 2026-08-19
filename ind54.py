# -*- coding: utf-8 -*-
"""Industry entries, part 54. Two routes the three guides do not cover.

Probing the 736 entries against the citizen-avenue set left two gaps, and both
pass the test the others were held to: an ordinary person can use them, and
each has produced something.

BEEKEEPERS. The one group with a recognised legal interest in what is planted
several kilometres from land they do not own, because their bees go there. That
is a standing almost nobody else has, and it has been used.

THE LOCAL COUNCIL. Guide 1 sends a reader to a national register and Guide 2 to
a state inspector. Between them sits the body that meets monthly, takes public
comment as a matter of course, and in several documented cases has been the
level at which cultivation was actually stopped.

Freedom of information was probed and left out on purpose: it is real and it is
slow, and these guides are about what can be done while something is still
happening.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND54 = {}

# ================================================== BEEKEEPERS ===============
IND54["DEU"] = [
 e("Beekeepers \u2014 the Bablok ruling and pollen in honey",
   "https://curia.europa.eu/",
   "A Bavarian beekeeper found engineered maize pollen in his honey from a trial "
   "planted several kilometres away, and in 2011 the European Court of Justice "
   "held that the honey could not be sold without authorisation covering it. It is "
   "the clearest legal recognition anywhere that a person can be harmed by a "
   "release on land they neither own nor farm. Beekeepers consequently have "
   "standing in consultations that neighbours often lack, and a hive is also a "
   "sampling device: pollen collected from a colony records what was flowering "
   "within a few kilometres, which no single field visit can.",
   ["rules:influence", "wild:drives", "rules:regulators"], base=REGI),
]

IND54["USA"] = [
 e("Beekeeping associations \u2014 registered hive locations",
   "https://www.abfnet.org/",
   "Most jurisdictions ask beekeepers to register hive locations, and applicators "
   "are often required to check that register and give notice before spraying. "
   "That makes a registered hive one of very few things a private person can put "
   "on a public record that a grower is obliged to work around \u2014 and an "
   "unregistered one has no such effect, which is the practical point.",
   ["rules:associations", "rules:regulators"], base=ASSN),
]

# ============================================ THE LOCAL COUNCIL ==============
