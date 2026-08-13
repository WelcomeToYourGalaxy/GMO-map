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
   "A large contract research organisation, taken private by investment firms. Private equity ownership of the companies generating regulatory evidence adds a return expectation to a business already paid by the party being assessed.",
   ["cro:cro","money:vc","clinical:trials"]),
 e("Catalent", "https://www.catalent.com/",
   "A contract manufacturer making other companies’ medicines, including cell and gene therapies, acquired by Novo Holdings. Manufacturing capacity for genetic medicine is scarce enough that ownership of it determines which therapies can be produced and in what order.",
   ["cro:cdmo","clinical:vectors","money:markets"]),
 e("ICON plc \u2014 site and patient networks", "https://www.iconplc.com/",
   "An Irish contract research organisation running trials through its own network of sites and recruited patients. Owning the sites as well as the trial management means one company controls both where a study happens and who is enrolled in it.",
   ["cro:cro","clinical:trials"]),
 e("Fujifilm Diosynth Biotechnologies", "https://fujifilmdiosynth.com/",
   "A biologics contract manufacturer built by a photographic film company that redeployed its chemistry into biotechnology. It is one of a handful of firms with capacity at the scale genetic medicines need.",
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
   "A South Korean biosimilars manufacturer, producing copies of biologic drugs after patent expiry. Biosimilar competition is the main mechanism by which biologic prices fall at all, and it arrives only when exclusivity ends.",
   ["cro:cdmo","clinical:therapy"])]

IND13["IND"] = [
 e("Serum Institute of India", "https://www.seruminstitute.com/",
   "The largest vaccine manufacturer in the world by doses, privately owned. Volume at this scale determines who gets vaccinated during a shortage more directly than any pricing commitment does.",
   ["cro:cdmo","clinical:vectors"])]

# ========================================== ASSISTED REPRODUCTION =============
IND13["USA"] = IND13["USA"] + [
 e("US Fertility", "https://www.usfertility.com/",
   "One of the largest fertility clinic groups in the United States, backed by private equity. Ownership at this level sets pricing, which add-ons are offered and which patients are accepted, across many clinics at once.",
   ["repro:clinics","money:vc"]),
 e("Kindbody", "https://kindbody.com/",
   "A fertility company selling directly to employers as a benefit rather than to patients as a treatment. The purchaser is an employer, which puts a commercial third party between a person and their reproductive care.",
   ["repro:clinics","money:vc"]),
 e("Cooper Surgical \u2014 culture media recall", "https://www.fda.gov/medical-devices/medical-device-recalls",
   "The 2024 recall of IVF culture media after embryos failed to develop, with litigation following from families whose cycles were lost. The media is regulated as a device rather than as the environment an embryo develops in, and the difference determines what testing was required beforehand.",
   ["repro:clinics","repro:banks"], base=REGI),
 e("Society for Reproductive Endocrinology and Infertility", "https://www.socrei.org/",
   "The US subspecialty body for fertility medicine, setting practice standards for a field largely governed by its own guidance. Professional self-regulation covers most of what US clinics do, and it carries no enforcement.",
   ["repro:clinics","rules:associations"], base=ASSN)]

IND13["GBR"] = [
 e("HFEA \u2014 treatment add-ons ratings", "https://www.hfea.gov.uk/treatments/treatment-add-ons/",
   "The UK regulator rates the optional extras fertility clinics sell by the evidence behind them. Most are rated red or amber — no good evidence they work — and they continue to be sold, which is what transparency achieves without the power to prohibit.",
   ["repro:clinics","repro:screening","rules:regulators"], base=REGI),
 e("Care Fertility", "https://www.carefertility.com/",
   "A large UK fertility group, private equity owned, operating clinics across Britain and Ireland. It sells add-ons the regulator rates as unevidenced, lawfully, because rating is not restricting.",
   ["repro:clinics","money:vc"])]

IND13["ESP"] = [
 e("Spanish Fertility Society \u2014 national registry", "https://www.registrosef.com/",
   "Spain’s fertility registry, in the country that performs more IVF cycles than any other in Europe and receives large numbers of patients from countries where treatments are restricted. The registry counts cycles; it does not count why the patients came.",
   ["repro:clinics","repro:banks"], base=REGI)]

IND13["ISR"] = [
 e("Cross-border surrogacy and gamete brokerage", "https://www.gov.il/en/departments/topics/fertility_treatments",
   "The arrangements through which intended parents obtain gametes and surrogacy in countries other than their own. A national prohibition becomes a travel itinerary, and the broker sitting between jurisdictions is regulated by neither.",
   ["repro:surrogacy","repro:banks","rules:regulators"], base=REGI)]

IND13["AUS"] = [
 e("Monash IVF", "https://monashivf.com/",
   "An Australian fertility group, listed, which has faced litigation over embryo screening errors including embryos wrongly identified as abnormal and discarded. The errors became public through court rather than through any reporting requirement.",
   ["repro:clinics","money:markets"])]
