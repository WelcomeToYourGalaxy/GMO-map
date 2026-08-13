# -*- coding: utf-8 -*-
"""Industry entries, part 5. Weighted to the four thinnest facets:
de-extinction, open release, assisted reproduction and livestock."""
from ind1 import e, CO, BODY, REGI, ASSN

IND5 = {}

# ================================ DE-EXTINCTION & CONSERVATION BIOTECH ========
IND5["USA"] = [
 e("Revive & Restore", "https://reviverestore.org/",
   "A conservation non-profit applying biotechnology to endangered species — cloned black-footed ferrets and Przewalski’s horses, biobanking, and work toward genetic rescue of populations too inbred to recover on their own. It occupies an awkward and useful position: the same techniques the rest of this map documents being used by people whose stated aim is to undo damage rather than sell a product. Whether that distinction survives contact with scale is the open question, and this is where to watch it.",
   ["deextinct:rescue","deextinct:biobank","deextinct:ventures"], base=BODY),
 e("San Diego Zoo Wildlife Alliance \u2014 Frozen Zoo", "https://science.sandiegozoo.org/",
   "Cell lines from more than a thousand species, frozen since 1972, and the reason the cloned ferrets and horses were possible at all — the cells used were banked decades before anyone could do anything with them. It is the clearest case for collecting material whose use has not yet been invented, and there are only a handful of such collections in the world.",
   ["deextinct:biobank","deextinct:rescue","livestock:cloning"], base=BODY),
 e("American Chestnut Foundation \u2014 Darling 58", "https://acf.org/",
   "The engineered blight-tolerant chestnut was studied for roughly a decade before anyone noticed the tree in the trials was not the tree in the application — two lines had been mixed up, and the one actually tested carries a second gene broken by the insertion, resists blight only patchily, and dies at high rates. The Foundation withdrew its support in 2023. An inserted gene lands somewhere, and what it lands in the middle of is not chosen, which is why this went unnoticed for ten years by people with every reason to look.",
   ["deextinct:trees","deextinct:rescue","wild:drives"], base=BODY),
 e("Colossal \u2014 Form Bio spin-out", "https://www.formbio.com/",
   "Colossal’s computational platform, spun out as its own company and sold to other biotechnology firms. It shows what the de-extinction business is actually built on: the mammoth raises the money and generates the coverage, and the software, enzymes and methods developed along the way are the products with buyers.",
   ["deextinct:ventures","editing:platform","money:vc"])]

# ============================= INSECTS, MICROBES & DELIBERATE OPEN RELEASE ====
IND5["USA"] = IND5["USA"] + [
 e("MosquitoMate", "https://mosquitomate.com/",
   "Releases male mosquitoes carrying Wolbachia bacteria so that their matings produce no offspring, sold as a commercial mosquito control service in US cities. The insects are not genetically engineered, which is why the product reached market with far less friction than an engineered equivalent — the same suppression outcome, achieved by a route the rules were not written to catch.",
   ["wild:insects","wild:microbes","rules:regulators"]),
 e("Ginkgo Bioworks \u2014 agricultural biologicals", "https://www.ginkgobioworks.com/agriculture/",
   "Ginkgo’s agricultural arm, engineering microbes applied to seed and soil across large acreages. Nothing here enters a biosafety register: a microbe on a seed is neither a plant nor planted, so the largest deliberate releases of engineered organisms by area produce no record anywhere in the world.",
   ["wild:microbes","editing:synbio","seed:distribution"]),
 e("Elemental Enzymes / biologicals sector", "https://elementalenzymes.com/",
   "One of a growing number of companies selling engineered enzymes and microbial products as agricultural inputs. The sector as a whole is the clearest instance of the regulatory gap working as a business model — products designed for the category that requires the least, sold at a scale that would attract intense scrutiny in any other form.",
   ["wild:microbes","seed:licensees","money:vc"])]

IND5["GBR"] = [
 e("Wolbachia \u2014 World Mosquito Program", "https://www.worldmosquitoprogram.org/",
   "Releases mosquitoes carrying Wolbachia so the population becomes unable to transmit dengue, across more than a dozen countries, with published trials showing large reductions in cases. It is the most successful large-scale insect release programme anywhere and involves no genetic engineering at all — and every argument that engineering was the only available route has to account for it.",
   ["wild:insects","wild:microbes"], base=BODY)]

