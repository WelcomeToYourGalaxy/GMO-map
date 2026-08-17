# -*- coding: utf-8 -*-
"""Industry entries, part 15."""
from ind1 import e, CO, BODY, REGI, ASSN

IND15 = {}

# =========================================================== SEED & TRAITS ====
IND15["DEU"] = [
 e("KWS SAAT", "https://www.kws.com/",
   "A German seed company, family-controlled, with a dominant position in sugar beet and a large one in maize. European breeders of this size operate under rules that make engineered crops commercially impossible to sell domestically, so their engineered work happens abroad or not at all.",
   ["seed:licensees","seed:germplasm","seed:traits"])]

IND15["DNK"] = [
 e("DLF Seeds", "https://www.dlf.com/",
   "A Danish cooperative that is the world's largest supplier of grass and clover seed, for pasture, forage and turf. Grassland covers more of the planet's agricultural area than any crop and receives almost none of the attention: a seed sector this large sits outside the entire engineered-crop argument because nobody has found it worth engineering.",
   ["seed:germplasm","seed:licensees"])]

IND15["FRA"] = [
 e("Groupe Florimond Desprez", "https://www.florimond-desprez.com/",
   "A French family seed company breeding wheat, sugar beet and potato, several centuries old. Family and cooperative ownership still holds a substantial share of European seed, which is why the four-company account of world seed is accurate globally and misleading in Europe.",
   ["seed:licensees","seed:germplasm","rules:ip"])]

IND15["JPN"] = [
 e("Sakata Seed", "https://www.sakataseed.co.jp/english/",
   "A Japanese vegetable and flower seed company operating worldwide, and one of the handful of firms that dominate vegetable breeding. Vegetables are bred conventionally almost everywhere, because the crops are too many and the markets too fragmented for engineered varieties to repay approval costs — so seed concentration in vegetables happened without any of the technology this map otherwise tracks.",
   ["seed:germplasm","seed:licensees"])]

IND15["CHE"] = [
 e("Bucher / agricultural machinery and data", "https://www.bucherindustries.com/",
   "Agricultural machinery that records field conditions as it works, feeding the same data streams the seed companies collect. Machinery makers and seed companies are now competing for the same asset — a continuous record of what was planted, sprayed and harvested on each field — and whoever holds it can price inputs to each farm individually.",
   ["seed:distribution","editing:platform"])]

# ==================================== GENE EDITING & SYNTHETIC BIOLOGY ========
IND15["USA"] = [
 e("Beam Therapeutics", "https://beamtx.com/",
   "Base editing changes a single DNA letter without cutting the double helix, which avoids the breaks that cause most unintended damage from earlier methods. Roughly half of known disease-causing mutations are single-letter changes, so the technique addresses more conditions than any other editing chemistry — and because it makes a change indistinguishable from a natural variant, it is also the hardest to detect afterwards in anything it is used on.",
   ["editing:platform","clinical:therapy"]),
 e("Prime Medicine", "https://primemedicine.com/",
   "Prime editing writes new sequence into a target site without cutting both strands of the DNA, which is where most unintended damage from earlier editing comes from. In principle it can make the majority of known disease-causing mutations correctable by one method. It is the most capable editing chemistry yet demonstrated and the furthest from routine use, which is the ordinary gap in this field between what works in a cell and what reaches a patient.",
   ["editing:platform","clinical:therapy","rules:regulators"]),
 e("Arcadia Biosciences", "https://www.arcadiabio.com/",
   "Developed wheat and other crops with altered nutritional composition, including reduced-gluten wheat, using both conventional and engineered approaches. It is a long-running example of the output trait — a change a consumer might want rather than one a farmer wants — which has repeatedly been promised as the next phase of this industry and repeatedly not arrived.",
   ["editing:agtech","rules:regulators"]),
 e("Zymergen / Ginkgo \u2014 the collapse and absorption", "https://investors.ginkgobioworks.com/news-releases",
   "Zymergen raised heavily on automated organism engineering, listed publicly in 2021, disclosed months later that its lead product had no viable market, and was bought by Ginkgo for a fraction of its valuation. It is the clearest failure on this map, and it is here because the pitch it failed on — that engineering biology would industrialise like software — is the pitch the sector still makes.",
   ["editing:synbio","money:vc","money:markets"])]

