# -*- coding: utf-8 -*-
"""Industry entries, part 9. Weighted to the thinnest facets: human clinical,
money, open release, and contract manufacturing."""
from ind1 import e, CO, BODY, REGI, ASSN

IND9 = {}

# ===================================================== HUMAN CLINICAL =========
IND9["USA"] = [
 e("Intellia Therapeutics", "https://www.intelliatx.com/",
   "Ran the first trial anywhere in which CRISPR was delivered into the body and edited a gene in place, rather than editing cells outside the body and returning them. In-body editing removes the need for the hospital apparatus that makes cell therapies cost millions, and it also removes the step at which an edited cell could be checked before it goes back.",
   ["clinical:therapy","editing:platform"]),
 e("Sarepta Therapeutics", "https://www.sarepta.com/",
   "Sells gene therapies for Duchenne muscular dystrophy approved on accelerated pathways over the objections of some FDA reviewers, at prices above three million dollars. Patient advocacy, regulator discretion and commercial interest converged on the same decision, and the confirmatory evidence arrived after the approval rather than before it.",
   ["clinical:therapy","clinical:trials"]),
 e("FDA \u2014 cellular & gene therapy approvals", "https://www.fda.gov/vaccines-blood-biologics/cellular-gene-therapy-products",
   "The US regulator’s list of approved cell and gene therapies, each with its review documents. The files record what the agency asked, what the sponsor answered, and where reviewers disagreed — which makes this the most detailed public account anywhere of how genetic medicines get cleared.",
   ["clinical:therapy","rules:regulators"], base=REGI),
 e("Alliance for Regenerative Medicine", "https://alliancerm.org/",
   "The cell and gene therapy sector’s trade association, publishing sector financing and pipeline data and lobbying on reimbursement. Its figures are the ones cited in most coverage of how large this field is, and they are compiled by the field about itself.",
   ["rules:associations","clinical:trials"], base=ASSN)]

IND9["GBR"] = [
 e("Genomics England", "https://www.genomicsengland.co.uk/",
   "The national programme that sequenced 100,000 genomes and now holds one of the largest linked genomic and health datasets in the world, publicly owned. Access is granted to researchers including commercial ones under controlled terms, so the arrangement is a working test of whether a public genomic asset can be used by industry without being handed to it.",
   ["synthesis:seq","money:public","clinical:trials"], base=BODY)]

IND9["CHE"] = [
 e("Roche / Genentech", "https://www.roche.com/",
   "Genentech was the first biotechnology company and is now inside Roche, which also owns one of the largest diagnostics businesses in the world. A company that sells both the test and the treatment for the same condition occupies a position competition authorities have blocked elsewhere, most recently in Illumina’s case.",
   ["clinical:therapy","cro:cdmo"])]

# ============================================================== MONEY =========
IND9["USA"] = IND9["USA"] + [
 e("Flagship Pioneering", "https://www.flagshippioneering.com/",
   "Creates companies rather than investing in them, founding businesses around a technology and then staffing and funding them — Moderna among them. A venture firm that originates its own portfolio decides which biological ideas get a company built around them, which is a different kind of influence from choosing between proposals.",
   ["money:vc","editing:synbio","seed:traits"]),
 e("USDA NIFA \u2014 grant database", "https://portal.nifa.usda.gov/lmd4/recent_awards",
   "Every US agricultural research grant, searchable by recipient, amount and subject. Public funding shapes which crops and traits get studied long before any product exists, and this is where that can be traced without asking anyone.",
   ["money:public","editing:agtech"], base=REGI)]

IND9["DEU"] = [
 e("Leaps by Bayer", "https://leaps.bayer.com/",
   "Bayer’s venture arm, funding cell therapy, agricultural biotechnology and reproductive technology across the same facets as its parent. Corporate venture money buys early sight of technologies that might otherwise reach a competitor, which is a form of consolidation that never appears in a merger filing.",
   ["money:vc","repro:clinics","seed:majors"])]

