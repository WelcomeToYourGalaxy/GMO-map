# -*- coding: utf-8 -*-
"""Industry entries, part 23. Weighted to the thinnest facets: open release,
de-extinction, contract research, livestock."""
from ind1 import e, CO, BODY, REGI, ASSN

IND23 = {}

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND23["USA"] = [
 e("Anastasia / RNAi biopesticide sector", "https://www.epa.gov/pesticide-registration",
   "Sprayed double-stranded RNA silences a gene in a target pest, with no organism modified. Nothing living is altered so no biosafety framework applies, and the mechanism is sequence-specific so pesticide assumptions about dose and residue do not fit. Both categories were built for something else.",
   ["wild:microbes","rules:regulators","editing:platform"], base=REGI),
 e("Verily / Debug \u2014 automated rearing systems", "https://verily.com/solutions/debug",
   "Automated mass-rearing, sorting and release systems for sterile mosquitoes, built by a technology company. When releasing tens of millions of insects becomes a logistics problem, the remaining constraint is permission — and permission systems were designed when rearing capacity was the brake.",
   ["wild:insects","cro:cdmo"]),
 e("GBIRd \u2014 Genetic Biocontrol of Invasive Rodents", "https://www.geneticbiocontrol.org/about/",
   "A partnership developing gene-drive mice to clear invasive rodents from islands. Islands are chosen because a drive should stay put, but mice reach islands on boats, which is how they arrived — so the containment argument rests on the same transport that defeated it before.",
   ["wild:drives","deextinct:rescue","animals:models"], base=BODY),
 e("Ceres Nanosciences / environmental RNA monitoring", "https://www.ceresnano.com/",
   "Technologies for detecting genetic material in water and soil samples. Environmental DNA methods could find engineered sequences in a river or a field margin without knowing in advance what to look for, and the capability is being funded for pathogen surveillance rather than for watching releases.",
   ["synthesis:seq","wild:microbes","rules:standards"])]

# ================================ DE-EXTINCTION & CONSERVATION BIOTECH ========
IND23["USA"] = IND23["USA"] + [
 e("Wisconsin Cryobank / amphibian biobanking", "https://www.amphibianark.org/",
   "Cryopreservation of amphibian sperm and cell lines, for the taxon losing species fastest. Amphibians are dying out faster than they are being sampled, and whatever is banked now is the entire set of options anyone will have later.",
   ["deextinct:biobank","deextinct:rescue"], base=BODY),
 e("Rewilding and genetic rescue \u2014 Florida panther precedent", "https://myfwc.com/wildlife-habitats/wildlife/panther/",
   "Texas cougars were introduced into the remnant Florida panther population in 1995, reversing inbreeding effects and tripling the population. It worked, it is decades old, and it required no biotechnology — which is the comparison any engineered genetic rescue has to make and rarely does.",
   ["deextinct:rescue","livestock:livestock"], base=REGI)]

IND23["GBR"] = [
 e("Royal Botanic Gardens Kew \u2014 Millennium Seed Bank", "https://www.kew.org/science/collections-and-resources/millennium-seed-bank",
   "The world’s largest wild plant seed bank, focused on wild relatives and endangered flora rather than crops. The wild relatives this map describes taking up engineered genes are the same material stored here, and a bank of what a population used to be is the only reference a later change can be measured against.",
   ["deextinct:biobank","seed:germplasm"], base=BODY)]

# ============================================== CONTRACT RESEARCH ============
IND23["USA"] = IND23["USA"] + [
 e("Medpace", "https://www.medpace.com/",
   "A listed clinical research organisation, which means its trial volumes, backlog and therapeutic mix are in its filings. That disclosure exists only because the company happens to be listed, and it is the clearest public view of how the contract layer earns.",
   ["cro:cro","clinical:trials","money:markets"]),
 e("Emulate / organ-on-chip", "https://emulatebio.com/",
   "Microfluidic devices lined with human cells that reproduce organ-level responses, as an alternative to animal testing. The law now permits non-animal methods and regulators still expect animal data, so the constraint stopped being legal and became conventional.",
   ["animals:models","cro:cro","clinical:trials"]),
 e("Certara / in-silico trial simulation", "https://www.certara.com/",
   "Modelling used to predict drug behaviour and increasingly to replace some trial arms with simulated controls. Fewer people receive placebo, which is a real gain, and part of the evidence for approval was produced by a model whose assumptions are commercial property.",
   ["cro:cro","clinical:trials","editing:platform"])]

IND23["CHE"] = [
 e("Lonza \u2014 capacity allocation and Moderna", "https://www.lonza.com/news",
   "Lonza’s disclosures on contract manufacturing capacity, including the arrangements that produced billions of vaccine doses. Which products get made, and when, is decided in private commercial negotiation — during a shortage that is a rationing decision by a company no health authority appoints.",
   ["cro:cdmo","clinical:vectors","money:markets"])]

# ================================================= LIVESTOCK & AQUACULTURE ===
IND23["USA"] = IND23["USA"] + [
 e("Select Sires / bovine genetics cooperatives", "https://www.selectsires.com/",
   "A farmer-owned cooperative supplying dairy and beef genetics across the United States. Genomic selection has compressed dairy generation intervals sharply, so a trait chosen now reaches a national herd within a few years whether the supplier is a cooperative or a corporation.",
   ["livestock:livestock","seed:germplasm"]),
 e("Sexing Technologies / STgenetics", "https://www.stgen.com/",
   "The dominant supplier of sexed semen, allowing breeders to choose the sex of calves. Most dairy calves born are now female, and the male calves that were the by-product are simply not conceived — a welfare problem reduced by removing the animals from existence.",
   ["livestock:livestock","repro:clinics"])]

IND23["DNK"] = [
 e("VikingGenetics", "https://www.vikinggenetics.com/",
   "A Nordic farmer-owned cattle cooperative running genomic selection across Danish, Swedish and Finnish herds. Cooperative breeding puts the genetics in the hands of the farmers who use them, and it produces the same narrowing of the gene pool as the corporate route, because selection intensity is what narrows it rather than ownership.",
   ["livestock:livestock","seed:germplasm"])]

# =============================================================== MONEY =======
IND23["GBR"] = IND23["GBR"] + [
 e("Legal & General / institutional stewardship", "https://www.lgim.com/uk/en/capabilities/investment-stewardship/",
   "A large asset manager that publishes its voting record and engages companies on governance, including in agriculture and pharmaceuticals. Stewardship of this kind is the only routine mechanism by which an owner questions a company's conduct between scandals, and it operates through private meetings with a public voting record attached.",
   ["money:markets","rules:influence"])]

# ================================================================ RULES ======
IND23["DEU"] = [
 e("Testbiotech", "https://www.testbiotech.org/",
   "A German institute producing independent scientific assessment of EU biotechnology applications and filing formal objections. Its submissions are the substantive scientific comments in EU authorisation files that did not come from an applicant, and a handful of staff constitute most of the independent technical scrutiny in the world’s largest import market.",
   ["rules:standards","rules:influence"], base=BODY)]

IND23["BEL"] = [
 e("Corporate Europe Observatory", "https://corporateeurope.org/",
   "Documents lobbying in the EU institutions, including on the new genomic techniques file. The Transparency Register publishes numbers; someone has to read them against meeting records to make them mean anything, and a small number of organisations do that work.",
   ["rules:influence","rules:associations"], base=BODY)]