IND15["GBR"] = [
 e("Tropic Biosciences", "https://tropicbioscience.com/",
   "A UK company editing bananas and coffee, crops propagated clonally and therefore hard to improve by breeding. Clonal crops are where editing has the strongest technical case, and bananas are facing a disease that conventional breeding has not solved.",
   ["editing:agtech","seed:traits"])]

# ============================================ DNA SYNTHESIS & SEQUENCING =====
IND15["USA"] = IND15["USA"] + [
 e("Element Biosciences", "https://www.elementbiosciences.com/",
   "A sequencing company competing with Illumina, part of the first real challenge to that dominance in over a decade. Competition in sequencing instruments changes the cost of checking things, which affects everyone doing verification rather than production.",
   ["synthesis:seq"]),
 e("Ultima Genomics", "https://www.ultimagenomics.com/",
   "Announced sequencing at a cost far below the prevailing price, on a machine built around a spinning wafer rather than a flow cell. Whether or not it displaces Illumina, the announcement changed what buyers expect to pay — and the cost of reading a genome is the variable that decides whether population-scale programmes, newborn sequencing and routine embryo screening are affordable at all.",
   ["synthesis:seq","clinical:trials"]),
 e("New England Biolabs", "https://www.neb.com/",
   "An employee-owned company supplying the enzymes molecular biology is done with, including many of the restriction enzymes and polymerases that made the field possible. Its ownership structure is the unusual part: a central supplier to a heavily consolidated industry that has stayed independent and prices its catalogue accordingly.",
   ["synthesis:reagents","editing:platform"])]

# ================================================ RULES, RECORDS & ADVOCACY ==
IND15["CHE"] = IND15.get("CHE", []) + [
 e("WHO \u2014 human genome editing governance framework", "https://www.who.int/teams/health-ethics-governance/emerging-technologies/human-genome-editing",
   "The World Health Organization’s framework for governing human genome editing, produced after the He Jiankui case. It is advisory: no country is bound by it, and the only enforcement of a germline prohibition anywhere so far has been a national criminal prosecution.",
   ["clinical:germline","rules:standards","rules:regulators"], base=BODY)]

IND15["KEN"] = [
 e("African Union \u2014 continental biosafety and biotechnology policy", "https://au.int/",
   "Continental coordination on biosafety policy through AUDA-NEPAD, providing model law and technical support to member states. Where a country has no capacity to assess an application, the assessment is effectively imported — and the continent's regulatory direction is therefore set in a small number of places rather than in fifty-five separate debates.",
   ["rules:standards","rules:regulators"], base=BODY)]

# ======================================================= NEW TERRITORIES ======
IND15["SRB"] = [
 e("Ministry of Agriculture \u2014 GMO prohibition", "https://www.minpolj.gov.rs/",
   "Serbia prohibits the cultivation and import of engineered crops, and EU accession requires aligning with EU rules that permit both. The prohibition is one of the specific things accession would change, and it is domestically popular.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND15["BGR"] = [
 e("Ministry of Environment and Water \u2014 GMO register", "https://www.moew.government.bg/",
   "Bulgaria’s GMO register, in a country that has used EU opt-outs to prohibit cultivation. The register exists to record what is not being grown, which is its own kind of document.",
   ["rules:regulators","seed:distribution"], base=REGI)]

IND15["LKA"] = [
 e("Sri Lanka \u2014 food labelling and import control", "https://www.health.gov.lk/",
   "Sri Lanka requires labelling of engineered foods and controls imports, in a country whose 2021 overnight ban on synthetic fertiliser produced a documented agricultural collapse. That episode is the strongest available caution about changing an agricultural system faster than it can adapt.",
   ["rules:regulators","rules:standards"], base=REGI)]

IND15["PHL"] = [
 e("SEARCA \u2014 regional biotechnology information", "https://www.searca.org/",
   "A Southeast Asian centre producing biotechnology information and training for governments across the region, in a part of the world where several countries have adopted carve-outs for edited crops within a few years of each other. Where a regional body supplies the briefing material, the regulatory texts tend to converge.",
   ["rules:influence","rules:regulators"], base=BODY, trust="medium")]
