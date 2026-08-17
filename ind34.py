# -*- coding: utf-8 -*-
"""Industry entries, part 34. Large players still absent.

Selected on influence rather than on geography. Three groups: the seed and
chemistry firms whose holdings sit behind names already here, the diagnostics
and vaccine manufacturers that use engineered organisms at the largest scale of
anyone, and the public research bodies that fund more of this work than any
company does.

The pattern in the previous three parts is worth stating, because it is the
useful finding: nearly every firm I expected to be missing was already present.
What is actually thin is the layer BEHIND the familiar names - the licensors,
the fund managers, the state programmes - and organisations whose engineered
work is real but not what they are known for.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND34 = {}

# ================================================ VACCINES & BIOLOGICS ========
# The largest deliberate use of engineered organisms in human medicine, and the
# one almost nobody files under biotechnology.
IND34["GBR"] = [
 e("GSK \u2014 vaccines",
   "https://www.gsk.com/en-gb/products/our-vaccines/",
   "Produces vaccines using recombinant antigens grown in engineered yeast and "
   "cell lines, at doses counted in the hundreds of millions a year. Recombinant "
   "hepatitis B vaccine, licensed in 1986, was among the first engineered products "
   "given to healthy people, and it set the precedent that this technology is "
   "acceptable when the alternative is a disease.",
   ["clinical:therapy", "cro:cdmo", "editing:synbio"]),
]

IND34["FRA"] = [
 e("Sanofi \u2014 recombinant vaccines and insulin",
   "https://www.sanofi.com/",
   "Makes recombinant influenza vaccine in insect cells and insulin in engineered "
   "bacteria. Insulin is the oldest engineered consumer product there is, approved "
   "in 1982, and it remains the example most often used to argue that this "
   "technology has a fifty-year safety record.",
   ["clinical:therapy", "editing:synbio", "cro:cdmo"]),
]

IND34["USA"] = [
 e("Pfizer \u2014 biologics and gene therapy",
   "https://www.pfizer.com/",
   "Runs gene-therapy programmes for haemophilia and Duchenne muscular dystrophy "
   "alongside its vaccine business, and manufactures viral vectors in-house. A "
   "company of this size entering gene therapy changes what the field costs to "
   "enter, because trial and manufacturing capacity stop being the limit.",
   ["clinical:therapy", "clinical:vectors", "cro:cdmo"]),
 e("Danaher \u2014 Cytiva and Pall",
   "https://www.danaher.com/",
   "Owns the bioprocessing businesses that supply the bags, filters, resins and "
   "single-use systems nearly every biologic is made in. When these ran short "
   "during 2020 the constraint on global vaccine supply was not the recipe, it was "
   "the plastic. A supplier that can halt production everywhere is part of this "
   "industry whatever its own filings say.",
   ["synthesis:reagents", "cro:cdmo"]),
 e("National Institutes of Health \u2014 recombinant DNA oversight",
   "https://osp.od.nih.gov/",
   "Writes the Guidelines that govern recombinant DNA research in the United "
   "States, and through its Office of Science Policy has been the main forum for "
   "arguments about gain-of-function work and human germline editing. It is also "
   "the largest single funder of biomedical research in the world, so the same body "
   "sets the rules and pays for most of the work.",
   ["rules:regulators", "rules:standards", "money:public"], base=BODY),
]

# ======================================================= STATE PROGRAMMES =====
IND34["CHN"] = [
 e("Ministry of Agriculture and Rural Affairs \u2014 biosafety certificates",
   "http://english.moa.gov.cn/",
   "Issues the biosafety certificates without which no engineered crop may be grown "
   "in China, and has used that power as a tap: cotton and papaya approved, food "
   "crops held back for over a decade, then maize and soy released from 2019. The "
   "clearest case anywhere of approval timing being a policy instrument rather than "
   "a technical outcome.",
   ["rules:regulators", "seed:traits"], base=BODY),
]

IND34["IND"] = [
 e("Genetic Engineering Appraisal Committee",
   "https://geacindia.gov.in/",
   "India\u2019s biosafety regulator, which approved Bt brinjal in 2009 only for the "
   "environment ministry to impose an indefinite moratorium, and cleared GM mustard "
   "in 2022 into a Supreme Court challenge. Approval and permission are separate "
   "things in India in a way they are almost nowhere else.",
   ["rules:regulators"], base=BODY),
]

IND34["BRA"] = [
 e("BNDES \u2014 bioeconomy lending",
   "https://www.bndes.gov.br/wps/portal/site/home/",
   "Brazil\u2019s development bank, a large lender to agriculture, ethanol and "
   "industrial biotechnology. State credit rather than venture capital is what "
   "built the engineered-crop economy in Brazil, and it does not appear in any "
   "count of biotechnology investment.",
   ["money:public", "money:markets"], base=BODY),
]

# ================================================= SEED AND CHEMISTRY =========
IND34["USA"] += [
 e("Land O\u2019Lakes \u2014 WinField United",
   "https://www.landolakesinc.com/",
   "A farmer-owned cooperative that is also one of the largest US distributors of "
   "seed and crop chemicals. Co-operatives sit between the trait owners and the "
   "field, and they decide which varieties a farmer is actually offered \u2014 a "
   "choke point that no approval process examines.",
   ["seed:distribution", "seed:licensees"]),
]


