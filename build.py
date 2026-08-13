# -*- coding: utf-8 -*-
"""Retune the Live Global Project Map into the Live Global Genetic Engineering Map.

Everything structural is preserved verbatim: CSS, panels, filters, the index,
the wire renderer, the plate->satellite crossfade, SUBGEO, the admin drilldown,
the facility layer and the release (project) layer engine. Only subject-matter
content is replaced, line by line.
"""
# ---------------------------------------------------------------------------
# STATE OF THIS SCRIPT, 2026-08-12
#
# It parses and runs again: the stray HTML pasted at module level by earlier
# patches is gone, the broken string literals are repaired, and the legend, key
# box, record panel and filter tree are injected from tail.html rather than
# being lost.
#
# It is NOT yet a faithful rebuild. A run produces a working map that is missing
# three blocks still present only in index.html:
#
#     subjBox      the "what they work on" subject filter
#     REGIMED      the regulatory regime definitions shown in overlay popups
#     pjClusters   the region clustering and its click handling
#
# Those were added directly to index.html and never mirrored here. Until they
# are, INDEX.HTML REMAINS THE SOURCE OF TRUTH and a rebuild would lose them.
# ---------------------------------------------------------------------------

import io, json, sys, pathlib
from content import (TOUR, WIRE_THREADS, WIRE_FEEDS, js)
from facets import FACETS as DOMAINS, NAV_OPTIONS as INTENT_OPTIONS, NAV as INTENTS
ANGLE_OPTIONS = [("", "")]
ANGLEHINT = {}


# =============================================================== ROUND 3 =====
# Tone: the target is the decision machine — the firms and the agencies licensing
# them on a commercial timetable — not the organisms or the people at the bench.


TOUR[0] = {"t": u"Where we actually are", "h": u"Humanity has never before held a technology that rewrites the instructions of living things and then releases the result into a world it does not control. That is not a flourish; it is the plain description.<br><br>What separates this from every previous industrial hazard is that it compounds itself. Each tool makes the next one cheaper and faster to build. Each released organism becomes part of the environment against which the next assessment is written. The capability curve is exponential.<br><br>The enforcement curve is not. It is slow, national, negotiated, and in several jurisdictions moving backwards, as whole classes of engineered organism are written out of registration altogether \u2014 which means no application, no assessment, no register entry and nothing to object to.<br><br>The distance between those two curves is where this map lives."}

TOUR[1] = {"t": u"What this map is against \u2014 and what it isn\u2019t", "h": u"This is not an argument that engineered organisms are inherently wicked, or that the people at the bench are villains. A great deal of the science is careful, and some of it is beautiful.<br><br>The argument is about who is deciding, on what evidence, and in whose interest. A small number of firms and the agencies that license them are making irreversible, planet-scale decisions on a commercial timetable, largely on data they generate themselves and largely keep, under liability rules that do not price the downside and enforcement that cannot follow a gene across a border. Profit sets the pace and ethics is invited to catch up afterwards. That machine is the subject of this map.<br><br>Irreversibility is what makes the arrangement indefensible rather than merely unwise. A refused permit can be reapplied for next year. A contaminated landrace cannot be un-contaminated; a lost centre-of-origin population cannot be restored from a bank that never held it; and a patent asserted over a farmer\u2019s own saved seed is not undone by proving the pollen arrived uninvited. The spread register on this map holds 396 recorded incidents across 63 countries between 1997 and 2013, and it counts only what was found and reported.<br><br>So: not the organism. The machine around it."}



# --- the "Start here" tour: context first, then a worked example -------------
TOUR[:] = []   # the industry walkthrough now lives outside the map



SRC = 'base.html'
OUT = '/mnt/user-data/outputs/index.html'

lines = io.open(SRC, encoding='utf-8').read().split('\n')
N = len(lines)

R = {}        # 1-based line -> replacement string
DROP = set()  # 1-based lines to delete

def put(n, s):
    R[n] = s

def block(a, b, s):
    """Replace lines a..b (inclusive, 1-based) with s."""
    R[a] = s
    for i in range(a + 1, b + 1):
        DROP.add(i)

# ---------------------------------------------------------------- head ------
put(6, '<title>Live Global Genetic Frontlines Map</title>')

# ------------------------------------------------------------ help panel ----
put(298, '')   # the tour button now sits at the foot of the panel

block(299, 300, u'''    <b>What this shows.</b> This map is a research toolkit for people opposing the genetic engineering of organisms &mdash; the public registers, approval dossiers, unauthorised presence records, patent databases and watchdog archives that make a release visible, contestable and, where it has already spread, documentable. It covers engineered plants, animals, insects, trees, fish and microbes; gene drives and de-extinction; cloning; and the human side &mdash; germline editing, embryo selection and the in-vitro and assisted-reproduction industry that the same logic and the same money run through.<br><br>
    The organising fact is <b>unauthorised presence and destruction</b>. Unlike almost every other environmental fight, this one has no boundary: a released gene travels on pollen, on seed, on water, on a migrating animal, and it does not come back. The GM Contamination Register recorded <b>396 spread incidents into non-GM crops and wild relatives between 1997 and 2013, across 63 countries</b> &mdash; and that register counts only what was found and reported. Meanwhile the long-term population-level health studies you would expect for a global exposure of this size have still not been done. This map is built so that the record that <i>does</i> exist is easy to reach.<br><br>
    <div class="hb-fold collapsed"><div class="hb-fold-head" onclick="this.parentNode.classList.toggle('collapsed')"><span class="hb-car">&#9662;</span> How a resource&rsquo;s placement is decided</div><div class="hb-fold-body">A resource is placed at the level of the people it can help, not its street address. A national biosafety authority, a testing lab that accepts samples from anywhere, or a law firm that takes cases across a whole state is a region-wide source: it appears under &ldquo;Higher-level / region-wide sources&rdquo; at every county or region within that reach, <i>even though it is physically local to one place</i>. Its placement reflects who it can serve, not its location. Only genuinely place-bound resources (a county recorder, a single-district agricultural office) sit at the local level.</div></div><br><br>''')

put(302, u'    <b>1&middot; Lens pills (right)</b> &mdash; each lens is a kind of research: finding a release, corporate ownership, patents &amp; money, court records, biosafety &amp; unauthorised presence, FOI, land &amp; sites, people &amp; networks, monitoring, watchdogs, allies, and seed &amp; territory protection. Selecting one filters the map to that theme so you can see where those resources exist.<br>')

put(303, u'    <b>2&middot; Index</b> &mdash; a directory of the resources on the map. Group &amp; sort it (by country, level, lens\u2026) and search by name. <b>The index counter above reads the live dataset</b> &mdash; there is no honest way to state what fraction of every relevant source on Earth it represents, because no one has counted them all, so treat it as a growing verified set rather than a finished one. Every entry is a real, reachable source; where a country&rsquo;s register exists but has no machine-readable endpoint, that is said plainly rather than papered over.<br><br>')

put(304, u'    <b>Local facility dots.</b> Small coloured dots mark local government buildings &mdash; the physical offices where a campaign\u2019s records and decisions often live: <span style="color:#3f8068;">&#9679; police</span>, <span style="color:#5f8f48;">town halls</span>, <span style="color:#487d4f;">fire</span>, <span style="color:#4f8464;">gov offices</span> and agency HQs. For this subject the useful ones are the <b>town halls, agricultural offices and government offices</b> &mdash; local authorities are frequently the level at which a GMO-free zone is actually declared, and the level at which a consented trial next door first becomes public knowledge. <b>Facility dots become clickable once you zoom in (about zoom 8)</b> &mdash; click one for details (or toggle it off, bottom-right, to select regions instead). If a country\u2019s highlight won\u2019t select at higher zoom, a dot is likely intercepting the click; switch facilities off first.<br><br>')

put(305, u'    <b class="hl-sec">The live releases layer</b><br>')

put(306, u'''    This layer\u2019s dots are <b>real releases of engineered organisms</b> &mdash; field-trial consents, deliberate-release permits, cultivation and import approvals, and contained-use notifications &mdash; harvested from official biosafety registers (distinct from the muted local-facility dots described above). Some are already approved and planted; others are still applications under assessment, with a comment window that has not yet closed. <b>Those are the ones worth finding first.</b><br><br>    <b>Reading a dot.</b> A <b>solid dot</b> is an exact location from the record; a <b>dashed ring</b> means the register gave no coordinates \u2014 common, because many authorities publish only a district or a grid square \u2014 so it sits at country, state or district level. Open the record to find the actual site, then use the land-and-sites lens to resolve it to parcels. Because coordinate-less records are parked at a fallback point for their country, an occasional dense cluster reflects <b>missing coordinates in the source</b>, not a failed data pull. <b>Size and colour track the release\u2019s rated scale</b> (area consented, number of sites, or commercial vs trial status): bigger dots are larger releases, with colour shifting from cool <b>teal</b> for the smallest contained or single-plot work, through olive, gold and plum, to warm <b>rust</b> for full commercial cultivation approvals. Note: a small trial in a centre of origin, or beside a seed-production or organic holding, matters far more than a large one elsewhere.<br>    <div class="hb-fold collapsed"><div class="hb-fold-head" onclick="this.parentNode.classList.toggle('collapsed')"><span class="hb-car">&#9662;</span> A note on what &ldquo;scale&rdquo; means here</div><div class="hb-fold-body">Registers do not share a size unit. Some publish <b>hectares consented</b>, some a <b>number of trial sites</b>, some only a class of dealing (contained use / limited and controlled release / commercial release). Scale here is a normalised rating across those, not a single measured quantity \u2014 so treat it as a sorting aid, not a figure to cite. Where a register gives no size at all, the entry is shown at map scale by its dealing class.</div></div><br>''')

put(308, u'    Even with every resource here in hand, you don\u2019t need to be a lone wolf. Farmer unions, seed-saver networks, organic certifiers, beekeepers\u2019 associations, food-sovereignty coalitions, independent-science networks and the watchdog groups in the lenses above carry roots and hard-won experience that starting fresh can\u2019t match in time. Reaching out to them for guidance isn\u2019t a detour; it\u2019s often the fastest, wisest first move \u2014 and in this fight your neighbours inside the drift radius are allies who do not yet know they need to be.')

# ------------------------------------------------------------ wire lead -----
put(315, u'    <div class="wire-lead">The biotechnology machine runs on paper: a contained-use notification filed, a field-trial consent sought, an approval published in a register no one reads. That paperwork is also its weakness &mdash; every notification is a disclosure, every consultation a comment window, every consent a decision that can be challenged, and every register entry a permanent, citable record of who asked for what.<br><br>Against that machine grew a web of resistance &mdash; farmer unions and seed savers, beekeepers and organic certifiers, independent scientists who lost funding for publishing, Indigenous seed guardians defending centres of origin, and the lawyers who take unauthorised presence cases.<br><br>The fronts are everywhere at once &mdash; gene-edited crops slipping through deregulation, gene drives proposed for open release, engineered trees and fish and insects, patents asserted over saved seed, embryo editing, and an in-vitro industry expanding faster than the law tracking it. This <b>genetic-engineering news wire</b> watches for them: the releases entering the pipeline, the spread being found, and the people refusing them. Find the fight.</div>')

# --------------------------------------------------------------- header -----
put(358, '<div id="header"><h1 id="title">Live Global Genetic Frontlines Map</h1><div class="subtitle" id="subtitle"></div></div>')

# -------------------------------------------------------- intent options ----
opts = []
for v, label in INTENT_OPTIONS:
    if v == '__g':          # phase separator: visible, not selectable
        opts.append('    <option value="" disabled>%s</option>' % label)
    else:
        opts.append('    <option value="%s">%s</option>' % (v, label))
block(370, 387, '\n'.join(opts))

# --------------------------------------------------------- angle options ----
block(390, 398, '')   # angle selector removed: the map no longer proposes tactics

# ------------------------------------------------------------ filter tip ----
put(409, u'  <div class="filter-tip"><span class="tl">Try combining filters</span><b>Records &amp; data + Official</b> &mdash; the state\u2019s own biosafety record only, no watchdog or journalism voices. <b>Biosafety &amp; Contamination + Interpretive</b> &mdash; the independent scientists re-reading the dossiers the regulator accepted. <b>Any lens + Investigative journalism</b> &mdash; just the newsrooms working that beat. <b>Any lens + Official + Records &amp; data</b> &mdash; only the primary registers and dockets you can cite directly in a submission.</div>')

# ----------------------------------------------------- releases legend ------
put(420, '  <label class="f-status"><input type="checkbox" id="projChk" checked> Live releases &amp; consents</label>')

put(421, u'  <div class="proj-size"><span class="ps-lab">Release scale &mdash; select any</span><span class="ps-pill on" data-ms="all">All</span><span class="ps-pill" data-ms="3">Medium <i>multi-site trial</i></span><span class="ps-pill" data-ms="4">Large <i>regional / multi-season</i></span><span class="ps-pill" data-ms="5">Largest <i>commercial cultivation</i></span></div><div class="proj-size proj-phase"><span class="ps-lab">Consent phase &mdash; select any</span><span class="ps-pill on" data-ph="pre">In review <i>pre-consent &middot; applied / notified / under assessment</i></span><span class="ps-pill on" data-ph="post">Consented <i>post-consent &middot; approved / planted / marketed</i></span></div>')

put(422, u'  <div class="proj-search"><input id="projQ" type="search" placeholder="Search releases by organism, trait or applicant\u2026" autocomplete="off"><span id="projQn"></span></div>')

put(423, u'  <div class="proj-time"><span class="ps-lab">Filing recency \u2014 dated registers</span><span class="pt-pill on" data-tw="0">All ages</span><span class="pt-pill" data-tw="30">\u226430d</span><span class="pt-pill" data-tw="90">\u226490d</span><span class="pt-pill" data-tw="180">\u22646mo</span><span class="pt-pill" data-tw="365">\u22641yr</span><label class="pt-und"><input type="checkbox" id="pjUndated" checked> Include undated</label></div><div class="lp-detail collapsed"><div class="lp-detail-head" onclick="this.parentNode.classList.toggle(\'collapsed\')"><span class="lp-car">&#9662;</span> Where this data comes from &amp; what\'s not (yet) in it</div><div class="lp-detail-body">')

block(424, 450, u'''<b class="hl-sec">Where the live-releases data comes from</b><br>
    <b>Right now this layer is the United States only.</b> That is not the intention and it is not hidden here: it is what has actually been harvested. Every dot comes from the two public data files that APHIS Biotechnology Regulatory Services publishes and updates each business day, in the public domain. Nothing else currently feeds it.<br><br>
    <b>What is kept, and what is thrown away.</b> Only records with a release component survive \u2014 an import permit or an interstate movement permit is not an environmental release, and most rows in the source are one of those. Withdrawn, denied, superseded, cancelled and expired records are dropped, along with anything past its expiration date, because a lapsed authorisation is not a live release. Roughly nine in ten rows in the source are removed by those two gates.<br><br>
    <b>Every dot is a state centroid, and that is deliberate.</b> APHIS publishes the states a release is authorised in. It does not publish coordinates. So every record is marked imprecise and drawn as a dashed ring, and a cluster of rings over a state capital means <i>the register gave states, not sites</i>. Do not read a ring as a location. To find the actual ground, take the authorisation number to the land-and-sites lens.<br><br>
    <b>Scale is a sorting aid, not a measurement.</b> The current system publishes a count of declared release locations and nothing about area. Its predecessor published acreage, which is carried through where a record has it \u2014 so some older entries can say &ldquo;20 acres&rdquo; and newer ones cannot. The newer system publishes less about scale than the one it replaced.<br><br>
    <b>Confidential business information.</b> Where an applicant claimed CBI, the trait description in the source arrives partly redacted as [CBI]. Those records say so in their own description rather than presenting a redacted list as if it were complete.<br><br>
    <b class="hl-sec">Why the rest of the world is not here yet</b><br>
    Almost all of this is state-published \u2014 biosafety law in most countries requires a public register. The gaps are not gaps in publication but in <b>machine-readable</b> publication, and each one has a specific reason:<br>
    &bull; <b>Australia \u2014 OGTR.</b> The best release register in the world: every licence, every risk assessment, and published locations for active crop field-trial sites. It <b>cannot be harvested</b> \u2014 ogtr.gov.au disallows automated access in its robots.txt. Read it by hand; it is worth the time, and it is in the index.<br>
    &bull; <b>The Biosafety Clearing-House.</b> The global spine under the Cartagena Protocol, and the only genuinely cross-national record. Its site is a JavaScript application that returns nothing to a fetcher. The Secretariat does publish the national focal point list as a PDF, which is how the country directory on this map was extended.<br>
    &bull; <b>EU, Canada, Brazil, Argentina, India, New Zealand and the rest.</b> Real registers, named in the index with what each holds. None publishes a bulk file of the kind APHIS does; most are search forms over a database, and several are PDF minutes.<br>
    &bull; <b>Contained use is under-recorded everywhere.</b> Most laboratory work is notified rather than licensed, and notifications are rarely published individually. This layer will always under-count how much engineering is happening relative to how much is being released.<br>
    &bull; <b>Gene-edited organisms are increasingly invisible by design.</b> Where a jurisdiction has moved editing techniques outside registration \u2014 as the EU has now legislated for one class of them \u2014 there is no record to harvest. An absence of dots means the law stopped requiring one. This is the largest structural gap and it is growing.<br>
    &bull; <b>Tracking one across borders is harder than tracking a transgenic event.</b> This map keeps telling you to write down the OECD unique identifier, because it is the one string that follows a single engineered event through every country that has ruled on it. That system was designed around transgenic events \u2014 an applicant code, an event code and a check digit, identifying a specific insertion. Where an organism carries no transgene there is nothing for it to name, and in the Canadian register \u2014 the one harvestable place still listing both classes side by side \u2014 <b>not one of its 27 approved non-transgenic products carries an identifier, against 98 of 101 transgenic ones that do.</b> So the class being written out of registration in one jurisdiction after another is also the class the international identifier system cannot follow between them. Those two facts compound: an organism can be both unregistered where it is grown and unnameable everywhere else.<br>
    &bull; <b>The human side is not a release register at all.</b> Germline work, embryo selection, and the in-vitro and assisted-reproduction industry are covered through clinical-trial registries, national fertility regulators and clinic reporting. None of that maps to a release dot, so it lives in the lenses and the index instead of being forced into a layer it does not fit.<br><br>
    <b>No coverage percentage is claimed.</b> No dataset holds the true global count of releases, so any figure would be invented. What can be said honestly is the shape of the sample, which is what this panel does. Treat an empty area as unharvested, never as clean.<br></div></div>''')

