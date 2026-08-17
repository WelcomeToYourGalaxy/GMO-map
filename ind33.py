# -*- coding: utf-8 -*-
"""Industry entries, part 33. Large players still absent, and the thin facets.

Selected on influence. The two facets still standing on one or two entries after
part 31 - preclinical contract research and regulatory consulting - are the ones
that decide what a regulator ever sees, so they are filled first. After that,
firms large enough that leaving them out misstates who runs this industry.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND33 = {}

# ============================================ PRECLINICAL & REGULATORY ========
# One and two entries respectively. These are the businesses that design the
# study, run it, and write the submission a regulator reads.
IND33["USA"] = [
 e("Exponent \u2014 regulatory and risk consulting",
   "https://www.exponent.com/",
   "Provides the scientific analysis used in regulatory submissions and in "
   "litigation about them, for clients including agrochemical and biotechnology "
   "firms. Consulting science of this kind rarely appears in the public record even "
   "though it shapes what the record says.",
   ["cro:regulatory", "rules:influence"]),
 e("Keller and Heckman \u2014 biotechnology regulatory practice",
   "https://www.khlaw.com/",
   "One of the firms that files novel-food and biotechnology notifications on behalf "
   "of companies, in a system where a notification rather than an approval is "
   "increasingly the route to market. The lawyer who writes the notification is "
   "often the only outside party who reads it.",
   ["cro:regulatory", "rules:ip", "rules:influence"]),
]

# ===================================================== LARGE ABSENTEES ========
IND33["USA"] += [
 e("Ginkgo Bioworks \u2014 biosecurity",
   "https://www.ginkgobiosecurity.com/",
   "The biosecurity arm of a large synthetic-biology company, running pathogen "
   "monitoring at airports and in wastewater under government contract. A private "
   "firm holding both the capacity to design organisms and the contract to detect "
   "them is a concentration worth seeing on one map.",
   ["editing:synbio", "wild:microbes", "money:defence"]),
]



IND33["DEU"] = [
 e("Merck KGaA \u2014 Life Science",
   "https://www.merckgroup.com/en/products/life-science.html",
   "Supplies reagents, cell-culture media and CRISPR licences to laboratories everywhere, and holds foundational patents on CRISPR use in eukaryotic cells. That puts it on both sides of the editing business at once — selling the materials and licensing the right to use the method — which is a position no other supplier holds.",
   ["synthesis:reagents", "editing:patents", "rules:ip"]),
]

