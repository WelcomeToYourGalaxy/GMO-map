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
   "Developed the blight-resistant Darling 58 chestnut, carrying a wheat gene that detoxifies the fungus which killed four billion American chestnuts in the twentieth century. It is the first engineered organism proposed for release into wild forests purely to restore a species rather than to produce anything, and it has spent years in a USDA petition that the project's own supporters criticised after data problems emerged. The case is where conservation and biosafety argue directly, with no commercial interest between them.",
   ["deextinct:trees","deextinct:rescue","money:public"], base=BODY),
 e("Colossal Foundation", "https://colossalfoundation.org/",
   "The de-extinction company's non-profit arm, funding conservation work on living endangered species alongside the extinct ones. The structure is worth recording: a venture-funded company raising money on mammoths while a foundation attached to it does conventional conservation, so the publicity from one supports the other.",
   ["deextinct:ventures","money:philanthropy","deextinct:rescue"]),
 e("Frozen Ark Project", "https://www.frozenark.org/",
   "A UK-led network banking DNA and viable cells from endangered animals, so that material survives the species. It assumes a future in which stored cells can be turned back into an animal, which is the premise de-extinction companies sell commercially and which this network has been quietly preparing for since 2004 without claiming it can be done.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND17["USA"] = IND17["USA"] + [
 e("Target Malaria \u2014 Imperial College programme record", "https://www.imperial.ac.uk/news/",
   "The published record of the gene-drive mosquito programme: the staged releases in Burkina Faso, Ghana and Uganda, the risk assessments, and the community consent processes conducted before each step. It is the most documented approach to an engineered release anywhere, deliberately so, because a drive designed to spread through a wild population cannot be recalled and the programme knows the precedent it is setting will govern everything after it.",
   ["wild:drives","wild:insects"], base=BODY),
 e("Cibus", "https://www.cibus.com/",
   "Edits crops using techniques it argues fall outside the definition of genetic modification, and has built a business on that argument rather than on a particular trait. Its canola was treated as non-GM in the United States and as GM in the European Union at the same time, which is the sharpest single demonstration that whether an organism is regulated depends on where it is standing rather than on what it is.",
   ["editing:agtech","seed:traits","rules:regulators"])]

# ============================================ LIVESTOCK & AQUACULTURE =========
IND17["USA"] = IND17["USA"] + [
 e("Center for Food Safety \u2014 animal biotechnology litigation", "https://www.centerforfoodsafety.org/",
   "A US organisation that has sued federal agencies over engineered animal approvals, including the AquaBounty salmon. Litigation is how approvals get tested in the United States, and the filings set out the strongest available case against each decision.",
   ["livestock:aqua","rules:regulators"], base=BODY),
 e("Genus \u2014 PRRS pig commercialisation record", "https://www.genusplc.com/media/",
   "The approval path for the edited pig resistant to porcine reproductive and respiratory syndrome, cleared by the FDA in 2025. It is the first edited food animal approved for a disease-resistance trait rather than a production one, and the argument made for it was welfare and antibiotic reduction rather than yield — which is the case the industry expects to make for everything that follows.",
   ["livestock:livestock","rules:regulators"])]

IND17["CHL"] = [
 e("AquaChile / Agrosuper", "https://www.aquachile.com/",
   "One of the largest Chilean salmon producers. Atlantic salmon is not native to the southern hemisphere; it was introduced for farming, escapes regularly, and has established in Patagonian rivers. Intensive breeding of a non-native fish in open sea cages is a release that happens continuously without ever being authorised as one.",
   ["livestock:aqua","seed:germplasm"])]

IND17["NOR"] = [
 e("Norwegian Institute of Marine Research \u2014 spread monitoring", "https://www.hi.no/en",
   "The only systematic long-term monitoring anywhere of farmed salmon genetics entering wild rivers, finding introgression in a large majority of assessed populations. Nothing engineered is involved, and it is the baseline any argument about engineered salmon starts from.",
   ["livestock:aqua","rules:regulators"], base=REGI)]

