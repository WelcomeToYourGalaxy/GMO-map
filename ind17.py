# -*- coding: utf-8 -*-
"""Industry entries, part 17."""
from ind1 import e, CO, BODY, REGI, ASSN

IND17 = {}

# ============================== DE-EXTINCTION & CONSERVATION BIOTECH ==========
IND17["USA"] = [
 e("IUCN \u2014 synthetic biology and biodiversity conservation", "https://www.iucn.org/our-work/topic/synthetic-biology-and-biodiversity",
   "The world conservation union’s position process on synthetic biology, which took years and split its membership. It is the most thorough attempt anywhere to reach a conservation position on engineered organisms, and it ended without prohibiting the tools.",
   ["deextinct:rescue","wild:drives","rules:standards"], base=BODY),
 e("American Chestnut Research and Restoration Project \u2014 SUNY ESF", "https://www.esf.edu/chestnut/",
   "The SUNY programme that developed the engineered blight-tolerant chestnut, including the line mix-up that went unnoticed for roughly a decade. The correction came from the researchers themselves, and it came ten years late.",
   ["deextinct:trees","deextinct:rescue","money:public"], base=BODY),
 e("Colossal Foundation", "https://colossalfoundation.org/",
   "The de-extinction company’s non-profit arm, funding conservation work alongside the commercial programme. A company with a foundation attached can direct its publicity toward the foundation while the returns sit with the company.",
   ["deextinct:ventures","money:philanthropy","deextinct:rescue"]),
 e("Frozen Ark Project", "https://www.frozenark.org/",
   "A UK-led network banking DNA and cells from endangered animals across institutions. Coordination between small biobanks is what turns separate freezers into a usable collection, and the coordination is the underfunded part.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND17["USA"] = IND17["USA"] + [
 e("Target Malaria \u2014 Imperial College programme record", "https://www.imperial.ac.uk/news/",
   "The published record of the gene-drive mosquito programme: the staged releases, the risk assessments, the community engagement. It is unusually documented for a release programme, which makes it possible to argue about on the evidence.",
   ["wild:drives","wild:insects"], base=BODY),
 e("Cibus", "https://www.cibus.com/",
   "Edits crops using techniques the company argues fall outside GMO rules in several jurisdictions, and the argument has largely been accepted. The regulatory classification is the product decision, taken before any agronomic one.",
   ["editing:agtech","seed:traits","rules:regulators"]),
 e("Bayer \u2014 Crop Science product safety summaries", "https://www.bayer.com/en/agriculture/product-safety",
   "The company's own safety summaries for its products. Self-published safety documentation is the industry's account of itself, and comparing it against independent studies is only possible because it exists in a fixed form.",
   ["seed:majors","wild:microbes","rules:standards"], trust="medium")]

# ============================================ LIVESTOCK & AQUACULTURE =========
IND17["USA"] = IND17["USA"] + [
 e("Center for Food Safety \u2014 animal biotechnology litigation", "https://www.centerforfoodsafety.org/",
   "A US organisation that has sued federal agencies over engineered animal approvals, including the AquaBounty salmon. Litigation is how approvals get tested in the United States, and the filings set out the strongest available case against each decision.",
   ["livestock:aqua","rules:regulators"], base=BODY),
 e("Genus \u2014 PRRS pig commercialisation record", "https://www.genusplc.com/media/",
   "The approval and commercialisation path for the edited pig cleared in April 2025, including the regulatory documents. The disease it resists spreads because of how pigs are housed, and the housing is not part of the assessment.",
   ["livestock:livestock","rules:regulators"])]

IND17["CHL"] = [
 e("AquaChile / Agrosuper", "https://www.aquachile.com/",
   "One of the largest Chilean salmon producers. Atlantic salmon are not native to Chile, have escaped in very large numbers, and have established in southern rivers — with no engineering involved, purely through farming at scale.",
   ["livestock:aqua","seed:germplasm"])]

IND17["NOR"] = [
 e("Norwegian Institute of Marine Research \u2014 spread monitoring", "https://www.hi.no/en",
   "The only systematic long-term monitoring anywhere of farmed salmon genetics entering wild rivers, finding introgression in a large majority of assessed populations. Nothing engineered is involved, and it is the baseline any argument about engineered salmon starts from.",
   ["livestock:aqua","rules:regulators"], base=REGI)]

# ========================================================= HUMAN CLINICAL =====
IND17["USA"] = IND17["USA"] + [
 e("Novartis \u2014 Zolgensma outcomes-based agreements", "https://www.novartis.com/news/",
   "Contracts under which payers pay less if the therapy does not work. Outcomes-based pricing is offered as the answer to multi-million-dollar treatments, and the terms of these agreements are mostly confidential.",
   ["clinical:therapy","money:markets"], trust="medium"),
 e("Cure Rare Disease and the 2022 trial death", "https://www.fda.gov/news-events/expanded-access",
   "A patient died in a custom gene therapy trial for a single individual with Duchenne muscular dystrophy. Bespoke therapies for one patient sit outside the trial structures built for populations, and this is the case that showed what that means.",
   ["clinical:therapy","clinical:trials","rules:regulators"], base=REGI),
 e("Alliance for Regenerative Medicine \u2014 sector data", "https://alliancerm.org/sector-data/",
   "The trade body's financing and pipeline figures, which are the numbers most coverage of this sector uses. They are compiled by the sector about itself, and no independent equivalent exists.",
   ["clinical:trials","rules:associations"], base=ASSN)]

IND17["GBR"] = [
 e("MHRA \u2014 Innovative Licensing and Access Pathway", "https://www.gov.uk/guidance/innovative-licensing-and-access-pathway",
   "A UK route intended to speed novel medicines to market, including genetic therapies. Faster approval moves evidence generation after the decision rather than before it, which is the trade the pathway makes explicitly.",
   ["rules:regulators","clinical:therapy"], base=REGI)]

# ============================================ CONTRACT RESEARCH ===============
IND17["USA"] = IND17["USA"] + [
 e("Thermo Fisher \u2014 Patheon and clinical services", "https://www.patheon.com/",
   "Thermo Fisher's contract manufacturing and clinical trial arms, added by acquisition. The company supplying the instruments, the reagents, the manufacturing and the trial services is one company.",
   ["cro:cdmo","cro:cro","synthesis:reagents"]),
 e("Advarra", "https://www.advarra.com/",
   "A commercial institutional review board that reviews trial ethics for sponsors who pay it. Ethics review became a purchased service in the United States, and the same competitive pressure that applies to contract laboratories applies here.",
   ["cro:cro","clinical:trials","rules:regulators"])]

IND17["CHN"] = [
 e("BGI \u2014 MGI Tech instruments", "https://en.mgi-tech.com/",
   "BGI's sequencing instrument arm, which broke Illumina's near-monopoly on the hardware. Competition in sequencers lowers the cost of reading DNA everywhere, including for the people doing verification rather than production.",
   ["synthesis:seq","money:defence"])]

# ============================================================ MONEY ===========
IND17["GBR"] = IND17["GBR"] + [
 e("Syncona", "https://www.synconaltd.com/",
   "A UK investment company building cell and gene therapy businesses, originally funded by Wellcome. Patient capital with a charitable origin behaves differently from a fund with a ten-year clock, and its portfolio shows it.",
   ["money:vc","money:markets","clinical:therapy"])]

IND17["DEU"] = [
 e("European Investment Bank \u2014 life sciences lending", "https://www.eib.org/",
   "Public lending to European biotechnology companies, at terms private capital would not offer. Public money at the growth stage is rare in this field, and it is one of the few counterweights to venture timelines.",
   ["money:public","money:vc"], base=REGI)]
