# -*- coding: utf-8 -*-
"""Industry entries, part 13. Weighted to the two facets thinnest against their
real size: contract research and manufacturing, and assisted reproduction."""
from ind1 import e, CO, BODY, REGI, ASSN

IND13 = {}

# ================================ CONTRACT RESEARCH & MANUFACTURING ===========
IND13["USA"] = [
 e("IQVIA", "https://www.iqvia.com/",
   "The largest clinical research organisation in the world, and also one of the largest holders of health data, selling analytics built from prescription and claims records. Running the trials and owning the market data are two businesses that reinforce each other, and the same company does both at a scale no regulator matches.",
   ["cro:cro","clinical:trials","money:markets"]),
 e("Parexel", "https://www.parexel.com/",
   "A large contract research organisation, taken private by investment funds, which runs clinical trials and through a substantial regulatory consulting arm writes and files the submissions that go to the FDA and EMA. The same firm can design the study, run it and argue for it, and none of that appears on the approval, which carries the sponsor's name.",
   ["cro:cro","money:vc","clinical:trials"]),
 e("Catalent", "https://www.catalent.com/",
   "A contract manufacturer making other companies’ medicines, including cell and gene therapies, acquired by Novo Holdings. Manufacturing capacity for genetic medicine is scarce enough that ownership of it determines which therapies can be produced and in what order.",
   ["cro:cdmo","clinical:vectors","money:markets"]),
 e("ICON plc \u2014 site and patient networks", "https://www.iconplc.com/",
   "An Irish contract research organisation running trials worldwide, and the owner of networks of clinical sites and patient recruitment operations. Owning the sites as well as running the trial concentrates the study, the participants and the data in one commercial relationship, which is efficient and removes the independent check a separate site once provided.",
   ["cro:cro","clinical:trials"]),
 e("Fujifilm Diosynth Biotechnologies", "https://fujifilmdiosynth.com/",
   "A biologics contract manufacturer built by a photographic film company on the chemistry it already had — Fujifilm moved into biotechnology as film collapsed, using its expertise in collagen and thin-film coating. It now makes viral vectors and antibodies for other companies at some of the largest sites in Europe and the US, and is one of the reasons manufacturing capacity rather than approval is the constraint on cell and gene therapy.",
   ["cro:cdmo","clinical:vectors"]),
 e("ClinicalTrials.gov \u2014 sponsor and site search", "https://clinicaltrials.gov/search?term=gene%20therapy",
   "The searchable interface to the trial register, by sponsor, site and condition. It is how the clinical facet of this map is compiled at all: 26,240 gene and cell therapy trials, 6,088 lead sponsors, from a public register that exists because a law requires it.",
   ["clinical:trials","cro:cro"], base=REGI)]

IND13["CHN"] = [
 e("Pharmaron", "https://www.pharmaron.com/",
   "A Chinese contract research organisation running preclinical and clinical work for international pharmaceutical clients. A large share of the data Western regulators assess is generated in a country whose own oversight system those regulators do not administer.",
   ["cro:cro","cro:cdmo","animals:services"]),
 e("BGI Genomics \u2014 clinical and prenatal testing", "https://www.bgi.com/global/clinical",
   "Prenatal screening at very large scale, and the operation behind Western government concern about where genetic data ends up. Prenatal testing generates genomic data on people who never consented to research use, which is a question every large provider faces and few answer publicly.",
   ["synthesis:seq","repro:screening","clinical:trials"], trust="medium")]

IND13["KOR"] = [
 e("Celltrion", "https://www.celltrion.com/en-us",
   "A South Korean manufacturer of biosimilars — copies of biological medicines whose patents have expired, each made in engineered cell lines and each requiring its own clinical trials because a living production system cannot be replicated exactly. Biosimilars are why an engineered medicine eventually falls in price, and the reason it takes so long is that copying an organism's product is not the same as copying a molecule.",
   ["cro:cdmo","clinical:therapy"])]