# ================================================= INSECTS, MICROBES, RELEASE =
IND9["USA"] = IND9["USA"] + [
 e("Verily \u2014 Debug programme", "https://verily.com/",
   "Automated mass-rearing and release of sterile mosquitoes, built by a technology company rather than an entomology institute. When releasing tens of millions of insects becomes a logistics problem rather than a biological one, the remaining constraint is permission — and permission systems were written when rearing capacity was the practical brake.",
   ["wild:insects","wild:microbes"]),
 e("Greenlight Biosciences", "https://www.greenlightbiosciences.com/",
   "Produces sprayed double-stranded RNA that silences a gene in a target pest, with no organism modified. No biosafety framework applies because nothing living is altered, and pesticide assumptions about dose and residue do not fit a sequence-specific mechanism. Both categories were built for something else, and the product sells while the question of which governs it stays open.",
   ["wild:microbes","editing:platform","rules:regulators"])]

IND9["BRA"] = [
 e("Oxitec do Brasil", "https://www.oxitec.com/en/brazil",
   "The Brazilian operation releasing engineered mosquitoes, where researchers later found the engineered lineage had introgressed into the wild population at Jacobina — which the company had said would not happen. The finding came from independent scientists, not from any monitoring programme attached to the release.",
   ["wild:insects","rules:regulators"])]

# ============================================= CONTRACT & MANUFACTURING =======
IND9["IRL"] = [
 e("WuXi Biologics Ireland", "https://www.wuxibiologics.com/",
   "A large biologics manufacturing site built in Ireland by a Chinese contract manufacturer. Where genetic medicines can be made determines who can get them, and that capacity is being sited according to tax, regulation and geopolitics rather than where patients are.",
   ["cro:cdmo","clinical:vectors"])]

IND9["SGP"] = [
 e("Lonza Singapore / biologics cluster", "https://www.edb.gov.sg/en/our-industries/pharmaceuticals-and-biotechnology.html",
   "Part of Singapore's deliberate build-out of biologics manufacturing, alongside the tax and land policy that brought it there. A state can acquire an industry this way in a decade, and the resulting capacity means therapies approved elsewhere are physically made in a country with no say in whether they were approved.",
   ["cro:cdmo","money:public"], base=BODY)]

# ================================================= LABORATORY ANIMALS =========
IND9["CHN"] = [
 e("Shanghai Model Organisms Center", "https://www.modelorg.com/",
   "A Chinese supplier of engineered mice and rats, serving a research system whose scale now rivals the American one. China publishes no national count of animals used in research, so the size of the practice is inferred from suppliers rather than reported.",
   ["animals:services","animals:breeders"])]

# ======================================================== ASSISTED REPRO ======
IND9["CHN"] = IND9["CHN"] + [
 e("Chinese assisted reproduction sector \u2014 NHC licensing", "http://www.nhc.gov.cn/",
   "China licenses fertility clinics centrally and prohibits several practices permitted elsewhere, including commercial surrogacy. It is also where He Jiankui produced the first gene-edited babies in 2018, and the response — a prison sentence and a tightened law — remains the only criminal enforcement of a germline prohibition anywhere.",
   ["repro:clinics","clinical:germline","rules:regulators"], base=REGI)]

# =========================================================== NEW COUNTRIES ====
IND9["MYS"] = [
 e("National Biosafety Board Malaysia", "https://www.biosafety.gov.my/",
   "Malaysia’s biosafety regulator, which approved the release of engineered mosquitoes and requires public consultation on release applications. Its consultation records are published, which makes it one of the few places the public part of a release decision can be examined afterwards.",
   ["rules:regulators","editing:synbio"], base=REGI)]

IND9["PER"] = [
 e("Ministerio del Ambiente \u2014 moratoria GMO", "https://www.gob.pe/minam",
   "Peru extended its moratorium on engineered crops to 2035, explicitly to protect a centre of origin for potatoes and other crops. It is the longest such moratorium anywhere and the clearest case of a country treating crop diversity as the thing being protected rather than as an obstacle.",
   ["rules:regulators","seed:germplasm"], base=REGI)]

IND9["AUT"] = [
 e("AGES \u2014 Austrian Agency for Health and Food Safety", "https://www.ages.at/en/",
   "Austria’s food and health agency, in a country that has been among the most consistently opposed to engineered crops in Europe and whose provinces have declared themselves GMO-free. Austria has used EU safeguard clauses to block specific approvals more often than any other member state.",
   ["rules:regulators","rules:standards"], base=REGI)]

IND9["CZE"] = [
 e("Ministry of the Environment \u2014 GMO register", "https://www.mzp.cz/",
   "The Czech Republic’s GMO register, in a country that grew engineered maize and then stopped as the area collapsed to nothing. The register documents both the adoption and the abandonment, which few national records do.",
   ["rules:regulators","seed:distribution"], base=REGI)]
