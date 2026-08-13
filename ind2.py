# -*- coding: utf-8 -*-
"""Industry entries, part 2."""
from ind1 import e, CO, BODY, REGI, ASSN

IND2 = {}

# =========================================================== LAB ANIMALS ======
IND2["USA"] = [
 e("The Jackson Laboratory", "https://www.jax.org/",
   "A non-profit that is also the world’s largest supplier of genetically defined mice, holding more than eleven thousand strains and shipping millions of animals a year. Its catalogue is the reason a paper published in one country can be repeated in another: the strain has a number and anyone with an institutional account can order it. That same catalogue is a list of thousands of lineages bred to be ill in a particular way, maintained in perpetuity because a researcher somewhere may want them. Mice are excluded from the US Animal Welfare Act’s definition of an animal, so almost none of this appears in any official count.",
   ["animals:models","animals:breeders"], base=BODY),
 e("Taconic Biosciences", "https://www.taconic.com/",
   "A commercial model-generation business — a laboratory brings a gene it wants altered and Taconic builds the mouse. Where Jackson holds a public catalogue, this end of the trade is contract work whose outputs may never be described anywhere. It sits in a market of a handful of firms supplying most of the world’s research animals, which means a small number of private companies effectively decide which biological questions are cheap to ask.",
   ["animals:services","animals:breeders"]),
 e("Envigo / Inotiv", "https://www.inotiv.com/",
   "One of the largest suppliers of dogs, rodents and other research animals, and the subject of a 2022 US federal seizure that removed around four thousand beagles from a Virginia breeding facility after repeated welfare violations. That case is unusual only in that it became public: inspection reports for licensed dealers are published, searchable and specific, and almost nobody reads them. For dogs, cats and primates this is the most detailed public accountability record anywhere in the world — and it still excludes the rodents that are the overwhelming majority.",
   ["animals:breeders","cro:cro"])]

IND2["JPN"] = [
 e("CLEA Japan / Japan SLC", "https://www.clea-japan.com/en/",
   "Japan’s principal laboratory-animal suppliers, serving a research system whose scale is comparable to Europe’s. Japan publishes no national count of animals used, so the size of the practice there is inferred from the suppliers rather than reported by anyone — a reminder that the US and UK figures on this map exist because those countries chose to collect them, not because collecting them is normal.",
   ["animals:breeders","animals:models"])]

# ============================== LIVESTOCK, AQUACULTURE & COMPANION ANIMALS ====
IND2["USA"] = IND2["USA"] + [
 e("Acceligen (Recombinetics)", "https://acceligen.com/",
   "Edits farm animals to order — hornless cattle, heat-tolerant cattle, pigs altered for disease resistance. Its flagship product is where the record is clearest. the hornless cattle were found to carry bacterial DNA nobody had noticed, including antibiotic-resistance genes, discovered by an FDA scientist re-reading the company’s own data. The company had said the edit was clean. It is the clearest documented case of an editing firm not knowing what it had made.",
   ["livestock:livestock","editing:agtech"]),
 e("AquaBounty Technologies", "https://aquabounty.com/",
   "Produced the first engineered animal approved anywhere for human consumption — a salmon growing to market weight in half the usual time — after roughly twenty-five years of regulatory review. It then failed commercially, closing its US operations and selling its farms. Both halves are on the record. two and a half decades to approve a single fish tells you what the approval path costs, and the collapse that followed tells you the constraint was never only regulatory.",
   ["livestock:aqua","rules:regulators"]),
 e("ViaGen Pets & Equine", "https://www.viagenpets.com/",
   "Clones pets and horses for anyone who pays, at around fifty thousand dollars for a dog. No biosafety rule applies at any point, because nothing foreign is inserted and the regulations only trigger on inserted material. It is also the company that produced cloned Przewalski’s horses for conservation programmes — so the capability now used to rescue an endangered subspecies exists because a consumer market paid to develop it first.",
   ["livestock:cloning","livestock:pets"])]

IND2["KOR"] = [
 e("Sooam Biotech", "https://en.sooam.com/",
   "The South Korean laboratory that commercialised pet cloning, founded by a researcher whose stem-cell papers were retracted for fabrication and who was convicted of embezzlement. He returned to a business with no regulatory gatekeeper at all: cloning a dog requires no biosafety approval anywhere, because nothing foreign is inserted. A career ended by scientific fraud continued in the part of the field that asks no questions.",
   ["livestock:cloning","livestock:pets"])]

