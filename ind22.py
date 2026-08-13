# -*- coding: utf-8 -*-
"""Industry entries, part 22."""
from ind1 import e, CO, BODY, REGI, ASSN

IND22 = {}

# =========================================================== SEED & TRAITS ====
IND22["USA"] = [
 e("American Seed Trade Association", "https://www.betterseed.org/",
   "The US seed industry association, active on plant variety protection and seed law. Association positions are what appear in the legislative record; individual member companies are not separately identifiable in them.",
   ["rules:associations","seed:distribution","rules:ip"], base=ASSN),
 e("Seed Savers Exchange", "https://seedsavers.org/",
   "A US non-profit maintaining thousands of heirloom varieties and distributing them between members. It preserves the varieties no commercial breeder has reason to keep, which is most of what has ever been grown.",
   ["seed:germplasm","rules:ip"], base=BODY),
 e("Organic Seed Alliance", "https://seedalliance.org/",
   "Works on seed for organic systems, and on the coexistence problems that arise when engineered pollen reaches an organic crop. The organic grower carries the loss when their crop tests positive, and this organisation is where that case is documented.",
   ["seed:germplasm","seed:distribution"], base=BODY)]

# ===================================== GENE EDITING & SYNTHETIC BIOLOGY =======
IND22["USA"] = IND22["USA"] + [
 e("Scribe Therapeutics", "https://scribetx.com/",
   "Engineers CRISPR enzymes to be smaller and more precise than the natural versions. The tools are being redesigned faster than the rules describing them.",
   ["editing:platform","editing:patents","clinical:therapy"]),
 e("Tome Biosciences / large-payload integration", "https://tome.bio/",
   "Worked on inserting large DNA sequences rather than making small edits, and shut down. Large-payload integration is what would be needed to add a whole gene, and it remains the hard problem.",
   ["editing:platform","rules:regulators","clinical:therapy"]),
 e("iGEM Foundation", "https://igem.org/",
   "The international synthetic biology competition for students, which has introduced tens of thousands of young people to building organisms and runs its own safety review. It is where much of the field learned both the techniques and the norms.",
   ["editing:synbio","synthesis:repos","rules:standards"], base=BODY)]

# ============================================================= ANIMALS ========
IND22["USA"] = IND22["USA"] + [
 e("Cyagen / knockout mouse repositories \u2014 IMPC", "https://www.mousephenotype.org/",
   "The international consortium systematically knocking out every mouse gene and characterising the result. It is the most comprehensive engineered animal programme ever run, and its output is public and free.",
   ["animals:models","money:public","synthesis:repos"], base=BODY),
 e("Physicians Committee / animal testing policy", "https://www.pcrm.org/",
   "A US organisation campaigning against animal testing and for non-animal methods, which has litigated and petitioned regulators. The FDA Modernization Act permitting non-animal methods came out of this kind of pressure.",
   ["animals:models","rules:regulators","rules:associations"], base=ASSN)]

# ==================================================== LIVESTOCK & AQUACULTURE =
IND22["USA"] = IND22["USA"] + [
 e("Cargill", "https://www.cargill.com/",
   "The largest privately held company in the United States, trading grain worldwide. Its purchasing decisions determine what is worth growing, and because it is private, it discloses far less than any listed company on this map.",
   ["seed:distribution","livestock:livestock","money:markets"], trust="medium"),
 e("Archer Daniels Midland", "https://www.adm.com/",
   "One of the largest agricultural processors in the world, turning maize and soy into ingredients, feed and fuel. Processors decide what a crop is worth, and their specifications reach further than most regulations.",
   ["seed:distribution","editing:synbio","money:markets"])]

# =========================================================== HUMAN CLINICAL ===
IND22["GBR"] = [
 e("Nuffield Council on Bioethics", "https://www.nuffieldbioethics.org/",
   "A UK body producing detailed reports on bioethical questions including germline editing and farm animal welfare. Its reports are what UK policy debate is argued from, and it is independent of both government and industry.",
   ["clinical:germline","repro:screening","rules:standards"], base=BODY),
 e("UK Biobank", "https://www.ukbiobank.ac.uk/",
   "Half a million volunteers with genomic, health and lifestyle data, accessible to researchers including commercial ones. It is the largest resource of its kind assembled with explicit consent, and the terms of commercial access are the ongoing argument.",
   ["synthesis:seq","clinical:trials","money:philanthropy"], base=BODY)]

# ======================================================== ASSISTED REPRO ======
IND22["USA"] = IND22["USA"] + [
 e("Nucleus Genomics", "https://www.mynucleus.com/",
   "Sells polygenic scoring of embryos, including for traits with no single genetic cause. Professional genetics bodies say the science does not support it; embryo selection requires no approval, so it is sold anyway.",
   ["repro:screening","clinical:germline"], trust="medium"),
 e("Society for Assisted Reproductive Technology \u2014 clinic outcome reports", "https://www.sartcorsonline.com/",
   "The US fertility profession’s clinic outcome data. Success rates depend heavily on which patients a clinic accepts, so a clinic can raise its published figures by declining harder cases and the data cannot show it.",
   ["repro:clinics","rules:associations"], base=ASSN)]

# =============================================================== MONEY ========
IND22["USA"] = IND22["USA"] + [
 e("Foundation for Food & Agriculture Research", "https://foundationfar.org/",
   "A US public-private research funder created by the Farm Bill, matching federal money with private contributions. Matched funding gives private donors influence over publicly funded research priorities by design.",
   ["money:public","money:philanthropy","editing:agtech"], base=REGI)]

IND22["NOR"] = [
 e("Norwegian Government Pension Fund Global \u2014 ethics exclusions", "https://www.nbim.no/en/responsible-investment/ethical-exclusions/",
   "The world’s largest sovereign wealth fund, with an ethics council that excludes companies on defined grounds and publishes its reasoning. It is the clearest working example of an investor applying stated criteria rather than stated values.",
   ["money:markets","rules:influence"], base=REGI)]

# ================================================================ RULES =======
IND22["CHE"] = [
 e("Swiss GMO moratorium \u2014 Federal Office for the Environment", "https://www.bafu.admin.ch/bafu/en/home/topics/biotechnology.html",
   "Switzerland has extended its moratorium on GM cultivation repeatedly since 2005, by parliamentary vote each time. A temporary measure renewed for two decades is a permanent policy that nobody has had to defend as one.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND22["AUT"] = [
 e("Global 2000 / Friends of the Earth Austria", "https://www.global2000.at/",
   "The Austrian environmental organisation that has campaigned against engineered crops and pesticides, including work on glyphosate. Austrian provinces declaring themselves GMO-free happened alongside campaigning of this kind.",
   ["rules:standards","rules:influence"], base=BODY)]

IND22["NLD"] = [
 e("Wageningen University & Research", "https://www.wur.nl/en.htm",
   "The leading agricultural university in Europe, and the research anchor of the Dutch seed and food cluster. It works closely with the companies in that cluster, which is both its strength and the reason its independence is questioned.",
   ["editing:agtech","money:public","money:vc"], base=BODY)]