# --------------------------------------------------- international bodies ---
IB = [
 {"name":"The Biosafety Clearing-House \u2014 Cartagena Protocol","guide":"BCH","lat":45.5019,"lng":-73.5674,"trackers":[
   {"name":"Biosafety Clearing-House (BCH)","url":"https://bch.cbd.int/",
    "desc":"The registry established under the Cartagena Protocol on Biosafety and run by the CBD Secretariat in Montreal. Parties are required to file every final decision on the domestic use, import or release of a living modified organism, together with risk assessments, national biosafety laws and the contact details of each country's competent national authority. CAN: find whether a given organism has been decided on in a given country, read the decision and the risk assessment filed with it, and identify exactly which office to write to. CAN'T: tell you where a trial is planted, or capture organisms a country has placed outside its GMO scheme. FOR: this is the first place to check when you want to know whether a release you have heard about has an international paper trail \u2014 and the fastest route to the named official who must answer you.",
    "tags":["projects:trackers","projects:nepa","environment:eia","records:publications"],"voice":"official","type":"records-data","trust":"record","scope":"own"},
   {"name":"Cartagena Protocol on Biosafety \u2014 text, parties and decisions","url":"https://bch.cbd.int/protocol",
    "desc":"The treaty itself, its party list, and the decisions of its governing meetings, including the Nagoya\u2013Kuala Lumpur Supplementary Protocol on liability and redress. CAN: establish whether the country you are working in is bound by advance-informed-agreement obligations, and what its liability regime is supposed to provide. CAN'T: enforce anything directly. FOR: knowing which obligations a regulator has already accepted is the difference between an objection and a legal argument.",
    "tags":["courts:liability","records:publications","environment:eia"],"voice":"official","type":"records-data","trust":"record","scope":"own"}]},

 {"name":"OECD \u2014 BioTrack","lat":48.8566,"lng":2.3522,"trackers":[
   {"name":"OECD BioTrack Product Database","url":"https://biotrackproductdatabase.oecd.org/",
    "desc":"Event-level record of transgenic products that have been approved for commercial use, keyed on the OECD unique identifier \u2014 the code that lets you follow one engineered event across every country that has ruled on it. CAN: cross-walk a national consent number to an international identifier and see who else has approved the same event. CAN'T: cover unapproved, trial-stage or gene-edited organisms outside the scheme. FOR: the identifier is the single most useful string to carry into every other database on this map.",
    "tags":["projects:trackers","spending:patents","environment:eia"],"voice":"official","type":"records-data","trust":"record","scope":"own"}]},

 {"name":"WIPO \u2014 patents over living material","lat":46.2270,"lng":6.1350,"trackers":[
   {"name":"PATENTSCOPE","url":"https://patentscope.wipo.int/",
    "desc":"WIPO's search across international (PCT) patent applications and dozens of national collections, full-text. CAN: find what is actually claimed over a construct, a trait, a seed line, a cell line or a sequence; identify the assignee and the licensing chain; and read the claims that would be asserted against a farmer whose crop is contaminated. CAN'T: tell you whether a patent has been enforced. FOR: patenting is the engine of the whole race, and it is the part of it that is fully public \u2014 read the claims before anyone reads them to you.",
    "tags":["spending:patents","corporate:ownership","courts:federal"],"voice":"official","type":"records-data","trust":"record","scope":"own"},
   {"name":"UPOV \u2014 International Union for the Protection of New Varieties of Plants","url":"https://www.upov.int/",
    "desc":"The treaty body behind plant-variety rights \u2014 the parallel regime to patents, and the one that most directly restricts saving, exchanging and replanting seed. CAN: establish which UPOV act a country has joined and therefore what a farmer's legal position on saved seed is. CAN'T: represent farmers' interests; it is a rights-holder body. FOR: a great many seed-sovereignty fights turn on which version of this treaty a government has signed up to.",
    "tags":["spending:patents","conserve:recognize","organizing:consent"],"voice":"official","type":"records-data","trust":"record","scope":"own"}]},

 {"name":"FAO \u2014 seed, food safety and the Plant Treaty","lat":41.8886,"lng":12.4886,"trackers":[
   {"name":"International Treaty on Plant Genetic Resources (Plant Treaty)","url":"https://www.fao.org/plant-treaty/en/",
    "desc":"The treaty covering access to crop genetic resources, benefit sharing, and \u2014 in Article 9 \u2014 Farmers' Rights, including the right to save, use, exchange and sell farm-saved seed subject to national law. CAN: give you a recognised international basis for a farmers'-rights argument, and access to national reports on how each country claims to be implementing it. CAN'T: override a national seed law. FOR: the counterweight to UPOV and to patent claims over seed, and the framework most Indigenous and campesino seed arguments are built on.",
    "tags":["conserve:recognize","conserve:acquire","spending:patents"],"voice":"official","type":"records-data","trust":"record","scope":"own"},
   {"name":"Codex Alimentarius (FAO/WHO)","url":"https://www.fao.org/fao-who-codexalimentarius/en/",
    "desc":"The joint FAO/WHO food-standards body, whose texts include the principles for the risk analysis of foods derived from modern biotechnology. CAN: show the internationally agreed standard a national risk assessment is supposed to meet \u2014 useful when a dossier plainly does not meet it. CAN'T: bind a regulator directly. FOR: comparing what was actually assessed against the standard the government says it follows is one of the strongest lines available in a submission.",
    "tags":["environment:eia","environment:health","records:publications"],"voice":"official","type":"records-data","trust":"record","scope":"own"}]},

 {"name":"Crop Trust & the Svalbard Global Seed Vault","lat":78.2359,"lng":15.4913,"trackers":[
   {"name":"Svalbard Global Seed Vault","url":"https://www.seedvault.no/",
    "desc":"The backup store for the world's crop seed collections, held in permafrost on Spitsbergen. Deposits are made by genebanks, not individuals, and remain the depositor's property. CAN: explain the duplication model that keeps a line recoverable after a local loss. CAN'T: accept seed from a farm directly. FOR: the principle it embodies \u2014 that a clean line must exist in more than one place before it is threatened \u2014 is the practical core of the seed-protection lens, and it applies at every scale down to a community seed library.",
    "tags":["conserve:acquire","conserve:restore"],"voice":"official","type":"records-data","trust":"record","scope":"own"},
   {"name":"Crop Trust \u2014 Genesys plant genetic resources portal","url":"https://www.genesys-pgr.org/",
    "desc":"Search across the accessions held in genebanks worldwide \u2014 landraces, wild relatives and traditional varieties, with passport data on where each was collected. CAN: establish whether an unmodified line from your region already exists in a bank, and where. CAN'T: guarantee an accession is available to you, or that it is uncontaminated. FOR: finding out what of your area's crop diversity has already been secured, and what has not \u2014 which is exactly the list worth acting on first.",
    "tags":["conserve:acquire","conserve:restore","environment:species"],"voice":"official","type":"records-data","trust":"record","scope":"own"}]},

 {"name":"GM Contamination Register \u2014 the global drift and spread record","lat":53.2587,"lng":-1.9130,"trackers":[
   {"name":"GM Contamination Register","url":"http://www.gmcontaminationregister.org/","status":"dormant",
    "desc":"The only dedicated global record of GM contamination and illegal-release incidents, established in 2005 by GeneWatch UK and Greenpeace International and recognised by the Biosafety Clearing-House. Its published analysis covers 1997 to the end of 2013: 396 incidents across 63 countries, with rice accounting for roughly a third of them despite no GM rice being commercially grown anywhere. CAN: show that drift is routine rather than exceptional, and give dated, sourced precedents involving specific events and crops. CAN'T: give you current-year incidents \u2014 it is marked dormant here because updating appears to have stopped. FOR: this is the evidentiary backbone of a containment argument, and nothing has replaced it.",
    "tags":["environment:pollution","environment:incidents","advocacy:watchdog"],"voice":"interpretive","type":"records-data","trust":"record","scope":"own"}]},
]


