# -*- coding: utf-8 -*-
"""Law firms, lobbying operations, and named individuals.

On individuals: everyone here is a public figure in a public role, and every
entry describes the role, the documented decisions attached to it, and the
structural point their position illustrates. Nothing here is about anyone's
character or private life. Where a person's conduct has been adjudicated, the
finding is cited as a finding rather than characterised.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND12 = {}

# ============================================== LAW FIRMS & LEGAL MACHINERY ===
IND12["USA"] = [
 e("Arnold & Porter \u2014 agricultural biotechnology practice", "https://www.arnoldporter.com/",
   "A law firm advising on agricultural biotechnology regulation, whose published client work and regulatory comments are part of the public record of how rules get shaped. Filings made by counsel on behalf of a company are searchable, and they say things companies do not say in their own name.",
   ["rules:regulators","rules:associations","cro:regulatory"]),
 e("Covington & Burling \u2014 food and drug regulatory", "https://www.cov.com/",
   "One of the principal firms advising food and biotechnology companies on US regulation, with lawyers moving between the firm and senior regulatory posts. The movement is documented in public appointment records, which makes it checkable rather than assumed.",
   ["rules:regulators","rules:influence","rules:associations"]),
 e("US Patent and Trademark Office \u2014 patent full-text search", "https://ppubs.uspto.gov/pubwebapp/",
   "Every US patent, searchable in full text. A patent is the most detailed public description a company ever gives of what it has actually built, because the disclosure is the price of the monopoly — which makes this the best free source on this map for what a given firm can do.",
   ["rules:ip","seed:traits"], base=REGI),
 e("Patent Trial and Appeal Board", "https://www.uspto.gov/patents/ptab",
   "Where US patents are challenged after grant, including the CRISPR interference proceedings. The filings set out each side’s evidence and the board’s reasoning, so a dispute that reshaped the licensing of a whole field is documented in full and open to read.",
   ["rules:ip","editing:patents"], base=REGI)]

IND12["DEU"] = [
 e("European Patent Office \u2014 opposition register", "https://register.epo.org/",
   "The EPO allows anyone to oppose a granted patent within nine months, and the whole file is public. Opposition has been used repeatedly against patents on conventionally bred plants, and it is the only route by which a member of the public can attack a European patent directly.",
   ["rules:ip","seed:traits"], base=REGI),
 e("No Patents on Seeds", "https://www.no-patents-on-seeds.org/",
   "A coalition that files oppositions at the European Patent Office against patents on plants and animals derived from conventional breeding. It has won revocations and narrowings, which makes it one of the few groups on this map with a documented record of changing outcomes rather than commenting on them.",
   ["rules:ip","rules:associations"], base=dict(kind="advocacy", voice="commentary", skind="ngo", type="institutional", trust="medium"))]

IND12["BEL"] = [
 e("EU Transparency Register \u2014 biotechnology lobbying", "https://ec.europa.eu/transparencyregister/public/homePage.do",
   "Declared lobbying spend, staff and meetings for organisations seeking to influence EU institutions. Bayer reports roughly €6.5 million in its own name against about €26 million in association fees, so most of the money moves under an association’s name rather than a company’s.",
   ["rules:influence","rules:associations","money:markets"], base=REGI),
 e("Euroseeds", "https://www.euroseeds.eu/",
   "The European seed industry association, coordinating the sector’s position on the new genomic techniques legislation. Association positions are what appear in the legislative record, and individual member companies are not separately identifiable in them.",
   ["rules:associations","rules:influence","seed:distribution"], base=ASSN)]

# ================================================= NAMED INDIVIDUALS ==========
# Public figures in public roles. Each entry describes the role and the decisions
# attached to it, not the person.
IND12["USA"] = IND12["USA"] + [
 e("Bayer Crop Science \u2014 divisional leadership", "https://www.bayer.com/en/agriculture/crop-science-leadership",
   "The named executives running the division, disclosed in corporate filings. Naming who decides is what makes a decision attributable at all — without it, an industry is discussed as though its choices were made by nobody.",
   ["seed:majors","rules:influence"]),
 e("Broad Institute \u2014 CRISPR inventors and the patent record", "https://www.broadinstitute.org/crispr",
   "The scientists credited on the patents the Broad prevailed with, and the institutional arrangements around them. Individual inventors are named on patents by law, so the record connecting people, institutions and licensing terms is public and complete.",
   ["editing:patents","money:public"], base=BODY),
 e("Innovative Genomics Institute \u2014 Jennifer Doudna", "https://innovativegenomics.org/",
   "The Berkeley institute founded by one of the CRISPR Nobel laureates, running work on agricultural and therapeutic editing with an explicit access mission for low-income settings. The same scientists appear on the patents, in the companies, and in the ethics debates, which is ordinary in this field and worth being able to trace.",
   ["editing:patents","clinical:therapy","money:philanthropy"], base=BODY),
 e("Colossal Biosciences \u2014 founders and scientific advisers", "https://colossal.com/team/",
   "The named founders and advisory board of the de-extinction company, several of whom hold senior academic posts. Academic credibility is part of what the company raises money on, and the affiliations are disclosed.",
   ["deextinct:ventures","money:vc","editing:platform"])]

IND12["CHN"] = [
 e("He Jiankui \u2014 the germline case and its aftermath", "https://www.nature.com/articles/d41586-019-00673-1",
   "The Chinese scientist who produced the first gene-edited babies in 2018, was imprisoned, and has since resumed publicly promoting embryo editing. The case remains the only criminal enforcement of a germline prohibition anywhere, and the fact that he is working again is part of the record.",
   ["clinical:germline","repro:screening","rules:regulators"], base=BODY, trust="high")]

# ============================================ MORE ORGANISATIONS BY FACET =====
IND12["GBR"] = [
 e("Rothamsted Research", "https://www.rothamsted.ac.uk/",
   "The oldest agricultural research station in the world, running field experiments that have continued since the 1840s and conducting engineered wheat and camelina trials. Its long-term experiments are the reference dataset against which agricultural change is measured, engineered or otherwise.",
   ["editing:agtech","money:public"], base=BODY)]

IND12["CHE"] = [
 e("Syngenta \u2014 sustainability and regulatory reporting", "https://www.syngenta.com/en/sustainability",
   "The company’s own published sustainability and regulatory disclosures. Self-reported figures are the industry’s account of itself, and having them in one place is what allows the account to be compared against independent measurement.",
   ["seed:majors","rules:influence"], trust="medium")]

IND12["FRA"] = [
 e("OECD \u2014 Working Party on Biotechnology", "https://www.oecd.org/en/topics/biotechnology.html",
   "Where national regulators harmonise consensus documents and unique identifiers for biotechnology products. Harmonisation decisions made here shape what national rules can practically diverge on, well upstream of any national debate.",
   ["rules:standards","rules:regulators"], base=REGI)]

IND12["ITA"] = [
 e("FAO \u2014 biotechnology and biosafety", "https://www.fao.org/biotech/en/",
   "The UN food agency’s biotechnology work, including capacity-building for national biosafety systems in countries without them. Which countries get a functioning regulator, and on whose model, is decided substantially through programmes like this one.",
   ["rules:regulators","money:philanthropy"], base=BODY)]
