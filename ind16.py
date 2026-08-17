# -*- coding: utf-8 -*-
"""Industry entries, part 16."""
from ind1 import e, CO, BODY, REGI, ASSN

IND16 = {}

# ========================================================= HUMAN CLINICAL =====
IND16["USA"] = [
 e("Regeneron Genetics Center", "https://www.regeneron.com/science/genetics-center",
   "Sequences the genomes of hundreds of thousands of volunteers linked to health records, in partnership with health systems including a large US one and the UK Biobank. Private companies now hold population-scale genomic datasets assembled with public and patient cooperation.",
   ["synthesis:seq","clinical:trials","money:markets"]),
 e("bluebird bio \u2014 the insertional oncogenesis cases", "https://www.fda.gov/vaccines-blood-biologics/safety-availability-biologics",
   "Patients treated with the company’s gene therapy later developed blood cancers, and trials were paused while whether the vector caused them was investigated. A therapy that inserts DNA into a patient’s genome can land somewhere that matters, and these are the documented cases.",
   ["clinical:therapy","clinical:vectors","rules:regulators"], base=REGI),
 e("Moderna", "https://www.modernatx.com/",
   "Built on messenger RNA delivered in lipid nanoparticles, and now applying the same platform beyond vaccines to cancer, rare disease and protein replacement. The mRNA itself is synthesised chemically rather than grown in an organism, which is why these products are regulated as medicines and never appear in a GMO debate — the instruction is engineered and nothing living is. It is the clearest case on this map of a technology reaching billions of people while sitting outside every framework built for engineered organisms.",
   ["clinical:therapy","cro:cdmo","editing:platform"]),
 e("Institute for Clinical and Economic Review", "https://icer.org/",
   "An independent US body that assesses whether a treatment's price is justified by its benefit, and has published on gene therapies priced in the millions. It has no legal power at all; its reports are used in negotiations because nobody else publishes the analysis, which makes a small non-profit a de facto price reference in a country with no formal one.",
   ["clinical:therapy","money:markets"], base=BODY)]

IND16["CHE"] = [
 e("CRISPR Therapeutics", "https://crisprtx.com/",
   "Co-developed Casgevy with Vertex, the first CRISPR therapy approved anywhere, cleared in the UK and US in late 2023 for sickle cell disease and beta thalassaemia. The company was co-founded by Emmanuelle Charpentier, so a share of the foundational patents and the first approved product sit in the same lineage. The treatment works: it edits a patient's own blood stem cells outside the body and returns them. It also costs over two million dollars per patient and requires a transplant-capable hospital, which means the disease it cures most often occurs in places that cannot deliver it — the sharpest example on this map of a technology working and reaching almost nobody.",
   ["editing:platform","clinical:therapy","editing:patents"])]

# ================================================================ MONEY =======
IND16["USA"] = IND16["USA"] + [
 e("a16z Bio + Health", "https://a16z.com/bio-health/",
   "The biology arm of a large venture firm, funding companies across editing, synthetic biology and health software. Venture capital decides which of these technologies gets built before any regulator sees them, on a return horizon of seven to ten years — which favours products with a clear buyer and a short path, and disfavours anything whose value shows up as harm avoided.",
   ["money:vc","editing:synbio"]),
 e("NIH RePORTER", "https://reporter.nih.gov/",
   "Every NIH grant, searchable by investigator, institution and amount. It is the most complete public record anywhere of who is paid to do biological research, and the practical starting point for tracing where a technology on this map came from — nearly every platform here traces back to a grant number that can be looked up. Comparable databases exist for almost no other funder, so the American record is disproportionately visible and everyone else's work is harder to see.",
   ["money:public","editing:platform","clinical:trials"], base=REGI),
 e("BARDA \u2014 Biomedical Advanced Research and Development Authority", "https://medicalcountermeasures.gov/barda/",
   "Buys vaccines, antibodies and antivirals for the US national stockpile, and is the largest single customer for engineered medical countermeasures anywhere. A guaranteed government purchase is what makes an unprofitable product get built: a drug used rarely, briefly and held in reserve cannot repay its own development, so procurement rather than science decides which threats the world is prepared for.",
   ["money:public","money:defence","cro:cdmo"], base=REGI)]

IND16["SGP"] = [
 e("Temasek \u2014 agri-food and life sciences", "https://www.temasek.com.sg/",
   "Singapore's state investment company, an early and large backer of cultivated meat and precision fermentation. Singapore approved cultivated meat before anywhere else and its sovereign fund had invested in the sector beforehand, which is state industrial policy and a regulatory decision arriving in the same country.",
   ["money:vc","money:public","editing:synbio"])]