# ============================= INSECTS, MICROBES & DELIBERATE OPEN RELEASE ====
IND2["GBR"] = [
 e("Oxitec", "https://www.oxitec.com/",
   "Releases engineered mosquitoes designed so that female offspring die before reproducing, in Brazil, the Cayman Islands, the United States and elsewhere — hundreds of millions of insects. In Jacobina, Brazil, researchers later found the engineered lineage had introgressed into the wild population, which the company had said would not happen. That finding is the single most useful piece of evidence about what happens after a release, and it came from independent scientists rather than any monitoring programme.",
   ["wild:insects","wild:drives"])]

IND2["USA"] = IND2["USA"] + [
 e("Target Malaria", "https://targetmalaria.org/",
   "A research consortium funded largely by the Gates Foundation, developing gene-drive mosquitoes intended to suppress the species that carries malaria in West Africa. It has released non-drive engineered mosquitoes in Burkina Faso as a staged step toward the real thing. Whatever one concludes, this is the most consequential deliberate release being prepared anywhere: a drive is designed to spread itself through a wild population without further releases, and nobody has demonstrated a way to recall one.",
   ["wild:drives","wild:insects"], base=BODY),
 e("Pivot Bio", "https://www.pivotbio.com/",
   "Sells engineered soil bacteria that fix nitrogen, applied to seed across millions of US acres. By area it is among the largest deliberate releases of an engineered organism in history — and it generates no entry in any biosafety register anywhere, because a microbe on a seed is not a plant and coating it is not planting. The scale and the invisibility are facts about the same product.",
   ["wild:microbes","editing:synbio"])]

# ================================ DE-EXTINCTION & CONSERVATION BIOTECH ========
IND2["USA"] = IND2["USA"] + [
 e("Colossal Biosciences", "https://colossal.com/",
   "The best-funded de-extinction company, valued in the billions, promising mammoths, thylacines and dodos. Read its own technology pages and the business is clearer than the publicity: the money is in the platform and the spin-outs — editing tools, computational methods, plastic-degrading enzymes — and the animal is the reason anyone funds them. Its conservation claims are contested by conservation biologists, largely on the grounds that the money would save more species spent otherwise.",
   ["deextinct:ventures","deextinct:rescue"]),
 e("Living Carbon", "https://www.livingcarbon.com/",
   "Engineered poplars intended to grow faster and store more carbon, planted on private land in the United States. It is the first company to plant an engineered forest tree for climate purposes at commercial scale, and it did so without the multi-year review a crop would face, because trees planted on private land under the US carve-out fall outside it. Forest trees outlive the companies that plant them and spread pollen for miles.",
   ["deextinct:trees","money:markets"])]

IND2["BRA"] = [
 e("Suzano / FuturaGene", "https://www.suzano.com.br/en/",
   "The world’s largest pulp producer, growing engineered eucalyptus approved in Brazil for commercial planting. It is the first engineered forest tree commercialised anywhere, on plantations measured in millions of hectares. Trees are not annual crops: they flower for decades, spread pollen for kilometres, and outlast every company and regulator involved in approving them.",
   ["deextinct:trees","seed:traits"])]

# ================================================ HUMAN CLINICAL & THERAPY ====
IND2["CHE"] = [
 e("Novartis \u2014 gene therapy", "https://www.novartis.com/",
   "Sells Zolgensma, a one-dose gene therapy for spinal muscular atrophy, at over two million dollars. Novartis is the case that makes the pricing argument concrete: a company of this size, with this much manufacturing capacity, still prices a single-dose cure at the outer edge of what health systems will pay — which is a decision about what the market will bear, not what the treatment costs.",
   ["clinical:therapy","money:markets"])]

IND2["USA"] = IND2["USA"] + [
 e("Vertex / CRISPR Therapeutics \u2014 Casgevy", "https://www.crisprtx.com/",
   "The first CRISPR therapy approved anywhere, for sickle cell disease and beta-thalassemia, listed at over two million dollars per patient. The scientific credit sits with the academic founders; the pricing decision sits here. Sickle cell is overwhelmingly a West African and Indian disease, and the cure for it was built for American insurance — which decides who gets fixed before any laboratory work begins.",
   ["clinical:therapy","editing:platform"]),
 e("ClinicalTrials.gov", "https://clinicaltrials.gov/",
   "The register that makes the clinical facet knowable. Essentially every interventional trial run in or submitted to the United States must be registered, with sponsor, phase, condition and sites. It exists because sponsors were found abandoning trials with unfavourable results unpublished, and Congress legislated. Every other facet on this map is argued about using figures the industry chose to release; this one is not, and the difference is a law.",
   ["clinical:trials","clinical:germline"], base=REGI)]