# ======================================== LIVESTOCK, AQUACULTURE & PETS =======
IND5["USA"] = IND5["USA"] + [
 e("Genus \u2014 PRRS-resistant pig approval", "https://www.genusplc.com/investors/",
   "The FDA approved gene-edited pigs resistant to PRRS on 30 April 2025 — the first edited food animal cleared in the United States. PRRS spreads because pigs are kept in crowded conditions, and the disease is said to drive antibiotic use up by more than 200%. The crowding is not addressed. The animal is rewritten to tolerate it, which is the pattern this facet keeps producing: the conditions stay, the organism changes.",
   ["livestock:livestock","money:markets"]),
 e("GloFish", "https://www.glofish.com/",
   "Fluorescent aquarium fish, the first engineered animal sold to the public anywhere, now a routine pet-shop product. Established populations have since been found in Brazilian streams, having spread from ornamental fish farms. The pathway that mattered was never the aquarium — it was the farm supplying them, and nobody was monitoring it because a decorative pet was not treated as an environmental question.",
   ["livestock:pets","livestock:aqua","wild:insects"]),
 e("Trans Ova Genetics", "https://transova.com/",
   "The largest bovine embryo transfer and cloning company in the United States, producing cloned cattle commercially since the 1990s. Cloned livestock and their descendants entered the food supply years ago with no labelling requirement, the argument about whether the public would accept it was resolved by not asking.",
   ["livestock:cloning","repro:clinics","livestock:livestock"])]

IND5["NZL"] = [
 e("Livestock Improvement Corporation", "https://www.lic.co.nz/",
   "A New Zealand farmer-owned cooperative supplying dairy genetics to most of the national herd, and running the genomic evaluation the herd is bred on. Cooperative ownership does not slow the genetics: an index change here reaches almost every dairy cow in the country within a few generations, which suggests the speed is set by the technology rather than by who owns the company.",
   ["livestock:livestock","seed:germplasm"])]

# ================================================= ASSISTED REPRODUCTION ======
IND5["USA"] = IND5["USA"] + [
 e("Progyny", "https://progyny.com/",
   "A fertility benefits manager that sits between employers and clinics, deciding which treatments are covered for a large number of US employees. Coverage decisions made at this layer determine what patients are actually offered, including which add-ons and how many cycles — a commercial intermediary shaping clinical practice without ever treating anyone.",
   ["repro:clinics","money:markets"]),
 e("Genomic Prediction / LifeView", "https://www.lifeview.com/",
   "Sells polygenic risk scoring of IVF embryos, including for traits with no single genetic cause. Professional genetics bodies have said the science does not support clinical use. It is sold regardless, because embryo selection requires none of the approval a drug or device would need — the distance between what the evidence supports and what may lawfully be sold is the entire market.",
   ["repro:screening","clinical:germline"]),
 e("Society for Assisted Reproductive Technology", "https://www.sart.org/",
   "The US fertility profession’s own body, which collects and publishes clinic outcome data and sets practice guidance. Self-regulation covers most of what US fertility clinics do, and this is what it looks like in practice: real data collection, real guidance, no enforcement, and a membership free to ignore either.",
   ["repro:clinics","rules:associations"], base=ASSN)]

IND5["ESP"] = [
 e("Eugin Group", "https://www.eugin.co.uk/",
   "An international fertility chain operating clinics across Europe, the Americas and Asia, with cross-border treatment as a core part of the business. Patients travel to where a treatment is permitted, so a national restriction becomes a travel itinerary rather than a limit — and the chain that owns clinics on both sides of the rule is the party that benefits from the difference.",
   ["repro:clinics","repro:banks","repro:surrogacy"])]

IND5["DNK"] = [
 e("Cryos International", "https://www.cryosinternational.com/",
   "One of the largest sperm banks in the world, shipping to more than a hundred countries from Denmark. Family limits are set per country and enforced per bank, so a donor can lawfully reach limits in a dozen jurisdictions at once and no one is counting the total. Donor-conceived people keep discovering sibling groups far larger than any published limit implies, and there is no register anywhere designed to prevent it.",
   ["repro:banks","repro:surrogacy"])]

# ============================================================== MONEY =========
IND5["GBR"] = IND5["GBR"] + [
 e("Baillie Gifford / growth capital in biotech", "https://www.bailliegifford.com/",
   "A Scottish investment partnership that has held large positions across biotechnology, and unusually for its size, is privately owned and explicitly long-horizon. It is the counter-example to venture money’s fixed clock: capital that can wait changes what a company is able to attempt, and there is very little of it in this field.",
   ["money:markets","money:vc"])]
