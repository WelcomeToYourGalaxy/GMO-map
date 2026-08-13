# -*- coding: utf-8 -*-
"""Animal experimentation facilities.

There is no global register of these. The closest things that exist are national
and partial: the USDA publishes an annual list of registered research facilities
with the animals each used, the UK Home Office publishes establishment licences
and annual procedure statistics, and the EU publishes non-technical project
summaries. None of them covers the world, none uses the same categories, and
mice and rats — the overwhelming majority of animals used — are excluded from the
US count entirely by statute.

So this is a curated set of the largest and best-documented facilities and
suppliers rather than a survey. Every entry links to something the institution
publishes about itself, and the gap is stated in the map rather than papered
over.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND11 = {}

# ---------------------------------------------------- the national registers --
IND11["USA"] = [
 e("USDA APHIS \u2014 annual research facility reports", "https://www.aphis.usda.gov/livestock-poultry-disease/annual-report-animal-usage-research-facility",
   "Every registered US research facility reports annually how many dogs, cats, primates and other covered animals it used, and by what pain category. The reports are published per facility. They also exclude mice, rats and birds bred for research, which are the overwhelming majority — so the most detailed animal-use record in the United States omits most of the animals.",
   ["animals:models","animals:breeders","rules:regulators"], base=REGI),
 e("Charles River \u2014 global site network", "https://www.criver.com/about-us/locations",
   "Breeding, holding and testing sites across North America, Europe and Asia, which is what lets one company supply animals and run the studies on them in the same corporate structure. The site list is public through inspection records in some countries and nowhere near it in others.",
   ["animals:breeders","animals:services","cro:cro"]),
 e("Jackson Laboratory \u2014 Bar Harbor", "https://www.jax.org/about-us/our-locations",
   "The Maine campus where the strain collection is maintained and distributed, one of a small number of places in the world holding a genetic archive of this size. A fire in 1989 destroyed part of the colony and strains were rebuilt from material other laboratories had received — the distribution network turned out to be the backup.",
   ["animals:models","animals:breeders"], base=BODY),
 e("Wisconsin National Primate Research Center", "https://www.primate.wisc.edu/",
   "One of seven federally funded US primate centres, holding several thousand monkeys. Primates are covered by the Animal Welfare Act, so numbers, procedures and inspection findings are public here in a way they are not for rodents — the difference is statutory, not practical.",
   ["animals:primates","animals:breeders","money:public"], base=BODY),
 e("Inotiv \u2014 facility network", "https://www.inotiv.com/locations",
   "The sites of the company formerly trading as Envigo, including the Virginia beagle facility from which around four thousand dogs were removed by federal seizure in 2022. Inspection reports documenting the violations were published for years beforehand.",
   ["animals:breeders","cro:cro"])]

# ------------------------------------------------------------- United Kingdom -
IND11["GBR"] = [
 e("Home Office \u2014 licensed establishments", "https://www.gov.uk/guidance/research-and-testing-using-animals",
   "Every UK establishment licensed to use animals in research is named in a public list, alongside the annual procedure statistics. Naming the places, not just counting the procedures, is a level of disclosure no other large research system matches.",
   ["animals:models","animals:breeders","rules:regulators"], base=REGI),
 e("The Francis Crick Institute \u2014 animal research", "https://www.crick.ac.uk/research/find-a-researcher/animal-research",
   "One of the largest biomedical research institutes in Europe, which publishes its animal numbers and describes the work under the UK Concordat on openness. Voluntary disclosure by an institution of this scale sets what other institutions can be asked for.",
   ["animals:models","money:public"], base=BODY)]

# --------------------------------------------------------------------- Europe -
IND11["DEU"] = [
 e("German Primate Center (DPZ)", "https://www.dpz.eu/en/home.html",
   "Germany’s national primate research centre, holding monkeys for neuroscience and infection research, and the subject of sustained legal and public challenge. German courts have ruled on whether specific experiments could proceed, which makes this one of the few places the question has been tested in law rather than in policy.",
   ["animals:primates","money:public"], base=BODY)]

IND11["NLD"] = [
 e("Biomedical Primate Research Centre", "https://www.bprc.nl/en",
   "The Dutch national primate centre, which has been under government pressure to reduce and eventually end primate research and has published reduction targets. A state-funded facility being wound down on political instruction is a different mechanism from any regulator refusing a licence.",
   ["animals:primates","money:public"], base=BODY)]

IND11["FRA"] = [
 e("Charles River / Janvier \u2014 European breeding sites", "https://janvier-labs.com/en/contact/",
   "The European rodent breeding operations supplying research across the continent. EU law requires member states to collect and publish animal-use statistics, so the scale of what these sites supply is visible in aggregate through ALURES.",
   ["animals:breeders","animals:models"])]

# ----------------------------------------------------------------------- Asia -
IND11["CHN"] = [
 e("Guangdong / Hainan primate breeding sector", "https://www.chinacdc.cn/en/",
   "China’s primate breeding industry, which supplies a large share of the world’s research monkeys and restricted exports during the pandemic — causing shortages and price rises in American laboratories. Research capacity in one country turned out to depend on animal supply from another.",
   ["animals:primates","animals:breeders"], base=CO, trust="medium"),
 e("Cyagen \u2014 Suzhou and Santa Clara facilities", "https://www.cyagen.com/us/en/contact-us",
   "Production sites for custom engineered mice on two continents, serving clients who commission animals without holding any facility themselves. The resulting lines often appear in no public catalogue, so the animals exist and the strains do not enter the shared record.",
   ["animals:services","animals:models"])]

IND11["JPN"] = [
 e("RIKEN BioResource Research Center", "https://web.brc.riken.jp/en/",
   "Japan’s national repository for engineered mice, cell lines and plant material, distributing to researchers worldwide. Japan publishes no national count of animals used in research, so a public repository of this size sits inside a system that does not report its own scale.",
   ["animals:models","synthesis:repos"], base=BODY)]

IND11["IND"] = [
 e("Committee for Control and Supervision of Experiments on Animals", "https://cpcsea.gov.in/",
   "India’s regulator for animal experimentation, which has banned the use of animals for cosmetics testing and for some educational purposes. Restrictions here apply to a research system serving 1.4 billion people and rarely enter English-language discussion of animal research policy.",
   ["animals:services","rules:regulators","cro:cro"], base=REGI)]

# ------------------------------------------------------- the counting problem -
IND11["BEL"] = [
 e("European Commission \u2014 ALURES animal use database", "https://environment.ec.europa.eu/topics/chemicals/animals-science_en",
   "The EU’s database of animal use across member states, by species, purpose and severity. It exists because a directive required it, and it is the only place a multi-country picture of laboratory animal use can be assembled at all.",
   ["animals:models","rules:standards","rules:regulators"], base=REGI)]
