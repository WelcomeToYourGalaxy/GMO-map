# -*- coding: utf-8 -*-
"""Industry entries, part 19. Weighted to the thinnest facets."""
from ind1 import e, CO, BODY, REGI, ASSN

IND19 = {}

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND19["USA"] = [
 e("Pivot Bio \u2014 PROVEN product record", "https://www.pivotbio.com/proven",
   "A nitrogen-fixing microbial product applied across millions of US acres, using engineered soil bacteria that supply nitrogen to maize directly. It is one of the largest deliberate releases of engineered microorganisms into open farmland anywhere, registered as a crop input, and it attracts almost none of the attention an engineered plant would.",
   ["wild:microbes","seed:distribution"]),
 e("Marrone / Pro Farm Group", "https://profarmgroup.com/",
   "Biological crop protection products — microbes and microbial extracts applied to fields instead of synthetic pesticides, some of them engineered. Biologicals are registered as pesticides rather than as releases, which is a faster and cheaper route than an engineered plant takes for a product that is also a living organism spread deliberately across farmland.",
   ["wild:microbes","seed:licensees","money:vc"]),
 e("USDA APHIS \u2014 biotechnology regulatory notices", "https://www.aphis.usda.gov/biotechnology/notices",
   "The notices and rule changes through which US oversight of engineered plants has been rewritten, most substantially by the SECURE rule of 2020. That rule let developers themselves determine whether a plant is exempt, with the agency confirming rather than assessing — which moved the initial judgement from the regulator to the company and is why the count of reviewed products fell sharply afterwards.",
   ["rules:regulators","wild:insects"], base=REGI)]

IND19["GBR"] = [
 e("Rothamsted \u2014 GM aphid-repellent wheat trial", "https://www.rothamsted.ac.uk/gm-field-trials",
   "A publicly funded field trial of wheat engineered to emit an aphid alarm pheromone, which drew protest, an attempted crop destruction and a fenced security cordon costing more than the science. The wheat did not repel aphids in the field. Both halves matter: a public trial conducted openly, at great cost, that produced a negative result and published it.",
   ["editing:agtech","money:public","wild:insects"], base=BODY)]

IND19["AUS"] = [
 e("CSIRO \u2014 agricultural biotechnology", "https://www.csiro.au/en/research/plants",
   "Australia’s national science agency, which developed the omega-3 canola and safflower traits now commercialised. Public research producing traits that private companies sell is the standard arrangement, and the public share of the return is usually small.",
   ["editing:agtech","money:public","rules:ip"], base=BODY)]

# ================================= DE-EXTINCTION & CONSERVATION BIOTECH =======
IND19["USA"] = IND19["USA"] + [
 e("ViaGen \u2014 Przewalski's horse and endangered species cloning", "https://www.viagen.com/",
   "Cloned Przewalski's horses from cells banked in the 1980s, reintroducing genetic diversity that had been lost from the living population entirely. The same company clones pet dogs and cats commercially. Conservation cloning and pet cloning are the same laboratory procedure sold to different buyers, and the commercial side is what pays for the capability.",
   ["deextinct:rescue","livestock:cloning","deextinct:biobank"]),
 e("Wildlife Conservation Society \u2014 biotechnology position", "https://www.wcs.org/",
   "One of the largest conservation organisations, and among the first to set out a position on engineered organisms in wild systems. Conservation is genuinely split here: gene drives and engineered resistance could save species from invasive predators and disease, and they are also irreversible releases into places chosen precisely because they are not managed. The argument runs inside the movement rather than between it and industry.",
   ["deextinct:rescue","rules:associations"], base=BODY)]

IND19["ZAF"] = [
 e("Rhino and wildlife biobanking \u2014 BioRescue partners", "https://www.biorescue.org/",
   "The programme attempting to produce northern white rhinos from banked cells and harvested eggs, with two females alive and no males. It has created viable embryos and has not yet produced a calf. If it works it is the first species brought back from functional extinction; if it does not, it is the clearest demonstration that banking material is not the same as saving a species.",
   ["deextinct:rescue","deextinct:biobank","repro:clinics"], base=BODY)]

