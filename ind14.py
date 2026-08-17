# -*- coding: utf-8 -*-
"""Industry entries, part 14. Weighted to the facets now thinnest: money, open
release, clinical, livestock, synthesis, de-extinction."""
from ind1 import e, CO, BODY, REGI, ASSN

IND14 = {}

# =============================================================== MONEY ========
IND14["USA"] = [
 e("Blackstone Life Sciences", "https://www.blackstone.com/our-businesses/life-sciences/",
   "The life sciences arm of one of the world’s largest private equity firms, funding late-stage drug development. Capital of this size chooses which candidates reach patients, applying a return requirement at the point where clinical need would otherwise decide.",
   ["money:vc","clinical:therapy","money:markets"]),
 e("Novo Holdings", "https://novoholdings.dk/",
   "The investment company controlling Novo Nordisk and holding stakes across biotechnology, ultimately owned by a Danish foundation. Foundation ownership means the profits fund research rather than shareholders, which is a genuinely different structure from the rest of the sector.",
   ["money:vc","cro:cdmo","money:markets"]),
 e("SEC EDGAR \u2014 full-text search", "https://efts.sec.gov/LATEST/search-index?q=%22gene%20editing%22",
   "Every filing by every US-listed company, searchable in full text. Companies must disclose material risks and segment finances accurately or commit an offence, which makes this the most reliable public account of what firms on this map actually earn and fear.",
   ["money:markets","rules:influence"], base=REGI),
 e("Open Philanthropy \u2014 biosecurity and science funding", "https://www.openphilanthropy.org/grants/",
   "A major private funder of biosecurity, including DNA synthesis screening, pandemic preparedness and far-ultraviolet light research. It is one of a small number of philanthropic sources setting the agenda in a field where governments fund response and almost nobody funds prevention — which means a handful of private decisions shape what defences exist.",
   ["money:philanthropy","synthesis:synth"], base=REGI)]

IND14["GBR"] = [
 e("Wellcome Sanger Institute", "https://www.sanger.ac.uk/",
   "One of the largest genome sequencing centres in the world, publicly funded, which sequenced a third of the human genome reference and now runs biodiversity genomics at scale. Its output is released openly, which is why so much downstream work is possible.",
   ["synthesis:seq","money:philanthropy","clinical:trials"], base=BODY)]

# ==================================== INSECTS, MICROBES & OPEN RELEASE ========
IND14["USA"] = IND14["USA"] + [
 e("Sterile Insect Technique programmes \u2014 IAEA and national partners", "https://www.iaea.org/topics/sterile-insect-technique",
   "Irradiated sterile insects released to suppress pest populations, run by national programmes with IAEA support since the 1950s. Nothing is genetically engineered, the technique has eradicated screwworm from North America, and it is the benchmark any engineered insect release should be measured against.",
   ["wild:insects","rules:standards"], base=BODY),
 e("Bayer / Ginkgo \u2014 Joyn Bio nitrogen fixation", "https://www.joynbio.com/",
   "A joint venture to engineer nitrogen-fixing microbes for cereals, since wound down. Nitrogen fixation in maize would displace a large share of world fertiliser use, and the attempt failing tells you how hard the biology is rather than how small the prize was.",
   ["wild:microbes","editing:synbio","seed:distribution"]),
 e("EPA \u2014 biopesticide and plant-incorporated protectant registrations", "https://www.epa.gov/pesticide-registration/biopesticide-registration",
   "The US register of pesticidal substances produced by plants themselves, including Bt traits. A plant that makes its own insecticide is registered as a pesticide, which puts the insecticide in the seed rather than in a tank and outside every measure of pesticide application.",
   ["wild:microbes","rules:regulators","seed:traits"], base=REGI)]

IND14["BRA"] = [
 e("Moscamed Brasil", "https://moscamed.org.br/",
   "Rears and releases sterile insects at very large scale, mainly Mediterranean fruit fly, and has produced engineered Aedes mosquitoes for release. Sterile insect technique has been used for seventy years and is uncontroversial; the same facility producing engineered insects for the same purpose is regulated differently, which is where the argument about the method rather than the outcome shows most plainly.",
   ["wild:insects","cro:cdmo"])]

