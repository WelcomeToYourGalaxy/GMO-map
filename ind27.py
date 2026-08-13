# -*- coding: utf-8 -*-
"""Industry entries, part 27.

Two gaps this batch. First, the security and defence end: this map has DARPA and
little else, and every capable state funds biology through defence budgets that
sit outside civilian biosafety oversight. Second, the regions still thinnest
here \u2014 central Asia, the Caucasus, west Africa and the Pacific.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND27 = {}

# ================================================ DEFENCE & SECURITY ==========
IND27["USA"] = [
 e("Defense Threat Reduction Agency", "https://www.dtra.mil/",
   "Funds and runs US work on biological threats, including sequencing, detection and "
   "countermeasures, and pays for laboratory capacity in partner countries. Defence "
   "biology sits outside the civilian biosafety systems this map documents, so the same "
   "techniques are being funded twice over under two sets of rules \u2014 and only one set "
   "publishes what it approved.",
   ["rules:regulators", "money:defence", "synthesis:seq"], base=BODY),
 e("Intelligence Advanced Research Projects Activity \u2014 biology programmes",
   "https://www.iarpa.gov/research-programs",
   "The US intelligence community\u2019s research arm has funded work on reading and "
   "attributing engineered biology \u2014 determining from a sample whether an organism was "
   "made deliberately and by whom. Attribution is the capability that would make any "
   "biological rule enforceable, and it is being built inside intelligence rather than "
   "inside biosafety.",
   ["synthesis:seq", "money:defence", "rules:standards"], base=BODY),
 e("NTI | bio \u2014 Nuclear Threat Initiative", "https://www.nti.org/area/biosecurity/",
   "Runs the International Biosecurity and Biosafety Initiative for Science and pushes "
   "for mandatory screening of synthetic DNA orders. It is the main organised effort to "
   "close the gap this map keeps returning to \u2014 that roughly a fifth of world synthesis "
   "capacity screens nothing \u2014 and it is philanthropy doing what no law requires.",
   ["synthesis:synth", "rules:standards", "rules:influence"], base=BODY),
]

IND27["GBR"] = [
 e("Defence Science and Technology Laboratory \u2014 Porton Down",
   "https://www.gov.uk/government/organisations/defence-science-and-technology-laboratory",
   "The UK\u2019s defence biology establishment, working on pathogens and countermeasures "
   "at the highest containment levels. Facilities like this exist in every state with "
   "the means, they hold the most dangerous material anywhere, and they are the least "
   "visible part of this entire field.",
   ["rules:regulators", "money:defence"], base=BODY),
]

IND27["RUS"] = [
 e("Vector State Research Centre of Virology and Biotechnology",
   "https://www.vector.nsc.ru/",
   "One of two facilities in the world authorised to hold live smallpox, the other being "
   "the US CDC. It has had a documented explosion and a laboratory-acquired infection. "
   "Whether the remaining stocks should be destroyed has been argued at the World Health "
   "Assembly for decades and repeatedly deferred \u2014 and since the sequence is published, "
   "the argument is now partly moot.",
   ["synthesis:repos", "rules:regulators"], base=BODY),
]

# =========================================== THE THINNEST REGIONS =============
IND27["KAZ"] = [
 e("National Center for Biotechnology of Kazakhstan", "https://biocenter.kz/",
   "Central Asia\u2019s largest biotechnology research institute, working on crops for "
   "steppe conditions and on veterinary vaccines. The region grows wheat at enormous "
   "scale and appears almost nowhere in accounts of agricultural biotechnology, which is "
   "a gap in the telling rather than in the activity.",
   ["seed:traits", "livestock:livestock"], base=BODY),
]

IND27["UZB"] = [
 e("Center of Genomics and Bioinformatics", "http://genomics.uz/",
   "Uzbekistan\u2019s genomics institute, with cotton as its central crop. Uzbek cotton has "
   "been the subject of a long international campaign over forced labour in the harvest \u2014 "
   "so the same crop carries an engineering question and a labour question, and the "
   "second is the one that changed practice.",
   ["seed:traits", "editing:agtech"], base=BODY),
]

IND27["GHA"] = [
 e("Council for Scientific and Industrial Research \u2014 Ghana",
   "https://csir.org.gh/",
   "Ghana\u2019s public research council, which developed Bt cowpea alongside the Nigerian "
   "institute and holds the national crop collections. West African public research is "
   "where the crops poor farmers actually eat get worked on, and it operates on budgets "
   "a fraction of any company on this map.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]

IND27["SEN"] = [
 e("Institut S\u00e9n\u00e9galais de Recherches Agricoles", "https://www.isra.sn/",
   "Senegal\u2019s agricultural research institute, working on millet, sorghum and cowpea \u2014 "
   "the crops of the Sahel, which no multinational breeds for because there is no market "
   "to capture. What happens to those crops depends almost entirely on public institutes "
   "like this one.",
   ["seed:traits", "seed:germplasm"], base=BODY),
]

IND27["FJI"] = [
 e("Pacific Community \u2014 Centre for Pacific Crops and Trees",
   "https://www.spc.int/cepact",
   "The regional genebank for Pacific island crops \u2014 taro, breadfruit, yam \u2014 held for "
   "countries too small to maintain national collections. Island crop diversity is "
   "concentrated, irreplaceable and directly exposed to sea level rise, and this is "
   "essentially the whole of its formal conservation.",
   ["seed:germplasm", "deextinct:biobank"], base=BODY),
]

IND27["PNG"] = [
 e("National Agricultural Research Institute \u2014 Papua New Guinea",
   "https://www.nari.org.pg/",
   "New Guinea is a centre of origin for sugarcane, banana and taro, and one of the most "
   "biologically diverse places on Earth. Its national research institute is small, its "
   "collections are globally significant, and the mismatch between those two facts is "
   "the ordinary condition of centres of origin.",
   ["seed:germplasm", "seed:traits"], base=BODY),
]
