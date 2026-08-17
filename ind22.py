# -*- coding: utf-8 -*-
"""Industry entries, part 22."""
from ind1 import e, CO, BODY, REGI, ASSN

IND22 = {}

# =========================================================== SEED & TRAITS ====
IND22["USA"] = [
 e("American Seed Trade Association", "https://www.betterseed.org/",
   "The US seed industry association, and the main lobby on plant variety protection, seed patents and state-level labelling. It is also the body that has argued consistently that edited crops should not be regulated as engineered ones — a position now written into US policy, which makes this association's advocacy one of the more consequential on the map.",
   ["rules:associations","seed:distribution","rules:ip"], base=ASSN),
 e("Seed Savers Exchange", "https://seedsavers.org/",
   "A US non-profit maintaining thousands of heirloom vegetable and grain varieties and distributing them between members. Varieties survive by being grown, not by being frozen: a seed bank preserves a sample, and a network like this preserves the plant in cultivation and the knowledge of how to grow it. It is the practical counterweight to a commercial seed market in which a variety that stops selling stops existing.",
   ["seed:germplasm","rules:ip"], base=BODY),
 e("Organic Seed Alliance", "https://seedalliance.org/",
   "Works on seed bred for organic systems, which cannot use engineered varieties and largely cannot use the treated seed the conventional market sells. Organic agriculture depends on breeding it does not control, so an entire sector's varieties come from programmes designed for a different set of inputs.",
   ["seed:germplasm","seed:distribution"], base=BODY)]

# ===================================== GENE EDITING & SYNTHETIC BIOLOGY =======
IND22["USA"] = IND22["USA"] + [
 e("Scribe Therapeutics", "https://scribetx.com/",
   "Engineers CRISPR enzymes to be smaller and more precise than the natural ones, founded by Jennifer Doudna and colleagues from the Berkeley laboratory whose patent claims lost the US interference proceedings to the Broad Institute. That outcome is part of why the company builds its own enzymes: a purpose-designed protein that is not Cas9 is not covered by the patents that were contested, so engineering around the estate is both a technical and a legal strategy. Size matters for delivery — a smaller enzyme fits inside the viral vectors used to carry it into a body, which is the practical limit on most gene therapy.",
   ["editing:platform","editing:patents","clinical:therapy"]),
 e("Tome Biosciences / large-payload integration", "https://tome.bio/",
   "Worked on inserting whole genes rather than making small edits, using integrase systems to place large DNA sequences at chosen sites. That capability is the line between correcting a letter and adding a function, and it is also where the carve-outs stop applying: an organism carrying an inserted gene from elsewhere is transgenic under every framework, however precisely it was placed. The company wound down in 2024, which is itself part of the record.",
   ["editing:platform","rules:regulators","clinical:therapy"]),
 e("iGEM Foundation", "https://igem.org/",
   "The international synthetic biology competition, in which student teams build engineered organisms and present them each year. It has trained a large share of the field's working scientists, maintains a registry of standard genetic parts, and runs its own safety and security review — a student competition operating biosecurity screening that most national governments do not require of anyone.",
   ["editing:synbio","synthesis:repos","rules:standards"], base=BODY)]

# ============================================================= ANIMALS ========
IND22["USA"] = IND22["USA"] + [
 e("Cyagen / knockout mouse repositories \u2014 IMPC", "https://www.mousephenotype.org/",
   "The International Mouse Phenotyping Consortium is systematically knocking out every protein-coding gene in the mouse and recording what happens, roughly twenty thousand genes across a network of centres. It is the largest deliberate programme of animal genetic modification ever undertaken, run by public institutions, and its output is a catalogue any laboratory can order from.",
   ["animals:models","money:public","synthesis:repos"], base=BODY),
 e("Physicians Committee / animal testing policy", "https://www.pcrm.org/",
   "A US organisation campaigning against animal testing on medical rather than welfare grounds, arguing that results in animals predict human responses poorly. It was among the forces behind the FDA Modernization Act of 2022, which removed the statutory requirement for animal testing before human trials — the first change to that requirement since 1938, and one that has not yet altered practice much.",
   ["animals:models","rules:regulators","rules:associations"], base=ASSN)]