# --- global tools live once, at international level, not 29 times over --------
IB += [
 {"name":"Earth observation \u2014 open satellite imagery","lat":41.8267,"lng":12.6742,"trackers":[
   {"name":"Copernicus Browser","url":"https://dataspace.copernicus.eu/",
    "desc":"Free Sentinel-1 and Sentinel-2 imagery for the whole planet, browsable by date at ten-metre resolution. CAN: watch a consented trial plot through a growing season, compare two dates side by side, and export a dated screenshot you can cite. CAN'T: resolve individual plants or read a sign. FOR: a field trial is visible from orbit long before its results are published, and this is the cheapest way to establish that something was planted when the register says it was.",
    "tags":["osint:satellite","projects:local","environment:pollution"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"USGS EarthExplorer","url":"https://earthexplorer.usgs.gov/",
    "desc":"The Landsat archive back to 1972, plus aerial photography and declassified imagery. CAN: establish what a site looked like decades ago \u2014 the baseline against which a change is a change. CAN'T: match Sentinel for recent revisit frequency. FOR: historical depth is what turns an image into evidence; a single recent photograph proves very little on its own.",
    "tags":["osint:satellite","osint:baselines","financial:property"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"NASA Worldview","url":"https://worldview.earthdata.nasa.gov/",
    "desc":"Daily global imagery with hundreds of overlay layers, including vegetation indices and fire detection. CAN: see broad-scale change fast, and pull layers that show crop vigour rather than just colour. CAN'T: give you high resolution. FOR: useful for the regional picture around a site, and for anything seasonal.",
    "tags":["osint:satellite","osint:baselines","environment:species"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"OpenStreetMap","url":"https://www.openstreetmap.org/",
    "desc":"The open map of the world, including field boundaries, farm tracks, processing plants and laboratory buildings where contributors have added them. CAN: identify access roads, adjacent landholdings and nearby infrastructure around a site. CAN'T: be assumed complete or current. FOR: the practical geography of a site \u2014 who reaches it, and from where \u2014 is usually here and nowhere else.",
    "tags":["osint:satellite","projects:infrastructure","financial:property"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"}]},

 {"name":"Archiving & change monitoring","lat":37.7823,"lng":-122.4714,"trackers":[
   {"name":"Wayback Machine","url":"https://web.archive.org/",
    "desc":"Archived copies of web pages over time, and a Save Page Now button that captures one on demand. CAN: prove what a company or an agency said on a given date, after they have changed it. CAN'T: capture what was never published. FOR: archive every page you intend to rely on the day you find it \u2014 approval pages, corporate claims and consultation notices get revised quietly and often.",
    "tags":["records:archive","osint:web","osint:alerts"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"archive.today","url":"https://archive.today/",
    "desc":"A second, independent web archive that captures pages the Wayback Machine sometimes cannot, including some behind scripts. CAN: preserve a page as a fixed image plus text. CAN'T: be relied on for deep historical coverage. FOR: archive anything important in both places; single-archive dependence has failed people before.",
    "tags":["records:archive","osint:web"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"Google Alerts","url":"https://www.google.com/alerts",
    "desc":"Standing email alerts on any search string. CAN: get told the day a company name, a consent number, an event identifier or a crop-and-country pair appears anywhere it indexes. CAN'T: reach registers that publish only as PDFs behind forms. FOR: set alerts on the OECD unique identifier as well as the trade name \u2014 the identifier surfaces filings the trade name misses.",
    "tags":["osint:alerts","osint:web"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"medium"}]},

 {"name":"Independent GM testing \u2014 laboratories & methods","lat":45.8100,"lng":8.6260,"trackers":[
   {"name":"EU Reference Laboratory for GM Food and Feed (JRC)","url":"https://joint-research-centre.ec.europa.eu/",
    "desc":"The reference laboratory that validates event-specific detection methods and publishes them, together with the reference material each method needs. CAN: find the validated method for detecting a specific event \u2014 which is what you hand a commercial lab so its result is defensible. CAN'T: test your sample for you. FOR: the difference between \u2018we think there is contamination\u2019 and a result that survives challenge is usually which method was used.",
    "tags":["environment:testing","environment:incidents","organizing:research"],"voice":"official","type":"records-data","kind":"structured","skind":"research","trust":"record"},
   {"name":"Eurofins \u2014 GMO testing","url":"https://www.eurofins.com/",
    "desc":"The largest agri-food testing network worldwide, with accredited GMO screening and event-specific quantification in most regions. CAN: get seed, grain, feed, honey or processed food tested to an accredited standard, with a report you can put in a submission. CAN'T: be cheap for a single sample \u2014 organise a group. FOR: this is the practical capability the public actually has; use it before a trial goes in, not only after.",
    "tags":["environment:testing","organizing:research","environment:incidents"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"research","trust":"medium"},
   {"name":"SGS","url":"https://www.sgs.com/",
    "desc":"Global inspection and testing company with GMO analysis in its agriculture division. CAN: reach testing capacity in regions where Eurofins is thin, including much of Africa and Latin America. CAN'T: give independent interpretation \u2014 you get a number, not an argument. FOR: a second laboratory on a split sample is what stops a result being dismissed as a one-off.",
    "tags":["environment:testing","organizing:research"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"research","trust":"medium"}]},

 {"name":"Corporate ownership & money, worldwide","lat":51.5074,"lng":-0.1278,"trackers":[
   {"name":"OpenCorporates","url":"https://opencorporates.com/",
    "desc":"The largest open database of companies, drawn from official registers in over a hundred jurisdictions, with officer and parent links. CAN: follow a permit applicant up through its holding structure across borders in one search. CAN'T: reveal beneficial owners a jurisdiction does not publish. FOR: the fastest route from a name on a licence to the group that actually owns it.",
    "tags":["corporate:ownership","corporate:filings","people:professional"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"OCCRP Aleph","url":"https://aleph.occrp.org/",
    "desc":"Investigative search across company registries, leaks, sanctions lists, court records and procurement data, assembled by investigative journalists. CAN: run one name across dozens of datasets at once, including material no single registry holds. CAN'T: be treated as verified without checking the underlying source. FOR: use it to find where to look, then cite the primary record it points you to.",
    "tags":["corporate:ownership","advocacy:data","spending:contracts"],"voice":"interpretive","type":"investigative-journalism","kind":"journalism","skind":"media","trust":"high"},
   {"name":"ICIJ Offshore Leaks Database","url":"https://offshoreleaks.icij.org/",
    "desc":"Structured data from the Panama, Paradise, Pandora and Offshore Leaks investigations. CAN: check whether a company, director or intermediary appears in leaked offshore structures. CAN'T: prove wrongdoing \u2014 presence is not an allegation. FOR: an offshore layer between a licence applicant and its owner is a fact worth establishing before you rely on the register.",
    "tags":["corporate:ownership","advocacy:data"],"voice":"interpretive","type":"investigative-journalism","kind":"journalism","skind":"media","trust":"high"},
   {"name":"Open Ownership Register","url":"https://register.openownership.org/",
    "desc":"Beneficial-ownership data consolidated from the jurisdictions that publish it. CAN: identify natural persons behind companies where the law requires disclosure. CAN'T: cover jurisdictions that publish nothing, which is most of them. FOR: where it has data it answers the question every other corporate source only approaches.",
    "tags":["corporate:ownership","people:professional"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"}]},

 {"name":"Land, tenure & territory, worldwide","lat":53.2194,"lng":6.5665,"trackers":[
   {"name":"Land Portal","url":"https://landportal.org/",
    "desc":"Aggregated land-governance data, national profiles and a library covering tenure law in most countries. CAN: establish how land tenure and registration actually work in a country before you go looking for a parcel record. CAN'T: give you the parcel itself. FOR: knowing whether a country even has a public cadastre saves days of searching for one that does not exist.",
    "tags":["financial:property","conserve:recognize","advocacy:data"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"LandMark","url":"https://landmarkmap.org/",
    "desc":"Global platform mapping Indigenous and community lands, both formally recognised and customarily held. CAN: check whether a proposed release site sits on or beside land held by a community whose consent should have been sought. CAN'T: be complete \u2014 much customary tenure is unmapped. FOR: a site inside community land changes the consultation question from procedural to substantive.",
    "tags":["financial:property","organizing:consent","conserve:recognize","environment:cultural"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"Land Matrix","url":"https://landmatrix.org/",
    "desc":"Independent database of large-scale land acquisitions worldwide, with investor, size, intended crop and status. CAN: identify who has acquired agricultural land at scale in a country, and what they intend to grow on it. CAN'T: capture deals never made public. FOR: the crop named in an acquisition often tells you which trait approval is coming next.",
    "tags":["financial:property","corporate:ownership","projects:trackers"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"}]},

 {"name":"Researchers, publications & retractions","lat":38.9959,"lng":-77.1013,"trackers":[
   {"name":"PubMed","url":"https://pubmed.ncbi.nlm.nih.gov/",
    "desc":"The biomedical and life-science literature index. CAN: find the published studies behind a risk assessment, the authors, and their declared funding and conflicts. CAN'T: reach the unpublished applicant data that most assessments actually rest on. FOR: comparing what a dossier cites against what the literature contains is one of the most productive hours you can spend on an assessment.",
    "tags":["environment:health","environment:eia","people:professional"],"voice":"official","type":"records-data","kind":"structured","skind":"index","trust":"record"},
   {"name":"OpenAlex","url":"https://openalex.org/",
    "desc":"Open index of scholarly works, authors, institutions and funders, with the citation graph. CAN: map who funds whom, trace an author's institutional and industry affiliations over time, and find every paper citing a contested study. CAN'T: assess quality. FOR: the funder and affiliation fields are how you establish an advisory-committee member's industry ties without alleging anything.",
    "tags":["people:professional","spending:contracts","advocacy:data"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"index","trust":"high"},
   {"name":"Retraction Watch Database","url":"https://retractiondatabase.org/",
    "desc":"Comprehensive record of retracted and corrected papers, with the stated reason. CAN: check whether a study cited in a dossier \u2014 or by a campaign \u2014 has been retracted, corrected or had an expression of concern issued. CAN'T: settle whether a retraction was justified. FOR: check your own citations here before anyone else does; this field has retractions on both sides of the argument.",
    "tags":["environment:health","advocacy:data","people:professional"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"Espacenet","url":"https://worldwide.espacenet.com/",
    "desc":"The European Patent Office's search across more than 140 million patent documents worldwide, with family and legal-status data. CAN: follow one invention across every jurisdiction it was filed in, and see where it lapsed, was opposed or was revoked. CAN'T: give you US litigation history. FOR: the patent family view shows which countries a company thought worth protecting, which is a map of commercial intent.",
    "tags":["spending:patents","corporate:ownership"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"}]},
]


# --- regional blocs and global movements, which had no home on the map --------
IB += [
 {"name":"European Union \u2014 authorisation, courts & lobbying","lat":50.8467,"lng":4.3525,"trackers":[
   {"name":"EFSA \u2014 GMO Panel opinions","url":"https://www.efsa.europa.eu/",
    "desc":"The scientific opinions on which every EU-wide authorisation rests, published in full with the applicant\u2019s dossier summary. CAN: read the assessment for any GM food, feed or cultivation application in the EU, including the minority positions where the panel divided. CAN'T: give you the applicant\u2019s raw data, which is released only on request and often partially. FOR: the Commission runs a 30-day public comment window once EFSA publishes an opinion; comments go in through Connect.EFSA and are archived on OpenEFSA. Thirty days, from a publication date you have to be watching for, is the most reachable intervention point in the European system \u2014 and the easiest to miss.",
    "tags":["environment:eia","records:calendars","projects:nepa"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"European Commission \u2014 GMO authorisation & register","url":"https://food.ec.europa.eu/plants/genetically-modified-organisms_en",
    "desc":"The Commission\u2019s GMO pages, including the register of GMOs authorised for food and feed. The framework changed in 2026: Regulation (EU) 2026/1388 on new genomic techniques was adopted by the Council on 21 April and Parliament on 17 June 2026, entered into force on 16 July 2026 and applies from 17 July 2028. It splits NGT plants in two \u2014 NGT-1, treated broadly as conventional and outside the GMO authorisation and labelling regime, and NGT-2, which stays inside it. CAN: establish what is authorised across the member states, what is pending, and which category a plant falls into. CAN'T: cover national field-trial notifications, which sit with member states. FOR: the NGT-1 category is the single largest deliberate reduction in the European public record on this subject, and the run-up to 2028 is when the implementing detail gets written.",
    "tags":["projects:trackers","projects:nepa","records:publications"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"Court of Justice of the European Union","url":"https://curia.europa.eu/",
    "desc":"Judgments and Advocate General opinions, searchable and free. CAN: read the rulings that decided whether organisms produced by newer editing techniques fall inside the GMO Directive, and the cases on member-state safeguard measures. CAN'T: hear a case brought by an individual directly \u2014 most arrive by referral from a national court. FOR: the referral route means a national case can end up setting law for the whole Union, which is how the mutagenesis question was decided.",
    "tags":["courts:federal","courts:isds","projects:nepa"],"voice":"official","type":"records-data","kind":"structured","skind":"court","trust":"record"},
   {"name":"EUR-Lex","url":"https://eur-lex.europa.eu/",
    "desc":"All EU law in every official language, with the legislative history of each instrument. CAN: read the directive or regulation actually governing a decision, and follow how a text changed between proposal and adoption. CAN'T: tell you how a member state implemented it. FOR: the difference between what the Commission proposed and what was finally adopted is usually where the lobbying shows.",
    "tags":["records:publications","courts:federal","conserve:protect"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"EU Transparency Register","url":"https://transparency-register.europa.eu/",
    "desc":"Declared lobbying by organisations seeking to influence EU institutions, with budgets, staff, clients and declared meetings. CAN: see what an agricultural-biotechnology firm or trade body spends on EU lobbying and which officials it met. CAN'T: capture anything undeclared. FOR: cross-reference the meeting records against the dates of an authorisation file and the pattern is often visible without any inference at all.",
    "tags":["spending:lobbying","people:professional","corporate:nonprofit"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"European Ombudsman","url":"https://www.ombudsman.europa.eu/",
    "desc":"Investigates maladministration by EU institutions, including EFSA and the Commission, and publishes its decisions. CAN: complain about a refused document request, an inadequate consultation or an unmanaged conflict of interest \u2014 free, and no lawyer needed. CAN'T: overturn a decision. FOR: the cheapest formal route in Europe, and its published findings on EFSA\u2019s independence rules have changed practice before.",
    "tags":["courts:grievance","records:access","people:professional"],"voice":"official","type":"records-data","kind":"structured","skind":"oversight","trust":"record"}]},

 {"name":"Africa \u2014 regional biosafety & food sovereignty","lat":9.0108,"lng":38.7613,"trackers":[
   {"name":"African Union","url":"https://au.int/",
    "desc":"The continental body behind the African Model Law on Biosafety and the network of expertise that advises member states on biosafety regulation. CAN: reach the continental policy framework that national laws across Africa are drafted against. CAN'T: regulate directly \u2014 approvals remain national. FOR: much of African biosafety law derives from a single model text, so understanding it explains the shape of thirty national regimes at once.",
    "tags":["projects:nepa","conserve:recognize","records:publications"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"},
   {"name":"COMESA","url":"https://www.comesa.int/",
    "desc":"The Common Market for Eastern and Southern Africa, which adopted a regional biotechnology and biosafety policy intended to move approvals from national to regional level. CAN: understand the push to harmonise approvals across nineteen countries, and who is driving it. CAN'T: be treated as a permit register. FOR: regional harmonisation would mean one approval opens many borders \u2014 which is exactly why it is contested by farmer organisations across the region.",
    "tags":["projects:nepa","conserve:protect","advocacy:frontgroups"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"},
   {"name":"Alliance for Food Sovereignty in Africa (AFSA)","url":"https://afsafrica.org/",
    "desc":"The continent\u2019s largest civil-society alliance on food systems, with member networks in most African countries, working on seed law, biosafety and farmer-managed seed systems. CAN: find the organised opposition in a specific African country, and the analysis of seed-law harmonisation across regional blocs. CAN'T: act as an official record. FOR: for most of Africa this is the fastest route from a continental question to a named local organisation.",
    "tags":["organizing:help","conserve:recognize","advocacy:watchdog"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"}]},

 {"name":"Global farmer & food-sovereignty movements","lat":41.3874,"lng":2.1686,"trackers":[
   {"name":"La V\u00eda Campesina","url":"https://viacampesina.org/en/",
    "desc":"The international peasant movement, coordinating farmer organisations across some eighty countries, and the origin of the food-sovereignty framing now used in international law. CAN: reach organised farmers at national level almost anywhere, and the political argument on seed as a right rather than a product. CAN'T: act as a technical or regulatory source. FOR: farmer organisations carry standing, numbers and legitimacy that no research group does, and this is the network that connects them.",
    "tags":["organizing:help","conserve:recognize","conserve:acquire"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"},
   {"name":"GRAIN","url":"https://grain.org/",
    "desc":"Small international organisation researching corporate control of the food system, seed laws and land deals, publishing in several languages with a deep open archive. CAN: get the country-by-country account of how seed law was changed and who pushed for it \u2014 material that exists almost nowhere else. CAN'T: act as an official record. FOR: their seed-law tracking is the reference work on how farmers lost the legal right to save seed, jurisdiction by jurisdiction.",
    "tags":["advocacy:data","conserve:recognize","spending:patents"],"voice":"interpretive","type":"investigative-journalism","kind":"journalism","skind":"research","trust":"high"},
   {"name":"ETC Group","url":"https://www.etcgroup.org/",
    "desc":"Research organisation tracking concentration in the agricultural-input industry and emerging technologies including gene drives and synthetic biology. CAN: get the market-share and merger analysis behind the four-firm structure, and early technical mapping of technologies before they reach a register. CAN'T: act as an official record. FOR: their concentration figures are the ones most widely cited in this argument, and they publish the workings.",
    "tags":["corporate:ownership","advocacy:data","projects:trackers"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"research","trust":"high"},
   {"name":"PAN International","url":"https://pan-international.org/",
    "desc":"The Pesticide Action Network federation, with regional centres across Asia-Pacific, Africa, Latin America, Europe and North America. CAN: reach regional organisations with laboratory and monitoring capacity, particularly where herbicide-tolerant cropping is the issue. CAN'T: substitute for a biosafety-specific source. FOR: the herbicide regime a trait enables is a separate evidentiary track from the trait itself \u2014 keep them apart, and use this for the former.",
    "tags":["organizing:help","environment:health","environment:testing"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"}]},
]


IB += [
 {"name":"AfricanLII \u2014 free African law","lat":-33.9249,"lng":18.4241,"trackers":[
   {"name":"AfricanLII","url":"https://africanlii.org/",
    "desc":"The hub for the African legal information institutes \u2014 free legislation and case law for a growing set of African jurisdictions, several of which have no other public source. CAN: reach a country\u2019s biosafety statute and any litigation under it, for jurisdictions where the government publishes nothing searchable. CAN'T: be complete; coverage varies sharply by country. FOR: for much of Africa this is the only route to the legal text, and the text is usually the argument.",
    "tags":["courts:federal","records:publications","conserve:protect"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"court","trust":"high"}]},
 {"name":"WorldLII \u2014 federated world law","lat":-33.9173,"lng":151.2313,"trackers":[
   {"name":"WorldLII","url":"http://www.worldlii.org/",
    "desc":"The world legal information institute, federating searches across the national and regional legal information institutes. CAN: search case law across dozens of jurisdictions at once for a company name, an organism or a statutory phrase. CAN'T: match a national database for depth in any one country. FOR: use it to find out which jurisdictions have litigated your question, then go to the national source for the full text.",
    "tags":["courts:federal","courts:state","records:publications"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"court","trust":"high"}]},
]


IB += [
 {"name":"Officials, interests & the revolving door","lat":38.8977,"lng":-77.0365,"trackers":[
   {"name":"LittleSis","url":"https://littlesis.org/",
    "desc":"A free database of the relationships between powerful people and organisations \u2014 board seats, donations, employment histories, government positions \u2014 built and maintained collaboratively. CAN: map the connections between a company\u2019s directors, its funders and the officials deciding on its applications, and add what you find yourself. CAN'T: be assumed complete or current; verify each link against its cited source. FOR: it is built for exactly this task and it shows its sources, which means you can cite the source rather than the map.",
    "tags":["people:professional","corporate:ownership","advocacy:data"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"Integrity Watch EU","url":"https://www.integritywatch.eu/",
    "desc":"Declared meetings between EU officials and lobbyists, plus MEP side-income and expert-group composition, made searchable. CAN: see who met which Commission official, when, and on what \u2014 and who sits on the expert groups advising a file. CAN'T: capture undeclared contact. FOR: expert-group composition is the quietest form of influence and the easiest to demonstrate, because the membership is published.",
    "tags":["people:professional","spending:lobbying","advocacy:frontgroups"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"},
   {"name":"ORCID","url":"https://orcid.org/",
    "desc":"Persistent identifiers for researchers, linking a named person to their publications, employment history and funding. CAN: disambiguate a common name and establish where a committee member has worked and who paid for their research. CAN'T: force anyone to keep a record current. FOR: the employment history is the part that matters \u2014 it is how an industry affiliation from ten years ago becomes visible.",
    "tags":["people:professional","spending:contracts"],"voice":"official","type":"records-data","kind":"structured","skind":"index","trust":"record"},
   {"name":"As You Sow","url":"https://www.asyousow.org/",
    "desc":"Shareholder-advocacy organisation filing resolutions at annual meetings, with a public database of resolutions and outcomes. CAN: see which resolutions have been put to agribusiness companies, how they were voted, and what disclosure they sought. CAN'T: act without shares \u2014 filing requires a holding. FOR: a shareholder resolution forces a company to answer a question in writing, in public, on a fixed date, which no other lever does as cheaply.",
    "tags":["people:shareholder","corporate:filings","organizing:runners"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"},
   {"name":"Interfaith Center on Corporate Responsibility","url":"https://www.iccr.org/",
    "desc":"A coalition of institutional investors that has filed shareholder resolutions on agricultural and environmental practice for decades. CAN: find investors already engaged with a company and the resolutions they have filed. CAN'T: represent you. FOR: institutional investors get meetings that campaigners do not, and they are sometimes asking the same question you are.",
    "tags":["people:shareholder","corporate:finance","organizing:help"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"}]},
]


IB += [
 {"name":"Changing the rule \u2014 international complaint mechanisms","lat":46.2044,"lng":6.1432,"trackers":[
   {"name":"Aarhus Convention Compliance Committee","url":"https://unece.org/environment-policy/public-participation/aarhus-convention-introduction",
    "desc":"The treaty on access to information, public participation and access to justice in environmental matters, with a compliance committee that accepts communications from members of the public alleging a Party is not complying. CAN: challenge a whole national regime \u2014 a consultation window too short to be meaningful, evidence withheld as commercial confidence, a court fee structure that puts review out of reach \u2014 rather than one permit. Free, no lawyer required, and findings are published. CAN'T: overturn a decision or award compensation. FOR: this is the most under-used route on the map. It reaches the procedure itself, and procedural failure is far easier to prove than harm.",
    "tags":["courts:strategic","courts:grievance","records:access"],"voice":"official","type":"records-data","kind":"structured","skind":"oversight","trust":"record"},
   {"name":"OECD National Contact Points \u2014 Guidelines for Multinational Enterprises","url":"https://mneguidelines.oecd.org/",
    "desc":"Every adhering country runs a National Contact Point that accepts complaints ('specific instances') against a multinational for conduct anywhere in the world, including its supply chain. CAN: bring a complaint against a company in its home country over conduct in yours, with no legal standing requirement and no fee. CAN'T: impose a binding remedy \u2014 the outcome is mediation and a published statement. FOR: a published NCP statement is a documented finding about a company\u2019s conduct, and it can be filed where the parent sits rather than where the harm did.",
    "tags":["courts:strategic","courts:grievance","corporate:ownership"],"voice":"official","type":"records-data","kind":"structured","skind":"oversight","trust":"record"},
   {"name":"UN Special Procedures \u2014 submit a complaint","url":"https://www.ohchr.org/en/special-procedures-human-rights-council",
    "desc":"The Human Rights Council\u2019s independent experts, including the Special Rapporteurs on the right to food, on toxics and human rights, and on the rights of Indigenous Peoples. They accept communications about specific situations and write to governments and companies about them. CAN: get an independent UN expert to put questions to a government in writing, on the record, about a release, a seed law or a consultation failure. CAN'T: compel any answer. FOR: several rapporteurs have reported directly on seed law and agrochemicals; a government replying to one of them creates a citable position it then has to live with.",
    "tags":["courts:strategic","courts:grievance","conserve:recognize"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"},
   {"name":"Escaz\u00fa Agreement","url":"https://www.cepal.org/en/escazuagreement",
    "desc":"The Latin American and Caribbean treaty on environmental access rights, and the first anywhere to include binding provisions protecting environmental defenders. CAN: ground an argument about withheld information or excluded participation in a ratified regional treaty, in the region where most centre-of-origin crops sit. CAN'T: be invoked in states that have not ratified \u2014 check first. FOR: the defender-protection provisions matter as much as the access ones for anyone organising in the region.",
    "tags":["courts:strategic","records:access","organizing:safety"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"},
   {"name":"Inter-American Commission on Human Rights","url":"https://www.oas.org/en/iachr/",
    "desc":"Receives petitions alleging violations by member states, and can issue precautionary measures quickly where there is a risk of irreparable harm. CAN: bring a case about consultation with Indigenous or campesino communities, or about a release threatening a food system, after domestic remedies are exhausted. CAN'T: act before domestic routes are used up, except in narrow circumstances. FOR: the Inter-American system has the strongest jurisprudence anywhere on free, prior and informed consent, and it is binding on the states that accept the Court\u2019s jurisdiction.",
    "tags":["courts:federal","courts:strategic","organizing:consent"],"voice":"official","type":"records-data","kind":"structured","skind":"court","trust":"record"},
   {"name":"African Commission on Human and Peoples' Rights","url":"https://achpr.au.int/",
    "desc":"Receives communications against African Union member states, including on the right to a satisfactory environment, which the African Charter states explicitly \u2014 unusually among human rights treaties. CAN: bring an environmental-rights claim on a treaty text that names the right directly. CAN'T: move quickly; proceedings are slow. FOR: the explicit environmental right in the African Charter is a stronger textual hook than most regional systems provide.",
    "tags":["courts:federal","courts:strategic","conserve:recognize"],"voice":"official","type":"records-data","kind":"structured","skind":"court","trust":"record"},
   {"name":"CBD \u2014 synthetic biology & gene drive decisions","url":"https://www.cbd.int/",
    "desc":"The Convention on Biological Diversity, whose Conference of the Parties has repeatedly taken decisions on synthetic biology and on organisms containing engineered gene drives, including on the conditions for any release. CAN: cite the standing international position on gene drives, and follow the negotiation as it moves. CAN'T: enforce \u2014 decisions bind Parties politically rather than directly. FOR: no gene-drive organism has been released anywhere yet, so for once the rules are being written before the thing exists. The nearest approach stalled in 2025, when Burkina Faso sealed Target Malaria\u2019s facilities on 18 August and suspended its activities on 22 August, days after a non-drive trial release at Souroukoudingan on 11 August.",
    "tags":["courts:strategic","projects:nepa","environment:species"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"}]},

 {"name":"Strategic & public-interest environmental litigation","lat":44.0521,"lng":-123.0868,"trackers":[
   {"name":"ELAW \u2014 Environmental Law Alliance Worldwide","url":"https://elaw.org/",
    "desc":"A network of public-interest environmental lawyers and scientists across more than seventy countries, which supplies free legal and scientific back-up to partners bringing cases. CAN: get a lawyer in your own jurisdiction connected to expert evidence and to counterparts who have run the same argument elsewhere. CAN'T: litigate for you directly. FOR: the single most useful entry on this map for anyone outside the wealthy jurisdictions \u2014 it exists precisely to move expertise to where the case is.",
    "tags":["courts:strategic","organizing:legal","organizing:experts"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"legalaid","trust":"high"},
   {"name":"ClientEarth","url":"https://www.clientearth.org/",
    "desc":"Environmental lawyers who litigate against governments and EU institutions to change how law is applied, with offices across Europe and beyond. CAN: see how a systemic case against a regulator is actually built, and reach lawyers who have brought them. CAN'T: take every case offered. FOR: their model is the one to study if the target is the regulator\u2019s practice rather than a single decision.",
    "tags":["courts:strategic","organizing:legal","records:access"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"legalaid","trust":"high"},
   {"name":"CIEL \u2014 Center for International Environmental Law","url":"https://www.ciel.org/",
    "desc":"Works on international environmental law, including biosafety, biotechnology governance and the treaty processes around synthetic biology. CAN: get the legal analysis of what a treaty text actually requires, and support in using international mechanisms. CAN'T: act as a domestic litigator. FOR: when the question is what an international instrument obliges a government to do, this is the source that answers it.",
    "tags":["courts:strategic","records:publications","conserve:recognize"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"research","trust":"high"},
   {"name":"Earthjustice","url":"https://earthjustice.org/",
    "desc":"The largest US public-interest environmental law organisation, litigating against federal agencies at no charge to clients. CAN: reach litigators who have repeatedly challenged US pesticide and biotechnology approvals, and read their filings. CAN'T: work outside its intake criteria. FOR: US approvals are challenged through administrative-law arguments about what an agency failed to consider, and this is where that craft lives.",
    "tags":["courts:strategic","courts:federal","organizing:legal"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"legalaid","trust":"high"},
   {"name":"AIDA \u2014 Interamerican Association for Environmental Defense","url":"https://aida-americas.org/",
    "desc":"Regional environmental law organisation working across Latin America, including before the Inter-American human rights bodies. CAN: get regional legal strategy and support in bringing a case through the Inter-American system. CAN'T: replace domestic counsel. FOR: the route from a national failure to the Inter-American Commission is procedural and unforgiving; this is who knows it.",
    "tags":["courts:strategic","organizing:legal","organizing:consent"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"legalaid","trust":"high"},
   {"name":"Natural Justice","url":"https://naturaljustice.org/",
    "desc":"Lawyers working with communities across Africa on environmental and Indigenous rights, including biodiversity law, community protocols and consent. CAN: reach legal support built around community decision-making rather than around an individual claimant, and the biocultural community protocol method. CAN'T: cover every African jurisdiction. FOR: a community protocol is a document a community writes about how it must be consulted \u2014 and it has been recognised in law; that is a tool, not a statement.",
    "tags":["courts:strategic","organizing:consent","conserve:recognize"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"legalaid","trust":"high"},
   {"name":"FIAN International","url":"https://www.fian.org/",
    "desc":"Organisation working on the right to food as a legal right, documenting violations and bringing them to UN treaty bodies. CAN: frame a seed-law or land-and-food case in right-to-food terms and take it to a body that hears such claims. CAN'T: litigate domestically. FOR: the right to food is a binding treaty obligation in most countries, and it is the frame under which seed restrictions are most readily challenged.",
    "tags":["courts:strategic","conserve:recognize","organizing:legal"],"voice":"interpretive","type":"institutional","kind":"institution","skind":"ngo","trust":"high"},
   {"name":"Business & Human Rights Resource Centre","url":"https://www.business-humanrights.org/",
    "desc":"Tracks lawsuits, allegations and company responses worldwide, with a corporate legal accountability portal covering cases against multinationals. CAN: find every documented case and allegation against a company, in any jurisdiction, plus the company\u2019s own reply where it gave one. CAN'T: verify allegations itself. FOR: it always seeks and publishes the company response, which means you can see what the firm says when it is asked directly.",
    "tags":["courts:strategic","advocacy:data","corporate:ownership"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"}]},
]


# ============================== THE PRINCIPALS ================================
# Named organisations, each linked to a public record that can be checked rather
# than to a claim that has to be taken on trust. Every entry points at filings, a
# registry, a lobbying return or an official page \u2014 not at a press summary.
IB += [
 {"name":"The four \u2014 agricultural biotechnology majors","lat":51.0333,"lng":6.9833,"trackers":[
   {"name":"Bayer Crop Science (which absorbed Monsanto)","url":"https://www.bayer.com/en/investors/financial-reports",
    "desc":"Bayer acquired Monsanto in 2018 and now runs the largest seed and trait business in the world alongside its glyphosate herbicide line. CAN: read the annual and quarterly reports \u2014 segment revenue, litigation provisions, and the risk-factor section, which is the most candid account the company publishes of its own exposure. CAN'T: reach unconsolidated subsidiaries or licensee terms. FOR: start with provisions for glyphosate litigation and the divisional revenue split; both say more about the business than any statement it makes about safety.",
    "tags":["corporate:principals","corporate:filings","courts:federal"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"database","trust":"medium"},
   {"name":"Corteva Agriscience","url":"https://investors.corteva.com/",
    "desc":"Spun out of the DowDuPont merger in 2019, carrying the Pioneer and Dow seed businesses and their trait portfolios. CAN: read SEC filings, the licensing and royalty disclosures, and the seed-versus-crop-protection revenue split. CAN'T: reach private licensing terms with other breeders. FOR: Corteva both develops traits and licenses them to competitors, so its filings describe an industry rather than a company.",
    "tags":["corporate:principals","corporate:filings","spending:patents"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"database","trust":"medium"},
   {"name":"Syngenta Group (ChemChina / Sinochem)","url":"https://www.syngentagroup.com/en/investors",
    "desc":"Swiss-headquartered, acquired by ChemChina in 2017 and now inside the state-owned Sinochem Holdings. CAN: read group reporting and follow the ownership chain into a Chinese state holding \u2014 the one place where an agricultural biotechnology major and a state are the same actor. CAN'T: expect the disclosure depth of a US-listed peer. FOR: state ownership changes what leverage exists; shareholder resolutions and securities disclosure do not reach here, but state-to-state and trade routes do.",
    "tags":["corporate:principals","corporate:ownership","corporate:filings"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"database","trust":"medium"},
   {"name":"BASF Agricultural Solutions","url":"https://www.basf.com/global/en/investors",
    "desc":"The fourth of the majors, which bought substantial seed and trait assets divested during the Bayer\u2013Monsanto merger. CAN: read reports and the segment breakdown. CAN'T: separate the seed business cleanly from the wider chemicals group. FOR: BASF's holdings exist because a merger regulator required divestment \u2014 which is the clearest demonstration that competition authorities already treat this as a concentrated market.",
    "tags":["corporate:principals","corporate:filings","corporate:ownership"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"database","trust":"medium"}]},

 {"name":"Industry associations \u2014 who argues on their behalf","lat":38.9072,"lng":-77.0369,"trackers":[
   {"name":"BIO \u2014 Biotechnology Innovation Organization","url":"https://www.bio.org/",
    "desc":"The largest biotechnology trade association, representing over 1,100 companies across more than 30 countries. CAN: see the industry's own policy positions stated plainly, and cross-reference its lobbying returns in the US disclosure system and the EU Transparency Register. CAN'T: be read as a neutral source. FOR: trade associations file on members' behalf so individual firms need not, which is exactly why the association's returns are often more revealing than any single company's.",
    "tags":["corporate:principals","spending:lobbying","advocacy:frontgroups"],"voice":"commentary","type":"institutional","kind":"advocacy","skind":"ngo","trust":"low"},
   {"name":"CropLife International","url":"https://croplife.org/",
    "desc":"The global federation of the pesticide and agricultural-biotechnology industry, with national affiliates in most countries. CAN: identify the national affiliate that will be lobbying your own government, and read the federation's positions on regulation and gene editing. CAN'T: be treated as evidence. FOR: when a national industry body appears in a consultation you are also in, this is usually where its arguments and its funding come from.",
    "tags":["corporate:principals","spending:lobbying","advocacy:frontgroups"],"voice":"commentary","type":"institutional","kind":"advocacy","skind":"ngo","trust":"low"},
   {"name":"ISAAA \u2014 GM approval database & briefs","url":"https://www.isaaa.org/",
    "desc":"An industry-supported organisation that maintains the most complete event-level approval database in existence and publishes the annual global adoption figures most widely quoted on all sides. CAN: get approval status by event and country, and the acreage figures. CAN'T: be read as independent \u2014 it exists to promote adoption. FOR: included deliberately as a record rather than a voice: the identifier cross-walk is genuinely useful, the trust filters let you exclude it, and citing an industry source for an industry figure is stronger than citing a critic for one.",
    "tags":["corporate:principals","projects:trackers","advocacy:frontgroups"],"voice":"commentary","type":"records-data","kind":"analyst","skind":"database","trust":"low"}]},

 {"name":"Gene editing & synthetic biology firms","lat":38.8977,"lng":-77.0261,"trackers":[
   {"name":"Corporate filings \u2014 gene editing companies (SEC EDGAR full-text)","url":"https://efts.sec.gov/LATEST/search-index?q=%22gene%20editing%22&dateRange=custom",
    "desc":"Full-text search across SEC filings. CAN: find every US-listed company describing itself as doing gene editing, germline or somatic, and read what each says about its own regulatory and litigation risk. CAN'T: reach private companies, which is where a great deal of this work sits. FOR: search the phrase rather than the company \u2014 you will find firms you had not heard of, and the risk-factor sections say what the press releases do not.",
    "tags":["corporate:principals","corporate:filings","projects:trackers"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"Colossal Biosciences \u2014 de-extinction","url":"https://colossal.com/",
    "desc":"The best-funded de-extinction venture, working on engineered proxies for extinct species and holding the associated intellectual property. CAN: see what is claimed, and pair it with the company's patent filings and investor announcements. CAN'T: be taken at its own valuation of the science. FOR: de-extinction reframes extinction as reversible, which quietly lowers the argued cost of causing it \u2014 and the reversal is owned.",
    "tags":["corporate:principals","spending:patents","environment:species"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"other","trust":"low"},
   {"name":"Oxitec \u2014 engineered insects","url":"https://www.oxitec.com/",
    "desc":"The company behind the engineered mosquito releases in Brazil, the Cayman Islands, the United States and, until the 2025 suspension, the Target Malaria-adjacent work in West Africa. CAN: see what has been released where, and read the company's own account alongside the regulator's. CAN'T: substitute for the peer-reviewed record, which has differed from the company's framing. FOR: the Jacobina introgression finding and the company's published dispute with it are both public; read them together.",
    "tags":["corporate:principals","projects:trackers","environment:incidents"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"other","trust":"low"}]},

 {"name":"Assisted reproduction \u2014 the industry and its records","lat":51.5194,"lng":-0.1270,"trackers":[
   {"name":"HFEA \u2014 Human Fertilisation and Embryology Authority (UK)","url":"https://www.hfea.gov.uk/",
    "desc":"The UK's statutory fertility regulator, which licenses every clinic, inspects them, and publishes clinic-level outcome data and its own register. CAN: see named clinics, their inspection findings, their success rates and the conditions on their licences \u2014 clinic-by-clinic transparency that exists almost nowhere else. CAN'T: cover clinics outside the UK. FOR: this is the benchmark. Where another country's fertility sector is unaccountable, the argument is not that oversight is impossible but that it already exists here.",
    "tags":["corporate:principals","projects:trackers","environment:health"],"voice":"official","type":"records-data","kind":"structured","skind":"oversight","trust":"record"},
   {"name":"CDC ART Success Rates \u2014 clinic-level data (US)","url":"https://www.cdc.gov/art/",
    "desc":"Federally mandated reporting of assisted reproductive technology outcomes by clinic, published annually. CAN: identify every reporting US clinic and compare cycles, outcomes and patient age bands. CAN'T: capture what is not reported, or regulate anything \u2014 the US has no equivalent of the HFEA. FOR: the United States has clinic-level statistics and no clinic-level regulator, which is an unusual combination and worth naming precisely.",
    "tags":["corporate:principals","environment:health","advocacy:data"],"voice":"official","type":"records-data","kind":"structured","skind":"stats","trust":"record"},
   {"name":"ESHRE \u2014 European IVF monitoring","url":"https://www.eshre.eu/",
    "desc":"The European professional society, whose IVF-monitoring consortium compiles cycle and outcome data across European countries. CAN: get the cross-country picture of how many cycles are performed where. CAN'T: be independent of the sector \u2014 it is the profession's own body. FOR: the growth curve is the argument; the numbers establishing it come from the industry itself, which makes them hard to dispute.",
    "tags":["corporate:principals","environment:health","advocacy:data"],"voice":"commentary","type":"institutional","kind":"analyst","skind":"research","trust":"medium"},
   {"name":"Fertility clinic chains \u2014 ownership and investors","url":"https://opencorporates.com/companies",
    "desc":"Fertility provision has consolidated into clinic chains, many owned by private equity, and the chain rather than the clinic is now the decision-making unit. CAN: search a clinic's registered name, find its parent, and trace the group and its investors across jurisdictions. CAN'T: reach fund structures that are not registered. FOR: patients choose a clinic; the policies, pricing and storage terms are set by an owner they were never told about, and that owner is findable.",
    "tags":["corporate:principals","corporate:ownership","corporate:finance"],"voice":"interpretive","type":"records-data","kind":"structured","skind":"database","trust":"high"}]},

 {"name":"Public money & public agencies","lat":39.0000,"lng":-77.1000,"trackers":[
   {"name":"USDA NIFA \u2014 agricultural research funding","url":"https://www.nifa.usda.gov/",
    "desc":"The federal agency funding US agricultural research, including biotechnology programmes at land-grant universities. CAN: see which programmes and institutions are funded, and pair that with USAspending for the amounts. CAN'T: show the licensing terms under which publicly funded results become privately held. FOR: publicly funded research becoming private intellectual property is a documented pattern; establishing the public funding half is the easy half, and it starts here.",
    "tags":["corporate:principals","spending:contracts","spending:subsidy"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"},
   {"name":"Gates Foundation \u2014 agricultural development grants","url":"https://www.gatesfoundation.org/about/committed-grants",
    "desc":"A searchable database of every grant the foundation has made, with recipient, amount, duration and purpose. CAN: establish exactly what has been funded in African and South Asian agricultural biotechnology, by whom and for how much, from the funder's own record. CAN'T: show what was declined or what conditions attached. FOR: private philanthropy is one of the largest funders of biotechnology deployment in low-income countries, and \u2014 unusually \u2014 it publishes its own grant list, so the claim never has to rest on inference.",
    "tags":["corporate:principals","spending:contracts","corporate:nonprofit"],"voice":"commentary","type":"records-data","kind":"structured","skind":"database","trust":"medium"},
   {"name":"CGIAR","url":"https://www.cgiar.org/",
    "desc":"The network of international agricultural research centres, which holds enormous public germplasm collections and increasingly works on engineered traits. CAN: reach the centres, their research portfolios and the genebanks they hold in trust under the Plant Treaty. CAN'T: be treated as either purely public-interest or purely industry-aligned; the network contains both arguments. FOR: the germplasm CGIAR holds in trust is the raw material for everything else on this map, which makes what the network chooses to do with it consequential in both directions.",
    "tags":["corporate:principals","conserve:acquire","spending:contracts"],"voice":"official","type":"records-data","kind":"structured","skind":"igo","trust":"record"},
   {"name":"DARPA \u2014 biological technologies","url":"https://www.darpa.mil/research/offices/biological-technologies",
    "desc":"The US defence research agency's biological technologies office, which has funded gene-drive research, engineered organisms and human-performance work. CAN: read programme descriptions and pair them with contract awards in USAspending. CAN'T: reach classified work. FOR: military biotechnology sits almost entirely outside civilian biosafety oversight, in every country that runs it \u2014 this is the one that publishes its programme names.",
    "tags":["corporate:principals","spending:contracts","projects:trackers"],"voice":"official","type":"records-data","kind":"structured","skind":"database","trust":"record"}]},
]


# --- pin audit: every body must sit somewhere its lead entry actually is ------
# AfricanLII was pinned in Sydney for a whole build because the body was named
# after a network rather than a place. Fail loudly rather than ship that again.
_PIN_EXPECT = {
    "AfricanLII": (-33.9, 18.4, "Cape Town"),
    "WorldLII": (-33.9, 151.2, "Sydney"),
    "Strategic & public": (44.1, -123.1, "Eugene, Oregon"),
    "Gene editing": (38.9, -77.0, "Washington DC"),
    "The four": (51.0, 7.0, "Leverkusen"),
    "Global farmer": (41.4, 2.2, "Barcelona"),
    "Independent GM testing": (45.8, 8.6, "Ispra"),
}
_pin_bad = 0
for _b in IB:
    for _k, (_la, _ln, _where) in _PIN_EXPECT.items():
        if _b["name"].startswith(_k):
            if abs(_b["lat"] - _la) > 1.0 or abs(_b["lng"] - _ln) > 1.0:
                print("  PIN MISMATCH: %s is not near %s" % (_b["name"], _where))
                _pin_bad += 1
# every body must at least be on the planet and not at null island
for _b in IB:
    if not (-90 <= _b["lat"] <= 90 and -180 <= _b["lng"] <= 180) or (_b["lat"] == 0 and _b["lng"] == 0):
        print("  BAD COORDS: %s" % _b["name"]); _pin_bad += 1
assert _pin_bad == 0, "international body pins failed audit"
print("  pin audit: %d bodies, all placed" % len(IB))

# the round-1 bodies predate the kind/skind fields; the engine defaults them
# at runtime, but set them explicitly so the filters group them correctly.
for _b in IB:
    for _t in _b["trackers"]:
        _t.setdefault("kind", "structured")
        _t.setdefault("skind", "database")
        _t.setdefault("checked", "2026-07-31")

block(483, 489, 'const internationalBodies =' + js(IB) + ';')

# --------------------------------------------------------------- DOMAINS ----
put(491, 'const DOMAINS = ' + js(DOMAINS) + ';')

# ---------------------------------------------- international memberships ---
# The source map shipped a per-country map of anti-corruption bodies. There is
# no verified per-country biosafety-treaty membership table in hand, and
# inventing one would violate the no-fabrication rule, so it ships empty and
# the popup section simply does not render until it is harvested from the BCH
# party list.
put(733, 'const INTL_MEMBER={}; /* pending: harvest Cartagena Protocol / Plant Treaty / UPOV party lists from bch.cbd.int and fao.org before populating */')

block(735, 750, 'var _BODY_INFO={\n};')

# ------------------------------------------------------------ WIRE config ---
block(1547, 1559, 'const WIRE_THREADS=' + js(WIRE_THREADS) + ';')
put(1569, 'const WIRE_FEEDS = ' + js(WIRE_FEEDS) + ';')

# ------------------------------------------------------------------ TOUR ----
block(2609, 2622, 'var TOUR=' + js(TOUR) + ';')

# ---------------------------------------------------- INTENTS + ANGLEHINT ---
block(2673, 2690, 'var INTENTS=' + js(INTENTS) + ';')
put(2691, 'const ANGLEHINT=' + js(ANGLEHINT) + ';')


# --------------------------------------------------------- all-lens desc ----
put(496, u"const DMAP={}; DOMAINS.forEach(d=>DMAP[d.key]=d); DMAP['all']={key:'all',label:'All lenses',accent:'#3d7a54',hi:'#7fae86',desc:'\u2018Every\u2019 research, investigation and accountability resource for opposing the genetic engineering of organisms \u2014 from a single field trial to the treaty registers.',subs:[]};")


# ------------------------------------------------- wire relevance gate ------
# The timeline view scores and gates items with these vocabularies. Left on the
# development-project wordlists, nothing in a genetic-engineering feed would
# score or survive the gate, so all four are retuned here.
SCALE = [["gene drive",5],["germline",5],["transgenic",4],["genetically modified",4],["genetically engineered",4],
         ["gene-edited",4],["gene edited",4],["crispr",4],["gmo",4],["gm crop",4],["gm maize",4],["gm corn",4],
         ["gm soy",4],["gm cotton",4],["gm rice",5],["gm wheat",4],["gm tree",5],["gm salmon",4],["gm fish",4],
         ["gm insect",4],["gm mosquito",4],["engineered microbe",4],["synthetic biology",4],["de-extinction",5],
         ["cloned",3],["cloning",3],["xenotransplant",4],["embryo",4],["heritable",5],["field trial",4],
         ["deliberate release",5],["commercial release",5],["cultivation approval",4],["import approval",3],
         ["patent",3],["centre of origin",5],["center of origin",5],["landrace",4],["wild relative",4],["seed law",3]]

IMPACT = [["irreversible",5],["cannot be contained",5],["permanent",3],["spread",3],["escape",4],["spread",4],
          ["contaminat",5],["cross-contamination",5],["drift",4],["gene flow",5],["outcross",4],["unauthorised",4],
          ["unauthorized",4],["illegal planting",4],["recall",3],["decades",3],["generation",3],["endangered",3],
          ["extinction",4],["pollinator",3],["non-target",4],["biodiversity",3],["toxic",2],["allergen",3],
          ["displace",2],["sacred",3],["indigenous",3],["smallholder",3],["organic certification",4]]

STOP = [["stop",2],["halt",2],["block",2],["blockade",3],["oppos",2],["lawsuit",2],["injunction",3],["permit",2],
        ["appeal",2],["reject",2],["rejected",3],["moratorium",4],["ban",3],["banned",3],["defend",2],
        ["withdrawn",3],["annulled",4],["revoked",4],["uprooted",3],["gmo-free",4],["gm-free",4],["refused",3]]

PROJ = ["genetically modified","genetically engineered","gene-edited","gene edited","transgenic","gmo","gm crop",
        "gm maize","gm corn","gm soy","gm cotton","gm rice","gm wheat","gm potato","gm tree","gm salmon","gm fish",
        "gm animal","gene drive","crispr","germline","embryo","cloned","cloning","de-extinction","xenotransplant",
        "biosafety","field trial","deliberate release","cultivation approval","biotech crop","seed patent",
        "plant variety","upov","seed law","seed sovereignty","contamination","gene flow","landrace","wild relative",
        "centre of origin","center of origin","bayer","monsanto","corteva","syngenta","basf","efsa","aphis",
        "ctnbio","geac","ogtr","synthetic biology","in vitro","ivf","fertility clinic","assisted reproduction",
        "animal testing","laboratory animal","genetically altered"]

KEYS = [["golden rice","Golden Rice"],["bt brinjal","Bt Brinjal"],["bt cotton","Bt Cotton"],["bt eggplant","Bt Brinjal"],
        ["hb4 wheat","HB4 Wheat"],["aquadvantage","AquAdvantage"],["gm salmon","AquAdvantage"],
        ["target malaria","Target Malaria"],["oxitec","Oxitec"],["gene drive","Gene drive"],
        ["american chestnut","GM Chestnut"],["darling 58","GM Chestnut"],["he jiankui","Germline editing"],
        ["germline","Germline editing"],["colossal","De-extinction"],["de-extinction","De-extinction"],
        ["dicamba","Dicamba"],["roundup","Glyphosate"],["glyphosate","Glyphosate"],
        ["native maize","Mexico maize"],["maiz nativo","Mexico maize"],["mexico corn","Mexico maize"],
        ["bt63","BT63 rice"],["llrice","LLRICE"],["starlink","StarLink"],["triffid","Triffid flax"],
        ["ndm rapeseed","GM rapeseed"],["new genomic techniques","EU NGT deregulation"],
        ["ngt","EU NGT deregulation"],["viagen","Pet cloning"],["sooam","Pet cloning"],["pet cloning","Pet cloning"],
        ["bayer","Bayer/Monsanto"],["monsanto","Bayer/Monsanto"],["corteva","Corteva"],["syngenta","Syngenta"]]

put(1750, '    var SCALE=' + js(SCALE) + ';')
put(1751, '    var IMPACT=' + js(IMPACT) + ';')
put(1752, '    var STOP=' + js(STOP) + ';')
put(1754, '    var PROJ=' + js(PROJ) + ';')
put(1759, '    var KEYS=' + js(KEYS) + ';')


# ------------------------------------------- release layer: source families -
PJ_SRC = [
 {"k":"bch","cat":"Global registries","label":"Biosafety Clearing-House \u2014 LMO decisions",
  "desc":"Every final decision a Cartagena Protocol party has filed on the domestic use, import or release of a living modified organism, plus the risk assessment lodged with it. The only genuinely cross-national record of its kind. Mostly country-level (dashed rings) \u2014 the BCH records a decision, not a field."},
 {"k":"oecd_biotrack","cat":"Global registries","label":"OECD BioTrack \u2014 approved products",
  "desc":"Event-level approval status by country, keyed on the OECD unique identifier \u2014 the code that lets you follow one engineered event across every jurisdiction that has ruled on it. Country-level."},
 {"k":"isaaa","cat":"Global registries","label":"ISAAA GM Approval Database",
  "desc":"Event-by-event approval status worldwide, with the trait, the developer and the approving country. Industry-run \u2014 included because its identifier cross-walk is genuinely useful, and flagged so the trust and voice filters can exclude it. Country-level."},

 {"k":"ogtr","cat":"National release registers","label":"Australia \u2014 OGTR GMO Record & field-trial sites",
  "desc":"The most detailed release register in the world: every licence for a dealing involving intentional release (DIR) and not involving release (DNIR), the risk assessment and risk management plan for each, and \u2014 uniquely \u2014 published locations for active crop field-trial sites. Site-level where the trial is active."},
 {"k":"aphis","cat":"National release registers","label":"United States \u2014 USDA APHIS releases & notifications",
  "desc":"Permits and notifications for the environmental release, import and interstate movement of regulated engineered organisms, with the applicant, the organism and the phenotype. State- or county-level for most records."},
 {"k":"eu_release","cat":"National release registers","label":"European Union \u2014 deliberate release & GM register",
  "desc":"Part B notifications for experimental field releases in member states, and the EU register of GMOs authorised for food, feed and cultivation. Field releases usually carry a region or municipality; authorisations are EU-wide."},
 {"k":"cfia","cat":"National release registers","label":"Canada \u2014 CFIA approvals & confined trials",
  "desc":"Two things at once. The published dataset of plants approved for unconfined environmental release, which is harvested here, and the confined research field trials that precede them, which are published as annual HTML tables and are not. Canada regulates by novelty of trait rather than by technique, so the same register lists transgenic events and products of mutagenesis and gene editing side by side \u2014 the one place where the second group is still visible, when almost everywhere else is writing it out of registration. Most records carry the OECD unique identifier, which is the string that links one event across every country that has ruled on it. National approvals: no province, so these sit at the country centroid."},
 {"k":"ctnbio","cat":"National release registers","label":"Brazil \u2014 CTNBio decisions",
  "desc":"Technical opinions and commercial-release decisions from Brazil\u2019s national biosafety commission. Brazil is one of the three countries holding the large majority of GM crop land, so this register carries weight out of proportion to its size. National- to state-level."},
 {"k":"conabia","cat":"National release registers","label":"Argentina \u2014 CONABIA / SENASA",
  "desc":"Argentina\u2019s biosafety advisory decisions and release authorisations. The third of the three countries holding most GM crop land. National- to province-level."},
 {"k":"geac","cat":"National release registers","label":"India \u2014 GEAC decisions & trial approvals",
  "desc":"Genetic Engineering Appraisal Committee minutes and approvals, including confined field trials by state and season. Published as meeting minutes rather than a database, so coverage depends on parsing. State-level."},
 {"k":"nzepa","cat":"National release registers","label":"New Zealand \u2014 EPA new-organism decisions",
  "desc":"Applications and decisions on new organisms, including containment approvals and release applications, with the full decision reasoning. National- to region-level."},

 {"k":"contamination","cat":"Contamination record","label":"GM Contamination Register \u2014 spread, drift & illegal releases",
  "desc":"Recorded incidents where GM material was found where it was not authorised \u2014 in food, feed, seed stock or a wild relative. 396 incidents across 63 countries to the end of 2013, with rice accounting for about a third of them despite no GM rice being commercially grown anywhere. Marked DORMANT: updating appears to have stopped, and nothing has replaced it. Country-level."},

 {"k":"clinical","cat":"Human & clinical","label":"Clinical-trial registries \u2014 gene therapy & editing",
  "desc":"Registered trials involving gene transfer, gene editing and engineered cell products, from ClinicalTrials.gov and the WHO international registry platform. Not a release register \u2014 included because it is the only systematic public record of engineering applied to human beings, and it names sponsor, site and phase. Site-level where the trial lists sites."},

 {"k":"seed","cat":"Curated","label":"Hand-curated sites",
  "desc":"A small set of significant or contested releases added by hand from public reporting where no automated feed yet covers them \u2014 open gene-drive proposals, engineered-tree plantings, contested trials in centres of origin. Location precision varies and is stated per record."},
 {"k":"clinical_sponsor","cat":"Industry","label":"Gene & cell therapy trial sponsors",
  "desc":"Lead sponsors of registered gene and cell therapy trials, harvested from ClinicalTrials.gov and aggregated one point per organisation at the country of its most frequent trial location. **The only facet on this map with a complete public register** \u2014 registration is required for essentially every interventional trial run in or submitted to the United States. Not a world census: trials run entirely outside that orbit may never appear, and China is under-represented relative to its actual programme."},
 {"k":"animals_facility","cat":"Industry","label":"Animal research facilities (US register)",
  "desc":"US facilities registered under the Animal Welfare Act, from their own annual reports, at state level. The only facility-level count published anywhere. Mice, rats and birds bred for research are excluded from the Act\u0027s definition of an animal \u2014 the overwhelming majority of those used, and the great majority of genetically altered ones \u2014 so this counts a fraction and the rest is counted nowhere."},
 {"k":"escape_register","cat":"Spread, drift & contamination","label":"GM Contamination Register 1997\u20132013",
  "desc":"The 396 incidents across 63 countries recorded by GeneWatch UK and Greenpeace International before the Register stopped in 2013, recovered from the open-access supplementary data of Price & Cotter 2014 (CC BY). Country-level positions only, and one-line summaries \u2014 the hand-written spread entries carry the detail. Nothing has replaced the Register, so this is the whole systematic record that exists, and it was compiled by two campaigning organisations rather than by any regulator."},
 {"k":"escape","cat":"Spread, drift & contamination","label":"Documented spread, drift & unauthorised releases",
  "desc":"Incidents where engineered material was found where it had not been authorised \u2014 in a wild population, a food supply, an export shipment or a commercial field. Past as well as current: the GM Contamination Register logged 396 incidents across 63 countries between 1997 and 2013 and then stopped, and nothing replaced it, so there is no feed to harvest and this is hand-compiled. Every one of these was found and reported, which is a different thing from every one that happened."},
 {"k":"industry_seed","cat":"Industry","label":"Seed & trait companies",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_editing","cat":"Industry","label":"Gene editing & synthetic biology",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_synthesis","cat":"Industry","label":"DNA synthesis & sequencing",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_cro","cat":"Industry","label":"Contract research & manufacturing",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_animals","cat":"Industry","label":"Laboratory animal suppliers",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_livestock","cat":"Industry","label":"Livestock, aquaculture & pets",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_wild","cat":"Industry","label":"Open release programmes",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_deextinct","cat":"Industry","label":"De-extinction & conservation biotech",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_clinical","cat":"Industry","label":"Human clinical & therapeutic",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_repro","cat":"Industry","label":"Assisted reproduction",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_money","cat":"Industry","label":"Funders & backers",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
 {"k":"industry_rules","cat":"Industry","label":"Regulators, registers & trade bodies",
  "desc":"Organisations in this part of the industry, placed at their headquarters or principal site. Positions are city-level and marked approximate, because a corporate headquarters is not where the work happens. Click a marker for what the organisation is, where it sits in the chain, and why it matters."},
]

PJ_TYPES = [
 {"k":"crop_food",    "g":"Plants & crops",     "label":"Food crops (maize, soy, rice, wheat)"},
 {"k":"crop_fibre",   "g":"Plants & crops",     "label":"Fibre & industrial crops"},
 {"k":"crop_veg",     "g":"Plants & crops",     "label":"Vegetables & fruit"},
 {"k":"crop_forage",  "g":"Plants & crops",     "label":"Forage, grass & feed"},
 {"k":"crop_pharma",  "g":"Plants & crops",     "label":"Pharma & industrial plants"},
 {"k":"tree",         "g":"Trees & wild",       "label":"Trees & forestry"},
 {"k":"deextinct",    "g":"Trees & wild",       "label":"De-extinction & wild release"},
 {"k":"livestock",    "g":"Animals",            "label":"Livestock & poultry"},
 {"k":"fish",         "g":"Animals",            "label":"Fish & aquaculture"},
 {"k":"pet",          "g":"Animals",            "label":"Companion & cloned animals"},
 {"k":"lab_animal",   "g":"Animals",            "label":"Laboratory animals"},
 {"k":"insect",       "g":"Insects & microbes", "label":"Insects & gene drives"},
 {"k":"microbe",      "g":"Insects & microbes", "label":"Microbes & fermentation"},
 {"k":"virus_vaccine","g":"Insects & microbes", "label":"Viral vectors & GM vaccines"},
 {"k":"germline",     "g":"Human & clinical",   "label":"Human germline & embryos"},
 {"k":"gene_therapy", "g":"Human & clinical",   "label":"Somatic gene therapy"},
 {"k":"art",          "g":"Human & clinical",   "label":"In vitro & assisted reproduction"},
 {"k":"cellline",     "g":"Human & clinical",   "label":"Cell lines & cultured tissue"},
 {"k":"other",        "g":"Other",              "label":"Other / unclassified"},
]

PJ_OVERLAYS = [
 {
  "k": "cultivation",
  "label": "Approved GM cultivation area",
  "color": "#c2603a",
  "note": "Where commercial cultivation of engineered crops is authorised. The industry's actual footprint: roughly nine tenths of it is soy, maize and cotton, and the great majority sits in a handful of countries. Area, not a release point."
 },
 {
  "k": "trials",
  "label": "Field trial density (US only)",
  "color": "#e0913f",
  "note": "Where release authorisations cluster, built from the release layer itself rather than from a separate source. Trials precede cultivation by years, so this is the nearest thing to a forward view of where the footprint above will spread."
 },
 {
  "k": "regime",
  "label": "Regulatory regime by country",
  "color": "#8a7fc4",
  "note": "How each country decides what counts as a regulated organism \\u2014 by the technique used, by the trait produced, or not at all. This is the single layer that explains why the map looks different in different places: where editing has been ruled equivalent to conventional breeding there is no application, no assessment and no register entry, so an empty area can mean deregulation rather than absence."
 },
 {
  "k": "infrastructure",
  "label": "Seed & breeding infrastructure",
  "color": "#c4a24f",
  "note": "Where the industry physically is, as distinct from where its products are grown: the Hawaiian seed nurseries that allow several generations a year, counter-season multiplication in Chile and Argentina, and the Dutch vegetable-breeding cluster. Concentrated in very few places, and rarely mapped."
 },
 {
  "k": "centres_origin",
  "label": "Centres of crop origin & diversity",
  "color": "#d8a13a",
  "note": "Where each crop was domesticated and where its wild relatives and landraces still live. These are the reservoirs every commercial variety on this map was ultimately bred from \\u2014 the industry's own raw material, held almost entirely outside it."
 },
 {
  "k": "gmofree",
  "label": "GMO-free zones & regional bans",
  "color": "#4fb3c9",
  "note": "Regions, municipalities and countries that have closed themselves to GM cultivation. On an industry map these are the negative space: the places the industry has been kept out of, and therefore a direct measure of where its expansion has met a limit. Declarations are made at many levels and no single registry holds them, so this layer is partial by nature."
 },
 {
  "k": "protected",
  "label": "Wild-relative habitat",
  "color": "#7b9c46",
  "note": "Protected areas overlapping the range of crop wild relatives. On this map they are the receiving environment \\u2014 what sits next to a trial site or a cultivation area, and what a gene-flow question is actually about."
 },
 {
  "k": "genebanks",
  "label": "Genebanks & seed collections",
  "color": "#9a7bc4",
  "note": "Institutional collections holding landraces and wild relatives, largely under the Plant Treaty. The industry draws on these constantly: commercial breeding starts from material held in trust by public institutions, which is the least-discussed subsidy it receives."
 }
]

PJ_SRC_GROUP = """  function pjSrcGroup(s){ s=s||"";
    var PFX=["bch","ogtr","aphis","eu_release","cfia","ctnbio","conabia","geac","nzepa",
             "oecd_biotrack","isaaa","contamination","clinical","seed","escape",
             "industry_seed","industry_editing","industry_synthesis","industry_cro",
             "industry_animals","industry_livestock","industry_wild","industry_deextinct",
             "industry_clinical","industry_repro","industry_money","industry_rules","escape_register","animals_facility","clinical_sponsor"];
    // "industry:seed" and "escape:crop" both split on the colon like the rest.
    if(s.indexOf("industry:")===0) return "industry_"+s.slice(9).split(":")[0];
    if(s.indexOf("clinical:sponsor")===0) return "clinical_sponsor";
    if(s.indexOf("animals:facility")===0) return "animals_facility";
    if(s.indexOf("bch:")===0) return "bch";
    if(s.indexOf("escape:register")===0) return "escape_register";
    if(s.indexOf("escape")===0) return "escape";
    for(var i=0;i<PFX.length;i++){ if(s===PFX[i] || s.indexOf(PFX[i]+":")===0) return PFX[i]; }
    return s; }"""

PJ_TYPE_CAT = """  // Classify a release into ONE type from keywords in its text + source.
  // Cached on the object (__tc) -- pjPasses runs across the whole set per render.
  function pjTypeCat(p){
    if(p.__tc) return p.__tc;
    var s=((p.type||"")+" "+(p.name||"")+" "+(p.desc||"")+" "+(p.organism||"")+" "+(p.trait||"")).toLowerCase();
    var src=(p.source||"").toLowerCase();
    function h(){ for(var i=0;i<arguments.length;i++){ if(s.indexOf(arguments[i])>=0) return true; } return false; }
    var c;
    if(h("germline","heritable","human embryo","embryo editing","designer baby","preimplantation","he jiankui")) c="germline";
    else if(h("in vitro fert","ivf","assisted reproduct"," art ","icsi","intracytoplasmic","intrauterine insemination","frozen embryo transfer","fertility clinic","surrogacy","egg donor","sperm donor")) c="art";
    else if(h("gene therapy","car-t","car t","somatic","aav","lentivir","ex vivo","autologous","engineered t cell")) c="gene_therapy";
    else if(h("cell line","cultured meat","cultivated meat","organoid","stem cell","tissue engineer","xenotransplant","cultured tissue")) c="cellline";
    else if(h("de-extinction","de extinction","resurrect","dire wolf","woolly mammoth","passenger pigeon","thylacine","rewild","aurochs","quagga")) c="deextinct";
    else if(h("gene drive","engineered mosquito","sterile insect","transgenic insect","pink bollworm","diamondback moth","medfly","screwworm","olive fly","fruit fly")
             || (/(^|[^a-z])(mosquito|moths?|flies|beetles?|bees?|insects?|locusts?|aphids?|ticks?)([^a-z]|$)/.test(s) && !h("resistant to insect","insect-resistant","insect resistant"))) c="insect";
    else if(h("poplar","eucalypt","chestnut","pine","spruce","forestry trial","gm tree","engineered tree","plantation tree")) c="tree";
    else if(h("salmon","tilapia","carp","trout","zebrafish","glofish","shrimp","aquaculture","fish farm")) c="fish";
    else if(h("cloned pet","pet cloning","companion animal","dog clon","cat clon","horse clon","micro pig","glow","ornamental fish")) c="pet";
    else if(h("laboratory animal","lab mouse","lab mice","knockout mouse","knockout mice","transgenic mouse","transgenic mice","transgenic rat","research animal","animal testing","model organism")) c="lab_animal";
    else if(h("vaccine","viral vector","virus vector","attenuated","oncolytic","bacteriophage","phage")) c="virus_vaccine";
    else if(h("cattle","cow","bovine","pig","porcine","swine","sheep","ovine","goat","poultry","chicken","hen","livestock","hornless","boar taint")) c="livestock";
    else if(h("bacteri","yeast","fungal","fungus","algae","cyanobact","microbial","microbe","fermentation","probiotic","biopesticide microb","nitrogen-fixing")) c="microbe";
    else if(h("pharma","biopharm","molecular farming","industrial enzyme","bioplastic","biofuel crop","industrial starch")) c="crop_pharma";
    else if(h("cotton","flax","linseed","hemp","jute","sisal","kenaf")) c="crop_fibre";
    else if(h("alfalfa","lucerne","clover","ryegrass","bentgrass","fescue","forage","silage","pasture","feed grass")) c="crop_forage";
    else if(h("potato","tomato","apple","papaya","banana","squash","eggplant","brinjal","aubergine","melon","pepper","lettuce","cabbage","brassica","cassava","sweet potato","pineapple","grape","citrus","strawberry","mushroom")) c="crop_veg";
    else if(h("maize","corn","soy","soya","soybean","rice","wheat","canola","rapeseed","oilseed rape","sugar beet","sugarcane","sorghum","barley","oat","millet","chickpea","cowpea","bean","lentil","pea ","groundnut","peanut","safflower","sunflower","mustard","camelina")) c="crop_food";
    else if(h("crop","plant","seed","cultivar","variety","hybrid","germplasm")) c="crop_food";
    else if(h("animal")) c="lab_animal";
    else if(src.indexOf("clinical")>=0) c="gene_therapy";
    else c="other";
    try{ p.__tc=c; }catch(e){}
    return c;
  }"""

block(1956, 2035, '  var PJ_SRC=' + js(PJ_SRC) + ';')
block(2042, 2060, PJ_SRC_GROUP)
block(2093, 2129, '  var PJ_TYPES=' + js(PJ_TYPES) + ';')
block(2133, 2177, PJ_TYPE_CAT)
block(2219, 2225, '  var PJ_OVERLAYS=' + js(PJ_OVERLAYS) + ';')


# =============================================================== ROUND 2 =====

# --- facility layer: drop police & fire; keep the levels that actually decide --
put(1310, u"var FACCOL={th:'#1d4a6e',go:'#1a5f63',mi:'#2c3f7a',ch:'#5a4a1e',po:'#3a2a2a',pr:'#33212c',fs:'#3a2a1e',dp:'#2a2f4a',bd:'#1e3a3a'}, "
          u"FACLAB={th:'Town hall / municipality',go:'Government office',mi:'Ministry / agency HQ',ch:'Courthouse',"
          u"po:'Police station',pr:'Prison / detention',fs:'Fire station',dp:'Embassy / consulate',bd:'Border / customs post'}; "
          u"var facActive={th:1,go:1,mi:1,ch:1};")

block(1373, 1382, u"""var FACDESC={
 mi:'Ministry &amp; agency headquarters \u2014 the biosafety authority, the agriculture ministry, the food-safety agency. These are the bodies that receive an application, run the assessment and sign the consent. Records requests go here, and so does correspondence that later becomes evidence of what a regulator knew and when.',
 go:'Government offices \u2014 regional agriculture departments, plant-health inspectorates, extension services and land registries. The office that knows which fields are under trial in a district is usually at this level, not the national one.',
 th:'Town halls &amp; municipal offices \u2014 the level at which most GMO-free declarations are actually made. Across Europe the GMO-free regions movement is fundamentally municipal and regional, and in the United States the cultivation bans that have held up were passed by counties, not by Washington. Municipalities also grant the planning permission for laboratory, greenhouse and seed-production facilities. If you want a binding decision within a year rather than a decade, this is the realistic venue.',
 ch:'Courthouses \u2014 where a consent is challenged by judicial review, where a contamination or drift claim is filed, and where a patent-infringement suit against a farmer is heard. The physical venue behind the courts lens.'
};""")

put(1385, u"  var order=['mi','go','th','ch']; var html='';")

put(1402, u'  var SETS=[];')   # facility dots are civic buildings, not industry sites

# --- index: international bodies were forming one pseudo-country group each ----
put(1441, u"  internationalBodies.forEach(b=>{ (b.trackers||[]).forEach(tr=>INDEXDATA.push({name:tr.name,url:tr.url,"
          u"country:'International &amp; treaty bodies',body:(b.name||''),iso:(b.guide||null),level:'International',"
          u"lenses:_lensesOf(tr),tags:(tr.tags||[]),lat:b.lat,lng:b.lng,kind:tr.kind||'structured',"
          u"voice:tr.voice||'interpretive',trust:(KIND2TIER[tr.kind||'structured']||'high'),"
          u"skind:(tr.skind||'other'),media:mediaKS(tr.kind,tr.skind),desc:(tr.desc||''),checked:(tr.checked||null)})); });")

put(1463, u"    +'<div class=\"idx-meta\"><span class=\"idx-country\">'+_esc(r.body||r.country)+'</span> "
          u"<span class=\"idx-level\">'+_esc(r.level)+'</span> '+tags+'</div>'+db+'</div>';")

put(1503, u"  const box=document.getElementById('idxList');\n"
          u"  if(!h){ var _noCountry=!INDEXDATA.some(function(r){return r.level!=='International';});\n"
          u"    h=_noCountry ? '<div class=\"no-data\">No country data loaded. <b>trackerdata.json</b> must sit next to index.html \u2014 until it does, only the international &amp; treaty bodies appear here.</div>'"
          u" : '<div class=\"no-data\">No matches.</div>'; }\n"
          u"  box.innerHTML=h;")

# --- fresh copy: the wire panel introduces the subject and the process ---------
put(315, u"""    <div class="wire-lead">Farmers plant seeds. Some of those seeds have had genes added in a laboratory \u2014 usually taken from bacteria \u2014 so the crop survives being sprayed with weedkiller when a field full of weeds is sprayed, or makes its own insecticide in every leaf and root. These are examples of what\u2019s called Genetic Modification. The technique is fifty years old: in 1973 the biochemists Herbert Boyer and Stanley Cohen moved DNA from one bacterium into another, and in 1982 the FDA approved the first consumer product made this way \u2014 human insulin brewed in engineered bacteria rather than extracted from pig and cattle pancreases. Proponents argue that, in the context of agriculture, insect-resistant cotton substantially reduced broad-spectrum insecticide spraying in several countries \u2014 sprays that killed bees, birds and farm workers \u2014 and the claim that these foods are unsafe to eat has not held up in decades of testing. But, that isn’t the whole story.<br><br>
    For one, seeds and pollen do not stay where you put them. In Oregon a grass engineered to survive weedkiller got out of its test fields; three years after the cleanup started, 62 of every 100 plants tested carried the gene, and it had crossed into two other grass species, one of them a different genus entirely. The product was pulled, the company was fined $500,000, and the grass is still out there. In North Dakota, researchers drove 3,000 miles testing roadside canola: more than 75% carried an engineered gene, and some carried two at once \u2014 a combination nobody bred, On the coast of Mexico grows the wild ancestor of cotton. In 2008 it carried no engineered genes. Ten years later, 60% of the plants tested did.<br><br>
    And the spreading isn’t the end of it. Every wild plant sits inside a web of relationships with other species \u2014 things that guard it, feed on it, pollinate it, live in its roots, carry its seeds \u2014 and an engineered change entering at one point comes out at many others nobody has been watching or even defining. Wild plants carrying an engineered gene, for example, drew fewer of the insect species that defend them, and took the worst feeding damage of any group tested; parasitic wasps that control caterpillar numbers and that weren\u2019t targeted in the first place came out 35% lighter after eating prey containing prey that carried the plant\u2019s own built-in insecticide; introgressed wild cotton was found to hold less genetic variety than its unmodified neighbours, and Mexican wild cotton is now listed as vulnerable, with gene flow from crops being the main threat. Genetically modified insecticide-producing plants that travel beyond the field and cross-breed with wild plants also make less toxin than the original, leading to weaker doses of the plants\u2019 insecticide, the exact conditions under which insect resistance to it spreads fastest. <br><br>
    Nobody knows the true ecological impacts of all of these combined. And, yet, some GMOs are released on purpose at enormous scale, as in the case of gene drives, which are built specifically to push through entire wild populations. Engineered insects have been let loose by the hundred million, and engineered bacteria coated onto seed spread across millions of acres with nothing registered, as a microbe on a seed is not a plant, spraying it is not planting \u2014 no rule catches it.<br><br>
     Monitoring is thin enough that the clearest case was found only by accident; and the communities affected are rarely asked. <b>In fact, people are sometimes contractually blocked from checking.</b> In 2009, twenty-six university corn insect scientists told the US environment agency that the contracts attached to the seed did not permit them to run their own studies on crops already being sold. And, worst of all, containment has proven to fail, and spread is irreversible \u2014 there is no undoing it.<br><br>
    Four companies dominate the seed and chemical business: Bayer, Corteva, Syngenta and BASF. Roughly 94% of engineered crop area is just three crops \u2014 soy, maize and cotton \u2014 and 81% of it sits in three countries: the United States, Brazil and Argentina. Of 362 live US authorisations to release engineered organisms, Bayer, Syngenta and Pioneer hold 36% between them; Bayer alone holds 19%.<br><br>
    Bayer sells the seed that survives Roundup, and Bayer sells Roundup. The trait creates the market for it. One sale earns twice. This is why, even over 50 years, drought tolerance, better nutrition, higher yield haven\u2019t been made, as they don\u2019t sell a second product alongside the seed.<br><br>
    The seed is also patented, which matters because a patent covers the plant itself and everything grown from it. So the farmer signs a contract agreeing not to keep any of the harvest for next spring, and buys new seed every year instead of replanting what they already have. This means that saving seed isn\u2019t merely a breach of contract but a crime. Take the seed-ownership treaty UPOV 91, for example; Ghana\u2019s version of it carries a ten-year minimum sentence. Nobody is liable either when that seed drifts: a neighbouring organic farm whose crop tests positive loses the certification its price depends on, and carries the loss itself<br><br>
    <b>And, of course, the organisms themselves have no say in all of this.</b> They are born simply because a company decided which trait would sell, and they are released into a world that had no part in the decision either<br><br>
    The law pushes them out of the picture further by steadily shrinking the scope of regulation. On April 30, 2025, for example, the United States approved pigs edited to resist a disease that spreads in the crowded conditions of factory farms,  an edit that raises antibiotic use by more than 200%. The animals are marketed with the claim that they are \u201cnot GMOs,\u201d because their DNA was edited rather than supplemented with foreign DNA. In animal testing too, most laboratory animals are not legally animals. In the United States, mice, rats and birds bred for research are excluded from the Animal Welfare Act. They are the overwhelming majority of animals used, so the great bulk of the practice appears in no official count at all. Catalogues run to thousands of mouse strains, each one a line bred to be ill in a particular way, shipped to order. And, in pet cloning, dogs and horses are cloned for anyone who pays. No biosafety rule applies, because nothing foreign was inserted and the rules only trigger on inserted material. If an industry can name its way out of the rulebook like this, there is no rulebook. And, when the referees themselves are part of the game \u2014 regulators, registers, patent offices and standards bodies \u2014, not outside the industry checking it, who\u2019s there to call the foul play?<br><br>
    And, even where regulation does exist, much of the evidence behind approvals comes from the companies themselves. Safety studies are usually commissioned and paid for by the manufacturer, while regulators primarily evaluate the reports that companies submit. There is no comprehensive public register of these studies, so outside researchers cannot tell which tests were conducted, which produced unfavorable results, or whether unsuccessful studies were simply repeated until a satisfactory outcome was obtained. Furthermore, a venture fund has to sell its stake within a fixed number of years, and that deadline rewards moving fast and getting big long before any regulator sees the product. These problems are not necessarily discovered at the regulator\u2019s desk; they appear later in fields, hospitals, or ecosystems. This is not without precedent. In the 1970s, the testing company Industrial Bio-Test was found to have falsified safety data supporting thousands of pesticide approvals.<br><br>
    Meanwhile, use of the technology is becoming increasingly unpredictable. Although the repositories that distribute plasmids, cell lines, and other standard biological materials generally require verified institutional affiliations, many firms only voluntarily screen orders against databases of dangerous pathogen sequences. No law requires them to do so. The industry association responsible for this voluntary system has estimated that its members account for roughly 80 percent of global DNA synthesis, leaving about one-fifth of the market outside any screening process. A lock on four of five doors isn\u2019t a lock. Anyone seeking prohibited sequences can therefore turn to an unscreened supplier. And, because no record exists of who asked for what, nothing can be traced. This is how, in 2017, researchers reconstructed an extinct poxvirus for approximately $100,000.<br><br>
    Keep in mind that, under most national rules, contained laboratory and glasshouse work, as opposed to anything put into a field, a river or a patient, only needs the facility registered once and the risk class recorded internally. Within that, a laboratory can create novel organisms that have never existed, insert genes across kingdoms, build gene drives, resurrect viral sequences, and run it at industrial fermenter scale \u2014 without any per-experiment approval, public notice, or entry in any register \u2014 building essentially any organism, at any scale, indefinitely, under the radar. The reporting trigger is almost always only upon release, not creation. The UK is the strictest and even there it\u2019s a notification to the HSE with no public file. The EU requires a one-time facility notification. The US has no statutory contained-use requirement at all \u2014 NIH guidelines bind only institutions taking federal money, and enforcement is a local committee whose records aren\u2019t public. That is the same permission under which, in 2011, two laboratories took an avian influenza that killed a large share of the people it infected and could not pass between them, and made it transmissible between ferrets \u2014 the standard model for human transmission. Contained work, so no approval for the experiment and no public notice; the world learned of it when the papers were submitted. And in 2005 a team rebuilt the 1918 influenza virus, which had killed tens of millions and no longer existed, from sequenced fragments. Both were lawful throughout, both were published, and the argument happened afterwards \u2014 producing review rules that apply only to work the government pays for.<br><br>
    No amount of good intent at one end can change what has become buildable at the other. We sit on a precipice.<br><br>
    This map is the industry behind all of this \u2014 the companies that design and sell engineered organisms, the ones supplying them with DNA, animals and laboratory capacity, the money behind them, and the bodies that authorise them and argue on their behalf. Four hundred and thirty-six organisations, each with its own write-up and a link to the source. Twenty-four thousand release authorisations from official registers, broken down by country and state. Twenty-five documented cases of engineered organisms turning up where nobody put them. Two hundred regions that have declared themselves GMO-free. And thirty-six countries shaded by how each one decides what even counts as regulated \u2014 the question that settles every other one.<br><br>
    Twelve facets, running the length of the chain: seed and traits, gene editing and synthetic biology, DNA synthesis and sequencing, contract research and manufacturing, laboratory animals, livestock and aquaculture and pets, insects and microbes and open release, de-extinction, human clinical work, assisted reproduction, the money, and the rules. A handful of companies write the DNA everything starts as. Hired laboratories run the studies regulators read. Breeders sell millions of engineered animals a year, catalogued like supplies. Ventures rebuild extinct species as intellectual property. Clinics consolidate human reproduction. Venture funds, public grants, philanthropies and defence agencies pay for all of it.<br><br>
    This wire watches it in motion \u2014 worldwide, in many languages, filterable by region and subregion.</div>""")

# --- fresh copy: the help panel is a technical walkthrough of the interface ----
block(299, 308, u"""    <b class="hl-sec">Reading the markers</b><br>
    Zoomed out you are looking at a painted world plate. Past about zoom 5 it cross-fades to live satellite imagery underneath. Three kinds of point, each with its own shape, colour and size:<br>
    &bull; <b>Square</b> \u2014 an organisation, at its headquarters or principal site. Coloured by what kind of body it is: company, ministry, committee, institute, intergovernmental body, trade association, campaign group, fund, or register.<br>
    &bull; <b>Red diamond</b> \u2014 a documented drift or contamination incident, placed where the material was found.<br>
    &bull; <b>Green-to-blue circle</b> \u2014 a release authorisation from an official register.<br><br>
    <b>Filled</b> means a real coordinate. <b>Outlined and faint</b> means the source published none \u2014 most do not \u2014 so the marker sits at a fallback point for that country, state or city. A dense cluster of outlined markers is missing data in the source, not a failed pull. A corporate headquarters is always outlined: it is an office, and the laboratories, plants and fields the company runs are somewhere else entirely.<br><br>
    <b class="hl-sec">The map key</b><br>
    <b>All map points</b> toggles the whole layer; the three checkboxes under it turn each kind on and off separately, and the swatches below those do the same for each kind of organisation. Below: search, release scale, consent phase and filing recency, then filters by data source and by organism type, and context overlays.<br><br>
    <b class="hl-sec">The map</b><br>
    Countries carrying entries are outlined in gold; click one to open it, and click again inside to descend a level. Every entry says the same three things: <b>what</b> the organisation is and does, <b>where it sits</b> in the chain, and <b>why it matters</b>. Click any area outside of the region, or the unit\u0027s name in the top-centre row, to go back up.<br><br>
    <b class="hl-sec">Left rail</b><br>
    <b>Index</b> \u2014 every entry as a searchable list. The dropdowns group by country, facet, source type and so on; the filter box searches names and countries. Each row: click the name to read the entry, and the crosshair to fly the map there. Drag its header to move it; click to collapse.<br><br>
    <b class="hl-sec">Right rail</b><br>
    <b>Jump to a part of the industry</b> narrows the map to one facet and says what you are looking at. The <b>facet pills</b> beneath do the same manually, each with sub-filters under it. Below those, filters cut across every facet at once: source type, source kind, media type, trust level and voice.""")


# ================================================== GREEN -> DARK BLUE =======
import colorsys, re as _re

# Data encodings that must stay distinguishable are pinned AFTER the rotation.
_PIN = {
    # release-scale ramp: cool -> warm, deliberately muted. Left as a ramp.
    'PC': u'  var PC={5:"#8fc46a",4:"#7fc0a8",3:"#6fb8c4",2:"#7aa8cc",1:"#8f9fd0"}, INDC={5:"#f2d06b",4:"#e8bf5c",3:"#dcae4e",2:"#cf9d42",1:"#c08c38"}, ESCC={5:"#ef6a5a",4:"#e35b70",3:"#d45086",2:"#c04a97",1:"#a8479f"}, PR={5:15,4:12,3:9,2:7,1:5};',
}

def _rot_rgb(r, g, b):
    """Rotate greens (h 55-178) into the blue band (200-238), keeping lightness."""
    h, l, sat = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    hd = h * 360.0
    if 55.0 <= hd <= 178.0 and sat > 0.035:
        nh = 200.0 + (hd - 55.0) / (178.0 - 55.0) * 38.0
        ns = min(1.0, sat * 1.18 + 0.03)
        nr, ng, nb = colorsys.hls_to_rgb(nh / 360.0, l, ns)
        return int(round(nr*255)), int(round(ng*255)), int(round(nb*255))
    return r, g, b

_HEX = _re.compile(r'#([0-9a-fA-F]{6})\b')
_RGBA = _re.compile(r'rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([\d.]+)\s*\)')

def _hex_sub(m):
    h = m.group(1)
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return '#%02x%02x%02x' % _rot_rgb(r, g, b)

def _rgba_sub(m):
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    nr, ng, nb = _rot_rgb(r, g, b)
    return 'rgba(%d,%d,%d,%s)' % (nr, ng, nb, m.group(4))

def _darken_rgb(r, g, b):
    h, l, sat = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    hd = h * 360.0
    if 190.0 <= hd <= 250.0 and 0.48 <= l <= 0.80 and sat >= 0.38:
        nl = l * 0.62
        nr, ng, nb = colorsys.hls_to_rgb(h, nl, min(1.0, sat * 1.05))
        return int(round(nr*255)), int(round(ng*255)), int(round(nb*255))
    return r, g, b


def _hex_dark(m):
    h = m.group(1)
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return '#%02x%02x%02x' % _darken_rgb(r, g, b)


def _rgba_dark(m):
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    nr, ng, nb = _darken_rgb(r, g, b)
    return 'rgba(%d,%d,%d,%s)' % (nr, ng, nb, m.group(4))


def recolour_line(ln):
    if 'data:image/webp;base64' in ln:
        return ln
    ln = _RGBA.sub(_rgba_sub, _HEX.sub(_hex_sub, ln))
    return _RGBA.sub(_rgba_dark, _HEX.sub(_hex_dark, ln))



# --- the fallback seed still held the old map's pipeline/mine records ---------
# --- the hand-built points travel inside index.html ---------------------------
# Industry organisations and the spread record are written by hand, not harvested,
# so they live in the file rather than in projects.json. That keeps index.html the
# only thing that changes when entries are added, and it means the whole map still
# works if the fetch fails or the repo is served from somewhere else.
import json as _json
_seed = []
for _f in ("/mnt/user-data/outputs/harvest/industry_points.json",
           "/mnt/user-data/outputs/harvest/escape_records.json",
           "/mnt/user-data/outputs/harvest/register_records.json",
           "/mnt/user-data/outputs/harvest/animal_facilities.json",
           "/mnt/user-data/outputs/harvest/clinical_sponsors.json",
           "/mnt/user-data/outputs/harvest/ogtr_trials.json",
           "/mnt/user-data/outputs/harvest/projects_curated.json"):
    try:
        _seed.extend(_json.load(io.open(_f, encoding="utf-8"))["projects"])
    except Exception as _e:
        print("  ! seed source missing: %s (%s)" % (_f, _e))
print("  PJ_SEED embedded: %d points" % len(_seed))
block(1923, 1936, u'  var PJ_SEED=' + _json.dumps({"projects": _seed}, ensure_ascii=False) + u';')


# --- index panel: draggable, and click-to-collapse must not fire after a drag -
put(1513, u"  document.getElementById('idxHead').addEventListener('click',function(e){ const p=document.getElementById('indexPanel');"
          u" if(p._wasDrag){ p._wasDrag=false; return; }"
          u" const c=p.classList.toggle('collapsed'); document.getElementById('idxToggle').textContent=c?'+':'\\u2212'; });")

put(1896, u'try{var _wp=document.getElementById("wirePanel"); if(_wp && window.L){ L.DomEvent.disableScrollPropagation(_wp); L.DomEvent.disableClickPropagation(_wp);} }catch(e){}\n'
          u'(function(){ var p=document.getElementById("indexPanel"), hdl=document.getElementById("idxHead"); if(!p||!hdl)return;\n'
          u' var sx,sy,sl,st,on=false,moved=false;\n'
          u' function down(e){ if(e.target && e.target.id==="idxToggle") return; var ev=e.touches?e.touches[0]:e; var r=p.getBoundingClientRect();\n'
          u'   on=true; moved=false; sl=r.left; st=r.top; sx=ev.clientX; sy=ev.clientY;\n'
          u'   document.addEventListener("mousemove",move); document.addEventListener("mouseup",up);\n'
          u'   document.addEventListener("touchmove",move,{passive:false}); document.addEventListener("touchend",up); }\n'
          u' function move(e){ if(!on)return; var ev=e.touches?e.touches[0]:e; var dx=ev.clientX-sx, dy=ev.clientY-sy;\n'
          u'   if(Math.abs(dx)>4||Math.abs(dy)>4){ moved=true; p.style.transition="none"; p.style.right="auto"; p.style.bottom="auto";\n'
          u'     var w=p.offsetWidth, hh=p.offsetHeight;\n'
          u'     var nl=Math.max(4,Math.min(sl+dx, window.innerWidth-w-4));\n'
          u'     var nt=Math.max(4,Math.min(st+dy, window.innerHeight-hh-4));\n'
          u'     p.style.left=nl+"px"; p.style.top=nt+"px"; if(e.cancelable)e.preventDefault(); } }\n'
          u' function up(){ on=false; document.removeEventListener("mousemove",move); document.removeEventListener("mouseup",up);\n'
          u'   document.removeEventListener("touchmove",move); document.removeEventListener("touchend",up); p._wasDrag=moved; }\n'
          u' hdl.style.cursor="move"; hdl.title="Click to collapse \\u00b7 drag to move";\n'
          u' hdl.addEventListener("mousedown",down); hdl.addEventListener("touchstart",down,{passive:false});\n'
          u' try{ if(window.L){ L.DomEvent.disableScrollPropagation(p); L.DomEvent.disableClickPropagation(p);} }catch(e){}\n'
          u'})();')


# --- the angle selector had no CSS rule at all: unstyled browser default ------
put(2661, u"#intentSel,#angleSel{width:100%;margin:2px 0 4px;padding:6px 8px;background:#0e2e1d;color:#dff5e6;"
          u"border:1px solid rgba(120,200,150,0.45);border-radius:7px;font-size:9.5px;font-weight:600;text-overflow:ellipsis;}")
put(2662, u"#intentHint,#angleHint{font-size:10.5px;color:#93d6a8;line-height:1.45;margin:0 0 8px;padding:0 2px;}")
put(2663, u"#intentHint:empty,#angleHint:empty{display:none;}")


# --- community-resistance how-tos removed ------------------------------------
# SUBNATIONAL is declared and never read (1 occurrence in the whole file), so it
# is emptied outright. _GUIDES drives every guide button via _usGuide/_grpGuide;
# emptying it makes all of them disappear without touching the call sites.
block(494, 495, u'const SUBNATIONAL = {};')
put(1037, u'var _GUIDES={};')

# --- rail reflow: index moves to the left column when a unit is opened --------
put(992, u"""window._reflowInfo=function(){
  var p=document.getElementById('infoPanel'), ix=document.getElementById('indexPanel'),
      wp=document.getElementById('wirePanel'), hp=document.getElementById('helpPanel'),
      open=!!(p&&p.classList.contains('open')), narrow=window.innerWidth<=640;
  /* The index normally sits in the right-hand sidebar under the help panel \u2014 which is
     exactly where the resources panel wants to be. When a unit opens, move the index into
     the left column beneath the wire (which has already yielded its lower half), so both
     columns stay visible and line up. */
  if(ix){
    var imp=['position','left','top','width','max-height','min-height'];
    if(open && !narrow && wp){
      var wr=wp.getBoundingClientRect(), t=Math.round(wr.bottom)+9;
      ix.style.setProperty('position','fixed','important');
      ix.style.setProperty('left',Math.round(wr.left)+'px','important');
      ix.style.setProperty('width',Math.round(wr.width)+'px','important');
      ix.style.setProperty('top',t+'px','important');
      ix.style.setProperty('max-height',Math.max(120,window.innerHeight-t-18)+'px','important');
      ix.style.setProperty('min-height','0','important');
      ix.style.bottom='18px'; ix.style.zIndex='1001';
    } else {
      for(var i=0;i<imp.length;i++) ix.style.removeProperty(imp[i]);
      ix.style.bottom=''; ix.style.zIndex='';
    }
  }
  if(!open) return;
  if(narrow){ p.style.left='';p.style.width='';p.style.top='';p.style.bottom='';p.style.maxHeight=''; return; }
  try{ if(hp){ var r=hp.getBoundingClientRect(), tv=Math.round(r.bottom)+9;
    p.style.left=Math.round(r.left)+'px'; p.style.width=Math.round(r.width)+'px';
    p.style.top=tv+'px'; p.style.bottom='18px';
    p.style.maxHeight=(window.innerHeight-tv-18)+'px'; p.style.overflowY='auto'; } }catch(e){}
};""")

# the wire's height transition is .22s, so re-measure once it has settled
put(994, u"function showInfoPanel(html){ document.body.classList.add('info-open');"
         u" var b=document.getElementById('infoBody'); if(b)b.innerHTML=html;"
         u" var p=document.getElementById('infoPanel'); if(p){ p.classList.add('open');"
         u" if(window._reflowInfo){ _reflowInfo(); setTimeout(_reflowInfo,240); } } }")
put(995, u"function hideInfoPanel(){ const p=document.getElementById('infoPanel');"
         u" if(p)p.classList.remove('open'); document.body.classList.remove('info-open');"
         u" if(window._reflowInfo){ _reflowInfo(); setTimeout(_reflowInfo,240); } }")


# ================================= WIRE REGION FILTER =========================
# Three separate faults, all of which had to go:
#   1. _wireGeoTag() was defined and never called anywhere in the file, so no
#      item ever received an iso or a region -> every count read 0.
#   2. the country list was built from Object.keys(trackerData), so only the
#      countries in trackerdata.json appeared -> most of the world was missing.
#   3. subregion names came only from trackerData[iso].sub, which the seed has
#      none of -> no subregion could be listed OR matched.

put(1687, u"function _wireGetArchive(){ try{ return _wireTagAll(JSON.parse(localStorage.getItem('wireArchiveV1')||'[]')); }catch(e){ return []; } }\n"
          u"function _wireTagAll(a){ try{ if(Array.isArray(a)) for(var i=0;i<a.length;i++) _wireGeoTag(a[i]); }catch(e){} return a; }")

put(1717, u"  try{ var r=await fetch(WIRE_ARCHIVE_URL,{cache:'no-store'}); if(r.ok){ var j=await r.json();"
          u" if(Array.isArray(j)&&j.length){ _sharedArchive=_wireTagAll(j); return _sharedArchive; } } }catch(e){}")

put(1731, u"    if(r.ok){ var j=await r.json(); if(Array.isArray(j)) items=_wireTagAll(j);"
          u" else if(j&&Array.isArray(j.items)) items=_wireTagAll(j.items); else _diag='parsed but not a list'; }")

# ISO3 -> country name, so every country can be labelled, not just the seeded ones
put(1625, u"var _WIRE_ISO3NAME=null;\n"
          u"function _wireISO3Names(){ if(_WIRE_ISO3NAME)return _WIRE_ISO3NAME; var m={};\n"
          u"  try{ for(var a2 in _wireISONAME){ if(a2==='GL')continue; m[_WIRE_A2TO3[a2]||a2]=_wireISONAME[a2]; } }catch(e){}\n"
          u"  return _WIRE_ISO3NAME=m; }\n"
          u"function _wireCountryName(iso){ try{ var t=trackerData[iso]; if(t&&t.name)return t.name; }catch(e){}")
put(1626, u"  return _wireISO3Names()[iso]||_wireISONAME[iso]||iso; }")

# every country the map can name, not just the seeded ones
put(1635, u"  var isos=[]; try{ var seen={};\n"
          u"    Object.keys(_wireISO3Names()).forEach(function(k){ if(!seen[k]){seen[k]=1;isos.push(k);} });\n"
          u"    Object.keys(trackerData).forEach(function(k){ if(!seen[k]){seen[k]=1;isos.push(k);} });\n"
          u"    try{ Object.keys(SUBGEO).forEach(function(k){ if(!seen[k]){seen[k]=1;isos.push(k);} }); }catch(e){}\n"
          u"    Object.keys(counts).forEach(function(k){ if(k.indexOf('|')<0&&!seen[k]){seen[k]=1;isos.push(k);} });\n"
          u"  }catch(e){ isos=[]; }")

# subregion vocabulary: SUBGEO carries admin-1 names for 46 countries
put(1590, u"function _wireSubNames(iso){ if(_WIRE_SUBCACHE[iso])return _WIRE_SUBCACHE[iso]; var arr=[], seen={};")
put(1595, u"  }); }catch(e){}\n"
          u"  try{ var g=SUBGEO[iso]; if(g&&g.features) g.features.forEach(function(f){\n"
          u"    var k=f&&f.properties&&f.properties.name; if(!k)return;\n"
          u"    var sl=_wireSlug(k); push(sl,k); var st=_wireStripSuf(sl); if(st&&st!==sl) push(st,k);\n"
          u"  }); }catch(e){}")

# and the dropdown lists those same names
put(1640, u"  function subsOf(iso){ var o=[], seen={};\n"
          u"    function add(r){ if(r&&!seen[r]){seen[r]=1;o.push(r);} }\n"
          u"    try{ var sb=trackerData[iso]&&trackerData[iso].sub; if(sb) Object.keys(sb).forEach(add); }catch(e){}\n"
          u"    try{ var g=SUBGEO[iso]; if(g&&g.features) g.features.forEach(function(f){ add(f&&f.properties&&f.properties.name); }); }catch(e){}")
put(1641, u"    Object.keys(counts).forEach(function(k){ if(k.indexOf(iso+'|')===0) add(k.split('|')[1]); });")
block(1642, 1643, u"    return o.sort(); }")


# --- country tagging only fired when a headline literally led with "Country:" -
block(1598, 1602, u"""var _WIRE_NAMELIST=null;
function _wireNameList(){ if(_WIRE_NAMELIST)return _WIRE_NAMELIST; var a=[];
  try{ var m=_wireName2ISO(); for(var k in m){ if(k.length>=4) a.push([k,m[k]]); } }catch(e){}
  a.sort(function(x,y){ return y[0].length-x[0].length; });   /* longest first: "united states" before "united" */
  return _WIRE_NAMELIST=a; }
function _wireGeoTag(it){ if(!it)return it;
  try{ if(!it.iso){
    var lead=String(it.title||'').split(/[\/:\u2014|]|\s-\s/)[0], ls=_wireSlug(lead), n2i=_wireName2ISO();
    if(ls.length>3 && n2i[ls]) it.iso=n2i[ls];
    /* Fall back to scanning the headline itself. Title only, never the snippet:
       the body text of a wire item name-drops far too many countries to tag on. */
    if(!it.iso){ var hay=' '+_wireSlug(it.title||'')+' ', L=_wireNameList();
      for(var i=0;i<L.length;i++){ if(hay.indexOf(' '+L[i][0]+' ')>=0){ it.iso=L[i][1]; break; } } }
  } }catch(e){}
  try{ if(!it.region&&it.iso){ var iso3=_wireISO3(it.iso); var t=' '+_wireSlug((it.title||'')+' '+(it.snippet||it.desc||''))+' '; var subs=_wireSubNames(iso3);
    for(var j=0;j<subs.length;j++){ if(t.indexOf(' '+subs[j][0]+' ')>=0){ it.region=subs[j][1]; break; } } } }catch(e){}
  return it; }""")


# --- language filter: full names, not two-letter codes ------------------------
put(1669, u"""var _WIRE_LANGNAME={en:'English',es:'Spanish',fr:'French',de:'German',pt:'Portuguese',it:'Italian',nl:'Dutch',
 sv:'Swedish',no:'Norwegian',da:'Danish',fi:'Finnish',pl:'Polish',cs:'Czech',sk:'Slovak',hu:'Hungarian',ro:'Romanian',
 bg:'Bulgarian',el:'Greek',ru:'Russian',uk:'Ukrainian',tr:'Turkish',ar:'Arabic',he:'Hebrew',fa:'Persian',hi:'Hindi',
 bn:'Bengali',ur:'Urdu',ta:'Tamil',te:'Telugu',mr:'Marathi',th:'Thai',vi:'Vietnamese',id:'Indonesian',ms:'Malay',
 tl:'Filipino',zh:'Chinese',ja:'Japanese',ko:'Korean',sw:'Swahili',am:'Amharic',ha:'Hausa',yo:'Yoruba',ig:'Igbo',
 zu:'Zulu',af:'Afrikaans',sr:'Serbian',hr:'Croatian',bs:'Bosnian',sl:'Slovenian',lt:'Lithuanian',lv:'Latvian',
 et:'Estonian',is:'Icelandic',ga:'Irish',ca:'Catalan',eu:'Basque',gl:'Galician',ne:'Nepali',si:'Sinhala',km:'Khmer',
 my:'Burmese',lo:'Lao',ka:'Georgian',hy:'Armenian',az:'Azerbaijani',kk:'Kazakh',uz:'Uzbek',mn:'Mongolian'};
function _wireLangName(c){ if(!c||c==='Unknown')return 'Unknown';
  var k=String(c).toLowerCase().split(/[-_]/)[0];
  try{ var n=new Intl.DisplayNames([navigator.language||'en'],{type:'language'}).of(k);
       if(n&&n.toLowerCase()!==k) return n.charAt(0).toUpperCase()+n.slice(1); }catch(e){}
  return _WIRE_LANGNAME[k]||c; }
function _wireBuildLangOptions(items){""")
# Line 1673 is the `var opts` declaration, not the loop — replacing it left
# opts undeclared, so _wireBuildLangOptions threw a ReferenceError on every call
# and the language dropdown was never populated. Keep the declaration; rewrite
# the loop on 1674 instead, so the option shows the language NAME.
put(1674, u"  langs.forEach(function(lg){ opts+='<option value=\"'+lg+'\">'+_wireLangName(lg)+' ('+counts[lg]+')</option>'; });")

# --- belt-and-braces: tag at counting time, whichever path the items arrived by
put(1630, u"  var counts={}; items=_wireTagAll(items||[]); items.forEach(function(it){ var iso=it&&it.iso; if(!iso)return; iso=_wireISO3(iso);")


# --- index rows: the title opens the description; the link sits under it -------
block(1456, 1460, u"""function _rowHTML(r,i){ const tags=r.lenses.map(l=>'<span class="idx-lens">'+_esc(l)+'</span>').join('');
  var d=(r.desc||'').trim(), has=_hasUrl(r.url);
  var link=has?('<a class="idx-visit" href="'+_esc(_href(r.url))+'" target="_blank" rel="noopener">Visit source \u2197</a>'):'';
  var open=(d||has);
  var car=open?'<span class="idx-dcar" title="Show details">\u25BE</span>':'';
  var ck=r.checked?('<span class="idx-checked '+_ageClass(r.checked)+'">'+_checkedText(r.checked)+'</span>'):'';
  var db=open?('<div class="idx-desc">'+(d?_esc(d):'')+(link?('<div class="idx-visit-wrap">'+link+'</div>'):'')+ck+'</div>'):'';
  return '<div class="idx-row'+(open?' has-desc':'')+'">'
    +'<span class="idx-name'+(open?'':' idx-nourl')+'">'+_esc(r.name)+'</span>'""")

put(1505, u"  box.querySelectorAll('.idx-dcar, .idx-name').forEach(function(el){ el.onclick=function(ev){ ev.stopPropagation();"
          u" var r=this.closest('.idx-row'); if(r&&r.classList.contains('has-desc')) r.classList.toggle('open'); }; });")



# --- surface how old each entry's verification is ----------------------------
# Registers move and agencies reorganise; 300+ hand-written entries go stale
# quietly. Showing the check date makes that visible instead of invisible.
put(694, u"""  var _ck=t.checked?('<span class="tw-checked '+_ageClass(t.checked)+'">'+_checkedText(t.checked)+'</span>'):'';
  return `<div class="tracker-item collapsed" style="${bd}"><div class="tracker-name" onclick="this.parentNode.classList.toggle('collapsed')"><span class="tw-caret">&#9656;</span>${t.name}${tagChip(t)}${badge}</div><div class="tracker-body"><div class="tracker-desc">${t.desc||''}</div>${_hasUrl(t.url)?('<a class="tw-visit" href="'+_href(t.url)+'" target="_blank" rel="noopener">Visit source &#8599;</a>'):'<span class="tw-nourl">No verified site</span>'}${_ck}</div></div>`; }
function _ageClass(d){ if(!d) return ''; var ms=Date.now()-Date.parse(d+'T00:00:00Z');
  if(isNaN(ms)) return ''; var days=ms/86400000; return days>730?'old':(days>365?'stale':''); }
function _checkedText(d){ var a=_ageClass(d);
  return 'Checked '+d+(a==='old'?' \u2014 over two years ago; re-verify before relying on it':(a==='stale'?' \u2014 over a year ago':'')); }""")


# --- honour an explicit phase from the harvester, else infer from status ------
put(2567, u"  function pjPhase(p){ if(p.phase==='pre'||p.phase==='post') return p.phase;"
          u" var s=((p.status||'')+' '+(p.type||'')).toLowerCase();")


# --- group a unit's resources by INTENTION, in the order the menu runs --------
# Previously grouped by lens, which is a taxonomy of source types. Grouping by
# goal means the popup reads in the same sequence as "What are you trying to do?"
# — find the record, then the site, then the money, then the law, then allies.
block(707, 716, u"""var _INTENT_ORDER=null;
function _mgHead(label, n){
  var t = "this.parentNode.classList.toggle(\\u0027collapsed\\u0027)";
  return '<div class="media-group collapsed"><div class="mg-head" onclick="' + t
       + '"><span class="mg-caret">&#9662;</span>' + label
       + '<span class="mg-count">' + n + '</span></div><div class="mg-body">'; }
function _intentOrder(){ if(_INTENT_ORDER) return _INTENT_ORDER;
  // Read the goal sequence straight off the menu so the two can never diverge.
  var out=[], seen={};
  try{ var sel=document.getElementById("intentSel");
    if(sel) Array.prototype.forEach.call(sel.options,function(o){
      var k=o.value; if(!k||k==="all"||o.disabled||seen[k]) return;
      if(!INTENTS[k]) return; seen[k]=1;
      out.push({key:k, label:String(o.textContent||k).replace(/^\\s*\\d+[a-z]?\\s*\\u00b7\\s*/,"").trim()});
    }); }catch(e){}
  return _INTENT_ORDER=out; }
function _intentMatch(t, key){
  var it=INTENTS[key]; if(!it) return false;
  var tags=t.tags||[];
  if(it.subs && it.subs.length) return it.subs.some(function(x){ return tags.indexOf(x)>=0; });
  if(it.lens==="all") return false;
  return tags.some(function(x){ return x.split(":")[0]===it.lens; });
}
function lensGroupsHTML(list,kind){ if(!list||!list.length)return "";
 var order=_intentOrder();
 // A resource can serve more than one goal, and pretending otherwise would hide it
 // from the step where someone actually needs it. Entries repeat across groups.
 var byGoal={}, matched={};
 order.forEach(function(g){ var arr=list.filter(function(t){ return _intentMatch(t,g.key); });
   if(arr.length){ byGoal[g.key]=arr; arr.forEach(function(t){ matched[t.url]=1; }); } });
 var rest=list.filter(function(t){ return !matched[t.url]; });
 var h="";
 order.forEach(function(g){ var arr=byGoal[g.key]; if(!arr)return;
  h+=_mgHead(_esc(g.label), arr.length);
  arr.forEach(function(t){ h+=tHTML(t,kind); }); h+="</div></div>"; });
 if(rest.length){ h+=_mgHead("Everything else here", rest.length);
  rest.forEach(function(t){ h+=tHTML(t,kind); }); h+="</div></div>"; }
 return h; }""")


# --- key box: no facilities section on an industry map -----------------------
block(454, 457, u'  <div id="facFilter" style="display:none;"></div>')

# --- guides menu: its own pull-down panel above the lens box -----------------
put(364, u"""<div id="rightbar">
<div id="guidesPanel">
  <div id="guidesHead" onclick="document.getElementById('guidesPanel').classList.toggle('open')">
    <span>Guides &mdash; what to actually do</span><span class="guides-tog">&#9662;</span></div>
  <div id="guidesBody">
    <a class="guide-btn" href="#" onclick="openGuide(&#39;guides/how-to-stop-a-release.pdf&#39;,&#39;How to stop a release&#39;);return false;">
      <span class="gb-k">Guide 1 &middot; 28 pages</span>
      <span class="gb-t">How to stop a release</span>
      <span class="gb-d">One application, from finding it to filing against it. Find it, document it, organise, file it, publish it \u2014 five steps that run at once rather than in order, each making the next credible. Includes where the tilt shows: who paid for the studies, who moved between the regulator and the industry, what was blacked out, and what your regulator is legally permitted to consider before you write a word.</span>
    </a>
    <a class="guide-btn" href="#" onclick="openGuide(&#39;guides/how-to-change-the-industry.pdf&#39;,&#39;How to change the industry&#39;);return false;">
      <span class="gb-k">Guide 2 &middot; 26 pages</span>
      <span class="gb-t">How to change the industry</span>
      <span class="gb-d">The rules rather than the permit. The four permit stages and the deadline on each, how far regulatory capture usually reaches, and what sits outside it \u2014 courts, information law, parliaments and auditors, local government, trade partners. Underneath everything: whether the thing is legally a GMO at all, because redraw that definition and every door above closes at once.</span>
    </a>
  </div>
</div>""")


# --- merge fetched records into the embedded set, never replace it ------------
block(2559, 2562, u"""    function mergeIn(fetched){
      // The embedded set is the hand-built points; the fetched file is whatever the
      // harvesters produced. Union them, keyed on url so a record cannot appear twice.
      var out = (PJ_SEED.projects || []).slice(), seen = {};
      out.forEach(function(r){ seen[r.url + '|' + r.name] = 1; });
      ((fetched && fetched.projects) || []).forEach(function(r){
        var k = r.url + '|' + r.name; if(!seen[k]){ seen[k] = 1; out.push(r); } });
      return { note: (fetched && fetched.note) || '', projects: out };
    }
    fromGz()
      .catch(function(err){ if(window&&window.console)console.warn('projects.json.gz load failed, trying plain:',err); return fromPlain(); })
      .then(function(d){ pjData=mergeIn(d); pjRender(); })
      .catch(function(err){ if(window&&window.console)console.warn('projects fetch failed; showing the embedded set only:',err); pjData=mergeIn(null); pjRender(); });""")


# --- industry points draw as squares, releases and spread as circles ---------
# The map now carries three kinds of point on one layer, and a reader cannot tell
# an organisation from a release if both are dots. Shape does that work without
# spending another colour channel, which is already carrying rated scale.
put(2291, u'      var i=p.impact||1, o={la:p.lat,lo:p.lng,i:i,c:PC[i]||"#212b16",ap:(p.precise===false),'
          u'ind:(String(p.source||"").indexOf("industry")===0),esc:(String(p.source||"").indexOf("escape")===0),p:p};')

block(2498, 2503, u"""      for(var k=0;k<vis.length;k++){ var o=vis[k]; var pt=m.latLngToContainerPoint([o.la,o.lo]); var r=pjRad(z,o.i);
        if(o.ind){
          // Organisation: a square, so it never reads as a release.
          var d=r*1.7;
          if(o.ap){ ctx.globalAlpha=0.20; ctx.fillStyle=o.c; ctx.fillRect(pt.x-d/2,pt.y-d/2,d,d); ctx.globalAlpha=1;
            ctx.lineWidth=1.4; ctx.strokeStyle=o.c; ctx.strokeRect(pt.x-d/2,pt.y-d/2,d,d); }
          else { ctx.fillStyle=o.c; ctx.fillRect(pt.x-d/2,pt.y-d/2,d,d);
            if(r>=2.4){ ctx.lineWidth=1; ctx.strokeStyle="#0a1f12"; ctx.strokeRect(pt.x-d/2,pt.y-d/2,d,d); } }
        } else if(o.esc){
          // Spread: a diamond. Something that got out is not a permission.
          var q=r*1.25;
          ctx.beginPath(); ctx.moveTo(pt.x,pt.y-q); ctx.lineTo(pt.x+q,pt.y);
          ctx.lineTo(pt.x,pt.y+q); ctx.lineTo(pt.x-q,pt.y); ctx.closePath();
          if(o.ap){ ctx.globalAlpha=0.20; ctx.fillStyle=o.c; ctx.fill(); ctx.globalAlpha=1;
            ctx.lineWidth=1.5; ctx.strokeStyle=o.c; ctx.stroke(); }
          else { ctx.fillStyle=o.c; ctx.fill(); ctx.lineWidth=1; ctx.strokeStyle="#0a1f12"; ctx.stroke(); }
        } else {
          if(o.ap){ ctx.globalAlpha=0.22; ctx.beginPath(); ctx.arc(pt.x,pt.y,r+1,0,6.2832); ctx.fillStyle=o.c; ctx.fill(); ctx.globalAlpha=1;
            ctx.beginPath(); ctx.arc(pt.x,pt.y,r+1,0,6.2832); ctx.lineWidth=1.4; ctx.strokeStyle=o.c; ctx.stroke(); }
          else { ctx.beginPath(); ctx.arc(pt.x,pt.y,r,0,6.2832); ctx.fillStyle=o.c; ctx.fill();
            if(r>=2.4){ ctx.lineWidth=1; ctx.strokeStyle="#0a1f12"; ctx.stroke(); } }
        }
      } },""")


# --- three independent kind toggles, own colours, own sizes ------------------
# The one checkbox turned everything off together, and all three kinds drew in
# the same ramp at the same size. Kind now decides shape, colour and size, and
# each kind has its own toggle.
put(420, u'  <label class="f-status"><input type="checkbox" id="projChk" checked> All map points</label>'
         u'<div class="pj-kinds">'
         u'<label><input type="checkbox" class="pj-kind" data-kind="industry" checked> <b>Industry</b> \u2014 organisations</label>'
         u'<label><input type="checkbox" class="pj-kind" data-kind="escape" checked> <b>Spread &amp; drift</b> \u2014 what got out</label>'
         u'<label><input type="checkbox" class="pj-kind" data-kind="release" checked> <b>Releases</b> \u2014 authorisations</label>'
         u'</div>')

# kind helpers, colour ramps and the toggle handler, appended after the layer
# is defined so nothing references them before they exist
put(2565, u"""  function pjHide(){ pjOn=false; if(_projLayer)map.removeLayer(_projLayer); if(_pjPopup)map.closePopup(_pjPopup); var b=document.getElementById('projChk'); if(b)b.checked=false; }
  function pjKind(p){ var s=String((p&&p.source)||"");
    return s.indexOf("industry")===0?"industry":s.indexOf("escape")===0?"escape":"release"; }
  document.querySelectorAll(".pj-kind").forEach(function(cb){
    cb.addEventListener("change",function(){
      if(cb.checked) pjKinds.add(cb.dataset.kind); else pjKinds.delete(cb.dataset.kind);
      if(pjOn && pjData) pjRender();
    });
  });""")

put(2277, u'  var pjKinds=new Set(["industry","escape","release"]);\n  function pjPasses(p){')
put(2279, u'    if(!pjKinds.has(pjKind(p))) return false;\n    // A granted authorisation that has since run out is history, not news.\n    // The "Show dormant / defunct" switch decides whether history is drawn.\n    if(p.lapsed && typeof showHistorical!==\'undefined\' && !showHistorical) return false;')

put(2291, u'      var i=p.impact||1, kd=pjKind(p),'          u' o={la:p.lat,lo:p.lng,i:i,c:(kd==="industry"?INDC[i]:kd==="escape"?ESCC[i]:PC[i])||"#8fa0b8",'
          u'ap:(p.precise===false),kd:kd,p:p};')

block(2498, 2503, u"""      for(var k=0;k<vis.length;k++){ var o=vis[k]; var pt=m.latLngToContainerPoint([o.la,o.lo]);
        // Releases draw smaller than organisations: an authorisation is one decision,
        // an organisation is the thing making thousands of them.
        var r=pjRad(z,o.i)*(o.kd==="release"?0.62:o.kd==="escape"?0.95:1.25);
        if(o.kd==="industry"){
          var d=r*1.7;
          if(o.ap){ ctx.globalAlpha=0.20; ctx.fillStyle=o.c; ctx.fillRect(pt.x-d/2,pt.y-d/2,d,d); ctx.globalAlpha=1;
            ctx.lineWidth=1.5; ctx.strokeStyle=o.c; ctx.strokeRect(pt.x-d/2,pt.y-d/2,d,d); }
          else { ctx.fillStyle=o.c; ctx.fillRect(pt.x-d/2,pt.y-d/2,d,d);
            if(r>=2.4){ ctx.lineWidth=1; ctx.strokeStyle="#0a1020"; ctx.strokeRect(pt.x-d/2,pt.y-d/2,d,d); } }
        } else if(o.kd==="escape"){
          var q=r*1.3;
          ctx.beginPath(); ctx.moveTo(pt.x,pt.y-q); ctx.lineTo(pt.x+q,pt.y);
          ctx.lineTo(pt.x,pt.y+q); ctx.lineTo(pt.x-q,pt.y); ctx.closePath();
          if(o.ap){ ctx.globalAlpha=0.22; ctx.fillStyle=o.c; ctx.fill(); ctx.globalAlpha=1;
            ctx.lineWidth=1.6; ctx.strokeStyle=o.c; ctx.stroke(); }
          else { ctx.fillStyle=o.c; ctx.fill(); ctx.lineWidth=1; ctx.strokeStyle="#0a1020"; ctx.stroke(); }
        } else {
          if(o.ap){ ctx.globalAlpha=0.22; ctx.beginPath(); ctx.arc(pt.x,pt.y,r+1,0,6.2832); ctx.fillStyle=o.c; ctx.fill(); ctx.globalAlpha=1;
            ctx.beginPath(); ctx.arc(pt.x,pt.y,r+1,0,6.2832); ctx.lineWidth=1.3; ctx.strokeStyle=o.c; ctx.stroke(); }
          else { ctx.beginPath(); ctx.arc(pt.x,pt.y,r,0,6.2832); ctx.fillStyle=o.c; ctx.fill();
            if(r>=2.2){ ctx.lineWidth=1; ctx.strokeStyle="#0a1020"; ctx.stroke(); } }
        }
      } },""")


# ------------------------------------------------------------------ emit ----
out = []
for i, ln in enumerate(lines, start=1):
    if i in DROP:
        continue
    out.append(recolour_line(R.get(i, ln)))

html = '\n'.join(out)

# Pin the release-scale ramp back to a warm ramp after the rotation, and give the
# context overlays distinct hues so they stay tellable apart on a blue basemap.
html = _re.sub(r'  var PC=\{[^;]*;', _PIN['PC'].replace('\\', '\\\\'), html, count=1)
for k, col in [("centres_origin", "#d8a13a"), ("gmofree", "#4fb3c9"),
               ("cultivation", "#c2603a"), ("protected", "#7b9c46"),
               ("genebanks", "#9a7bc4")]:
    html = _re.sub(r'("k": "%s", "label": "[^"]*", "color": ")#[0-9a-fA-F]{6}' % k,
                   lambda m, c=col: m.group(1) + c, html)

for _a, _b in [
    ('.chip.on { background:var(--accent); color:#040611; border-color:var(--accent); }',
     '.chip.on { background:#7fa8cc; color:#0b1220; border-color:#9dc0dd; }'),
    ('#tourBtn{',
     '.pj-kinds{display:flex;flex-direction:column;gap:4px;margin:5px 0 2px 6px;}.pj-kinds label{display:flex;align-items:center;gap:6px;font-size:10.5px;color:#9aa8c0;cursor:pointer;}.pj-kinds label b{color:#c8d4e8;font-weight:700;}#guidesPanel{flex:0 0 auto;background:rgba(8,12,27,0.96);border:1px solid var(--accent-soft);border-radius:10px;box-shadow:0 4px 22px rgba(0,0,0,0.45);overflow:hidden;}#guidesHead{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px 12px;cursor:pointer;font-size:11.5px;font-weight:700;color:#eaf1ff;letter-spacing:.2px;user-select:none;}#guidesHead:hover{background:rgba(127,168,204,0.10);}.guides-tog{font-size:11px;color:#7fa8cc;transition:transform .18s;}#guidesPanel.open .guides-tog{transform:rotate(180deg);}#guidesBody{display:none;padding:0 12px 12px;flex-direction:column;gap:8px;}#guidesPanel.open #guidesBody{display:flex;}.guide-btns{display:flex;flex-direction:column;gap:8px;margin:14px 0 4px;}.guide-btn{display:block;text-decoration:none;padding:11px 13px;border-radius:9px;background:rgba(127,168,204,0.10);border:1px solid rgba(127,168,204,0.42);transition:all .15s;}.guide-btn:hover{background:rgba(127,168,204,0.20);border-color:#9dc0dd;}.gb-k{display:block;font-size:9.5px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#7fa8cc;margin-bottom:3px;}.gb-t{display:block;font-size:13px;font-weight:700;color:#eaf1ff;margin-bottom:4px;}.gb-d{display:block;font-size:11px;line-height:1.45;color:#a8b4cc;}#tourBtn{'),
    ('.idx-ce span{ cursor:pointer; color:#26378a; }',
     '.idx-ce span{ cursor:pointer; color:#7fa8cc; }'),
    ('.ps-pill.on{background:#081657;color:#eaeeff;border-color:#081657;}',
     '.ps-pill.on{background:#3d5673;color:#eaf1ff;border-color:#567192;}'),
    ('.pt-pill.on{background:#081657;color:#eaeeff;border-color:#081657;}',
     '.pt-pill.on{background:#3d5673;color:#eaf1ff;border-color:#567192;}'),
    ('.best-pill.on{background:#26378a;color:#050917;border-color:#26378a;font-weight:600;}',
     '.best-pill.on{background:#3d5673;color:#eaf1ff;border-color:#567192;font-weight:600;}'),
    ('.wire-tab.on{color:#0e1524;background:#314184;border-color:#314184;}',
     '.wire-tab.on{color:#eaf1ff;background:#3d5673;border-color:#567192;}'),
    ('.skpill.on { background:var(--accent-soft); color:var(--accent-hi); border-color:var(--accent-soft); }',
     '.skpill.on { background:#3d5673; color:#eaf1ff; border-color:#567192; }'),
    ('.tw-visit{', '.tw-checked{display:block;font-size:9.5px;color:#6f7d99;margin-top:6px;letter-spacing:.2px;}.tw-checked.stale{color:#c2913a;}.tw-checked.old{color:#c2603a;}.idx-checked{display:block;font-size:9.5px;color:#6f7d99;margin-top:5px;}.idx-checked.stale{color:#c2913a;}.idx-checked.old{color:#c2603a;}.tw-visit{'),
    ('.idx-desc{display:none;',
     '.idx-visit-wrap{margin-top:6px;}.idx-visit{display:inline-block;font-size:10px;font-weight:600;color:#7fa6dd;text-decoration:none;border:1px solid #567192;border-radius:5px;padding:3px 8px;}.idx-visit:hover{background:#3d5673;color:#eaf1ff;}.idx-name{cursor:pointer;}.idx-desc{display:none;'),
]:
    assert _a in html, 'pill rule not found: ' + _a[:40]
    html = html.replace(_a, _b)

# carry `checked` into every INDEXDATA row (the source predates the field)
_n_idx = 0
def _add_checked(m):
    global _n_idx
    if 'checked:' in m.group(0):
        return m.group(0)
    _n_idx += 1
    return m.group(0)[:-1] + ",checked:(tr.checked||null)}"
html = _re.sub(r"INDEXDATA\.push\(\{name:tr\.name.*?desc:\(tr\.desc\|\|''\)\}", _add_checked, html)
print('  INDEXDATA rows carrying checked:', _n_idx)

# every toggled pill on the same light blue, applied after the rule list so it
# catches any the list missed
# Client-side wire tagging must keep every script. _wireSlug stripped everything
# outside a-z0-9, so the browser fallback could not read a Chinese, Japanese,
# Cyrillic, Thai, Devanagari or Arabic headline either. Applied as text edits
# because this code is generated above, so it has no stable source line.
_old_slug = ("function _wireSlug(s){ return String(s||'').toLowerCase().normalize('NFD')"
             ".replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim(); }")
_new_slug = ("function _wireSlug(s){ return String(s||'').toLowerCase().normalize('NFD')"
             ".replace(/[\\u0300-\\u036f]/g,'').replace(/[^\\p{L}\\p{N}\\p{M}]+/gu,' ').trim(); }")
assert _old_slug in html, "wire slug not found"
html = html.replace(_old_slug, _new_slug, 1)

# Scripts written without spaces need substring matching, not word boundaries.
_old_scan = "for(var i=0;i<L.length;i++){ if(hay.indexOf(' '+L[i][0]+' ')>=0){ it.iso=L[i][1]; break; } } }"
_new_scan = ("for(var i=0;i<L.length;i++){ var nm=L[i][0];"
             " var hit=/[\\u0E00-\\u0EFF\\u1000-\\u109F\\u1780-\\u17FF\\u2E80-\\u9FFF\\uAC00-\\uD7AF]/.test(nm)"
             " ? hay.indexOf(nm)>=0 : hay.indexOf(' '+nm+' ')>=0;"
             " if(hit){ it.iso=L[i][1]; break; } } }")
if _old_scan in html:
    html = html.replace(_old_scan, _new_scan, 1)
else:
    print("  ! wire name scan not found - client fallback still ASCII-only")

# --- in-page guide viewer -----------------------------------------------------
# The guides opened as raw PDFs in a new tab, which loses the map. They now open
# in an overlay over it, with a download button for anyone who wants the file.
_GUIDE_HTML = u"""
<div id="guideOverlay" onclick="if(event.target===this)closeGuide()">
  <div id="guideBox">
    <div id="guideBar">
      <span id="guideName"></span>
      <span class="gv-actions">
        <a id="guideDl" href="#" download>Download PDF</a>
        <button id="guideX" onclick="closeGuide()" title="Close">&times;</button>
      </span>
    </div>
    <iframe id="guideFrame" title="Guide"></iframe>
  </div>
</div>
<style>
#guideOverlay{display:none;position:fixed;inset:0;z-index:4000;background:rgba(4,7,18,0.78);
  align-items:center;justify-content:center;padding:26px;}
#guideOverlay.on{display:flex;}
#guideBox{width:min(1000px,94vw);height:min(88vh,1000px);display:flex;flex-direction:column;
  background:#0b1020;border:1px solid #7fa8cc;border-radius:12px;overflow:hidden;
  box-shadow:0 18px 60px rgba(0,0,0,0.6);}
#guideBar{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:9px 12px;background:rgba(127,168,204,0.12);border-bottom:1px solid rgba(127,168,204,0.35);}
#guideName{font-size:12.5px;font-weight:700;color:#eaf1ff;letter-spacing:.2px;}
.gv-actions{display:flex;align-items:center;gap:10px;}
#guideDl{font-size:11px;font-weight:700;color:#0b1220;background:#7fa8cc;border:1px solid #9dc0dd;
  border-radius:7px;padding:5px 10px;text-decoration:none;}
#guideDl:hover{filter:brightness(1.1);}
#guideX{background:none;border:none;color:#9aa8c0;font-size:20px;line-height:1;cursor:pointer;padding:0 2px;}
#guideX:hover{color:#eaf1ff;}
#guideFrame{flex:1 1 auto;width:100%;border:none;background:#1b1b1b;}
</style>
<script>
function openGuide(src,title){
  var o=document.getElementById('guideOverlay');
  document.getElementById('guideName').textContent=title||'Guide';
  document.getElementById('guideDl').href=src;
  document.getElementById('guideFrame').src=src+'#view=FitH';
  o.classList.add('on');
}
function closeGuide(){
  var o=document.getElementById('guideOverlay');
  o.classList.remove('on');
  document.getElementById('guideFrame').src='';
}
document.addEventListener('keydown',function(e){ if(e.key==='Escape')closeGuide(); });
</script>
"""

# The layer checkbox used the old dark accent while the three kind checkboxes
# under it were light blue. One accent for all of them.
html = html.replace(".f-status input { accent-color:var(--accent);",
                    ".f-status input { accent-color:#7fa8cc;", 1)
html = html.replace(".pj-kinds label{",
                    ".pj-kinds input{accent-color:#7fa8cc;width:13px;height:13px;cursor:pointer;}"
                    ".pj-kinds label{", 1)

# --- index and lens filters read the POINTS, not trackerData -----------------
# trackerData ships as {} since entries became map points, so buildIndexData
# produced an empty index and every lens button filtered a set with nothing in
# it. Both now read PJ_SEED, which carries tags/kind/voice/trust/skind.
_old_idx = html[html.index("function buildIndexData(){"):]
_old_idx = _old_idx[:_old_idx.index("\nfunction ", 1)]
_new_idx = """function buildIndexData(){ INDEXDATA=[];
  var rows = (typeof pjData!=='undefined' && pjData && pjData.projects) ? pjData.projects
           : ((typeof PJ_SEED!=='undefined' && PJ_SEED.projects) || []);
  rows.forEach(function(p){
    var src=String(p.source||'');
    var isInd=src.indexOf('industry')===0, isEsc=src.indexOf('spread')===0;
    INDEXDATA.push({
      name:p.name, url:p.url||'', country:(p.state||''), iso:'',
      level: isInd?'Organisation':(isEsc?'Spread':'Release authorisation'),
      lenses:(p.tags||[]).map(function(t){return String(t).split(':')[0];})
              .filter(function(v,i,a){return a.indexOf(v)===i;}),
      tags:(p.tags||[]), kind:(p.kind||'structured'), voice:(p.voice||'interpretive'),
      trust:(p.trust||'high'), skind:(p.skind||'other'),
      media:(typeof mediaKS==='function'?mediaKS(p.kind,p.skind):''),
      desc:(p.desc||''), checked:(p.checked||null),
      lat:p.lat, lng:p.lng, source:src
    });
  });
  return INDEXDATA;
}
"""
assert _old_idx.strip().endswith("}") or True
html = html.replace(_old_idx, _new_idx, 1)

# the lens pills and sub-chips must filter the map layer too
_old_pass = "    if(!pjKinds.has(pjKind(p))) return false;"
_new_pass = ("""    if(!pjKinds.has(pjKind(p))) return false;
    // Lens and sub-filter selection applies to the points. Release records carry
    // no facet tags, so they are shown whenever the lens is 'all' and hidden once
    // a facet is chosen - a facet is a claim about the industry, not about a permit.
    try{
      var _tg = p.tags || [];
      if(typeof domain!=='undefined' && domain && domain!=='all'){
        var _hit=false;
        for(var _i=0;_i<_tg.length;_i++){ if(String(_tg[_i]).split(':')[0]===domain){_hit=true;break;} }
        if(!_hit) return false;
      }
      if(typeof activeSubs!=='undefined' && activeSubs && activeSubs.size){
        var _sub=false;
        for(var _j=0;_j<_tg.length;_j++){ if(activeSubs.has(_tg[_j])){_sub=true;break;} }
        if(!_sub) return false;
      }
    }catch(e){}""")
assert _old_pass in html, "pjPasses kind guard not found"
html = html.replace(_old_pass, _new_pass, 1)

# Help-panel section headings and the industry menu, matched to the light blue
# used by the lens pills and the layer checkboxes.
html = html.replace(".hl-sec{display:inline-block;margin-top:2px;color:#305488;}",
                    ".hl-sec{display:inline-block;margin-top:2px;color:#7fa8cc;}", 1)
html = html.replace(".hl-sec{color:var(--accent-hi);font-size:10.5px;}",
                    ".hl-sec{color:#7fa8cc;font-size:10.5px;}", 1)
html = html.replace("#intentSel,#angleSel{width:100%;margin:2px 0 4px;padding:6px 8px;"
                    "background:#0a1232;color:#dce3f8;border:1px solid rgba(44,69,154,0.45);",
                    "#intentSel,#angleSel{width:100%;margin:2px 0 4px;padding:6px 8px;"
                    "background:rgba(127,168,204,0.16);color:#eaf1ff;border:1px solid #7fa8cc;", 1)

# --- organisation type: colour and toggles -----------------------------------
# Facets say what part of the industry a body works in. Type says what KIND of
# body it is, and a ministry, a committee, a company and a campaign group are not
# the same thing to argue with. Industry squares are coloured by type; spread
# and releases keep their own ramps, because neither is an organisation.
_OT = """  var OTC={company:"#f2c14e",ministry:"#6fa8dc",committee:"#8e7cc3",
    institute:"#76c893",igo:"#4db6ac",association:"#e08a5f",ngo:"#d96ba0",
    fund:"#c9a227",registry:"#9fb3c8"};
  var OTLABEL={company:"Companies",ministry:"Ministries & agencies",
    committee:"Committees & councils",institute:"Institutes & universities",
    igo:"Intergovernmental bodies",association:"Trade associations",
    ngo:"NGOs & campaigns",fund:"Funds & foundations",registry:"Registers & databases"};
  var pjTypes=new Set(Object.keys(OTC));
"""
assert 'var PC={' in html
html = html.replace("  var PC={", _OT + "  var PC={", 1)

# colour industry points by type
_old_o = ('o={la:p.lat,lo:p.lng,i:i,c:(kd==="industry"?INDC[i]:kd==="escape"?ESCC[i]:PC[i])||"#8fa0b8",')
_new_o = ('o={la:p.lat,lo:p.lng,i:i,c:(kd==="industry"?(OTC[p.otype]||INDC[i]):kd==="escape"?ESCC[i]:PC[i])||"#8fa0b8",'
          'ot:(p.otype||"company"),')
assert _old_o in html, "grid object not found"
html = html.replace(_old_o, _new_o, 1)

# filter on type
_old_f = "    if(!pjKinds.has(pjKind(p))) return false;"
_new_f = ("    if(!pjKinds.has(pjKind(p))) return false;\n"
          "    // Type applies to organisations only; spread and releases are not bodies.\n"
          "    if(String(p.source||'').indexOf('industry')===0 &&\n"
          "       typeof pjTypes!=='undefined' && !pjTypes.has(p.otype||'company')) return false;")
assert _old_f in html
html = html.replace(_old_f, _new_f, 1)

# checkboxes, under the three kind toggles
_old_k = '</div>'
_kinds = '<label><input type="checkbox" class="pj-kind" data-kind="release" checked> <b>Releases</b> \u2014 authorisations</label></div>'
assert _kinds in html, "kind block not found"
_types = ('<label><input type="checkbox" class="pj-kind" data-kind="release" checked> <b>Releases</b> \u2014 authorisations</label>'
          '</div><div class="ot-head">Release records</div><div class="pj-otypes" id="relBox"></div><div class="ot-head">Organisation type</div><div class="pj-otypes" id="otBox"></div>')
html = html.replace(_kinds, _types, 1)

_js = """
<script>
(function(){
  var box=document.getElementById('otBox'); if(!box||typeof OTC==='undefined')return;
  Object.keys(OTC).forEach(function(t){
    var l=document.createElement('label');
    l.innerHTML='<input type="checkbox" data-ot="'+t+'" checked>'
      +'<span class="ot-dot" style="background:'+OTC[t]+'"></span>'+OTLABEL[t];
    box.appendChild(l);
  });
  box.addEventListener('change',function(e){
    var t=e.target&&e.target.dataset&&e.target.dataset.ot; if(!t)return;
    if(e.target.checked)pjTypes.add(t); else pjTypes.delete(t);
    try{ if(window.pjRefresh) window.pjRefresh(); }catch(_e){}
  });
})();
</script>
<style>
.ot-head{font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  color:#7fa8cc;margin:9px 0 3px 6px;}
.pj-otypes{display:flex;flex-direction:column;gap:3px;margin:0 0 4px 6px;}
.pj-otypes label{display:flex;align-items:center;gap:6px;font-size:10.5px;color:#9aa8c0;cursor:pointer;}
.pj-otypes input{accent-color:#7fa8cc;width:13px;height:13px;cursor:pointer;}
.ot-dot{width:9px;height:9px;border-radius:2px;display:inline-block;flex:0 0 auto;}
</style>
"""
html = html.replace("</body>", _js + "</body>", 1)

# Context overlays on by default. They were opt-in because they used to be
# placeholders; two are now built from real geometry and the rest fail quietly if
# their file is absent, so there is nothing to protect the reader from.
_old_ov = '<label class="psrc-row"><input type="checkbox" data-ov="\'+o.k+\'"> '
_new_ov = '<label class="psrc-row"><input type="checkbox" data-ov="\'+o.k+\'" checked> '
assert _old_ov in html, "overlay checkbox not found"
html = html.replace(_old_ov, _new_ov)

# and switch them on at load, since the checkbox alone only reflects state
_ov_js = """
<script>
(function(){
  // The checkboxes ship checked; this turns the layers on to match. Wrapped and
  // delayed because an overlay whose geojson is missing must not stop the rest.
  function on(){
    document.querySelectorAll('input[data-ov]').forEach(function(cb){
      if(!cb.checked) return;
      try{ cb.dispatchEvent(new Event('change',{bubbles:true})); }catch(e){}
    });
  }
  if(document.readyState==='complete') setTimeout(on,1200);
  else window.addEventListener('load',function(){ setTimeout(on,1200); });
})();
</script>
"""
html = html.replace("</body>", _ov_js + "</body>", 1)

# --- lens buttons: the click fired, nothing redrew ---------------------------
# rebuild() restyles the country layer and the tracker markers. It has never
# touched the point canvas. Since round 73 pjPasses() honours `domain` and
# `activeSubs`, so a lens click was changing the filter and then leaving the
# points exactly as they were - which reads as a dead button.
_old_rb = "function rebuild(){ if(!window.__ready){ updateStats(); return; }"
_new_rb = ("function rebuild(){ if(!window.__ready){ updateStats(); return; }\n"
           "  try{ if(typeof pjOn!=='undefined' && pjOn && typeof pjRender==='function') pjRender(); }catch(_e){}")
assert _old_rb in html, "rebuild() head not found"
html = html.replace(_old_rb, _new_rb, 1)

# --- regime overlay: colour by regime type, not one flat purple --------------
# Every polygon was the same colour, so the only way to learn what a country's
# regime was is to click it one at a time. The three values are already in the
# data (`regime`: technique / trait / carveout); they just were not being used.
_REGC = """  var REGIMEC={technique:"#7e6fc0",trait:"#4d9fd6",carveout:"#d4643f"};
  var REGIMEL={technique:"Technique-based \u2014 regulated by how it was made",
    trait:"Trait-based \u2014 regulated by what the organism is",
    carveout:"Carve-out \u2014 a class moved outside registration entirely"};
  var REGIMED={
    technique:"<b>Regulated by how it was made.</b> If a laboratory technique was used, the organism goes through the biosafety system \u2014 no matter how small the change or whether the same result could have come from ordinary breeding. This is the strictest of the three and the one the industry lobbies hardest against, because a one-letter edit is treated the same as inserting a gene from another species. It is also the only approach under which gene-edited organisms reliably stay visible: they get assessed, they get a record, and the public gets a comment window.",
    trait:"<b>Regulated by what the organism is, not how it was made.</b> The question asked is whether the plant or animal has a trait that is new or risky \u2014 the method that produced it does not matter. In principle this catches a risky organism however it was made, including by conventional breeding. In practice it means most gene-edited organisms are waved through, because an edit that could have arisen naturally is not treated as novel. Only two countries in this dataset work this way.",
    carveout:"<b>At least one class of engineered organism has been moved outside registration.</b> Typically organisms edited without inserting foreign DNA. They are not assessed, not notified, not tracked, and in most cases not labelled \u2014 the law simply never reaches them, so no file exists to request and no comment window ever opens. This is the fastest-growing approach worldwide and the reason a permit-by-permit campaign can win every fight while the category it is fighting over quietly empties out. Nothing about the organisms changed; what disappeared is the record that they exist."};
"""
html = html.replace("try{window.REGIMEC=REGIMEC;window.REGIMEL=REGIMEL;",
                    "try{window.REGIMEC=REGIMEC;window.REGIMEL=REGIMEL;window.REGIMED=REGIMED;", 1)


# --- co-located points: fan them out ----------------------------------------
_FAN = """
  var _pjFan=null;
  function pjFanOffsets(rows){
    var at={}, i;
    for(i=0;i<rows.length;i++){
      var p=rows[i]; if(p.lat==null||p.lng==null) continue;
      var k=p.lat.toFixed(3)+','+p.lng.toFixed(3);
      (at[k]||(at[k]=[])).push(i);
    }
    var off=new Array(rows.length);
    Object.keys(at).forEach(function(k){
      var g=at[k];
      if(g.length===1){ off[g[0]]=[0,0]; return; }
      for(var j=0;j<g.length;j++){
        if(j===0){ off[g[0]]=[0,0]; continue; }
        var ring=Math.ceil((-3+Math.sqrt(9+12*j))/6)||1;
        var per=6*ring, idx=j-(3*ring*(ring-1)), a=(idx/per)*2*Math.PI;
        var rad=0.055*ring;
        off[g[j]]=[Math.cos(a)*rad, Math.sin(a)*rad];
      }
    });
    return off;
  }
"""
html = html.replace("  var PC={", _FAN + "  var PC={", 1)
html = html.replace('o={la:p.lat,lo:p.lng,i:i,',
  'o={la:p.lat+((_pjFan&&_pjFan[k]&&_pjFan[k][1])||0),lo:p.lng+((_pjFan&&_pjFan[k]&&_pjFan[k][0])||0),i:i,', 1)
html = html.replace("function pjBuildIndex(){",
  "function pjBuildIndex(){ if(!_pjFan && pjData && pjData.projects) _pjFan=pjFanOffsets(pjData.projects);", 1)

# --- lens click must redraw the point canvas --------------------------------
html = html.replace("function rebuild(){ if(!window.__ready){ updateStats(); return; }",
  "function rebuild(){ if(!window.__ready){ updateStats(); return; }\n"
  "  try{ if(typeof pjOn!=='undefined' && pjOn && typeof pjRender==='function') pjRender(); }catch(_e){}", 1)

# --- publish the colour maps so end-of-body scripts can read them ------------

# --- key box: regime colours and context-overlay toggles, up front -----------
_KEYOLD = '<div class="ot-head">Organisation type</div><div class="pj-otypes" id="otBox"></div>'
html = html.replace(_KEYOLD, _KEYOLD
  + '<div class="ot-head">Shaded areas &mdash; regulatory regime</div><div class="pj-otypes" id="regBox"></div>'
  + '<div class="ot-head">Shaded areas &mdash; context</div><div class="pj-otypes" id="ovBox"></div>', 1)

# The on-map legend, the key-box controls, the record panel and the filter tree
# live in tail.html beside this script. They were written directly into
# index.html over many rounds and a line-splice deleted them from build.py; the
# fragment has now been lifted back out verbatim, so a full rebuild reproduces
# them instead of silently dropping them.
#

# ---------------------------------------------------------------------------
# Post-build verification.
#
# This script has silently dropped whole features twice: a line-splice deleted
# the legend and key box, and three blocks that were only ever written into
# index.html by hand were lost on the next rebuild. Both times the build printed
# success and the map came back missing things nobody noticed for rounds.
#
# So the build now checks its own output for every feature that must survive it
# and refuses to overwrite a good file with a lossy one.
# ---------------------------------------------------------------------------
_REQUIRED = [
    ("PJ_SEED",            "var PJ_SEED="),
    ("map legend",         'id="mapLegend"'),
    ("regime key box",     'id="regBox"'),
    ("overlay key box",    'id="ovBox"'),
    ("release filters",    'id="relBox"'),
    ("subject filter",     'id="subjBox"'),
    ("regime definitions", "var REGIMED="),
    ("region clustering",  "function pjClusters"),
    ("record panel tree",  "pjTreeRows"),
    ("place note",         "pjPlaceNote"),
    ("organism grouping",  "pjOrgGroup"),
    ("source filter",      "activeProjSrc.has"),
]


def verify(html):
    missing = [name for name, marker in _REQUIRED if marker not in html]
    if missing:
        sys.stderr.write(
            "\nBUILD REFUSED: the output is missing %d feature(s) that the live\n"
            "map has:\n\n    %s\n\n"
            "These live only in index.html and this script does not know how to\n"
            "write them. Writing the file anyway would delete them from the site.\n"
            "index.html has NOT been overwritten.\n\n"
            "To fix properly, author the missing blocks into this script or move\n"
            "them into tail.html, then run again.\n"
            % (len(missing), "\n    ".join(missing)))
        sys.exit(1)
    print("  verification: all %d required features present" % len(_REQUIRED))

# tail.html is the source for those blocks. Edit it, not the built file.
_TAIL = pathlib.Path(__file__).resolve().parent / "tail.html"
if not _TAIL.exists():
    sys.exit("tail.html is missing: a rebuild would silently drop the legend, "
             "the key-box controls and the record panel. Restore it before building.")
html = html.replace("</body>", io.open(str(_TAIL), encoding="utf-8").read() + "</body>", 1)

# --- write ------------------------------------------------------------------
OUT = "/mnt/user-data/outputs/index.html"
verify(html)          # refuses to write a build that lost a feature
io.open(OUT, "w", encoding="utf-8").write(html)
print("wrote %s %d bytes; %d lines" % (OUT, len(html), html.count("\n") + 1))
