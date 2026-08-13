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
   "A Danish cooperative that is the world’s largest grass and forage seed company. Grass gets almost no attention in this debate, and it is the crop where the clearest documented case of transgene spread into wild relatives occurred, in Oregon.",
   ["seed:germplasm","seed:licensees"])]

IND15["FRA"] = [
 e("Groupe Florimond Desprez", "https://www.florimond-desprez.com/",
   "A French family seed company breeding wheat, sugar beet and potato, several centuries old. Family and cooperative ownership still holds a substantial share of European seed, which is why the four-company account of world seed is accurate globally and misleading in Europe.",
   ["seed:licensees","seed:germplasm","rules:ip"])]

IND15["JPN"] = [
 e("Sakata Seed", "https://www.sakataseed.co.jp/english/",
   "A Japanese vegetable seed company with worldwide operations. Vegetable seed is a separate market from row crops, more fragmented and less discussed, and a handful of Japanese and Dutch firms hold much of it.",
   ["seed:germplasm","seed:licensees"])]

IND15["CHE"] = [
 e("Bucher / agricultural machinery and data", "https://www.bucherindustries.com/",
   "Agricultural machinery that collects field data as it works. Machinery data and seed data converge on the same platforms, so the company that sells the seed can end up holding the record of how it performed.",
   ["seed:distribution","editing:platform"])]

# ==================================== GENE EDITING & SYNTHETIC BIOLOGY ========
IND15["USA"] = [
 e("Beam Therapeutics", "https://beamtx.com/",
   "Base editing changes a single DNA letter without cutting both strands, which avoids some of the unintended rearrangements cutting produces. It is a genuine reduction in one class of risk, and it does not address where in the genome the change lands.",
   ["editing:platform","clinical:therapy"]),
 e("Prime Medicine", "https://primemedicine.com/",
   "Prime editing writes new sequence into a target site with a template, in principle correcting mutations rather than disrupting genes. The technique is newer than the companies built on it, which is the usual sequence in this field.",
   ["editing:platform","clinical:therapy","rules:regulators"]),
 e("Arcadia Biosciences", "https://www.arcadiabio.com/",
   "Developed wheat and other crops with altered nutritional composition, and shifted toward consumer products after the agricultural business struggled. Trait companies without distribution keep discovering that the breeding is not the hard part.",
   ["editing:agtech","rules:regulators"]),
 e("Zymergen / Ginkgo \u2014 the collapse and absorption", "https://investors.ginkgobioworks.com/news-releases",
   "Zymergen raised heavily on automated organism design, failed to deliver its first product, collapsed, and was bought by Ginkgo. The platform promise and the product reality diverged publicly, in filings, which is rare enough to be worth reading.",
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
   "Announced very low-cost sequencing, aimed at making genome reading cheap enough to do routinely at population scale. Cheap sequencing expands both surveillance and verification, and the same instrument serves both.",
   ["synthesis:seq","clinical:trials"]),
 e("New England Biolabs", "https://www.neb.com/",
   "An employee-owned company supplying the enzymes molecular biology runs on, which has kept prices low and published methods openly. Ownership structure has visibly shaped its behaviour in a sector where most suppliers are inside conglomerates.",
   ["synthesis:reagents","editing:platform"])]

# ================================================ RULES, RECORDS & ADVOCACY ==
IND15["CHE"] = IND15.get("CHE", []) + [
 e("WHO \u2014 human genome editing governance framework", "https://www.who.int/teams/health-ethics-governance/emerging-technologies/human-genome-editing",
   "The World Health Organization’s framework for governing human genome editing, produced after the He Jiankui case. It is advisory: no country is bound by it, and the only enforcement of a germline prohibition anywhere so far has been a national criminal prosecution.",
   ["clinical:germline","rules:standards","rules:regulators"], base=BODY)]

IND15["KEN"] = [
 e("African Union \u2014 continental biosafety and biotechnology policy", "https://au.int/",
   "Continental coordination on biosafety policy, which shapes what individual African regulators adopt. Model laws written at this level propagate into national statutes, so the drafting is more consequential than any single country’s decision.",
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
   "A Southeast Asian centre producing biotechnology information and training for regional regulators and journalists. Who supplies the briefing material shapes what regulators consider normal, and this function is rarely examined.",
   ["rules:influence","rules:regulators"], base=BODY, trust="medium")]