# ========================================================= HUMAN CLINICAL =====
IND17["USA"] = IND17["USA"] + [
 e("Novartis \u2014 Zolgensma outcomes-based agreements", "https://www.novartis.com/news/",
   "Zolgensma is a one-time gene therapy for spinal muscular atrophy priced above two million dollars, sold in some countries under contracts where the payer pays less if the child does not improve. Paying for a result rather than a product is a new arrangement in medicine, and it exists because a single-dose cure breaks the instalment logic every health system was built on.",
   ["clinical:therapy","money:markets"], trust="medium"),
 e("Cure Rare Disease and the 2022 trial death", "https://www.fda.gov/news-events/expanded-access",
   "A patient died in 2022 in a custom gene therapy trial built for his own single mutation, funded and organised by a non-profit his brother founded. Bespoke therapies for one person sidestep the economics that make ultra-rare disease untreatable, and they also sidestep the accumulated safety evidence that comes from treating many patients with the same product. This is the case the whole n-of-one field is measured against.",
   ["clinical:therapy","clinical:trials","rules:regulators"], base=REGI),
 e("Alliance for Regenerative Medicine \u2014 sector data", "https://alliancerm.org/sector-data/",
   "The trade body for cell and gene therapy, and the source of the financing, trial and pipeline figures almost every account of the sector uses — including this map's. An industry association counting its own field is the only systematic count that exists, because no regulator publishes one, and the numbers therefore come with the interests of the people compiling them.",
   ["clinical:trials","rules:associations"], base=ASSN)]

IND17["GBR"] = [
 e("MHRA \u2014 Innovative Licensing and Access Pathway", "https://www.gov.uk/guidance/innovative-licensing-and-access-pathway",
   "A UK route intended to speed novel medicines to market through earlier and closer contact between developer and regulator. Routes of this kind trade certainty for speed, and for cell and gene therapies — where the evidence base is thin and the patient numbers small — that trade is made more often than anywhere else in medicine.",
   ["rules:regulators","clinical:therapy"], base=REGI)]

# ============================================ CONTRACT RESEARCH ===============
IND17["USA"] = IND17["USA"] + [
 e("Advarra", "https://www.advarra.com/",
   "A commercial institutional review board reviewing clinical trial ethics for sponsors who pay it, and one of two firms that between them review a very large share of US industry trials. Ethics review was designed to be done by a committee at the institution running the study; contracting it to a company chosen and paid by the sponsor is now the norm, and nothing about that arrangement is disclosed on the resulting publication.",
   ["cro:cro","clinical:trials","rules:regulators"])]

IND17["CHN"] = [
 e("BGI \u2014 MGI Tech instruments", "https://en.mgi-tech.com/",
   "BGI's instrument arm, which built sequencers to escape dependence on Illumina after patent litigation restricted its access in several markets. It is the only serious challenge to a near-monopoly on the machines that read DNA, and the dispute has been fought in courts on three continents — which makes the price of sequencing partly a function of patent law rather than of engineering.",
   ["synthesis:seq","money:defence"])]

# ============================================================ MONEY ===========
IND17["GBR"] = IND17["GBR"] + [
 e("Syncona", "https://www.synconaltd.com/",
   "A UK investment company that builds cell and gene therapy businesses rather than buying into them, founded with Wellcome Trust money. Company creation on this model means a single investor chooses which scientific programmes become companies at all, which is a narrower gate than a competitive funding round.",
   ["money:vc","money:markets","clinical:therapy"])]

IND17["DEU"] = [
 e("European Investment Bank \u2014 life sciences lending", "https://www.eib.org/",
   "Public lending to European biotechnology companies, at terms and stages private capital will not cover. It is the main reason a European company can develop a therapy without selling itself to an American one, and the effect is visible in which companies still exist — development finance rather than science determines much of where this industry ends up owned.",
   ["money:public","money:vc"], base=REGI)]
