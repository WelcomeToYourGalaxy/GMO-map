# -*- coding: utf-8 -*-
"""Industry entries, part 48. The biorisk governance layer.

WHAT THIS FILE IS NOT. It is not the Global BioLabs lab list. That report gives
regional totals, national scorecards and network membership; it names no
individual laboratory, and the saved map page carries no coordinates - the
markers are drawn from data the page fetches separately. So no BSL4 facility
points can be added from either file without inventing them, and none are.

WHAT IT IS. The report's Chapter 5 lists the bodies that actually govern
high-containment work internationally, and every one of them was missing from
this map. That is a real gap and a bad one: the map held the Biological Weapons
Convention and the Australia Group and nothing in between, which made the
governance of the most dangerous laboratories look emptier than it is - and
also less fragmented, which is the report's central finding.

The numbers worth carrying from the report, and used in the entries below:
69 BSL4 labs across 27 countries, 51 operational, 18 planned or under
construction. 57 BSL3+ labs. Of the 27 countries with BSL4 labs, 21 score high
on biosafety governance, 12 on biosecurity, and ONE on dual-use research
oversight.
"""
from ind1 import e, CO, BODY, REGI, ASSN

IND48 = {}

# ============================================== INTERNATIONAL NETWORKS =======
IND48["FRA"] = [
 e("ERINHA \u2014 European Research Infrastructure on Highly Pathogenic Agents",
   "https://www.erinha.eu/",
   "A pan-European network of ten BSL3+ and BSL4 laboratories that opens their "
   "facilities to outside scientists working on dangerous pathogens. Shared access "
   "is how a country without maximum containment gets work done in one \u2014 and it "
   "also means the people using a lab and the country answerable for it are not "
   "always the same.",
   ["wild:microbes", "rules:standards", "money:public"], base=BODY),
]

IND48["CAN"] = [
 e("BSL4ZNET \u2014 Biosafety Level 4 Zoonotic Laboratory Network",
   "https://www.bsl4znet.org/",
   "A dozen BSL4 laboratories in five countries sharing knowledge and training on "
   "zoonotic disease. Networks of this kind are the only routine contact between "
   "maximum containment facilities in different states: there is no inspectorate "
   "and no obligation to declare what is held, so a voluntary network is the "
   "nearest thing to mutual oversight that exists.",
   ["wild:microbes", "rules:standards", "livestock:livestock"], base=ASSN),
]

IND48["CHE"] = [
 e("International Federation of Biosafety Associations",
   "https://internationalbiosafety.org/",
   "A non-governmental federation of national and regional biosafety associations, "
   "providing training and professional certification in biorisk management. In "
   "most countries there is no licence to work in a containment laboratory, so a "
   "voluntary certificate from an international federation is the only credential "
   "the role has.",
   ["rules:standards", "rules:associations", "wild:microbes"], base=ASSN),
 e("ISO 35001 \u2014 biorisk management standard",
   "https://www.iso.org/standard/71293.html",
   "Published in 2019, this is the international standard for managing biological "
   "risk in a laboratory. It describes a management system rather than prescribing "
   "equipment, which is why it can be adopted anywhere \u2014 and it is voluntary "
   "everywhere, with no international mechanism to audit compliance. The Global "
   "BioLabs report's first recommendation is that laboratories doing "
   "high-consequence work should adopt it.",
   ["rules:standards", "wild:microbes"], base=BODY),
 e("WHO Laboratory Biosafety Manual",
   "https://www.who.int/publications/i/item/9789240011311",
   "The reference that defines what containment levels mean. Its fourth edition "
   "moved from prescribing equipment by pathogen to requiring a risk assessment for "
   "the work actually being done \u2014 which is more flexible and puts more weight "
   "on the judgement of the institution doing it. There is no definition of BSL3+ "
   "in it, or anywhere else, which is why that category is self-declared.",
   ["rules:standards", "wild:microbes"], base=BODY),
]

# =============================================== REGULATOR AND STATE GROUPS ==
IND48["USA"] = [
 e("International Experts Group of Biosafety and Biosecurity Regulators",
   "https://www.iegbbr.org/",
   "National regulators from eleven countries sharing practice on biosafety and "
   "biosecurity. Eleven is the number worth noticing: there are 27 countries with "
   "BSL4 laboratories, so most of the states running maximum containment are not in "
   "the room where regulators compare notes.",
   ["rules:regulators", "rules:standards", "wild:microbes"], base=BODY),
 e("Global Health Security Agenda",
   "https://globalhealthsecurityagenda.org/",
   "More than seventy countries matching donors to recipients for public health "
   "capacity building, with a specific package on biosafety and biosecurity. It is "
   "the main route by which a country without containment capability acquires one "
   "\u2014 which means the same programme builds the laboratories and is supposed to "
   "govern them.",
   ["money:public", "rules:standards", "wild:microbes"], base=BODY),
]

IND48["CAN"] += [
 e("Global Partnership Biosecurity Working Group",
   "https://www.gpwmd.com/",
   "The biosecurity arm of the G7-led Global Partnership Against the Spread of "
   "Weapons of Mass Destruction, funding capacity-building in more than twenty "
   "countries. Biosecurity assistance is delivered as a nonproliferation programme "
   "rather than a health one, which shapes what gets funded: securing pathogens "
   "attracts money that operating a laboratory safely does not.",
   ["money:defence", "rules:standards", "money:public"], base=BODY),
]

IND48["AUT"] = [
 e("UN Security Council Resolution 1540 Committee",
   "https://www.un.org/en/sc/1540/",
   "Requires every state to prohibit non-state actors from acquiring biological, "
   "chemical and nuclear weapons, and to report on the measures it has taken. It is "
   "binding on all UN members, which is rare in this field \u2014 and its "
   "implementation is measured by self-reporting, so what it actually produces is a "
   "record of what governments say they have done.",
   ["rules:regulators", "rules:standards", "money:defence"], base=BODY),
]

IND48["CHE"] += [
 e("UN Secretary-General's Mechanism for investigation of alleged use",
   "https://disarmament.unoda.org/wmd/secretary-general-mechanism/",
   "The only standing international capability to investigate an alleged use of "
   "biological weapons, since the Biological Weapons Convention has no verification "
   "system of its own. It relies on a roster of experts and laboratories nominated "
   "by member states and can only be triggered by the Secretary-General \u2014 an "
   "investigative body with no inspectors of its own.",
   ["rules:regulators", "money:defence", "wild:microbes"], base=BODY),
 e("WHO Joint External Evaluation",
   "https://www.who.int/emergencies/operations/international-health-regulations-monitoring-evaluation-framework",
   "A voluntary peer review of a country's capacity to prevent, detect and respond "
   "to health emergencies, covering nineteen technical areas of which biosafety and "
   "biosecurity is one. Voluntary and public: a country choosing to be evaluated "
   "and publishing the result is the closest thing to an inspection that exists for "
   "laboratory biosafety anywhere.",
   ["rules:regulators", "rules:standards", "wild:microbes"], base=BODY),
]

IND48["CHN"] = [
 e("Tianjin Biosecurity Guidelines for Codes of Conduct for Scientists",
   "https://www.tianjinbiosecurityguidelines.org/",
   "Ten guiding principles for responsible conduct in the life sciences, agreed "
   "between Chinese and international academies in 2021 and endorsed by the "
   "InterAcademy Partnership. They carry no force at all. Their significance is "
   "where they came from: a code of conduct for dual-use research negotiated with "
   "Chinese institutions is a rarer thing than another Western guideline.",
   ["rules:standards", "wild:microbes", "rules:associations"], base=ASSN),
]