# ==================================================== LIVESTOCK & AQUACULTURE =
IND22["USA"] = IND22["USA"] + [
 e("Cargill", "https://www.cargill.com/",
   "The largest privately held company in the United States, trading and processing a very large share of the world's grain, oilseed and animal feed. Being private means it discloses almost nothing: no quarterly filings, no shareholder meeting, no obligation to explain a sourcing decision. Almost every engineered commodity crop grown anywhere passes through a trader of this kind, and traders are regulated as merchants rather than as participants in biotechnology.",
   ["seed:distribution","livestock:livestock","money:markets"], trust="medium"),
 e("Archer Daniels Midland", "https://www.adm.com/",
   "One of the largest agricultural processors in the world, turning engineered maize and soy into starches, sweeteners, oils and feed, and running industrial fermentation at scale. Processing is the point where an engineered crop stops being a plant and becomes an ingredient: after it, no label follows the material, and the identity of the variety is gone from the record.",
   ["seed:distribution","editing:synbio","money:markets"])]

# =========================================================== HUMAN CLINICAL ===
IND22["GBR"] = [
 e("Nuffield Council on Bioethics", "https://www.nuffieldbioethics.org/",
   "A UK body producing detailed reports on genome editing, embryo research and farmed animals, with no statutory power at all. Its 2018 report concluding that heritable human genome editing could be ethically acceptable in some circumstances shifted the terms of a global argument, which is what a body like this does instead of regulating.",
   ["clinical:germline","repro:screening","rules:standards"], base=BODY),
 e("UK Biobank", "https://www.ukbiobank.ac.uk/",
   "Half a million volunteers with genomic, health and lifestyle data, accessible to researchers including commercial ones. It is the largest resource of its kind assembled with explicit consent, and the terms of commercial access are the ongoing argument.",
   ["synthesis:seq","clinical:trials","money:philanthropy"], base=BODY)]

# ======================================================== ASSISTED REPRO ======
IND22["USA"] = IND22["USA"] + [
 e("Nucleus Genomics", "https://www.mynucleus.com/",
   "Sells polygenic scoring of IVF embryos, including for traits with no medical meaning, and has advertised it that way. Polygenic prediction for complex traits is weak at the individual level even where the statistics are sound, and the professional bodies have said so; the service is sold anyway, because nothing prohibits it. This is embryo selection marketed as a consumer product.",
   ["repro:screening","clinical:germline"], trust="medium"),
 e("Society for Assisted Reproductive Technology \u2014 clinic outcome reports", "https://www.sartcorsonline.com/",
   "Publishes US clinic outcome data alongside the CDC's, and sets much of the professional guidance the sector follows where there is no law — including voluntary donor family limits. Publishing success rates per clinic creates an incentive that shapes practice: a clinic can improve its numbers by treating easier patients, and the published figure cannot distinguish that from better medicine.",
   ["repro:clinics","rules:associations"], base=ASSN)]

# =============================================================== MONEY ========
IND22["USA"] = IND22["USA"] + [
 e("Foundation for Food & Agriculture Research", "https://foundationfar.org/",
   "A US public-private research funder created by the Farm Bill, matching federal money with private contributions. Match-funded research means the private partner influences what public money studies, and in agriculture the private partners are the companies whose products the research may assess.",
   ["money:public","money:philanthropy","editing:agtech"], base=REGI)]

IND22["NOR"] = [
 e("Norwegian Government Pension Fund Global \u2014 ethics exclusions", "https://www.nbim.no/en/responsible-investment/ethical-exclusions/",
   "The world's largest sovereign wealth fund, with an ethics council that can exclude companies from the portfolio and publishes its reasons for doing so. Divestment by an investor this size is one of the few sanctions that reaches a company without a regulator or a court, and the published reasoning becomes a reference other investors cite.",
   ["money:markets","rules:influence"], base=REGI)]

# ================================================================ RULES =======
IND22["CHE"] = [
 e("Swiss GMO moratorium \u2014 Federal Office for the Environment", "https://www.bafu.admin.ch/bafu/en/home/topics/biotechnology.html",
   "Switzerland has extended its moratorium on growing engineered crops repeatedly since 2005, most recently to 2027, while continuing to import engineered feed and to host some of the largest agricultural biotechnology companies in the world. A country can prohibit the cultivation and house the industry at once, and this is the clearest case of it.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND22["AUT"] = [
 e("Global 2000 / Friends of the Earth Austria", "https://www.global2000.at/",
   "The Austrian environmental organisation behind the country's long opposition to engineered crops, and the campaigning that made Austria the first EU member to invoke a national safeguard clause against an approved variety. Austria's stance later became the template for the opt-out mechanism written into EU law in 2015.",
   ["rules:standards","rules:influence"], base=BODY)]

IND22["NLD"] = [
 e("Wageningen University & Research", "https://www.wur.nl/en.htm",
   "The leading agricultural university in Europe and one of the largest sources of plant science anywhere, with a research funding model that ties it closely to industry. Much of the technical evidence the EU relies on when assessing crops originates in a small number of institutions of this kind, and this is the largest of them.",
   ["editing:agtech","money:public","money:vc"], base=BODY)]
