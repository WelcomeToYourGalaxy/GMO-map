# -*- coding: utf-8 -*-
"""Industry entries. Description format: WHAT / WHERE IT SITS / WHY IT MATTERS.

Every entry names a real organisation and links to something it publishes about
itself. The third part of each description argues from the documented position —
market share, published terms, incident record, the structure of the arrangement
— rather than from characterisation.
"""

CHECKED = "2026-07-31"

CO   = dict(kind="institution", voice="commentary",   skind="other",    type="institutional", trust="medium")
BODY = dict(kind="institution", voice="official",     skind="igo",      type="institutional", trust="high")
REGI = dict(kind="structured",  voice="official",     skind="database", type="records-data",  trust="record")
ASSN = dict(kind="institution", voice="commentary",   skind="ngo",      type="institutional", trust="low")


def e(name, url, desc, tags, base=CO, **kw):
    d = dict(base); d.update(name=name, url=url, desc=desc, tags=tags)
    d.setdefault("checked", CHECKED); d.update(kw); return d


IND1 = {}

# ============================================================ SEED & TRAITS ===
IND1["DEU"] = [
 e("Bayer Crop Science", "https://www.bayer.com/en/agriculture/crop-science",
   "The largest seed and agricultural-trait business on Earth, assembled when Bayer bought Monsanto in 2018 for around $63 billion and retired the name. It sells maize, soybean, cotton, vegetable and canola seed under Dekalb, Asgrow and Seminis, and it sells the glyphosate those traits are engineered to survive, so the seed and the chemical are one purchase. Its short-stature corn is the first attempt to change the shape of the plant rather than its chemistry, which lets a field be sprayed later in the season by machine. Through Climate FieldView it also holds the agronomic data of tens of millions of hectares, which is a position no seed company has held before: what is planted, what is sprayed and what results, field by field. Joyn Bio, its joint venture with Ginkgo, worked on microbes engineered to fix nitrogen so that maize might need less fertiliser. Against all of that sits the glyphosate litigation inherited with Monsanto — many billions paid and reserved, the largest mass tort ever attached to an agricultural product, and the reason the company now lobbies US state legislatures for statutory protection it has been losing in court.",
   ["editing:agtech", "editing:platform", "money:markets", "rules:influence", "rules:standards", "seed:distribution", "seed:majors", "seed:traits", "wild:microbes"])]

IND1["USA"] = [
 e("Corteva Agriscience", "https://www.corteva.com/",
   "Spun out of DowDuPont in 2019 with the Pioneer seed brand and the crop-protection lines, Corteva is the closest thing Bayer has to a peer. It holds the second-largest share of US release authorisations and a comparable position in maize genetics. Its Enlist system pairs seed with the herbicides that seed is engineered to tolerate, the same coupling Bayer runs with glyphosate. It sells microbial and chemical seed treatments, so an engineered seed arrives already coated in living organisms that are regulated as a crop input rather than as a release. It runs a hybrid wheat programme, wheat having been left alone for twenty years because it is eaten directly and traded everywhere. And it holds the exclusive agricultural licence to the Broad Institute's CRISPR patents, which means a company that grows nothing decides who may commercialise an edited crop, and Corteva decides it for agriculture.",
   ["editing:agtech", "editing:patents", "money:public", "rules:ip", "seed:distribution", "seed:germplasm", "seed:licensees", "seed:majors", "seed:traits", "wild:microbes"])]

IND1["CHE"] = [
 e("Syngenta Group", "https://www.syngentagroup.com/",
   "Chinese state-owned since ChemChina bought it in 2017 for $43 billion, Syngenta is one of the four companies that dominate world seed and crop protection, and the only one under government ownership. That changes what the concentration argument is about: this is not only four corporations, it is four corporations of which one answers to a state. Its seedcare business coats seed with chemical and microbial treatments before it is sold, and its acquisition of Valagro moved it into biologicals — living products applied to fields under a lighter regulatory route than an engineered plant takes. Folded into Sinochem alongside China National Seed Group, it is also the vehicle through which Chinese agricultural policy reaches farms outside China.",
   ["money:markets", "rules:influence", "seed:distribution", "seed:majors", "seed:traits", "wild:microbes"])]

