# -*- coding: utf-8 -*-
"""Industry entries, part 21."""
from ind1 import e, CO, BODY, REGI, ASSN

IND21 = {}

IND21["USA"] = [
 e("Ohalo Genetics", "https://www.ohalo.com/",
   "Working on making crops produce seed that breeds true rather than segregating, which would let farmers replant hybrids. The same technique would also let a company keep a variety uniform without hybrid seed sales, and which use it gets put to has not been settled.",
   ["editing:agtech","seed:germplasm","rules:regulators"]),
 e("Inari \u2014 SEEDesign platform", "https://inari.com/seedesign/",
   "Multiplex editing that alters dozens of genes at once in a single plant. The carve-outs adopted across forty countries were written around single small changes that could plausibly have arisen in nature, and no framework anywhere has drawn a line at a number of edits — so a plant with fifty deliberate changes can be exempt where a plant with one inserted gene is not.",
   ["editing:agtech","editing:platform","rules:regulators"])]

IND21["DEU"] = [
 e("BASF \u2014 enzymes and industrial biotechnology", "https://www.basf.com/global/en/products/segments/nutrition_and_care",
   "BASF's enzyme and fermentation businesses, putting engineered organisms into detergents, food processing and animal feed. None of it is labelled and none of it appears in the argument about GM food, because the organism stays in a tank and only its product is sold. Contained industrial use of this kind is the largest deliberate use of engineered organisms by volume anywhere, and the least contested.",
   ["editing:synbio","seed:majors","livestock:livestock"])]

IND21["NLD"] = [
 e("dsm-firmenich", "https://www.dsm-firmenich.com/",
   "A merger of a nutrition company and a fragrance house, producing vitamins, enzymes, flavours and feed additives by fermentation with engineered organisms. Its Bovaer additive suppresses methane production in cattle — a product designed to change what comes out of a cow rather than what goes into a field, and regulated as a feed additive rather than as anything to do with engineering.",
   ["editing:synbio","livestock:livestock","cro:cdmo"])]

IND21["DNK"] = [
 e("Novo Nordisk \u2014 recombinant insulin manufacture", "https://www.novonordisk.com/",
   "Insulin was the first recombinant medicine, approved in 1982, and is now made entirely this way. It is the strongest single case for the technology, and US insulin prices have been the subject of congressional inquiry for years — both facts belong to the same product.",
   ["clinical:therapy","cro:cdmo","money:markets"])]

IND21["IND"] = [
 e("Biocon \u2014 biosimilar insulin", "https://www.biocon.com/",
   "Manufactures insulin in engineered organisms at prices far below the American market, supplying much of the developing world from India. Insulin was the first engineered consumer product, approved in 1982, and its patent expired decades ago — yet US list prices rose for years through incremental reformulation. The technology being old and cheap to make is not what determines what a patient pays.",
   ["clinical:therapy","cro:cdmo"])]

IND21["GBR"] = [
 e("Oxford Nanopore \u2014 field sequencing", "https://nanoporetech.com/products/minion",
   "Handheld sequencers that work outside a laboratory, running from a laptop and reading long stretches of DNA in real time. They were used to track Ebola in Guinea in 2015 and Zika in Brazil, sequencing outbreak samples where they were collected rather than shipping them to a distant institute — which changes who holds the data and how fast a response can begin. The portability cuts both ways: a field-usable sequencer lets a grower, an inspector or a campaigner check what is in a sample without asking anyone's permission.",
   ["synthesis:seq","rules:standards"]),
 e("Roslin Institute", "https://www.ed.ac.uk/roslin",
   "Where Dolly the sheep was cloned in 1996, and still a centre for farm animal genetics and editing — the PRRS-resistant pig approved in the United States in 2025 came out of work done here. Dolly is the reason the public argument about animal biotechnology has the shape it does: cloning a mammal from an adult cell was announced as a technical result and received as a question about human cloning, and the regulatory reflexes formed in that year still govern editing done for entirely different reasons.",
   ["livestock:livestock","livestock:cloning","money:public"], base=BODY)]

IND21["CHN"] = [
 e("Yuan Longping High-Tech Agriculture", "http://www.lpht.com.cn/",
   "Named for the breeder whose hybrid rice is credited with feeding a very large share of China, and now one of the country's biggest seed companies. Yuan's work was conventional hybridisation done in a public institute and given away, which is the opposite of how the seed business now operates — and the company carrying his name is a commercial one. The contrast is the reason to record it.",
   ["seed:majors","seed:traits","money:public"])]

IND21["BRA"] = [
 e("Bioceres / Moolec \u2014 molecular farming", "https://moolecscience.com/",
   "Grows pharmaceutical and animal proteins inside crop plants — pig proteins in soy, bovine proteins in peas. Molecular farming puts a substance intended for a factory into a plant grown in a field, which means containment depends on agronomy rather than on a fermenter wall. It also produces an organism that no category handles cleanly: a food crop that is not food, grown outdoors, regulated as a crop.",
   ["editing:agtech","seed:traits","livestock:livestock"])]

IND21["KEN"] = [
 e("ISAAA AfriCenter", "https://africenter.isaaa.org/",
   "The African office of the industry-funded biotechnology information service, producing the adoption figures and briefings widely cited in African policy debate. Its numbers are the most quoted on the continent and its funding comes from the industry whose adoption it counts, which is worth knowing when the figures appear in a parliamentary submission.",
   ["rules:influence","rules:associations"], base=ASSN),
 e("Kenya Plant Health Inspectorate Service", "https://kephis.go.ke/",
   "Kenya's plant health and seed regulator, responsible for variety approval and seed certification, and the body that had to implement the 2022 lifting of the engineered-crop import ban while a court challenge to that decision was still running. Regulators in this position carry out a policy that may be reversed above them.",
   ["rules:regulators","rules:standards"], base=REGI)]

IND21["MEX"] = [
 e("CIMMYT \u2014 maize and wheat genebank", "https://www.cimmyt.org/",
   "The international maize and wheat centre, holding the largest public collections of both, distributed free under the Plant Treaty's multilateral system. Norman Borlaug's wheat came from here, and the varieties grown across much of the developing world still trace to this collection — which makes a genebank in Mexico one of the few places in this industry where the foundational material is not owned by anyone.",
   ["seed:germplasm","money:philanthropy","rules:ip"], base=BODY)]

IND21["PHL"] = [
 e("MASIPAG", "https://masipag.org/",
   "A Philippine network of farmers and scientists breeding rice varieties collectively and keeping them out of the patent system, and one of the petitioners in the case that revoked the Golden Rice approval. It is the clearest example of farmers doing the breeding themselves rather than choosing between varieties others have bred, which is a different argument from opposing a technology.",
   ["seed:germplasm","rules:regulators"], base=BODY)]
