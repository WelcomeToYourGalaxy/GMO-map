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
   "The largest seed and agricultural-trait business on Earth, assembled when Bayer bought Monsanto in 2018 for around $63 billion and retired the name. It sells maize, soybean, cotton, vegetable and canola seed under Dekalb, Asgrow and Seminis, and it sells the glyphosate its traits are engineered to survive. The seed is not where its position rests. The licensing is. Traits developed here appear in competitors’ bags across most of the world’s engineered acreage, so rivals pay Bayer on their own sales, and the company holds roughly a third of every US release authorisation ever granted. The Monsanto purchase also bought the glyphosate litigation, tens of billions in provisions against it, and a share price that has never recovered — which is why the seed and trait business now has to earn back what the chemical business cost.",
   ["seed:majors","seed:traits","editing:agtech"])]

IND1["USA"] = [
 e("Corteva Agriscience", "https://www.corteva.com/",
   "Spun out of DowDuPont in 2019 with the Pioneer seed brand and the crop-protection lines, Corteva is the closest thing Bayer has to a peer. It holds the second-largest share of US release authorisations and a comparable position in maize genetics, and it has spent the years since the split buying its way into gene editing rather than building from scratch. Its leverage runs through the same mechanism as Bayer’s: a farmer choosing a non-Corteva bag is often still planting a Corteva trait under licence.",
   ["seed:majors","seed:traits","seed:licensees"]),
 e("Bayer \u2014 investor filings", "https://www.bayer.com/en/investors/annual-reports",
   "What a company tells its shareholders is a different document from what it tells a regulator, and both are public. The filings carry segment revenue, litigation provisions, R&D spend and the risk factors the board is legally obliged to disclose — including, in Bayer’s case, the running cost of the glyphosate claims. For anyone trying to establish what this business actually earns and fears, it is the most reliable source there is, because getting it wrong is a securities offence.",
   ["seed:majors","money:markets"], base=REGI)]

IND1["CHE"] = [
 e("Syngenta Group", "https://www.syngentagroup.com/",
   "Chinese state-owned since ChemChina bought it in 2017, Syngenta is one of the four companies that dominate world seed and crop protection, and the only one under government ownership. That changes what the concentration argument is about: this is not only four corporations, it is four corporations one of which answers to a state pursuing seed sovereignty as industrial policy. Its traits and chemicals reach farmers on every continent.",
   ["seed:majors","seed:traits","money:markets"]),
 e("Syngenta \u2014 seedcare & seeds portfolio", "https://www.syngenta.com/en/seeds",
   "The coatings and treatments applied to seed before it is sold, including neonicotinoid insecticides. This layer travels with every bag and mostly escapes pesticide-use reporting, because nothing is sprayed and so nothing is recorded. By area treated it is among the largest insecticide applications in world agriculture, and among the least documented — a whole category of use the statistics simply do not see.",
   ["seed:distribution","seed:traits"])]

IND1["NLD"] = [
 e("BASF Agricultural Solutions", "https://agriculture.basf.com/global/en.html",
   "The fourth major, and the one usually left out of the discussion because it is thought of as a chemicals company. It bought large parts of the Bayer seed business that competition authorities forced Bayer to divest, so the remedy for one merger built the fourth player. Its fermentation and enzyme businesses also put engineered organisms into food processing and animal feed by an entirely separate route — unlabelled, and never counted when this company’s reach is measured.",
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
 e("Corteva \u2014 CRISPR licensing framework", "https://www.corteva.com/who-we-are/open-innovation.html",
   "Corteva holds or licenses much of the foundational CRISPR intellectual property for agriculture, and has published terms under which universities and small companies may use it. That sounds like openness and functions as a chokepoint: the terms are set by one party, apply to a technique everyone now needs, and can be revised. Whoever writes the licence decides which agricultural editing gets done, and by whom — more influence over the field’s direction than any single product carries.",
   ["editing:patents","editing:agtech","money:public"]),
 e("Ginkgo Bioworks", "https://www.ginkgobioworks.com/",
   "Ginkgo rents out the ability to design organisms. Clients bring a molecule they want made; Ginkgo’s automated foundries build and test the microbes that make it. It went public at an $​​15 billion valuation in 2021 and has since lost most of it, which matters less than what the model establishes: a company can build engineered organisms for hundreds of customers without ever owning a product, appearing on a label, or being the party a regulator assesses. The clients are the applicants. Ginkgo is the factory behind them.",
   ["editing:synbio","editing:platform","cro:cro"]),
 e("Inari Agriculture", "https://inari.com/",
   "Inari edits many genes at once rather than one, using predictive design to alter dozens of targets in soy, maize and wheat simultaneously. The consequence is regulatory rather than commercial. carve-outs for gene editing were written around single small changes that could plausibly have arisen in nature, and multiplex editing stretches that reasoning past where it was meant to reach. No framework anywhere has drawn a line at a number of edits, which is precisely the gap the company operates in.",
   ["editing:agtech","editing:platform","rules:regulators"])]

IND1["GBR"] = [
 e("Oxford Nanopore Technologies", "https://nanoporetech.com/",
   "Handheld sequencers that work outside a laboratory — in a field, at a border post, beside a river. This is one of the few technologies here that helps the people checking rather than the people releasing: verifying what is in a seed lot, a shipment or a wild population stops requiring an institutional laboratory. That is a real shift in who is able to find things out, and it did not happen by anyone’s design.",
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
   "Illumina has dominated DNA sequencing for over a decade, and the cost curve it drove is why reading a genome went from a national project to a line item. Regulators in the US and EU blocked its acquisition of the cancer-test maker Grail on the grounds that owning both the sequencers and a test that runs on them would let it squeeze every competitor — a rare case of a competition authority naming the chokepoint out loud. Most of the genomic data in this map’s clinical and synthesis facets was generated on its machines.",
   ["synthesis:seq","synthesis:reagents"]),
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
   "Charles River supplies laboratory animals and runs the safety testing that regulators read, which makes it both the largest animal vendor in the world and one of the largest contract testing businesses. The same company breeds the animal and reports the result. It also harvests horseshoe crabs for the endotoxin reagent every injectable medicine is tested with — a recombinant substitute exists, works, and is in the US pharmacopoeia, and adoption has been slow because the old test is what everyone is used to.",
   ["cro:cro","animals:breeders","animals:services"]),
 e("Labcorp Drug Development (formerly Covance)", "https://drugdevelopment.labcorp.com/",
   "One of the largest contract research organisations, running trials for sponsors who pay for the result and can take the work elsewhere. Its scale is the point: a handful of these firms run most of the trials that regulators worldwide assess, so the evidence base for approval is produced by companies whose next contract depends on the industry being satisfied. Nothing here is hidden; it is simply how the system is arranged.",
   ["cro:cro","clinical:trials"])]