# ========================================================= ASSISTED REPRO =====
IND2["GBR"] = IND2["GBR"] + [
 e("HFEA \u2014 licensed clinic register", "https://www.hfea.gov.uk/choose-a-clinic/clinic-search/",
   "The UK fertility regulator’s public register, with every licensed clinic, its inspection history and its ratings of the optional add-on treatments clinics sell. Most add-ons are rated red or amber — no good evidence they work — and they continue to be sold. It is the most transparent fertility regulator in the world, and this is what transparency alone achieves without the power to prohibit.",
   ["repro:clinics","rules:regulators"], base=REGI)]

IND2["ESP"] = [
 e("IVIRMA Global", "https://ivirma.com/",
   "One of the largest fertility groups in the world, operating clinics across dozens of countries and running its own research institute. Fertility care is consolidating into international chains, so treatment protocols, add-on offerings and pricing are increasingly set at group level rather than by the clinic a patient walks into.",
   ["repro:clinics","repro:surrogacy"])]

IND2["USA"] = IND2["USA"] + [
 e("Orchid Health", "https://www.orchidhealth.com/",
   "Sells whole-genome screening of IVF embryos, including polygenic scores for conditions with no single cause. Professional genetics bodies have stated the science does not support this clinically. It is sold anyway, because embryo selection faces none of the approval requirements a drug or a device would — the gap between what the evidence supports and what may lawfully be sold is the whole business, and it is widening.",
   ["repro:screening","clinical:germline"]),
 e("CDC ART clinic data", "https://www.cdc.gov/art/",
   "The clinic-by-clinic outcome data behind US fertility reporting: cycles, transfers, live births. It is the only place a prospective patient can compare clinics on results. The catch is structural — success rates depend heavily on which patients a clinic accepts, so a clinic can raise its published figures by declining harder cases, and the data cannot show you that.",
   ["repro:clinics","rules:regulators"], base=REGI)]

# ========================================================== MONEY & BACKERS ===
IND2["USA"] = IND2["USA"] + [
 e("Gates Foundation \u2014 committed grants database", "https://www.gatesfoundation.org/about/committed-grants",
   "Every grant the foundation has committed, searchable by recipient and amount. It matters because philanthropy is among the largest funders of putting engineered organisms into the ground in low-income countries — which means the usual test of whether farmers want a product, that they buy it, never happens. This database is how you find out who was paid to do what, and it is unusually complete for a private funder.",
   ["money:philanthropy","money:public"], base=REGI),
 e("DARPA \u2014 Biological Technologies Office", "https://www.darpa.mil/research/offices/biological-technologies",
   "The US defence research agency’s biology programme, funding gene drives, engineered insects that deliver genes to crops in the field, and rapid biological manufacturing. Every country doing this work funds some of it through defence, and defence agencies sit outside the civilian biosafety oversight that applies to everyone else. DARPA is simply the one that publishes what it funds.",
   ["money:defence","wild:drives"], base=REGI)]

# =========================================== RULES, RECORDS & ADVOCACY ========
IND2["USA"] = IND2["USA"] + [
 e("BIO \u2014 Biotechnology Innovation Organization", "https://www.bio.org/",
   "The largest biotechnology trade association in the world, representing over a thousand companies. Trade bodies exist so that positions no single company wants attributed to it can still be advanced — and companies route most of their political money this way, so it is the association’s name, not the member’s, that appears in lobbying registers and lawsuits.",
   ["rules:associations","rules:influence"], base=ASSN),
 e("ISAAA \u2014 GM approval database", "https://www.isaaa.org/gmapprovaldatabase/",
   "The most-cited record of which engineered events are approved where, used by supporters and opponents alike because little else covers the same ground. It is also produced by an organisation funded substantially by the industry it reports on. The data is useful and the framing is promotional, and both should be said at once — which is the ordinary condition of information in this field.",
   ["rules:influence","rules:standards"], base=ASSN)]

IND2["BEL"] = [
 e("CropLife International", "https://croplife.org/",
   "The trade association of the four majors and their peers, coordinating industry positions on pesticide and biotechnology regulation worldwide. Its member fees exceed what most members declare in lobbying spend in their own names. An association can hold a position no individual company wants recorded against it.",
   ["rules:associations","rules:influence"], base=ASSN)]

IND2["FRA"] = [
 e("OECD BioTrack", "https://biotrackproductdatabase.oecd.org/",
   "The international register of approved biotechnology products, and the source of the unique identifiers that let one country’s approval be matched to another’s. Its usefulness is also where it fails: gene-edited organisms deregulated under national carve-outs never receive an identifier, so the class of product growing fastest is precisely the class this system cannot follow.",
   ["rules:standards","rules:regulators"], base=REGI)]
