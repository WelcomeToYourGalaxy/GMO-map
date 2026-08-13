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
   "Built on mRNA delivery and now applying it beyond vaccines. The company took public money for development and holds the resulting patents, an arrangement disputed in litigation with the NIH over inventorship.",
   ["clinical:therapy","cro:cdmo","editing:platform"]),
 e("Institute for Clinical and Economic Review", "https://icer.org/",
   "An independent body that assesses whether a treatment’s price is justified by its benefit, and has repeatedly found gene therapy prices above what its models support. Its assessments carry no legal force and are cited by payers anyway.",
   ["clinical:therapy","money:markets"], base=BODY)]

IND16["CHE"] = [
 e("CRISPR Therapeutics", "https://crisprtx.com/",
   "Co-developer with Vertex of the first approved CRISPR therapy. The company holds the scientific credit and Vertex holds the commercial control, which is visible in how the revenue splits.",
   ["editing:platform","clinical:therapy","editing:patents"])]

# ================================================================ MONEY =======
IND16["USA"] = IND16["USA"] + [
 e("a16z Bio + Health", "https://a16z.com/bio-health/",
   "The biology arm of a large venture firm, funding companies across therapeutics and agriculture. Venture capital sets a return clock on biological work, and the clock is the same whether the product is a drug or a seed.",
   ["money:vc","editing:synbio"]),
 e("NIH RePORTER", "https://reporter.nih.gov/",
   "Every NIH grant, searchable by investigator, institution and amount. Public funding shapes which questions get asked years before any company exists, and this is where that is traceable.",
   ["money:public","editing:platform","clinical:trials"], base=REGI),
 e("BARDA \u2014 Biomedical Advanced Research and Development Authority", "https://medicalcountermeasures.gov/barda/",
   "US government funding for medical countermeasures, including vaccine and therapeutic platforms. Defence and preparedness money funds a substantial share of the technology later commercialised privately.",
   ["money:public","money:defence","cro:cdmo"], base=REGI)]

IND16["SGP"] = [
 e("Temasek \u2014 agri-food and life sciences", "https://www.temasek.com.sg/",
   "Singapore’s state investment company, holding large positions in agricultural and food technology worldwide. State capital investing for food security behaves differently from venture capital, and it is a growing share of the money in this field.",
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
   "Supplies food safety testing including tests for engineered material in grain and seed. Detection is a purchased product, so the ability to find unauthorised GM presence depends on someone buying the test.",
   ["synthesis:reagents","rules:standards","livestock:livestock"])]

IND16["NZL"] = [
 e("Fonterra", "https://www.fonterra.com/",
   "A New Zealand dairy cooperative, one of the largest dairy exporters in the world, owned by its farmers. New Zealand permits no GM cultivation, and its export position depends partly on that status — which makes the country’s restriction a commercial asset as well as a policy.",
   ["livestock:livestock","seed:distribution"])]

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND16["USA"] = IND16["USA"] + [
 e("Revive & Restore \u2014 black-footed ferret cloning", "https://reviverestore.org/projects/black-footed-ferret/",
   "The cloned ferrets were produced from cells frozen in 1988, decades before cloning them was possible. Banking material whose use has not been invented yet is the whole argument for cryobanking, and this is the case that demonstrates it.",
   ["deextinct:rescue","deextinct:biobank","livestock:cloning"], base=BODY),
 e("Oxitec \u2014 US releases and EPA experimental use permits", "https://www.epa.gov/pesticides",
   "The US permits under which engineered mosquitoes were released in Florida and Texas, with the EPA rather than a biosafety agency as the regulator. An engineered insect is handled as a pesticide in the United States, which determines what review it receives.",
   ["wild:insects","rules:regulators"], base=REGI)]

IND16["CHN"] = [
 e("Guangzhou Wolbaki \u2014 mosquito production", "https://www.wolbaki.com/",
   "A Chinese facility rearing Wolbachia-carrying mosquitoes at very large scale for release. Rearing capacity is the practical limit on any release programme, and China has built more of it than anyone.",
   ["wild:insects","wild:microbes","cro:cdmo"])]

# ============================================================ NEW TERRITORIES =
IND16["ZAF"] = [
 e("African Centre for Biodiversity \u2014 corporate research", "https://acbio.org.za/",
   "A South African organisation researching seed and agricultural corporations in Africa, publishing on ownership, philanthropy and policy influence. Independent research on this industry from within Africa is scarce, and this is one of the few sustained sources.",
   ["rules:influence","seed:distribution"], base=BODY),
 e("Grain SA and the commercial maize sector", "https://www.grainsa.co.za/",
   "The South African commercial grain producers’ organisation, in the country where engineered white maize is a human staple. Farmer organisations are where adoption decisions are argued out in practice, and their positions are public.",
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