# ========================================================= HUMAN CLINICAL =====
IND19["USA"] = IND19["USA"] + [
 e("Vertex Pharmaceuticals", "https://www.vrtx.com/",
   "Holds commercial control of Casgevy, the first approved CRISPR therapy, developed with CRISPR Therapeutics. Vertex is the partner that took it through approval and sets the price, and its earlier cystic fibrosis franchise is the template: a small patient population, an extremely high price, and a payer system reorganised around a single company's product. The same model applied to a curable genetic disease is what the sickle cell rollout is now testing.",
   ["clinical:therapy","editing:platform","money:markets"]),
 e("National Marrow Donor Program / NMDP \u2014 cell therapy infrastructure", "https://nmdp.org/",
   "The US registry through which unrelated stem cell donors are matched to patients, and the infrastructure gene therapies for blood disorders depend on. Casgevy and its equivalents need the same capability — conditioning, apheresis, a specialist transplant unit — so a cure delivered as edited cells can only reach patients where that system already exists, which is a smaller map than the disease.",
   ["clinical:therapy","clinical:trials"], base=BODY),
 e("Sickle Cell Disease Association of America", "https://www.sicklecelldisease.org/",
   "The patient organisation for a disease with an approved cure that almost no patient can obtain. Casgevy costs over two million dollars and requires chemotherapy conditioning and a transplant-capable hospital; sickle cell is most common in sub-Saharan Africa and, in the United States, among Black Americans, and it was for decades among the least funded conditions relative to its burden. The gap between an approval and a treated patient is the whole subject here, and this is the organisation that has to argue it.",
   ["clinical:therapy","rules:associations"], base=ASSN)]

IND19["JPN"] = [
 e("PMDA \u2014 regenerative medicine conditional approval", "https://www.pmda.go.jp/english/",
   "Japan grants conditional, time-limited approval to regenerative and cell therapies on evidence of safety and probable benefit, with efficacy confirmed afterwards. It is the most permissive route of its kind in a major jurisdiction, and it is the live experiment in whether approving early gets treatments to patients sooner or gets ineffective ones onto the market.",
   ["clinical:therapy","rules:regulators"], base=REGI)]

# ================================================================ MONEY =======
IND19["USA"] = IND19["USA"] + [
 e("Fidelity and index funds \u2014 passive ownership of the sector", "https://www.sec.gov/edgar/search/",
   "Index funds hold large stakes in nearly every listed company on this map at once, because they hold the index rather than choosing companies. The consequence is that the same handful of managers are simultaneously among the largest owners of firms that compete with each other — a concentration produced by a savings product, examined by no merger review, and voted at every annual meeting.",
   ["money:markets","money:vc"], base=REGI),
 e("Bill & Melinda Gates Agricultural Innovations (Gates Ag One)", "https://www.gatesagone.org/",
   "The foundation’s agricultural vehicle, funding crop development for low-income countries. Philanthropy is among the largest funders of putting engineered organisms into the ground there, so the usual test of whether farmers want a product never happens.",
   ["money:philanthropy","rules:ip","seed:traits"], base=BODY)]

IND19["CHN"] = [
 e("Chinese state agricultural investment \u2014 seed industry revitalisation", "https://www.moa.gov.cn/",
   "State-directed consolidation of Chinese seed companies into a smaller number of national champions, through Sinochem, COFCO and provincial funds. The stated aim is seed self-sufficiency: China imports a large share of its maize and soy genetics and treats that as a strategic exposure. Consolidation here is industrial policy, where the same concentration elsewhere is the residue of private mergers.",
   ["money:public","seed:majors","rules:regulators"], base=REGI)]

# ============================================ CONTRACT RESEARCH ===============
IND19["IND"] = [
 e("Aurigene / Dr Reddy's discovery services", "https://www.aurigene.com/",
   "An Indian contract discovery operation running early-stage work for international pharmaceutical companies. Discovery outsourcing means the earliest decisions about what to develop — which target, which molecule, which disease — are increasingly taken in laboratories that will never appear on the resulting approval.",
   ["cro:cro","clinical:trials"])]

IND19["KOR"] = [
 e("SK pharmteco", "https://www.skpharmteco.com/",
   "The contract manufacturing arm of a Korean conglomerate, making cell and gene therapies and their viral vectors for other companies. Asian manufacturing capacity of this kind is why a therapy approved in the United States may be physically produced somewhere with no say in whether it was approved.",
   ["cro:cdmo","clinical:vectors"])]

# ================================================ SEED, RULES, TERRITORIES ====
IND19["POL"] = [
 e("Ministry of Agriculture \u2014 GMO cultivation prohibition", "https://www.gov.pl/web/rolnictwo",
   "Poland prohibits the cultivation of engineered crops while importing engineered feed. The objection attaches to growing rather than to eating, which is the distinction most national positions end up making.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND19["MYS"] = [
 e("Malaysian Palm Oil Board \u2014 genome programme", "https://mpob.gov.my/",
   "Sequenced the oil palm genome and identified the single gene controlling shell thickness, which determines oil yield per fruit. A test for that gene lets a planter reject unproductive seedlings before planting a tree that occupies land for twenty-five years. It is the clearest case of genomics changing a plantation crop without any engineering — the knowledge alone was worth the programme.",
   ["editing:agtech","money:public","editing:synbio"], base=BODY)]