IND1["NLD"] = [
 e("BASF Agricultural Solutions", "https://agriculture.basf.com/global/en.html",
   "The fourth of the companies that dominate world seed and crop protection, and the one with the smallest seed business relative to its chemistry. It bought the vegetable seed and hybrid wheat lines Bayer was forced to divest as a condition of the Monsanto acquisition, so a competition remedy is what gave it the position it now holds. Its herbicide-tolerance systems are licensed into other companies' varieties, which is the usual arrangement: the trait and the seed it travels in are frequently owned by different firms, and a farmer buying one is paying both.",
   ["seed:majors","seed:germplasm"]),
 e("Rijk Zwaan", "https://www.rijkzwaan.com/",
   "A large Dutch vegetable breeder, family-owned and deliberately unlisted, in a small region that supplies a very large share of the world’s vegetable seed. The Dutch cluster is a concentration nobody treats as one: a handful of firms in one province breed much of what the world eats fresh, and because they are private and regional, that position appears in no national statistic and no merger review.",
   ["seed:licensees","seed:germplasm"])]

IND1["FRA"] = [
 e("Limagrain / Vilmorin", "https://www.limagrain.com/en",
   "A French agricultural cooperative that owns one of the world’s largest seed businesses — farmers collectively own the company selling farmers their seed. It is the strongest counter-example to the argument that seed consolidation is inevitable under corporate ownership, and worth watching precisely for that: whether cooperative structure produces different behaviour at scale, or whether scale produces the same behaviour regardless of who holds the shares.",
   ["seed:licensees","seed:germplasm","seed:distribution"])]

# ================================== GENE EDITING & SYNTHETIC BIOLOGY ==========
IND1["USA"] = IND1["USA"] + [
 e("Ginkgo Bioworks", "https://www.ginkgobioworks.com/",
   "Ginkgo rents out the ability to design organisms. Clients bring a molecule they want made; Ginkgo’s automated foundries build and test the microbes that make it. It went public at an $​​15 billion valuation in 2021 and has since lost most of it, which matters less than what the model establishes: a company can build engineered organisms for hundreds of customers without ever owning a product, appearing on a label, or being the party a regulator assesses. The clients are the applicants. Ginkgo is the factory behind them.",
   ["editing:synbio","editing:platform","cro:cro"]),
 e("Inari Agriculture", "https://inari.com/",
   "Inari edits many genes at once rather than one, using predictive design to alter dozens of targets in soy, maize and wheat simultaneously. The consequence is regulatory rather than commercial. carve-outs for gene editing were written around single small changes that could plausibly have arisen in nature, and multiplex editing stretches that reasoning past where it was meant to reach. No framework anywhere has drawn a line at a number of edits, which is precisely the gap the company operates in.",
   ["editing:agtech","editing:platform","rules:regulators"])]

IND1["GBR"] = [
 e("Oxford Nanopore Technologies", "https://nanoporetech.com/",
   "Handheld sequencers that work outside a laboratory, running on a laptop and reading long stretches of DNA in real time. They were used to track Ebola in Guinea in 2015 and Zika in Brazil, sequencing outbreak samples where they were collected rather than shipping them to a distant institute — which changes who holds the data and how fast a response can begin. The same portability makes verification possible in the other direction: a field-usable sequencer means a grower, a customs officer or a campaigner can check what is in a sample without asking anyone's permission.",
   ["synthesis:seq","synthesis:reagents"])]

