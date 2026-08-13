# -*- coding: utf-8 -*-
"""Industry entries, part 21."""
from ind1 import e, CO, BODY, REGI, ASSN

IND21 = {}

IND21["USA"] = [
 e("Corteva \u2014 hybrid wheat programme", "https://www.corteva.com/products-and-solutions/seeds.html",
   "Hybrid wheat has been attempted for decades because hybrids yield more and cannot be saved — the seed has to be repurchased annually. The agronomic argument and the commercial one point the same way, which is why it keeps being attempted.",
   ["seed:traits","seed:germplasm","rules:ip"]),
 e("Bayer \u2014 short-stature corn", "https://www.cropscience.bayer.com/innovations/seeds-traits",
   "Maize bred and edited to grow shorter, standing up to the stronger winds a warmer climate produces. It is one of the few products here aimed at a climate effect rather than at a herbicide or an insect.",
   ["seed:traits","seed:majors","editing:agtech"]),
 e("Corteva \u2014 Enlist herbicide system", "https://www.corteva.us/products-and-solutions/crop-protection/enlist-one.html",
   "Crops engineered to survive 2,4-D and glyphosate together, sold as the answer to weeds that survived glyphosate alone. Each generation of resistant weeds is met with another herbicide the crop is engineered to tolerate.",
   ["seed:traits","seed:majors","wild:microbes"]),
 e("Ohalo Genetics", "https://www.ohalo.com/",
   "Working on making crops produce seed that breeds true rather than segregating, which would let farmers replant hybrids. The same technique would also let a company keep a variety uniform without hybrid seed sales, and which use it gets put to has not been settled.",
   ["editing:agtech","seed:germplasm","rules:regulators"]),
 e("Inari \u2014 SEEDesign platform", "https://inari.com/seedesign/",
   "Multiplex editing that alters dozens of genes at once. Gene-editing carve-outs were written around single small changes that could plausibly have arisen naturally, and no framework anywhere has drawn a line at a number of edits.",
   ["editing:agtech","editing:platform","rules:regulators"])]

IND21["CHE"] = [
 e("Syngenta \u2014 biologicals and Valagro", "https://www.syngenta.com/en/company/media/syngenta-news",
   "Syngenta’s acquisition of a biologicals company, part of every major buying into microbial and biostimulant products. The category that requires the least regulatory review is the one they are all expanding into.",
   ["wild:microbes","seed:majors","money:markets"])]

IND21["DEU"] = [
 e("BASF \u2014 enzymes and industrial biotechnology", "https://www.basf.com/global/en/products/segments/nutrition_and_care",
   "BASF’s enzyme and fermentation businesses, putting engineered organisms into detergents, food processing and animal feed. None of it is labelled and none of it appears in the argument about GM food.",
   ["editing:synbio","seed:majors","livestock:livestock"])]

IND21["NLD"] = [
 e("dsm-firmenich", "https://www.dsm-firmenich.com/",
   "A merger of a nutrition and a fragrance company, producing vitamins, enzymes and flavour compounds by fermentation with engineered organisms. Ingredients arriving this way are identified as engineered nowhere in the chain.",
   ["editing:synbio","livestock:livestock","cro:cdmo"])]

IND21["DNK"] = [
 e("Novo Nordisk \u2014 recombinant insulin manufacture", "https://www.novonordisk.com/",
   "Insulin was the first recombinant medicine, approved in 1982, and is now made entirely this way. It is the strongest single case for the technology, and US insulin prices have been the subject of congressional inquiry for years — both facts belong to the same product.",
   ["clinical:therapy","cro:cdmo","money:markets"])]

IND21["IND"] = [
 e("Biocon \u2014 biosimilar insulin", "https://www.biocon.com/",
   "Biocon manufactures insulin at prices far below the American market, supplying much of the world. What a medicine costs is a decision rather than a consequence, and the same molecule made by a different company demonstrates it.",
   ["clinical:therapy","cro:cdmo"])]

IND21["GBR"] = [
 e("Oxford Nanopore \u2014 field sequencing", "https://nanoporetech.com/products/minion",
   "Handheld sequencers usable outside a laboratory. Verifying what is in a seed lot, a shipment or a wild population stops requiring institutional facilities, which shifts who is able to find things out.",
   ["synthesis:seq","rules:standards"]),
 e("Roslin Institute", "https://www.ed.ac.uk/roslin",
   "Where Dolly the sheep was cloned in 1996, and still a centre for farm animal genetics and editing. The institute that produced the defining image of this technology has spent thirty years since working on livestock.",
   ["livestock:livestock","livestock:cloning","money:public"], base=BODY)]

IND21["CHN"] = [
 e("Yuan Longping High-Tech Agriculture", "http://www.lpht.com.cn/",
   "A Chinese seed company named after the hybrid rice breeder whose work fed hundreds of millions, now holding engineered maize approvals. The name carries a public-good history into a commercial trait business.",
   ["seed:majors","seed:traits","money:public"])]

IND21["BRA"] = [
 e("Bioceres / Moolec \u2014 molecular farming", "https://moolecscience.com/",
   "Growing pharmaceutical proteins and animal proteins in crop plants. It puts a medicinal or industrial product into a food crop grown in fields, which is the category the StarLink episode concerned.",
   ["editing:agtech","seed:traits","livestock:livestock"])]

IND21["KEN"] = [
 e("ISAAA AfriCenter", "https://africenter.isaaa.org/",
   "The African office of the industry-funded biotechnology information service, supplying briefing material to regulators and journalists across the continent. Who provides the background reading shapes what regulators treat as settled.",
   ["rules:influence","rules:associations"], base=ASSN),
 e("Kenya Plant Health Inspectorate Service", "https://kephis.go.ke/",
   "Kenya’s plant health and seed regulator, responsible for variety approval and seed certification. Seed certification decides what may lawfully be sold, which is a separate gate from biosafety approval and often the more restrictive one.",
   ["rules:regulators","rules:standards"], base=REGI)]

IND21["MEX"] = [
 e("CIMMYT \u2014 maize and wheat genebank", "https://www.cimmyt.org/",
   "The international maize and wheat centre, holding the world’s largest maize and wheat genebank, in Mexico. Nearly every commercial wheat and maize variety traces back to material held here, and it is distributed under treaty terms rather than sold.",
   ["seed:germplasm","money:philanthropy","rules:ip"], base=BODY)]

IND21["PHL"] = [
 e("MASIPAG", "https://masipag.org/",
   "A Philippine farmer-scientist network breeding rice varieties collectively and keeping them in farmers’ hands. It is a working alternative to the seed-purchase model rather than an argument against it, and it has operated for decades.",
   ["seed:germplasm","rules:regulators"], base=BODY)]