IND13["IND"] = [
 e("Serum Institute of India", "https://www.seruminstitute.com/",
   "The largest vaccine manufacturer in the world by doses, privately owned, supplying a very large share of the vaccines used in low and middle income countries through UNICEF and Gavi. Much of what it makes is recombinant — produced by engineered organisms — including hepatitis B and the HPV vaccine it developed for the Indian market at a fraction of the imported price. One family firm in Pune is a load-bearing part of global immunisation, which is a concentration nobody chose and few discuss.",
   ["cro:cdmo","clinical:vectors"])]

# ========================================== ASSISTED REPRODUCTION =============
IND13["USA"] = IND13["USA"] + [
 e("US Fertility", "https://www.usfertility.com/",
   "One of the largest fertility clinic groups in the United States, private equity backed, operating dozens of practices under separate local names. The CDC publishes success rates clinic by clinic; it does not publish who owns them, so the consolidation of American fertility care into a few backers is visible only by assembling it from outside the register.",
   ["repro:clinics","money:vc"]),
 e("Kindbody", "https://kindbody.com/",
   "A fertility company selling directly to employers as a staff benefit rather than to patients. Routing fertility treatment through an employment package means an employer chooses the provider, the clinical options and the coverage limits for its staff — a purchasing arrangement with no equivalent in most of medicine, and one that ties a reproductive decision to a job.",
   ["repro:clinics","money:vc"]),
 e("Cooper Surgical \u2014 culture media recall", "https://www.fda.gov/medical-devices/medical-device-recalls",
   "The 2024 recall of IVF culture media after embryos failed to develop, with litigation following from families whose cycles were lost. The media is regulated as a device rather than as the environment an embryo develops in, and the difference determines what testing was required beforehand.",
   ["repro:clinics","repro:banks"], base=REGI),
 e("Society for Reproductive Endocrinology and Infertility", "https://www.socrei.org/",
   "The US subspecialty body for fertility medicine, setting practice guidance in a field where almost nothing is set by statute. Embryo screening, the number transferred, donor limits and what may be offered as an add-on are all governed by professional consensus rather than law, which means the profession regulates itself and publishes its own outcome data.",
   ["repro:clinics","rules:associations"], base=ASSN)]

IND13["GBR"] = [
 e("HFEA \u2014 treatment add-ons ratings", "https://www.hfea.gov.uk/treatments/treatment-add-ons/",
   "The UK regulator rates the optional extras fertility clinics sell by the evidence behind them. Most are rated red or amber — no good evidence they work — and they continue to be sold, which is what transparency achieves without the power to prohibit.",
   ["repro:clinics","repro:screening","rules:regulators"], base=REGI),
 e("Care Fertility", "https://www.carefertility.com/",
   "One of the largest fertility groups in the United Kingdom, private equity owned, operating clinics across the UK and Ireland and appearing in the HFEA register under many separate site names. It is the clearest illustration of what consolidation looks like in a register that lists sites rather than owners: the regulator publishes each clinic, and the fact that a dozen of them answer to one balance sheet has to be assembled from elsewhere.",
   ["repro:clinics","money:vc"])]

IND13["ESP"] = [
 e("Spanish Fertility Society \u2014 national registry", "https://www.registrosef.com/",
   "Spain’s fertility registry, in the country that performs more IVF cycles than any other in Europe and receives large numbers of patients from countries where treatments are restricted. The registry counts cycles; it does not count why the patients came.",
   ["repro:clinics","repro:banks"], base=REGI)]

IND13["ISR"] = [
 e("Cross-border surrogacy and gamete brokerage", "https://www.gov.il/en/departments/topics/fertility_treatments",
   "The arrangements through which intended parents obtain eggs, sperm or a surrogate in a country other than their own, chosen because it permits what theirs prohibits. When India, Thailand and Nepal closed to foreign commissioning parents, the trade moved to Ukraine, Georgia and Mexico rather than stopping. Prohibition in one jurisdiction relocates the practice; it does not end it.",
   ["repro:surrogacy","repro:banks","rules:regulators"], base=REGI)]

IND13["AUS"] = [
 e("Monash IVF", "https://monashivf.com/",
   "An Australian fertility group, publicly listed, which has faced litigation and regulatory scrutiny over embryo handling errors including embryos transferred to the wrong patient. Listed ownership means these failures appear in disclosures and share prices as well as in clinical records, which is more visibility than most of this sector produces.",
   ["repro:clinics","money:markets"])]
