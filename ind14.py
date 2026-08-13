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
   "A major funder of biosecurity work, including DNA synthesis screening. Much of the effort to close the screening gap is paid for by philanthropy rather than required by law, which is why the coverage is partial.",
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
   "A Brazilian sterile insect facility rearing and releasing hundreds of millions of insects, including for engineered mosquito programmes. Rearing at this scale is the practical constraint on any release strategy, engineered or not.",
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
   "Commercialised RNA interference as medicine, delivering sequence-specific silencing to patients. The same mechanism sprayed on a field is regulated as a pesticide or as nothing at all, depending on the jurisdiction.",
   ["clinical:therapy","editing:platform"])]

# ============================================= LIVESTOCK & AQUACULTURE ========
IND14["USA"] = IND14["USA"] + [
 e("FDA \u2014 intentional genomic alterations in animals", "https://www.fda.gov/animal-veterinary/biotechnology-products-cvm-animals-and-animal-food/intentional-genomic-alterations-igas-animals",
   "The US pathway for approving edited and engineered animals, under which the AquaBounty salmon spent twenty-five years and the PRRS-resistant pig was cleared in 2025. The approvals and the review documents are public.",
   ["livestock:livestock","rules:regulators"], base=REGI),
 e("Hendrix Genetics", "https://www.hendrix-genetics.com/",
   "A Dutch multi-species animal breeding company — poultry, pigs, aquaculture, turkeys. A handful of breeding companies supply the genetics for most of the world’s farmed animals, so a trait selected here reaches enormous populations within a few generations.",
   ["livestock:livestock","livestock:aqua","seed:germplasm"])]

IND14["NLD"] = [
 e("Topigs Norsvin", "https://www.topigsnorsvin.com/",
   "A Dutch-Norwegian pig genetics company supplying breeding stock internationally. With Genus and a few others it forms the small group deciding what the world’s pigs are bred to be.",
   ["livestock:livestock","seed:germplasm"])]

IND14["NOR"] = [
 e("Mowi", "https://mowi.com/",
   "The largest farmed salmon producer in the world, Norwegian, operating across several countries. Escapes from farms of this scale have already introgressed into wild rivers with no engineering involved, which sets the baseline for any argument about engineered fish.",
   ["livestock:aqua","seed:germplasm"])]

# ================================================ SYNTHESIS & INSTRUMENTS =====
IND14["USA"] = IND14["USA"] + [
 e("International Gene Synthesis Consortium", "https://genesynthesisconsortium.org/",
   "The industry body whose members voluntarily screen DNA orders against dangerous sequence lists. Its members estimate they make about 80% of world supply, leaving roughly a fifth unscreened — and no law requires any of it.",
   ["synthesis:synth","rules:associations","rules:standards"], base=ASSN),
 e("Benchling", "https://www.benchling.com/",
   "Software that laboratories use to design and record genetic engineering work, holding the design files for a substantial share of the field. Where the designs live is a question about security and access that the biosafety frameworks were not written to consider.",
   ["editing:platform","synthesis:synth"]),
 e("Codex DNA / Telesis Bio", "https://telesisbio.com/",
   "Sells benchtop machines that synthesise DNA in a laboratory rather than ordering it from a supplier. Order screening only works if orders are placed; a machine on a bench removes the step at which screening happens.",
   ["synthesis:synth","editing:platform"])]

# ==================================================== DE-EXTINCTION ===========
IND14["AUS"] = [
 e("Australian Frozen Zoo \u2014 threatened species cryobanking", "https://www.zoo.org.au/melbourne/",
   "Cryopreservation of Australian threatened species, in a country with among the highest extinction rates in the world. The collecting is racing a clock nobody controls, and it is done by a small number of underfunded programmes.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]

IND14["GBR"] = IND14["GBR"] + [
 e("Nature's SAFE", "https://www.natures-safe.com/",
   "A European biobank preserving reproductive tissue and cells from endangered species. What is banked now is the whole set of options anyone will have later, and this work is done by a handful of small, underfunded organisations.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY)]