# ========================================= DNA SYNTHESIS & SEQUENCING =========
IND1["USA"] = IND1["USA"] + [
 e("Twist Bioscience", "https://www.twistbioscience.com/",
   "Twist prints DNA to order on silicon, which made synthesis cheap enough to be routine. It is among the largest suppliers in the world and one of the firms that screens orders against lists of dangerous sequences — voluntarily, because no law requires it. That places a private company at the most consequential control point in the industry: everything downstream, in every facet of this map, begins as a sequence somebody ordered from a supplier like this one.",
   ["synthesis:synth","synthesis:reagents"]),
 e("Integrated DNA Technologies (Danaher)", "https://www.idtdna.com/",
   "IDT supplies the oligonucleotides and CRISPR reagents that laboratory work runs on, now inside Danaher, a conglomerate that has bought much of the life-science supply chain. A handful of holding companies control the consumables every laboratory needs daily, so a purchasing decision made for margin at group level propagates into thousands of experiments that have no alternative supplier.",
   ["synthesis:synth","synthesis:reagents"]),
 e("Illumina", "https://www.illumina.com/",
   "Illumina has dominated DNA sequencing for over a decade, and the cost curve it drove is why reading a genome went from a national project to a line item. Almost every genome on this map — prenatal screens, newborn programmes, embryo screening, pathogen surveillance, consumer ancestry tests, crop breeding — was read on its machines or a competitor built in response to them. That position is closer to a monopoly than anything else here, and it is held through instruments plus the consumable reagents each run requires, which is where the revenue is. Regulators in the US and EU blocked its acquisition of the cancer-test maker Grail on the grounds that owning both the sequencers and a test that runs on them would let it disadvantage every rival test; it completed the deal anyway, was fined, and divested in 2024. It is the clearest case on this map of a company whose product is not an organism but without which most of the rest could not operate.",
   ["synthesis:seq", "synthesis:reagents", "repro:screening", "clinical:trials", "money:markets", "rules:ip", "wild:microbes"]),
 e("Addgene", "https://www.addgene.org/",
   "A non-profit repository through which laboratories deposit and share plasmids — the rings of DNA that carry an engineered construct. It has distributed well over a million, and it is the reason a technique published in a paper can be reproduced by someone else rather than remaining a claim. It is also a gate: shipping requires a verified institutional account, so the method is free to read and the material is not.",
   ["synthesis:repos","synthesis:reagents"], base=BODY)]

IND1["CHN"] = [
 e("BGI Group", "https://www.bgi.com/global",
   "The largest genomics organisation in the world by sequencing capacity, based in Shenzhen, and the subject of sustained Western government concern about where the genetic data it processes ends up. Read alongside the US and European companies on this map, every large genomic operation accumulates human data and every one of them is trusted or distrusted according to its flag rather than its practices.",
   ["synthesis:seq","synthesis:synth"])]

# ======================================== CONTRACT RESEARCH & MANUFACTURE =====
IND1["USA"] = IND1["USA"] + [
 e("Charles River Laboratories", "https://www.criver.com/",
   "Supplies laboratory animals and runs the safety testing that regulators read, which makes it both the largest animal vendor in the world and one of the largest contract testing businesses. The same company breeds the animal and reports the result. Its Safety Assessment division runs the regulated toxicology studies required before anything is given to a person, at sites including Mattawan and Ashland that are among the largest animal facilities in the United States by capacity. Its European breeding network, extended by the Janvier acquisition, supplies the same market on that side of the Atlantic. And it bleeds horseshoe crabs for the lysate used to test injectable drugs for contamination — a business that depends on a wild animal, has no synthetic substitute in widespread use, and is the reason a fifty-million-year-old species now appears in pharmaceutical supply chains.",
   ["animals:breeders", "animals:services", "cro:cro", "cro:preclinical", "cro:regulatory", "editing:synbio", "synthesis:reagents"]),
 e("Labcorp Drug Development (formerly Covance)", "https://drugdevelopment.labcorp.com/",
   "One of the largest contract research organisations, running trials for sponsors who pay for the result and can take the work elsewhere. Its scale is the point: a handful of these firms run most of the trials that regulators worldwide assess, so the evidence base for approval is produced by companies whose next contract depends on the industry being satisfied. Nothing here is hidden; it is simply how the system is arranged.",
   ["cro:cro","clinical:trials"])]
