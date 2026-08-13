# -*- coding: utf-8 -*-
"""Industry entries, part 19. Weighted to the thinnest facets."""
from ind1 import e, CO, BODY, REGI, ASSN

IND19 = {}

# ===================================== INSECTS, MICROBES & OPEN RELEASE =======
IND19["USA"] = [
 e("Pivot Bio \u2014 PROVEN product record", "https://www.pivotbio.com/proven",
   "The nitrogen-fixing microbial product applied across millions of US acres. By area it is among the largest deliberate releases of an engineered organism in history, and it generates no entry in any biosafety register anywhere.",
   ["wild:microbes","seed:distribution"]),
 e("Marrone / Pro Farm Group", "https://profarmgroup.com/",
   "Biological crop protection products, some using engineered microbes. The biologicals sector grew into the regulatory space where the least is required, which is visible in what it chooses to sell.",
   ["wild:microbes","seed:licensees","money:vc"]),
 e("USDA APHIS \u2014 biotechnology regulatory notices", "https://www.aphis.usda.gov/biotechnology/notices",
   "The notices and rule changes through which US biotechnology regulation is actually altered, including the exemptions that removed whole classes of edited plants from oversight. The rulemaking record is public and the comment periods are open.",
   ["rules:regulators","wild:insects"], base=REGI)]

IND19["GBR"] = [
 e("Rothamsted \u2014 GM aphid-repellent wheat trial", "https://www.rothamsted.ac.uk/gm-field-trials",
   "A publicly funded field trial of wheat engineered to repel aphids, which worked in the laboratory and not in the field. The negative result was published, which is rarer than it should be and is the reason this trial is worth knowing about.",
   ["editing:agtech","money:public","wild:insects"], base=BODY)]

IND19["AUS"] = [
 e("CSIRO \u2014 agricultural biotechnology", "https://www.csiro.au/en/research/plants",
   "Australia’s national science agency, which developed the omega-3 canola and safflower traits now commercialised. Public research producing traits that private companies sell is the standard arrangement, and the public share of the return is usually small.",
   ["editing:agtech","money:public","rules:ip"], base=BODY)]

# ================================= DE-EXTINCTION & CONSERVATION BIOTECH =======
IND19["USA"] = IND19["USA"] + [
 e("ViaGen \u2014 Przewalski's horse and endangered species cloning", "https://www.viagen.com/",
   "Cloned Przewalski’s horses from cells banked decades earlier, for a subspecies with almost no remaining genetic diversity. The capability now used for conservation exists because a consumer pet-cloning market paid to develop it.",
   ["deextinct:rescue","livestock:cloning","deextinct:biobank"]),
 e("Wildlife Conservation Society \u2014 biotechnology position", "https://www.wcs.org/",
   "A major conservation organisation’s position on engineered organisms in conservation. The conservation movement is genuinely split on this, and the split runs through organisations rather than between them.",
   ["deextinct:rescue","rules:associations"], base=BODY)]

IND19["ZAF"] = [
 e("Rhino and wildlife biobanking \u2014 BioRescue partners", "https://www.biorescue.org/",
   "The programme attempting to produce northern white rhino embryos from banked material, with two females remaining and no males. It is the clearest test of whether biobanking can recover a species after the population has effectively gone.",
   ["deextinct:rescue","deextinct:biobank","repro:clinics"], base=BODY)]

# ========================================================= HUMAN CLINICAL =====
IND19["USA"] = IND19["USA"] + [
 e("Vertex Pharmaceuticals", "https://www.vrtx.com/",
   "Holds the commercial control of the first approved CRISPR therapy, priced above two million dollars. Sickle cell is overwhelmingly a West African and Indian disease, and the treatment was priced for American insurance.",
   ["clinical:therapy","editing:platform","money:markets"]),
 e("National Marrow Donor Program / NMDP \u2014 cell therapy infrastructure", "https://nmdp.org/",
   "The US registry and network through which stem cell transplants are matched and delivered, now also handling cell therapy logistics. The infrastructure that determines who can physically receive a cell therapy was built for transplants.",
   ["clinical:therapy","clinical:trials"], base=BODY),
 e("Sickle Cell Disease Association of America", "https://www.sicklecelldisease.org/",
   "The patient organisation for a disease with an approved cure most patients cannot obtain. Patient organisations are where the gap between approval and access is documented most concretely.",
   ["clinical:therapy","rules:associations"], base=ASSN)]

IND19["JPN"] = [
 e("PMDA \u2014 regenerative medicine conditional approval", "https://www.pmda.go.jp/english/",
   "Japan grants conditional approval to regenerative medicine products on preliminary evidence, with confirmation required later. Several products approved this way were subsequently found ineffective, and the pathway remains.",
   ["clinical:therapy","rules:regulators"], base=REGI)]

# ================================================================ MONEY =======
IND19["USA"] = IND19["USA"] + [
 e("Fidelity and index funds \u2014 passive ownership of the sector", "https://www.sec.gov/edgar/search/",
   "Index funds hold large stakes in nearly every listed company on this map without choosing any of them. Passive ownership at this scale means the largest shareholders of the industry have no view on it at all.",
   ["money:markets","money:vc"], base=REGI),
 e("Bill & Melinda Gates Agricultural Innovations (Gates Ag One)", "https://www.gatesagone.org/",
   "The foundation’s agricultural vehicle, funding crop development for low-income countries. Philanthropy is among the largest funders of putting engineered organisms into the ground there, so the usual test of whether farmers want a product never happens.",
   ["money:philanthropy","rules:ip","seed:traits"], base=BODY)]

IND19["CHN"] = [
 e("Chinese state agricultural investment \u2014 seed industry revitalisation", "https://www.moa.gov.cn/",
   "State-directed consolidation of Chinese seed companies into larger national champions. Concentration is being produced deliberately as policy rather than emerging through mergers.",
   ["money:public","seed:majors","rules:regulators"], base=REGI)]

# ============================================ CONTRACT RESEARCH ===============
IND19["IND"] = [
 e("Aurigene / Dr Reddy's discovery services", "https://www.aurigene.com/",
   "An Indian contract discovery operation working for international pharmaceutical clients. A large share of the world’s preclinical data is generated in a country whose regulator is not the one reading it.",
   ["cro:cro","clinical:trials"])]

IND19["KOR"] = [
 e("SK pharmteco", "https://www.skpharmteco.com/",
   "A Korean conglomerate’s contract manufacturing arm, including cell and gene therapy production. Manufacturing capacity determines which therapies can exist at scale, and it is concentrating in a few groups.",
   ["cro:cdmo","clinical:vectors"])]

# ================================================ SEED, RULES, TERRITORIES ====
IND19["POL"] = [
 e("Ministry of Agriculture \u2014 GMO cultivation prohibition", "https://www.gov.pl/web/rolnictwo",
   "Poland prohibits the cultivation of engineered crops while importing engineered feed. The objection attaches to growing rather than to eating, which is the distinction most national positions end up making.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND19["MYS"] = [
 e("Malaysian Palm Oil Board \u2014 genome programme", "https://mpob.gov.my/",
   "Sequenced the oil palm genome and identified genes controlling yield, in a public programme. Palm oil is among the most consequential crops in the world for land use, and the research on it is largely state-run.",
   ["editing:agtech","money:public","editing:synbio"], base=BODY)]
