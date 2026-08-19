# -*- coding: utf-8 -*-
"""Industry entries, part 52. Testing a person can do without a laboratory.

Guide 1 tells a reader they can test for themselves and sends them here for
the equipment. These are the entries that have to exist for that to be true.

Lateral flow strips are the same format as a pregnancy test: crush tissue in
water, dip, read one line or two. Grain elevators use them to accept or reject
a lorry in minutes, and they are sold to anyone at a few pounds each.

Every entry carries the same limit, because a person who thinks a negative
strip means no engineered crop is worse off than one who never tested. A strip
finds a PROTEIN. An edited organism usually has no novel protein, so no strip
will ever find one, and processing destroys protein so cooked food cannot be
tested this way.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND52 = {}

# ================================================ STRIP TEST SUPPLIERS =======
IND52["USA"] = [
 e("EnviroLogix \u2014 QuickStix strip tests",
   "https://www.envirologix.com/",
   "The strips most widely used at grain elevators, sold to anyone in packs of "
   "twenty-five or fifty at a few pounds each. Crush tissue or seed in water, dip "
   "the strip, read it in five to ten minutes. Strips are trait-specific: the "
   "common ones are CP4 EPSPS for glyphosate tolerance and the Bt proteins "
   "Cry1Ab, Cry1F and Cry1Ac. Combs testing several traits at once cost a little "
   "more. It finds a protein, so it cannot find a gene-edited organism, which "
   "usually has no novel protein for a strip to bind, and it will not work on "
   "cooked or refined material.",
   ["rules:standards", "seed:traits"]),
 e("Romer Labs \u2014 AgraStrip GMO tests",
   "https://www.romerlabs.com/",
   "Strip tests and the extraction kits that go with them \u2014 tubes, buffer and "
   "a grinder, so a sample is prepared the same way every time. Sold "
   "internationally, which matters because the trait to test for differs by "
   "region: what is planted in Brazil is not what is planted in Spain. Same limit "
   "as any strip: it reads a protein, in fresh tissue or whole seed only.",
   ["rules:standards", "seed:distribution"]),
 e("Agdia \u2014 ImmunoStrip field tests",
   "https://www.agdia.com/",
   "Field test strips sold mainly to growers and plant clinics, including for "
   "engineered traits. Their catalogue is the most useful of the three for "
   "someone testing a small number of samples rather than a lorry, because it "
   "sells in small quantities and prices are published rather than quoted.",
   ["rules:standards", "seed:traits"]),
]

# =========================================== WHAT TO TEST FOR, AND WHY =======