# ============================================ LIVESTOCK, AQUACULTURE, PETS ====
IND16["USA"] = IND16["USA"] + [
 e("Alliance for Science / Cornell \u2014 agricultural biotechnology communications", "https://allianceforscience.org/",
   "A communications programme promoting agricultural biotechnology, hosted at a university and funded substantially by the Gates Foundation. Advocacy carrying a university's name is read differently from advocacy carrying a company's, and the funding is disclosed.",
   ["rules:influence","rules:associations"], base=ASSN),
 e("Zoetis", "https://www.zoetis.com/",
   "The largest animal health company in the world, spun out of Pfizer, selling vaccines and medicines for livestock and pets. Animal health products are how intensive production is sustained, which puts this company upstream of the conditions that edited disease resistance is designed to tolerate.",
   ["livestock:livestock","clinical:vectors"]),
 e("Neogen", "https://www.neogen.com/",
   "Supplies food safety testing including strip tests for engineered material, used at grain elevators and processing plants to accept or reject a load in minutes. Rapid tests are where a labelling threshold meets a lorry: the decision is made on the spot by a technician with a disposable device, and everything downstream follows from it.",
   ["synthesis:reagents","rules:standards","livestock:livestock"])]

IND16["NZL"] = [
 e("Fonterra", "https://www.fonterra.com/",
   "A New Zealand dairy cooperative, one of the largest dairy exporters in the world, owned by its farmers. New Zealand permits no GM cultivation, and its export position depends partly on that status — which makes the country’s restriction a commercial asset as well as a policy.",
   ["livestock:livestock","seed:distribution"])]

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND16["USA"] = IND16["USA"] + [
 e("Revive & Restore \u2014 black-footed ferret cloning", "https://reviverestore.org/projects/black-footed-ferret/",
   "The cloned ferrets were produced from cells frozen in 1988 from an animal with no living descendants, returning genetic variation that the surviving population had lost entirely. It is the first case of cloning used to address inbreeding in an endangered species rather than to recreate an extinct one, and the material existed only because somebody banked it thirty years earlier.",
   ["deextinct:rescue","deextinct:biobank","livestock:cloning"], base=BODY),
 e("Oxitec \u2014 US releases and EPA experimental use permits", "https://www.epa.gov/pesticides",
   "The US permits under which engineered mosquitoes were released in Florida and Texas, with the EPA rather than a biosafety agency as the regulator. An engineered insect is handled as a pesticide in the United States, which determines what review it receives.",
   ["wild:insects","rules:regulators"], base=REGI)]

IND16["CHN"] = [
 e("Guangzhou Wolbaki \u2014 mosquito production", "https://www.wolbaki.com/",
   "Rears Wolbachia-carrying mosquitoes at very large scale for release, in the facility behind the Guangzhou trials that suppressed local Aedes albopictus populations. Wolbachia is a bacterium rather than an engineered gene, so these releases sit outside biosafety frameworks entirely while doing what a gene drive is meant to do — which makes them the closest thing to a precedent for the engineered version.",
   ["wild:insects","wild:microbes","cro:cdmo"])]

# ============================================================ NEW TERRITORIES =
IND16["ZAF"] = [
 e("African Centre for Biodiversity \u2014 corporate research", "https://acbio.org.za/",
   "A South African organisation researching seed and agricultural corporations in Africa, publishing on ownership, philanthropy and policy influence. Independent research on this industry from within Africa is scarce, and this is one of the few sustained sources.",
   ["rules:influence","seed:distribution"], base=BODY),
 e("Grain SA and the commercial maize sector", "https://www.grainsa.co.za/",
   "The South African commercial grain producers' organisation, in the country with the highest adoption of engineered maize in Africa and the only one where it is a staple food rather than feed. South Africans eat engineered white maize directly, which makes it the one place where the food-crop argument is not hypothetical.",
   ["seed:distribution","livestock:livestock"], base=ASSN)]

IND16["ARG"] = [
 e("INASE \u2014 seed royalties and farm-saved seed", "https://www.argentina.gob.ar/inase",
   "Argentina’s seed institute, at the centre of a long dispute over whether farmers may save seed and what royalties are owed. Argentina is where the seed-saving argument has been most fiercely contested, because a large share of farmers did save seed and companies attempted to charge on the harvest instead.",
   ["rules:ip","seed:distribution","rules:regulators"], base=REGI)]

IND16["IND"] = [
 e("Federation of Seed Industry of India", "https://www.fsii.in/",
   "The Indian seed industry association, which has argued for trait fee levels against state governments that capped them. Indian states have set Bt cotton seed prices by law, which is one of the few places a government has directly controlled what a trait may be sold for.",
   ["rules:associations","rules:ip","seed:licensees"], base=ASSN)]

IND16["MEX"] = [
 e("CONAHCYT \u2014 native maize and public research", "https://conahcyt.mx/",
   "Mexico’s national science council, funding research on native maize varieties and supporting the government’s position on GM maize imports. Public research money directed at landraces rather than at commercial varieties is unusual and deliberate here.",
   ["money:public","seed:germplasm","rules:regulators"], base=BODY)]
