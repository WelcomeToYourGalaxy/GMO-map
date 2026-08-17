# -*- coding: utf-8 -*-
"""Industry entries, part 42. The defence side.

The map already holds the plaintiffs' firms that won the glyphosate verdicts. It
held nothing on the other side, which is the larger and better-resourced half:
the defence firms, the litigation-support scientists, and the trade bodies that
run the legislative response.

This is not a symmetry exercise. Defence work is where the industry's legal
position is actually formed - the arguments about preemption, about what a
regulator's approval means in a courtroom, and about which studies count - and
those arguments have changed the law in ways no approval ever did.

Note on the rule this map applies. None of these firms makes an organism. They
are here on the same footing as regulators and funders: what they decide changes
which engineered organisms exist and reach people. A supermarket's labelling
policy does not clear that bar, and two entries that did not have been removed.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND42 = {}

# ================================================== DEFENCE LITIGATION ========
IND42["USA"] = [
 e("Hollingsworth LLP",
   "https://www.hollingsworthllp.com/",
   "A firm built around defending manufacturers in mass-tort science cases, "
   "including agrochemical and pharmaceutical claims. Its speciality is the "
   "admissibility fight \u2014 arguing which scientific evidence a jury may hear at "
   "all \u2014 which decides more cases than the trial does.",
   ["rules:ip", "rules:influence"]),
 e("Gradient \u2014 litigation science consulting",
   "https://gradientcorp.com/",
   "Produces exposure and risk assessments used by manufacturers in litigation and "
   "in regulatory comment. Consulting science of this kind is published in "
   "peer-reviewed journals and cited like any other work, and the funding "
   "relationship is disclosed in a line most readers do not reach.",
   ["cro:regulatory", "rules:influence"]),
]

# ================================================ LEGISLATIVE RESPONSE ========
IND42["USA"] += [
 e("Modern Ag Alliance",
   "https://modernagalliance.com/",
   "A coalition formed by Bayer and farm organisations to press US state "
   "legislatures for laws shielding pesticide manufacturers from failure-to-warn "
   "claims where the label matches the federal one. Bills have been introduced in "
   "more than a dozen states and passed in several since 2024. This is the industry "
   "seeking in statute what it has been losing in court.",
   ["rules:influence", "rules:associations", "seed:majors"], base=ASSN),
 e("Washington Legal Foundation",
   "https://www.wlf.org/",
   "Files briefs supporting manufacturers on preemption, expert evidence and the limits of regulatory authority, in cases including agrochemical claims. Amicus work of this kind is how a position enters the record without a party appearing to argue it, and the funders of such briefs are not always disclosed on the face of them.",
   ["rules:influence", "rules:ip"], base=ASSN),
]

# ==================================================== INTERNATIONAL ===========

IND42["CHE"] = [
 e("Sidley Austin \u2014 Geneva trade practice",
   "https://www.sidley.com/",
   "Advises on WTO disputes over agricultural biotechnology, including the case "
   "brought against the EU\u2019s approval moratorium. Trade law is the route by "
   "which one country\u2019s biosafety rules become another country\u2019s problem, "
   "and it is argued by a small number of firms.",
   ["rules:ip", "rules:influence", "rules:standards"]),
]