# ========================================================= HUMAN CLINICAL =====
IND14["USA"] = IND14["USA"] + [
 e("Recombinant DNA Advisory Committee \u2014 archive", "https://osp.od.nih.gov/policies/biosafety-and-biosecurity-policy/",
   "The archive of the committee that oversaw early US genetic engineering, created after scientists themselves called for a moratorium at Asilomar in 1975. It is the record of a field agreeing to pause and then designing its own oversight, and of what happened to that oversight afterwards.",
   ["clinical:trials","rules:regulators"], base=REGI),
 e("Jesse Gelsinger and the 1999 trial death \u2014 FDA record", "https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/office-good-clinical-practice",
   "An eighteen-year-old died in a gene therapy trial in 1999, and the investigation found undisclosed conflicts of interest and unreported adverse events in earlier patients. The field stalled for a decade. The records are the reason trial registration and conflict disclosure exist in their current form.",
   ["clinical:trials","rules:regulators"], base=REGI),
 e("Alnylam Pharmaceuticals", "https://www.alnylam.com/",
   "Turned RNA interference into medicine, delivering short RNA sequences that switch off a specific gene's message before it becomes protein. It took twenty years and the near-abandonment of the field by every large pharmaceutical company between the Nobel-winning discovery in 1998 and the first approval in 2018. The result is a drug that silences a gene without editing it — reversible, repeatable, and outside every framework written for permanent genetic change.",
   ["clinical:therapy","editing:platform"])]

# ============================================= LIVESTOCK & AQUACULTURE ========
IND14["USA"] = IND14["USA"] + [
 e("FDA \u2014 intentional genomic alterations in animals", "https://www.fda.gov/animal-veterinary/biotechnology-products-cvm-animals-and-animal-food/intentional-genomic-alterations-igas-animals",
   "The US pathway for approving edited and engineered animals, which treats the introduced genetic change as an animal drug. That framing has been in place since 2009 and is why AquAdvantage salmon took twenty years: a drug approval requires evidence about the compound in every animal that receives it, which fits a veterinary medicine and does not fit a heritable trait. The agency has since created faster routes for low-risk alterations.",
   ["livestock:livestock","rules:regulators"], base=REGI),
 e("Hendrix Genetics", "https://www.hendrix-genetics.com/",
   "A Dutch multi-species animal breeding company — poultry, pigs, aquaculture, turkeys. A handful of breeding companies supply the genetics for most of the world’s farmed animals, so a trait selected here reaches enormous populations within a few generations.",
   ["livestock:livestock","livestock:aqua","seed:germplasm"])]

IND14["NLD"] = [
 e("Topigs Norsvin", "https://www.topigsnorsvin.com/",
   "A Dutch-Norwegian pig genetics company supplying breeding stock across Europe, the Americas and Asia, and one of the three companies that between them supply most of the world's commercial pig genetics. It runs genomic selection and computed-tomography scanning of breeding animals, and has worked on editing for disease resistance. Pigs are the animal where editing is furthest advanced in food production and also the source of engineered organs for human transplant, so the same breeding companies sit behind both.",
   ["livestock:livestock","seed:germplasm"])]

IND14["NOR"] = [
 e("Mowi", "https://mowi.com/",
   "The largest farmed salmon producer in the world, Norwegian, operating across several countries. Escapes from farms of this scale have already introgressed into wild rivers with no engineering involved, which sets the baseline for any argument about engineered fish.",
   ["livestock:aqua","seed:germplasm"])]

# ================================================ SYNTHESIS & INSTRUMENTS =====
IND14["USA"] = IND14["USA"] + [
 e("International Gene Synthesis Consortium", "https://genesynthesisconsortium.org/",
   "The industry body whose members voluntarily screen DNA orders against sequences of concern and check the identity of customers. Its members cover a large share of commercial synthesis capacity, which is the reassuring half of the sentence. The other half is that membership is voluntary, non-members are not counted anywhere, and benchtop synthesisers remove the order that screening depends on.",
   ["synthesis:synth","rules:associations","rules:standards"], base=ASSN),
 e("Benchling", "https://www.benchling.com/",
   "Software that laboratories use to design and record genetic engineering work, holding the design files for a substantial share of the field. Where the designs live is a question about security and access that the biosafety frameworks were not written to consider.",
   ["editing:platform","synthesis:synth"]),
 e("Codex DNA / Telesis Bio", "https://telesisbio.com/",
   "Sells benchtop machines that synthesise and assemble DNA in a laboratory, including whole genes, without an order passing through any manufacturer. Synthesis screening exists because orders can be checked; a machine on a bench removes the order. It is the same gap DNA Script opens from the enzymatic side, and no jurisdiction has legislated for either.",
   ["synthesis:synth","editing:platform"])]

# ==================================================== DE-EXTINCTION ===========
IND14["AUS"] = [
 e("Australian Frozen Zoo \u2014 threatened species cryobanking", "https://www.zoo.org.au/melbourne/",
   "Cryopreservation of cells and reproductive tissue from Australian threatened species, in a country with the highest recorded rate of mammal extinction in the world. Banking material now is a bet that assisted reproduction or cloning will later be able to use it — and for several of the species held, the bet is already the only remaining option.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]

IND14["GBR"] = IND14["GBR"] + [
 e("Nature's SAFE", "https://www.natures-safe.com/",
   "A European biobank preserving reproductive tissue and cells from endangered animals, working with zoos to collect material at death rather than losing it. Banking is only useful if something can later be done with the material, so this is infrastructure built on the assumption that assisted reproduction and cloning in wild species will improve — a bet made by storing things.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]
