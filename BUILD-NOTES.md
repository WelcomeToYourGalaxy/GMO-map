# Live Global Genetic Engineering Map — build notes

A structural replica of the Live Global Project Map, retuned to opposition to the
genetic engineering of organisms, organised around **contamination and destruction**.

---

## Files

| File | What it is |
|---|---|
| `index.html` | The map. Self-contained except for the runtime data files below and the two CDN scripts (Leaflet, TopoJSON) the original also used. |
| `trackerdata.json` | Seed of the per-country resource directory — 18 countries, 35 verified entries. |

Drop both at the root of the repo and it runs. Everything else is optional and
degrades gracefully.

---

## What was preserved verbatim from the source map

Nothing structural was rewritten. Carried across unchanged:

- All CSS, every panel, the collapse/drag behaviour
- Leaflet setup, `maxBounds`, the painted-plate → Esri satellite crossfade (the
  533 KB base64 plate is intact)
- `SUBGEO` — the 1.34 MB embedded subnational geometry
- The country → ADM1 → ADM2 → ADM3/4 drilldown (`gb*` functions, CGAZ boundaries)
- The Index panel: group, sub-group, sort, search, locate
- The Global Wire: live/timeline modes, region **and subregion** breakdown,
  language filter, age filter, localStorage archive
- The facility-dot layer (`welcometoyourgalaxy.github.io/executive-map/`)
- The release-layer engine: clustering, scale sizing/colour, popups, deadline
  banners, "dig deeper" row, source/type/overlay filter boxes
- Every filter taxonomy: kind, voice, trust, source kind, media type, government
  level, angle, best-sources
- The tour machinery and the guide/PDF panel mechanism

---

## What was retuned

| Block | Change |
|---|---|
| `<title>`, `h1`, all-lens subtitle | Live Global Genetic Engineering Map — Contamination & Destruction |
| `DOMAINS` | 12 lenses, **same keys** (so angles, intents and guide wiring keep working), 66 sub-filters |
| `INTENTS` + `<option>` list | 17 goals rewritten |
| `ANGLEHINT` + angle options | 4 angles rewritten |
| `TOUR` | 12 steps rewritten |
| Help panel, wire lead, legend copy, filter tip | rewritten |
| `WIRE_THREADS` | 11 threads |
| `WIRE_FEEDS` | 30 feeds (18 publishers + 12 Google News front queries) |
| `SCALE` / `IMPACT` / `STOP` / `PROJ` / `KEYS` | **Functionally critical.** These gate and score the wire timeline. On the old wordlists no genetic-engineering item would have survived the gate at all. |
| `internationalBodies` | 6 bodies, 10 entries |
| `PJ_SRC` | 14 release-register families |
| `PJ_TYPES` + `pjTypeCat()` | 19 organism/application types + a rewritten classifier (22/22 on the test set) |
| `pjSrcGroup()` | new source prefixes |
| `PJ_OVERLAYS` | 5 context overlays |

---

## Deliberately empty, and why

**`INTL_MEMBER = {}`** — the source shipped a per-country map of anti-corruption
bodies. There is no verified per-country Cartagena / Plant Treaty / UPOV party
table in hand, and inventing ~200 rows would break the no-fabrication rule. The
popup section simply doesn't render until it's harvested from the BCH party list.
`_BODY_INFO` is empty for the same reason.

**`projects.json` is not shipped.** The release layer will read empty until it's
harvested. The in-map provenance panel says this outright rather than hiding it
behind a plausible-looking map.

---

## Harvest manifest for `projects.json`

Source keys must match `PJ_SRC[].k`, optionally suffixed (`bch:AR`, `ogtr:DIR-190`).

| key | Target | Location precision |
|---|---|---|
| `bch` | Biosafety Clearing-House LMO decisions, `bch.cbd.int` | country |
| `oecd_biotrack` | `biotrackproductdatabase.oecd.org` — browse by identifier / company / organism | country |
| `isaaa` | ISAAA GM Approval Database (flag as industry voice) | country |
| `ogtr` | OGTR GMO Record + **published active crop field-trial sites** | **site** |
| `aphis` | USDA APHIS BRS release permits & notifications | state/county |
| `eu_release` | EU deliberate-release Part B notifications + EU GM register | region |
| `cfia` | CFIA confined research field trials | province |
| `ctnbio` | CTNBio technical opinions & release decisions | national/state |
| `conabia` | CONABIA / SENASA authorisations | national/province |
| `geac` | GEAC minutes (parse, not a database) | state |
| `nzepa` | EPA NZ new-organism decisions | national/region |
| `contamination` | GM Contamination Register — **mark dormant** | country |
| `clinical` | ClinicalTrials.gov + WHO ICTRP, gene transfer/editing | site |
| `seed` | hand-curated | varies |

**Start with OGTR.** It is the only register in the world that publishes
field-trial site locations, so it is the only feed that will produce solid dots
rather than dashed rings on day one.

Overlay files go at `overlays/<key>.geojson` — `centres_origin`, `gmofree`,
`cultivation`, `protected`, `genebanks`. Missing ones show "— not yet available".

---

## Known gaps carried honestly into the UI

- **Contained use is under-recorded everywhere.** Most lab work is notified, not
  licensed, and notifications are rarely published individually.
- **Gene-edited organisms are increasingly invisible by design.** Where a
  jurisdiction has moved editing techniques outside GMO registration, there is no
  record to harvest. Absence of a dot means the law stopped requiring one. This
  is the largest structural gap and it is growing.
- **Coordinates are the exception, not the norm.** Expect dashed rings to
  outnumber solid dots.
- **The human side is not a release register at all** — germline, embryo
  selection, IVF/ART. It lives in the lenses and the index deliberately, rather
  than being forced into a layer it doesn't fit.
- **No coverage percentage is claimed.** No dataset holds the true global count.

---

## Still to do

1. `SUBNATIONAL` still points at the per-country `*-community-resistance-how-to`
   guide files. The mechanism is subject-neutral and intact; the guides need
   writing for the new subject (or the `file:`/`pdf:` keys stripped).
2. Extend `trackerdata.json` — the seed covers 18 countries. `legmap_sub.json`
   (subnational) and the laws layer are unpopulated.
3. `wire.json` needs a harvester writing against the new `WIRE_FEEDS`.

---

## Verified this build

- All 5 inline scripts parse (`new Function`, zero failures)
- Every `INTENTS` lens and sub resolves to a real `DOMAINS` entry
- Every `internationalBodies` tag resolves to a real lens:sub
- Every `trackerdata.json` tag, skind, kind, voice and URL scheme validates
- `pjTypeCat()` classifier: 22/22 on the test set
- Figures cited in-map (396 incidents / 63 countries / 1997–2013; rice ≈ one
  third of incidents) check out against the published register analysis

---

## Round 2 changes

**Palette: green → dark blue.** Done as an HSL hue rotation over every colour in
the file (hue 55–178° → 200–238°, lightness preserved, saturation nudged up so
dark values read blue rather than grey), not by hand-picking. 114 greens moved;
2 deliberately did not. Result: `--accent:#2e3e72`, `--accent-hi:#7889b5`,
body `#040611`, map `#090a1e`. Gold country highlighting was left alone — it
reads better against blue than it did against green.

Data encodings were pinned back *after* the rotation so they stay tellable apart:

- the release-scale ramp `PC` (cool→warm, 1→5)
- the five context-overlay colours (amber / cyan / rust / olive / violet)
- the four facility-dot colours

**Facility dots cut from six kinds to four.** Kept: ministry & agency HQ,
government office, town hall, courthouse. Dropped: police, fire. Removed from
`SETS` (so the data isn't fetched at all), `facActive`, and the filter UI order.

**Index grouping fixed.** `buildIndexData()` was writing each international
body's *name* into the `country` field, so "Group: Country" produced one
pseudo-country heading per body. They now share a single
`International & treaty bodies` group, with the body name moved to a `body`
field shown in the row meta. Result with the seed loaded: 19 groups — 18 real
countries plus one international group. Also added an empty-state message that
names `trackerdata.json` when no country data has loaded, since that is the
condition that produced the symptom.

**Help panel and wire panel rewritten from scratch**, and given the right jobs:

- *Global Wire* — introduces the subject and how a release actually proceeds,
  then names the four points where an activist can intervene.
- *How to use this map* — a mechanical walkthrough of every control: the plate
  → satellite crossfade, drilldown and breadcrumb, both rails, every filter row,
  and how to read release dots versus facility dots.

Shared visible-text runs with the source map are now down to one, and it is a
row of dropdown labels, not prose.

---

## Round 3 changes

**Tone corrected throughout.** The target is the decision machine, not the
organisms and not the people at the bench. Rewritten on that basis: all 12 lens
descriptions, the all-lens subtitle, the first two tour steps, the wire panel and
the help-panel opener. The release toggle is now **"Live releases & consents"** —
it names a record rather than passing a verdict on an organism.

Tour step 1 is now *Where we actually are*: a technology that rewrites the
instructions of living things and releases them into a world it doesn't control;
capability compounding exponentially while enforcement stays slow, national and
in places moving backwards. Tour step 2 is *What this map is against — and what
it isn't*: not the science, but a small number of firms and the agencies
licensing them making irreversible planet-scale decisions on a commercial
timetable, on self-generated evidence, under liability that doesn't price the
downside.

The paragraph beginning "The organising fact is contamination and destruction"
is gone — it had already been dropped from the help panel in round 2, and the
surviving restatement inside the tour went with the step-2 rewrite.

**Wire panel rewritten as continuous prose.** No bolded category lead-ins, no
jumping between headings. It now walks the pipeline once, in order, then draws
the leverage points out of that same sequence.

**New: a basics primer** folded into the wire panel — "New to this? The basics".
Covers what the technology is, what's genuinely open (published methods, microbial
and plant bench work, sequencing), what's walled off (mammalian cells, viral
vectors, gene drives, anything above BSL-1 — gated by institutional account
verification, not secrecy), the voluntary state of synthesis screening, and that
lawful release by an unaffiliated party is zero. Ends on the asymmetry: what has
been democratised is verification, not creation. The public got the microscope,
not the tools.

Figures in the primer carry their own caveats — the "fewer than one in a hundred
thousand" community-size estimate is stated as an inference from lab registries
and kit sales, not as a measured statistic.

---

## Round 4 changes

**Map key box was rendering wrong — fixed.** The provenance block I wrote in
round 1 opened `.lp-detail` and `.lp-detail-body` but never closed them, so the
data-source filter, the release-type filter, the context overlays and the whole
facility-dots section were nested *inside* the collapsed "Where this data comes
from" fold. They only appeared if you expanded it. Both wrappers now close;
the `#rightbar` div tree balances at 53/53.

**Index panel is now draggable**, matching the wire panel: drag `#idxHead` to
move, click it to collapse. A `_wasDrag` guard stops the collapse firing at the
end of a drag. Leaflet scroll/click propagation disabled on the panel.

**Help panel edits** — heading "The map itself" → "The map"; dropped the
loading-glitch aside, the wire's two-modes sentence, "the manual version of the
same thing", the filter-combining sentence, and the police/fire aside;
"breadcrumb" replaced with "a row of place names"; spacing added before Index;
the Group/then-by/Sort sentence replaced with a plain list of what the dropdowns
filter by; the country-crosshair note moved up into the row description.

**Coverage named explicitly** in the opener: farmers and saved seed, animals in
laboratories, livestock and pets, de-extinction, assisted reproduction, military
human-enhancement programmes, and the eugenic logic underneath.

**"Start here" tour rewritten to 14 steps** for readers with no background —
five of context (where we are, what the argument is, who it is done to, how a
release happens, why so little is visible), then one continuous worked example
in seven steps that also walks every control on the screen, then a summary card.

**`overlays/README.md` now says where each layer actually comes from** — only
WDPA is a ready-made download; Genesys is points not polygons; the other three
have to be built by joining a published list to admin boundaries, and the README
says so rather than implying the files are just missing.

**One more classifier fix:** a GM veterinary vaccine was landing in `livestock`
because the target species was tested before the word "vaccine". Vaccine now
takes precedence. Regression back to 12/12.

---

## Round 5 changes

**"Other angles" removed** from the angle selector. The internal `other` bucket
is left in place, so "Show all angles" still passes everything — only the
menu entry is gone.

**The angle selector had no CSS rule at all.** `#intentSel` was styled;
`#angleSel` was an unstyled browser default, which is why it looked wrong beside
it. Both selectors now share one rule, as do `#intentHint` / `#angleHint`.

**Wire description rewritten** in the register-walk style of the unearthings
map: a definition, then the process stage by stage, with the structural critique
carried inside the same sentence as the mechanism rather than argued separately.
Runs: what a release is → whether the law recognises it as one → who has
standing → consultation and what it reliably produces → who pays for the
assessment → the decision and the register → the conditions → the absence of
surveillance → patents outlasting all of it → nothing ever ending. Closes on the
feed count, which is checked against `WIRE_FEEDS` (30) rather than asserted.

---

## Round 6 changes

**Left rail re-flows when a unit is opened.** Previously the resources panel was
positioned under the help panel — the same slot the index occupies in
`#sidebar` — so opening a unit covered the index. `window._reflowInfo` now moves
the index into the left column beneath the wire (which already yields its lower
half via `body.info-open`), and puts it back when the panel closes. Both columns
bottom-align at `viewport - 18px`.

Two details that mattered: `#indexPanel` carries `position/left/top/width/
max-height: static !important` from the sidebar rule, so the reflow has to use
`setProperty(..., 'important')` rather than plain inline styles; and the wire's
height change is a .22s transition, so `showInfoPanel` / `hideInfoPanel` measure
once immediately and again at 240ms.

**Community-resistance how-tos removed.** `_GUIDES` is now `{}`, which kills
every guide button through `_usGuide` and `_grpGuide` without touching the call
sites. `SUBNATIONAL` turned out to be declared and never read anywhere in the
file — one occurrence total — so it is emptied outright. Zero
"community-resistance" strings remain.

**New wire fold: "The evidence, condensed."** Three parts — what people think
(World Risk Poll 2019 and Pew 2019–20, with the point that the undecided share
exceeds the approval share, and the income split running opposite to the common
assumption), what eating it shows (GRACE / G-TwYST / GMO90+, the livestock
dataset and its broiler caveat, the ~900-study review, the dissenting reading,
and the structural reason no human dietary study exists), and what releasing it
shows (Oregon bentgrass, feral canola, the Jacobina *Aedes* introgression,
Mexican maize landraces, GM eucalyptus and the GE chestnut, Bt persistence and
mirid release, gene drives).

It closes on the registrant-monitoring problem and on the two cases that cut
against a simple anti-GMO frame — dengue control and forest restoration — since
those are the strongest test of the map's framing, and it survives them: what is
opposed is a release architecture with no recall, no consent and no independent
monitoring, whatever the stated purpose.

---

## Round 7 changes

**Framing corrected.** The wire opened "A release is any moment an engineered
organism leaves containment", which frames the organism as a thing that
inherently ought to be contained. That is not the argument. It now opens on the
transaction: *every engineered organism outside a laboratory is there because
somebody applied for permission and somebody granted it — that is the subject of
this map; not the organism, the permission.*

**Wire prose rewritten in form rather than in wording.** The previous draft
tracked the unearthings piece sentence by sentence. Measured against the sample:
**zero shared runs of 25 characters or more.** What is carried across is the
shape — a definition, then the process walked in order, with the criticism
inside the same sentence as the mechanism.

The "world map of the paper trail" paragraph moved out of the help panel and
into the wire, where it now closes the sequence. The help panel points at it
instead of repeating it.

Applied: "Then nothing ends" and "Permanence without a decision…" deleted; the
"no review date, no expiry, no recall" sentence moved ahead of the patent
paragraph; the ownership passage cut to two sentences.

**Wire region filter — three separate faults, all fixed.**

1. `_wireGeoTag()` was **defined and never called anywhere in the file**, so no
   item ever received an `iso` or a `region`. Every bucket read 0. Now applied
   at all three load paths via `_wireTagAll()`.
2. The country list was built from `Object.keys(trackerData)` — 18 countries in
   the seed, so most of the world was absent from the dropdown. Now built from
   the full ISO table (102 nameable countries) unioned with `SUBGEO`,
   `trackerData` and whatever the wire actually carries.
3. Subregion names came only from `trackerData[iso].sub`, which the seed has
   none of — so no subregion could be listed *or* matched. Now also drawn from
   the embedded `SUBGEO` geometry: USA 52, JPN 46, IND 34, BRA 27, AUS 11.

A fourth fault surfaced while testing: the country tagger only matched headlines
that literally led with "Country:" or "Country —", so "Brazil approves new GM
maize…" tagged as nothing. It now falls back to scanning the headline for any
country name, longest first. Title only, never the snippet — body text
name-drops far too many countries to tag on. Test feed went from 3/6 to 7/8
country-tagged and 3/6 to 4/8 subregion-tagged, with the untagged item correctly
untagged (a company story with no country in it).

**Vivid blues darkened.** A second colour pass pulls blues in the 190–250° band
with lightness 0.48–0.80 and saturation ≥0.38 down to 62% lightness. Text-weight
blues above 0.80 are untouched so popup copy stays legible. One vivid blue
survives by design: the cyan pinned for the GMO-free-zones overlay.

---

## Round 8 changes

**Retitled** to *Live Global Genetic Frontlines Map* (`<title>` and `h1`).

**Tour cut from 14 slides to 9.** The five context slides are gone from the
popup; what was worth keeping is condensed into the wire panel as running prose.
The tour is now the worked example and nothing else: the situation, seven steps,
and the summary card.

**The compounding claim was wrong and is corrected.** "Each tool makes the next
one cheaper and faster to build" describes industry in general, not this. The
distinctive property is the product, not the tooling: shut a refinery and the
emissions stop, but an organism does not need the company to keep operating — it
reproduces, crosses with its relatives, and travels. The decision is made once;
what it authorises goes on repeating itself.

**Show, don't tell.** "Irreversibility is what makes that indefensible rather
than merely unwise" asserted a conclusion and carried no weight. It is replaced
by the Oregon record: a grass engineered to survive glyphosate got out of its
test plots, the source fields were taken out of production, a mitigation
programme was run, and three years later 62 of 585 plants pulled and tested were
still resistant, with the published conclusion that eradication was not
realistic — from a grass that was never sold, escaping the trials meant to
establish whether it was safe to sell.

The abstract landrace/patent list is likewise replaced with the Mexican maize
finding stated concretely: the reservoir every future maize variety is bred
from, held for generations by people who licensed nothing and were asked
nothing, with no procedure for taking it back out and no agency with a mandate
to try.

The basics fold now ends the same way — a beekeeper can send a jar of honey to a
laboratory and get back a dated result naming the construct in it for the price
of a week's groceries, but cannot be in the room where the trial upwind was
approved. Checking has become cheap; deciding has not moved.

**Deletions applied** (all verified at zero): the flourish disclaimer, "the
distance between those two curves", "inherently wicked", "who decides, on what
evidence", "Irreversibility is what makes…", "not the organism. The machine
around it", "quietly lowers the cost of causing it", "a screening option, a
health metric", "usually means supermarket food", "the microscope, not the
tools", and "Now the practical part…".

**Added:** assisted reproduction is now flagged in the wire as "not technically
genetic modification, but a kind of genetic engineering nonetheless".

---

## Round 9 changes

- Both wire folds ("The evidence, condensed" and "New to this? The basics")
  deleted with their text. Wire panel is now the lead prose only, 988 words.
- Tour button relabelled **"A worked example"**. Note: the round-4 relabel had
  silently failed — the source uses `&mdash;`, and the replacement targeted
  `\u2014`, so it never matched and was never verified. Now checked in output.
- Help opener: pointer sentence to the wire panel removed.
- Language filter shows full names via `Intl.DisplayNames`, with a ~70-entry
  static map as fallback. Values stay as codes so filtering is unaffected.
- Selected-pill fill changed from `var(--accent)` / `#081657` to `#24548c` with
  `#eaf1ff` text and a `#3a6fae` border, on `.chip.on`, `.ps-pill.on` and
  `.pt-pill.on`. Applied after the colour passes so it survives them.
- `_wireBuildRegionOptions` now calls `_wireTagAll(items)` before counting, so
  items are tagged whichever path they arrived by.

### Correction to the round-7 wire diagnosis

Round 7 claimed `_wireGeoTag()` was never called. That was wrong: line 1795
already had `items = items.map(_wireGeoTag)`. The grep that produced the claim
searched for `_wireGeoTag(` and missed the reference passed without parentheses.
The other two faults found in round 7 (country list drawn from `trackerData`,
subregion names drawn only from `trackerData[iso].sub`) were real and are fixed.

---

## Round 10 changes

Global Wire panel cut to the two closing paragraphs only — **988 words down to
137.** Everything else in the lead is gone: the permission framing, the
stage-by-stage walk through application / standing / consultation / assessment /
decision / conditions / monitoring, the Oregon bentgrass passage, the Mexican
maize passage, and the no-review-date and patent lines.

The panel now carries the scope statement and the wire's own description, and
nothing else.

---

## Round 11 — deep tier, first pass

`trackerdata.json`: **18 countries / 35 entries → 29 countries / 129 entries.**
All 129 validate against the live taxonomy — every tag resolves to a real
lens:sub, every skind/kind/voice is legal, every URL unique, every description
in the CAN / CAN'T / FOR house style. Zero problems.

New countries: UK, Spain, Italy, Netherlands, Austria, Switzerland, Norway,
Poland, Sweden, South Korea, China, Uganda, Ghana. Deepened: US (19), Australia,
Germany, Canada, India, France, Brazil, South Africa.

Depth is deliberately uneven — a country gets what it actually has. US 19,
UK 9, Australia/Germany 8, down to one entry each for Poland, Sweden, Korea,
Uganda and Ghana.

### Lens coverage, and where it is thin

    projects 68   environment 51   records 48   conserve 37   advocacy 33
    organizing 30 corporate 30     courts 25    spending 24
    people 5      financial 3      osint 2

The bottom three are genuinely under-served and it is not an oversight:

- **osint** — satellite and monitoring tools are global products, not national
  resources. They belong in `internationalBodies` rather than repeated 29 times.
- **financial** — per-country land and parcel registries exist nearly
  everywhere, but the URLs are the least stable of any category and many are
  regional rather than national. Only the ones I could stand behind went in.
- **people** — professional and vital-record databases are mostly commercial and
  jurisdiction-specific; adding them at volume would mean guessing.

### What is not here

No GM testing labs per country. The major accredited labs are global companies
operating across borders, so they belong at international level. No per-country
lobbying registers beyond the US and EU, because most countries do not maintain
one. Roughly 60 countries worldwide have no independent watchdog on this beat;
those slots stay empty rather than being filled with a general environmental NGO.

---

## Round 12 — global tools, then the medium tier

**Global tools moved to international level.** Six new bodies, 21 entries,
fixing the three thin lenses at one stroke instead of repeating the same tools
in 46 country files:

- **Earth observation** (Frascati) — Copernicus Browser, USGS EarthExplorer,
  NASA Worldview, OpenStreetMap
- **Archiving & change monitoring** (San Francisco) — Wayback Machine,
  archive.today, Google Alerts
- **Independent GM testing** (Luxembourg) — the JRC EU reference laboratory that
  validates event-specific detection methods, plus Eurofins and SGS
- **Corporate ownership & money** (London) — OpenCorporates, OCCRP Aleph, ICIJ
  Offshore Leaks, Open Ownership Register
- **Land, tenure & territory** (Groningen) — Land Portal, LandMark, Land Matrix
- **Researchers, publications & retractions** (Bethesda) — PubMed, OpenAlex,
  Retraction Watch Database, Espacenet

The ten round-1 international entries predated the `kind`/`skind` fields. The
engine defaulted them at runtime, so nothing was broken, but they were falling
into the wrong filter buckets. Now set explicitly.

**Medium tier added** — 17 countries at 1–2 entries each: Chile, Colombia, Peru,
Uruguay, Paraguay, Costa Rica, Ireland, Belgium, Denmark, Czechia, Hungary,
Romania, Türkiye, Thailand, Taiwan, Zambia, Ethiopia.

### Totals

**46 countries · 12 international bodies · 180 entries · 0 validation problems.**

    projects 99   environment 76   conserve 57   records 56   advocacy 40
    corporate 40  organizing 35    spending 31   courts 29
    osint 13      people 11        financial 9

osint went 2 → 13, people 5 → 11, financial 3 → 9 — entirely from the
international layer, which is where those resources belong.

### Entries worth knowing about

Several medium-tier countries are there because they are *arguments*, not
because they are large: Peru administers one of the longest national moratoria
anywhere; Hungary wrote a GMO-free commitment into its constitution; Denmark
operates a statutory compensation fund for contamination of a neighbouring crop;
Chile hosts GM seed multiplication for export while barring GM cultivation for
its own farmers, and the site-location question there was won on transparency
grounds rather than biosafety grounds.

---

## Round 13 — intent menu resequenced, thin tier begun

**The intent menu now runs in the order you would actually work.** It was 17
options in arbitrary order, each assuming you already knew how the process goes.
It is now numbered 1–17 and grouped into phases with non-selectable separator
rows:

    FIRST: find out what is actually happening   1-3
    THEN:  get what they did not publish         4
    THEN:  work out who is behind it             5-9
    THEN:  find out what the law already says    10
    THEN:  build the side that fights it         11-15
    DO THESE ANYWAY - they hold win or lose      16-17

One new intent added along the way: **6 · Read the patent** (`spending:patents`)
— it was reachable through the lens pills but had no goal entry, and it is one
of the highest-value steps in the sequence.

Every hint rewritten to carry its own context: why this step, why *now*, and
what you come away with. Steps 1 and 3 name the two things people most often
miss — the consent identifier and the comment-window closing date, and the
neighbours inside the drift radius who have standing and do not know a trial has
been consented. Step 13 says to contact a lawyer early, because the windows are
short. Verified: 18 intents, 18 selectable options, 7 separators, every option
maps to a real intent and every intent to an option.

**Thin tier begun** — 8 more countries where a national source could be stood
behind: Portugal (parcel-level GM maize declarations, the closest thing in
Europe to a public map of where GM crops actually grow), Ecuador (constitutional
prohibition), Viet Nam, Pakistan, Israel, Finland, Slovenia, Malaysia.

### Totals

**54 countries · 12 international bodies · 188 entries · 0 validation problems.**

### How the rest of the thin tier should be built

Not by hand. Roughly 90 countries remain, and I cannot verify that many national
authority URLs at volume without guessing — which would break the standard the
rest of this map is held to.

The right source already exists: the **Biosafety Clearing-House publishes a
competent-national-authority record for every Cartagena Protocol party**, with
the authority's name, contact and website. That is an authoritative, machine-
readable, per-country list of exactly the entry this map needs first for each
remaining country. Harvest it, and the thin tier builds itself from the treaty
registry rather than from anyone's recollection.

---

## Round 14

**The wire tagging is now done in the harvester, not the browser.** Three
attempts to fix it in `index.html` did not hold, and that path is hard to
inspect from outside. `wire_harvest.py` now ships `wire.json` with `iso`,
`region` and `lang` already populated, so the region dropdown counts come
straight from the data and the output can be checked before it is committed.

It carries 163 country name forms (including demonyms and "USDA"/"APHIS"),
subregion tables for 16 countries, and infers the country from an unambiguous
subregion name when the headline never names one — so "Oregon bentgrass escape,
USDA says" tags as USA / Oregon. Ambiguous names are excluded by construction
plus an explicit list: Georgia, Victoria, Washington, Pará, Córdoba, Valencia,
New York. Feed language is read from the feed's own `<language>` element.

    python3 harvest/wire_harvest.py --selftest

prints the tagging for a sample and writes nothing. Currently 8/10, with the two
misses correct — a Bayer patent story with no country in it, and an EU
parliament vote, which is supranational.

The harvest run also prints country-tagged and subregion-tagged counts, and
warns on stderr if nothing was tagged at all.

**A real bug found in `_wireGeoTag`.** The split regex had been emitted with
doubled backslashes — `/[\\/:\\u2014|]|\\s-\\s/` — so it was splitting on
literal backslashes and the letters `u`, `2`, `0`, `1`, `4` rather than on an em
dash or " - ". Headlines in the common `Country — Headline` form were never
being split, so the lead-name match could not fire. Fixed.

**Index rows reworked.** Clicking an entry's title now opens its description
instead of leaving the map. The source link moved to a button under the
description: **Visit source ↗**. The caret still works and does the same thing.

**"A worked example" moved to the foot of the help panel**, after the interface
walkthrough rather than before it.

**All active pills on one steel blue** (`#24548c` on `#3a6fae`): `.chip.on`,
`.ps-pill.on`, `.pt-pill.on`, `.best-pill.on`, `.wire-tab.on`, `.skpill.on`.
`.best-pill.on` and `.wire-tab.on` had been on separate blues and `.skpill.on`
on a translucent navy.

---

## Round 15 — regional blocs, global movements, more countries

**Three bodies that had no home on the map, 13 entries.**

*European Union* — the single most consequential bloc for this subject and, until
now, entirely absent. EFSA GMO Panel opinions (and the public comment window
that opens when each one publishes — the most reachable intervention point in
the European system), the Commission authorisation register, the Court of
Justice, EUR-Lex, the EU Transparency Register, and the European Ombudsman.
The Ombudsman is the one worth knowing about: free, no lawyer, and its published
findings on EFSA's independence rules have changed practice.

*Africa — regional* — the African Union model law that thirty national regimes
were drafted against, COMESA's push to move approvals from national to regional
level, and AFSA, the continent's largest civil-society alliance, which is the
fastest route from a continental question to a named local organisation.

*Global farmer & food-sovereignty movements* — La Vía Campesina, GRAIN, ETC
Group, PAN International.

**Eight more country entries**, including two worth singling out: Germany's
**Standortregister**, the statutory public register of release sites searchable
by location — the strongest available proof that publishing release locations is
both possible and lawful — and the **APHIS docket view on Regulations.gov**,
which is where a US deregulation proposal appears first.

### Totals

**55 countries · 15 international bodies · 211 entries · 0 validation problems.**

    projects 125  environment 81  conserve 68  records 64  advocacy 46
    corporate 45  organizing 38   courts 35    spending 35
    financial 16  people 14       osint 13

One defect caught in validation: the Court of Justice entry had `kind:"court"`,
but `court` is a *source kind*, not a *kind*. It would have fallen into the
wrong filter bucket silently. Fixed.

---

## Round 16 — courts, patents and access routes

A deepening pass rather than a widening one: the countries already on the map
mostly had a regulator and a watchdog but no way to check what the courts had
already decided. Nineteen entries across seventeen countries, weighted to case
law, plus four new countries (Greece, Serbia, Tanzania, Bulgaria).

**`courts` went 35 → 54.** The additions that carry the most:

- **Germany — Rechtsprechung im Internet.** German law imposes strict liability
  on the GMO user for damage to a neighbouring crop. The case law interpreting
  that is the closest thing in Europe to an answer to "who pays".
- **Colombia — Constitutional Court.** Its prior-consultation jurisprudence is
  among the strongest anywhere and applies directly to any release on or near
  collective territory.
- **Argentina — SAIJ.** Courts there have repeatedly restricted spraying near
  schools and settlements; those judgments travel well across the region.
- **Mexico — SCJN.** The procedural history of the transgenic-maize collective
  action, which is the longest-running centre-of-origin case anywhere.
- **Chile — Poder Judicial.** The seed-multiplication site-location question was
  decided in litigation, on transparency grounds.

**New international body: free legal information networks.** AfricanLII and
WorldLII. For much of Africa, AfricanLII is the only public route to a country's
biosafety statute, and the statute is usually the argument. WorldLII federates a
search across dozens of jurisdictions at once — useful for finding *which*
countries have litigated a question before going to the national source.

Four new countries chosen for what their law says rather than their size:
Bulgaria bans cultivation within a set distance of protected areas and organic
farms; Serbia prohibits commercial cultivation and trade outright and is under
continuous accession pressure over it; Tanzania's strict-liability clause was the
most demanding in Africa, and its relaxation is a documented case of regulatory
pressure working; Greece opted out of cultivation across its whole territory.

### Totals

**59 countries · 16 international bodies · 232 entries · 0 validation problems.**

    projects 131  environment 86  conserve 78  records 72  courts 54
    corporate 49  advocacy 46     organizing 39  spending 38
    financial 17  people 14       osint 13

---

## Round 17 — the two thinnest lenses

`people` and `financial` were the weakest parts of the map, and both matter more
here than their size suggested: one answers *who decided and what they had
declared*, the other answers *whose ground is this, and who has standing*.

**`people` 14 → 27.** New international body, *Officials, interests & the
revolving door*: LittleSis, Integrity Watch EU, ORCID, As You Sow, ICCR. Plus
national interest and lobbying registers for the UK, Canada, Australia, Germany,
the US and Ireland.

Three of those are worth naming:

- **ACOBA (UK)** publishes, case by case, which jobs former ministers and senior
  civil servants may take and on what conditions. It is the rare public record of
  a regulator's staff moving to the industry they regulated, written down by the
  government itself.
- **Integrity Watch EU** makes expert-group composition searchable. Expert groups
  are the quietest form of influence and the easiest to demonstrate, because the
  membership is published.
- **As You Sow.** A shareholder resolution forces a company to answer a question
  in writing, in public, on a fixed date. Nothing else on this map does that as
  cheaply — though it requires a holding.

**`financial` 17 → 26.** Cadastres and land registries for Mexico, Brazil,
France, Spain, the Netherlands and India. Two of these change the nature of the
question rather than just locating a parcel:

- **Mexico's Registro Agrario Nacional** holds ejido and comunidad records —
  collective tenure over a very large share of Mexican farmland. An ejido
  assembly is a decision-making body, not a neighbour.
- **Brazil's INCRA** shows whether a settlement or quilombola territory adjoins a
  site, which changes both the consultation duty and who has standing.

France's cadastre is open data and downloadable, so a drift radius can be mapped
against real parcels for nothing. India's is the honest opposite: land is a state
subject, there is no national search, and GEAC minutes give only a district — so
the entry says where the route actually starts rather than pretending to a
national answer.

### Totals

**59 countries · 17 international bodies · 251 entries · 0 validation problems.**

    projects 135  environment 86  conserve 81  records 72  courts 54
    corporate 54  advocacy 48     spending 47  organizing 43
    people 27     financial 26    osint 14

---

## Round 18 — going after the rule, not just the permit

The map could find precedent but had nothing for *changing* the law. Fixed at
three levels.

**New sub-filter: `courts:strategic` — "Strategic litigation & law reform."**
`courts:federal` also relabelled to "National, federal **& international**
courts", since regional human-rights courts were being misfiled under a label
that said national.

**New goal, step 11: "Go after the rule itself, not just this permit."** The
hint makes the tactical point plainly: the routes that work here are procedural —
consultation that was inadequate, evidence withheld, an exemption granted without
assessment. *You do not have to prove an organism is dangerous to establish that
the public was shut out of the decision, and the second is far easier to prove.*
Most of these bodies take a complaint from any member of the public, free,
without a lawyer.

**Two new international bodies, 15 entries.**

*International complaint mechanisms* — the **Aarhus Convention Compliance
Committee** first, because it is the most under-used route on this map: it
reaches the procedure itself, accepts communications from any member of the
public, costs nothing, needs no lawyer, and publishes its findings. Then **OECD
National Contact Points**, where a complaint can be filed against a multinational
in its *home* country over conduct in yours. Then UN Special Procedures, the
Escazú Agreement (with its defender-protection provisions), the Inter-American
Commission, the African Commission — whose Charter names a right to a
satisfactory environment explicitly, an unusually strong textual hook — and the
CBD, where the global position on gene drives is being written.

*Strategic litigation organisations* — **ELAW** first, a network of
public-interest environmental lawyers and scientists across seventy-plus
countries that supplies free legal and scientific back-up. For anyone outside the
wealthy jurisdictions it is probably the single most useful entry on the map.
Then ClientEarth, CIEL, Earthjustice, AIDA, Natural Justice, FIAN International
and the Business & Human Rights Resource Centre.

### Totals

**59 countries · 19 international bodies · 266 entries · 0 validation problems.**

    projects 136  environment 87  conserve 86  records 76  courts 75
    corporate 56  organizing 53   advocacy 49  spending 47
    people 27     financial 26    osint 14

`courts` went 54 → 75, and 15 of those carry the new strategic tag.

---

## Round 19 — the BCH route, verified

I had been recommending a Biosafety Clearing-House harvest for several rounds
without having verified it. Doing that now changed the plan in two ways.

**bch.cbd.int cannot be harvested.** It is a JavaScript application; its record
pages return "Error loading the Biosafety Clearing-House" to any fetcher. There
is no scrapeable HTML behind it.

**But the Secretariat publishes the same information as a PDF.**
`cbd.int/doc/lists/bch-fp.pdf` — the BCH national focal point list, **189
countries**, regenerated periodically, currently dated 6 July 2026. It gives the
institution for every Party, and for a good many it gives that institution's
website. Fetched and read; the structure is stable and parseable.

**`harvest/bch_focal_points.py`** parses it into per-country stubs. Two things
about it worth stating plainly:

- *Privacy.* The source carries named officials, their direct e-mail addresses
  and their phone numbers. None of that belongs in a public map. The script keeps
  only the institution and its published website, and asserts at the end that no
  e-mail address and no honorific survived into the output.
- *It produces a review queue, not a drop-in file.* Each stub says
  "TODO write CAN / CAN'T / FOR", and warns that a BCH focal point is not always
  the body that decides approvals. What the harvest removes is the guesswork
  about which countries exist and what their institutions are called — not the
  writing.

**Thirteen new countries added by hand from that list**, using only entries where
it gives an explicit institutional website. No domain was inferred from an e-mail
address: Cyprus, Lithuania, Latvia, Slovakia, North Macedonia, Ukraine,
Singapore, Guatemala, Panama, Kuwait, Sierra Leone, Bhutan, Lebanon — plus
better addresses for Hungary (a dedicated government GMO portal), Serbia (the
directorate rather than the ministry) and **a correction to Zambia**, whose
authority I had at the wrong domain.

Several were chosen for the argument rather than the size: Guatemala repealed a
seed law after mass protest; Lebanon sits inside the Fertile Crescent, the centre
of origin for wheat and barley, which is discussed far less than the maize one;
Latvia lets municipalities declare themselves GM-free and a large share have;
Bhutan built agricultural policy around organic production, which makes GM
cultivation moot rather than prohibited.

### Totals

**72 countries · 19 international bodies · 282 entries · 0 validation problems.**

    projects 155  conserve 96  environment 90  records 79  courts 75
    corporate 59  organizing 53  advocacy 49  spending 47
    people 27     financial 26   osint 14

---

## Round 20 — the subnational drilldown, which had never done anything

Until now **no country had a `sub` block**, which means the map's entire
state/province drilldown resolved to nothing: click into a country, descend a
level, and every region was empty. A headline feature doing no work.

**14 regions, 17 entries** across the United States and Australia. Region keys
verified against the embedded geometry — zero name mismatches. (Caveat: the live
drilldown matches against ADM1 names fetched from the boundary service, not the
embedded copy; they share a source, so this is a good proxy rather than a
guarantee.)

**United States — 10 states.** The ones carrying the most:

- **Hawaii.** The highest concentration of open-air GM breeding anywhere on
  Earth, because the climate allows several generations a year — sitting on a
  small island chain next to homes, schools and endemic species found nowhere
  else. Paired with the state judiciary, because Kaua'i, Hawai'i and Maui
  counties each passed measures and each was challenged. That litigation is the
  clearest US test of whether a county may regulate what the state and federal
  governments have not.
- **Oregon.** Where the bentgrass escaped. The state's own control-area orders
  are the paper record of how containment went, and Jackson County is the
  standing example of a county ban that took effect and held.
- **Vermont.** The first mandatory GMO labelling law to actually take effect in
  the United States. Industry could not stop it in court; Congress preempted it
  instead. The sequence is the lesson.
- **Washington**, because it grows a large share of the world's brassica and beet
  seed, where cross-pollination risk is highest and growers already organise
  around it.

**Australia — 4 states**, all chosen for the mechanism: Tasmania's moratorium,
justified on **market-access and brand grounds rather than safety**, which
sidesteps the argument industry is best equipped to win; South Australia, which
kept the moratorium for Kangaroo Island after lifting it on the mainland;
Western Australia, backdrop to the fully litigated neighbour-contamination case;
and New South Wales, whose repeal debate is the fullest Australian record of the
arguments on both sides.

### Totals

**72 countries · 14 subnational regions · 19 international bodies · 299 entries ·
0 validation problems.**

    projects 165  environment 105  conserve 105  records 83  courts 80
    corporate 59  organizing 53    advocacy 51   spending 47
    financial 28  people 27        osint 14

---

## Round 21 — subnational, continued

Seven more countries given `sub` blocks: Mexico, Brazil, India, Argentina,
Canada, Germany, Spain, South Africa. **10 countries · 32 regions · 35
subnational entries**, region keys copied exactly from the boundary data
including diacritics and native spellings — zero mismatches.

These were picked for where the argument actually lives, not by size:

- **Oaxaca and Chiapas** — Oaxaca is not a place where maize is grown so much as
  the place it comes from, and several Mexican states declared themselves free of
  transgenic maize before the federal position hardened. **Sinaloa** is in as the
  other side: the commercial case for transgenic maize in Mexico is made from
  there, and understanding it beats ignoring it.
- **Rio Grande do Sul** — Brazil's GM soy was legalised *after* years of
  unauthorised planting concentrated in this state. The clearest case anywhere of
  approval following adoption rather than preceding it.
- **Maharashtra and Gujarat** — unapproved herbicide-tolerant cotton has been
  planted at scale in Maharashtra for years, and Gujarat is where India's first
  unapproved Bt cotton was found before any approval existed. State enforcement
  records are the record of what happens when approval is simply bypassed.
- **Córdoba and Entre Ríos** — the first criminal convictions in Latin America
  for spraying beside a populated area, and the school-buffer cases whose
  reasoning has been borrowed across the region.
- **Aragón and Cataluña** — almost all GM cultivation in the European Union
  happens in these two Spanish regions, which makes their coexistence enforcement
  the whole of Europe's practical experience of it.
- **Mecklenburg-Vorpommern** — where German commercial GM maize actually was,
  which makes the state's own record the best account of why it stopped.
- **Prince Edward Island** — its legislative committee held one of the few
  sustained, formal public deliberations on this subject by any legislature in
  North America. The submissions are a record of what people actually said.
- **Free State** — South Africa grows GM white maize as a staple food rather than
  as feed, which is close to unique globally, and most of it is grown there.

### Totals

**72 countries · 10 with subnational data · 32 regions · 19 international bodies
· 317 entries · 0 validation problems.**

    projects 178  environment 121  conserve 116  records 84  courts 84
    corporate 59  organizing 56    advocacy 54   spending 47
    financial 29  people 27        osint 14

---

## Round 22 — bringing the anchors up to date

Six of the map's factual anchors described a position that has since moved. A
large, current map beats a larger stale one, so this round fixed the facts rather
than adding volume.

**United States — the SECURE rule was vacated.** The APHIS entry described
"regulatory-status determinations that exempt an organism from oversight", which
was the SECURE mechanism. A court vacated that rule on **2 December 2024**;
APHIS reverted to the pre-2020 regulations at 7 CFR 340, and permitting,
notifications and petitions restarted through early 2025. USDA then ran a request
for information on a replacement framework, closing **15 June 2026**. The entry
now says so, and makes the point that the framework governing every US release is
being rewritten in public right now — which is the rarest and best moment to be
watching one.

**European Union — the NGT file is now law.** The Commission entry described a
pending "deregulation file". **Regulation (EU) 2026/1388** was adopted by the
Council on 21 April and Parliament on 17 June 2026, entered into force on 16 July
2026, and applies from 17 July 2028. It splits NGT plants into NGT-1 (treated
broadly as conventional, outside authorisation and labelling) and NGT-2 (inside).
The entry now names it, and names what it costs: NGT-1 is the single largest
deliberate reduction in the European public record on this subject.

**EFSA — the comment window has mechanics.** Saying a window "opens" was not
actionable. It is 30 days from EFSA publishing an opinion, comments go through
Connect.EFSA, and they are archived on OpenEFSA.

**OGTR — likewise, plus a warning.** Consultation runs a minimum of 30 days and
is advertised in the Government Notices Gazette, with email alerts available. The
entry now also says what the statute puts *out* of scope — trade, marketing, food
safety and claimed benefits — because an objection built on any of those will not
land, and that is worth knowing before writing one.

**Mexico — the prohibition moved into the Constitution.** After a USMCA panel
ruled against the maize decree on 20 December 2024, Mexico amended Articles 4 and
27, published **17 March 2025**. The entry now frames Mexico as the clearest test
anywhere of a constitutional prohibition set against a trade-agreement ruling.

**Gene drives — the nearest approach stalled.** Burkina Faso sealed Target
Malaria's facilities on **18 August 2025** and suspended all its activities on 22
August, days after a non-drive trial release at Souroukoudingan on 11 August.

**New country: Burkina Faso**, with its national biosafety agency and the farmer
and civil-society side. It has now ended two flagship programmes on its own
terms — Bt cotton, and the engineered-mosquito work — which is not the usual
direction of travel and deserves its own entry rather than a footnote.

### Totals

**73 countries · 32 subnational regions · 19 international bodies · 319 entries ·
0 validation problems.**

---

## Round 23 — making staleness visible

Last round's finding was that drift is this map's main long-term risk: 300+
hand-written entries go out of date quietly, and nothing about a stale entry
looks wrong. This round builds the machinery for that instead of adding entries.

**Every entry now carries a `checked` date** — all 319, country, subnational and
international. The map renders it under each entry in both the unit popups and
the index rows: grey under a year, amber over a year, rust over two with
"re-verify before relying on it".

**`harvest/check_links.py`** checks every URL and reports what has rotted,
separating outcomes that mean different things: 404/410 is gone, 403/429 is
usually a bot filter rather than a dead link, 5xx may be transient. `--stale-only`
skips the network and just ranks entries by verification age. `--update-dates`
stamps today on entries that resolved — and prints a warning that this is the
weaker check, because a URL resolving is not the same as an entry being accurate.

### A build failure worth recording

The first attempt at this put a `put(2454, ...)` over two lines that turned out
to be live code in the project popup. Caught by reading the target lines before
trusting the line number — the same class of error as the round-1 `PJ_SEED`
problem, where a line-numbered edit landed somewhere plausible and wrong.

Then the rewritten build crashed on a `NameError`, and because the build command
had `2>/dev/null` on it, the failure was invisible and the validator was reading
a **stale output file from the previous run** — reporting clean results for code
that had never been generated. Both fixed. The lesson is the same one twice:
suppressing build output makes a validator lie.

### Totals

**73 countries · 32 subnational regions · 19 international bodies · 319 entries ·
0 validation problems · 0 entries without a verification date.**

---

## Round 24 — the principals

The map could find registers, courts and money but had no answer to the plainest
question anyone asks first: *who is doing this?*

**New sub-filter `corporate:principals` — "The principals: who is actually doing
this."** New goal **5b · "See the handful of firms and agencies behind most of
it"**, sitting beside the existing ownership step. Its hint carries the rule this
whole section is built on: *a name without a document is only an accusation.*

**Five new bodies, 18 entries.** Every one links to a public record that can be
checked — filings, a registry, a lobbying return, an official page — not to a
press summary or anyone's characterisation.

*The four agricultural biotechnology majors.* Bayer (which absorbed Monsanto),
Corteva, Syngenta (ChemChina/Sinochem) and BASF, each pointed at investor
filings rather than corporate homepages, because the risk-factor section is the
most candid account a company publishes of its own exposure. Syngenta is flagged
for what state ownership changes: shareholder resolutions and securities
disclosure do not reach it. BASF's seed holdings exist because a merger regulator
required divestment — which is competition authorities already treating this as a
concentrated market.

*Industry associations.* BIO, CropLife International and ISAAA. ISAAA is included
as a record while flagged as an industry voice, on the reasoning that citing an
industry source for an industry figure is stronger than citing a critic for one.

*Gene editing & synthetic biology.* An SEC full-text search for the phrase rather
than a company list — you find firms you had not heard of, and the risk factors
say what the press releases do not. Plus Colossal and Oxitec.

*Assisted reproduction.* HFEA first, because clinic-level licensing, inspection
and outcome data exists there and almost nowhere else — which makes it the answer
to "oversight isn't possible". Then CDC ART data, which gives the United States
clinic-level statistics and no clinic-level regulator; ESHRE; and clinic-chain
ownership, because patients choose a clinic while the owner sets the policies and
the owner is findable.

*Public money & public agencies.* USDA NIFA, the Gates Foundation's own
searchable grant database, CGIAR, and DARPA's biological technologies office —
military biotechnology sitting outside civilian biosafety oversight in every
country that runs it.

All five are tagged `medium` or `low` trust where they are the subject's own
voice, so the existing trust filters exclude them cleanly.

### Totals

**73 countries · 32 subnational regions · 24 international bodies · 337 entries ·
0 validation problems.**

    projects 185  environment 127  conserve 119  corporate 87  courts 85
    records 84    advocacy 60      organizing 57  spending 56
    financial 29  people 27        osint 14

    trust tiers: record 251 · high 72 · medium 9 · low 5

---

## Round 25 — the release layer finally has a harvester

The map's headline feature has read near-empty since round 1. Fixed.

**The OGTR recommendation was wrong.** For several rounds these notes said to
start with OGTR, because it publishes field-trial site locations and nothing else
does. That was said without checking. `ogtr.gov.au` **disallows automated access
in robots.txt** — its records are still the best in the world to read by hand,
but they cannot be harvested, and recommending it repeatedly without verifying
was the same failure as the BCH portal two rounds ago.

**APHIS publishes exactly what was needed, and invites reuse.** Two CSVs,
updated every business day, public domain (CC0):

    https://www.aphis.usda.gov/sites/default/files/efile-data.csv      (current)
    https://www.aphis.usda.gov/sites/default/files/brs-public-apps.csv (legacy)

Schema verified by fetching and reading the file, not assumed: authorisation
number, type, movement type, organisation, organism, status, effective and
expiration dates, `Location(s)`, CBI flag, number of release locations, and
intended traits with two-letter prefix codes.

**`harvest/aphis_releases.py`.** Gates applied, each for a stated reason:

- keeps only records with a `Rel -` component — **import and interstate movement
  are not environmental releases**, and most rows in the file are one of those
- drops withdrawn, denied, superseded, expired, cancelled
- drops anything past its expiration date: a lapsed authorisation is not a live
  release
- sets `phase` explicitly from status, so the map's consent-phase filter
  distinguishes *issued/acknowledged* from *still under assessment* rather than
  guessing from a keyword
- sets `precise: false` on every record, because **APHIS publishes release states
  and never coordinates** — every dot is a state centroid and draws as a dashed
  ring, which is what that means
- rates `impact` from declared release locations and state span, and the code
  says in a comment that this sorts rather than quantifies
- says in the description when the applicant claimed CBI, rather than silently
  presenting a redacted trait list as complete

Tested offline against six real rows captured from the live file: it kept the
three genuine releases and correctly dropped an import-only record, a denied one
and a superseded one. Classification through the map's own `pjTypeCat`: cotton →
fibre crops, chestnut → trees, fruit fly → insects, bacteria → microbes.

`pjPhase()` in the map now honours an explicit `phase` field and falls back to
the old keyword inference for hand-written records.

**`harvest/projects_curated.json`** holds the five hand-written OGTR records, and
the harvester merges them in front of what it fetches — so `projects.json` can be
overwritten weekly without losing anything written by hand.

**New workflow** `.github/workflows/releases.yml`, weekly.

### A near miss

The `pjPhase` patch was first aimed at line 2489, which in the source is
`this._draw(); },` inside the canvas renderer. Caught by reading the target line
before building — the same check that saved the project popup two rounds ago.
Line-numbered edits against a file this size need the target read every time.

---

## Round 26 — two bugs the first live run exposed

The first real run reported `epermits 54903 rows → 0 live releases` and
`+ 0 curated`. Both were real defects, not data.

**The two APHIS files do not share a schema.** I assumed they did. Verified by
reading both headers:

    eFile:    Authorization Number / Organization / Organism / Location(s) /
              Number of Release Locations / Intended Trait(s) / Expiration Date
    ePermits: Permit Number / Institution / Article / Locations / Sites /
              Acres / Phenotypes / Expire Date

Every legacy row was therefore returning `None` for `Location(s)`, finding no
release states, and being dropped. Fixed with an explicit `LEGACY_MAP` and a
`get()` accessor.

The separators differ too: eFile writes `Rel - HI-PR`, ePermits writes
`Rel-IA,IL,IN`. The old regex would have taken only the first state from a
comma-separated legacy list. Both forms now parse.

**The legacy file has acreage; eFile does not.** `Acres` is a real measured
quantity and it is now carried into the size line — so legacy records read
"10 declared release locations across 4 states, 20 acres" while eFile records
can only give the location count. That asymmetry is worth knowing: the newer
system publishes *less* about scale than the one it replaced.

Tested against real legacy rows: 3 of 4 kept, with the withdrawn one and the
2022-expired one correctly dropped, and the four-state comma list parsed.

**Expect the legacy file to stay near zero, and that is correct.** ePermits
stopped accepting applications on 30 September 2022 and its permits expire on
their own terms. A closed system with expired permits *should* yield almost
nothing under a live-release gate. The bug was that it yielded nothing for the
wrong reason.

**`+ 0 curated` was a missing file, not a merge failure.**
`harvest/projects_curated.json` is new and had not been added to the repo. The
script now says so on stderr instead of printing a silent zero.

**Concentration is now computed and printed.** From the first live run: Bayer 70,
Syngenta 35, Pioneer 26 — **131 of 362 records, 36%, from three firms**, with
Bayer alone at 19%. That is the map's own principals layer confirmed from the
regulator's own file, and it is a stronger statement than any market-share figure
because it counts authorisations rather than revenue.

Also worth noting from that run: **333 consented against 29 under assessment.**
The window where objection is cheapest is a small fraction of what is on the map,
which is exactly why the consent-phase filter defaults to showing both.

---

## Round 27 — the first scheduled run, and what it caught

The harvest worked (`epermits 54903 → 20344`, so the schema fix landed) and the
**push failed**. Three defects, one of them serious.

**1. The workflows race each other.** Both commit to `main`. The wire runs every
six hours, releases weekly; when they overlap, the second push is rejected with
`fetch first`. Both now rebase onto whatever landed and retry three times.

**2. `epermits → 20344` was wrong, and the cause was a date format.**
`parse_date` had `%d-%b-%y` but not `%d-%b-%Y`. ePermits writes `01-May-2029` —
four-digit year. Every legacy expiry date therefore failed to parse, returned
`None`, and sailed through the `if exp and exp < today` gate as though it had no
expiry at all. Twenty thousand dead permits from a system closed since September
2022 were being treated as live releases.

Fixed by adding `%d-%b-%Y` **before** `%d-%b-%y`, and by parsing the whole
string rather than a fixed-width slice sized for the shorter format.

A second gate now backs it up: a legacy record with no expiry date is dropped,
because a closed system cannot be shown to have current authorisations. Belt and
braces, since the first bug was invisible for two rounds.

The earlier prediction that legacy would yield near-zero was right; the harvester
was wrong about it twice, in opposite directions, for two different reasons.

**3. The concentration figure was understated.** The run showed
"Pioneer Hi-Bred International" and "Pioneer Hi-Bred International, Inc." as
separate applicants, and Bayer split across "Bayer Crop Science" and "Bayer
Research and Development Services, LLC". Counting them apart dropped the top-3
share from 36% to 23% — the wrong direction. A `norm_org()` now merges corporate
groups (Monsanto → Bayer, Pioneer/Dow → Corteva) and strips legal suffixes, for
the **summary only**. Each record keeps the applicant name exactly as filed.

---

## Round 28 — the panel now matches the map, and Canada joins the layer

**The provenance panel was describing a map that no longer existed.** It still
said the layer "will read sparse or empty until projects.json is populated" and
laid out a manifest of registers as though several fed it. One does. Rewritten to
say what actually ships: **this layer is the United States only**, from the two
APHIS files, with every other register listed alongside the specific reason it is
absent — OGTR's robots.txt, the BCH being a JavaScript application, and the rest
having search forms rather than bulk files. It also now explains why every dot is
a dashed ring, why scale sorts rather than measures, and what a [CBI] redaction
in a description means.

**Canada added: `harvest/cfia_approvals.py`.** The CFIA "Plants with Novel
Traits" dataset on open.canada.ca, Open Government Licence, direct CSV endpoint,
schema verified by fetching and reading it.

Two things make it worth more than one more country:

- It carries the **OECD unique identifier**. That is the string this map keeps
  telling people to write down, because it links one engineered event to every
  other country that has ruled on it. No other feed here supplies it.
- Canada regulates by **novelty of trait, not by technique**, so the register
  lists transgenic events and products of mutagenesis and gene editing side by
  side, with an LMO column saying which is which. Everywhere else that second
  group is increasingly written out of registration entirely. This is the one
  harvestable register where it is still visible — which is a direct answer to
  the map's own largest stated gap.

Gates: only rows approved for unconfined release in Canada are kept. "Not grown
in Canada" means feed or food import clearance and never planting — the same
import-versus-release distinction the APHIS harvester enforces. Withdrawn, not
considered novel, and no-application rows are dropped. Tested against six real
rows: kept the three genuine approvals, dropped the import-only, the withdrawn
and the not-novel.

Every Canadian record sits at the national centroid and is marked imprecise,
because that register records a national approval rather than a planting
location. The dashed ring means the same thing it means for a US record: the
source did not give a place.

The weekly workflow now runs CFIA first, then APHIS, which merges the output.

---

## Round 29 — a finding from the first CFIA run

The first live run returned **165 rows → 128 approved for unconfined release; 101
transgenic, 27 products of mutagenesis or gene editing; 101 carrying an OECD
identifier.**

101 and 101 is either a coincidence or a fact about how the identifier system
works. Two changes so the run answers that instead of implying it:

**The identifier test now checks shape, not emptiness.** A real OECD unique
identifier is applicant code, event code, check digit — `MON-00179-5`, or
`BCS-GHØØ24-7` using the Ø the standard specifies for zero. The register also
puts free text and repeated product names in that column: one Non-LMO camelina
row carries `14CS0851-01-14`, which is the product name, not an identifier. The
old test counted it. The new one rejects it, and correctly pulls both identifiers
out of a stacked-event cell like `MS1: ACS-BN004-7; RF1: ACS-BN001-4`.

**The run now prints a cross-tab rather than two separate counts** — transgenic
against has-identifier, four cells — and states the conclusion only when the
off-diagonal cells are actually zero.

### Why it matters

The reasoning is definitional, not just observed: OECD unique identifiers are
assigned to **transgenic events**. An organism made by mutagenesis or gene
editing has no transgene to identify, so it never receives one.

Which means the map's own standing advice — write down the OECD identifier,
because it is the one string that follows an event through every country that has
ruled on it — **does not work for the class of organism growing fastest and being
deregulated hardest.** Canada is the one harvestable register still listing both
classes side by side, so it is the one place this is visible at all.

That is now in the provenance panel, next to the deregulation gap it compounds:
the class being written out of registration is the same class the international
tracking system was never built to follow.

---

## Round 30 — the cross-tab was measuring its own prose

The run printed:

    transgenic  with id 101   without   0
    non-LMO     with id  27   without   0

Every record counted as having an identifier, including the 27 that do not. The
test was `"OECD unique identifier" in r["desc"]` — and the description for a
record *without* one reads "**No** OECD unique identifier. Those are assigned to
transgenic events…". The phrase is in both messages. The table could only ever
return one answer.

Fixed by putting the facts on the record as fields — `oecd` (a list, possibly
empty) and `transgenic` (a boolean) — and cross-tabbing on those. Nothing infers
a fact from a sentence it wrote itself.

The `else` branch now also reports the disagreement rather than staying silent
when the correlation does not hold.

**And I had already put the unverified claim in the map.** Round 29 added to the
provenance panel that "every transgenic approval carries an identifier and not
one edited product does" — asserted from a table that could not have shown
otherwise. That sentence is gone.

What replaced it is what the source actually supports: the identifier system was
designed around transgenic events — applicant code, event code, check digit,
naming a specific insertion — and where there is no transgene there is nothing
for it to name. The Canadian register records no identifier for most of its
non-transgenic approvals. So the class being written out of registration is also
the class that system is least able to follow between jurisdictions.

That is the same argument, made at the strength the evidence carries.

---

## Round 31 — the measurement, once the table could disagree

With the cross-tab reading fields instead of its own prose:

    transgenic  with id  98   without   3
    non-LMO     with id   0   without  27

**The non-transgenic side is absolute.** Not one of the 27 approved products of
mutagenesis or gene editing carries an OECD unique identifier. That is now in the
provenance panel with the figures attached, alongside the point it compounds: an
organism can be both unregistered where it is grown and unnameable everywhere
else.

**The transgenic side has three exceptions, and guessing at them would repeat the
mistake.** A transgenic event with no identifier is either genuinely unassigned
or a formatting quirk in the published cell, and those mean different things. The
run now prints each one with its raw OECD cell so the difference is visible.

At least one is known to be formatting: the register writes soybean MON 94637's
identifier with spaces rather than hyphens, `MON 94637`, which the shape test
correctly declines to accept as an identifier — the standard's format is
applicant-event-checkdigit. Others carry a literal "Not assigned", which is a
real absence. The printout distinguishes them; the description does not
characterise them.

Note what the prediction did: it got the direction right and the number wrong. It
went into the map only after the table was capable of contradicting it, and the
sentence there now carries the exceptions rather than rounding them away.

---

## Round 32 — twenty more entries

**73 countries · 32 subnational regions · 24 international bodies · 356 entries ·
0 validation problems.**

Deepening across twenty existing countries rather than adding new ones. The
entries that do the most work:

- **Brazil — Ministério Público Federal.** In Brazil the effective challenges to
  GM approvals have come from federal prosecutors, not private litigants, and
  **anyone may file a representation asking them to open one, at no cost.** That
  is a route most people in Brazil do not know they have.
- **India — Plant Varieties and Farmers' Rights Authority.** India legislated a
  right most countries only debate: farmers may register their own varieties
  alongside breeders'. This is where it is actually exercised, not argued about.
- **South Korea — Rural Development Administration.** Korea systematically looks
  for escaped LMOs around ports, feed mills and transport routes, and publishes
  what it finds. Almost no other country runs post-release monitoring of that
  kind, which makes Korean data one of the few real answers to "what actually
  gets out".
- **Denmark — Retsinformation.** The statutory compensation scheme for GM
  contamination of a neighbouring crop, written into law rather than left to
  litigation. When someone asks what a remedy would even look like, this is the
  working example.
- **Thailand — Department of Agriculture.** Thailand restricts field trials
  through **plant quarantine law**, not biosafety law. Worth understanding
  because that mechanism is available in many countries that have no biosafety
  act at all.
- **Austria — AGES.** Systematic seed-lot testing is why Austria's GM-free
  position is enforceable rather than declaratory. The testing is the mechanism.
- **Norway — GenØk.** Independent biosafety research and the training material
  used by regulators elsewhere. Much of the working critique of risk-assessment
  practice worldwide comes from a handful of institutes; this is one.
- **China — Supreme People's Court judgments.** Unauthorised planting of
  unapproved GM crops has been prosecuted in China, and the judgments are public.
  Rarely examined outside the country.

One entry is deliberately flagged low-trust: the Indonesian biotechnology
information centre. Information centres of that kind are generally
industry-aligned, and it is included as a record rather than a voice because for
several Southeast Asian countries it is the only consolidated public account that
exists. The trust filters exclude it cleanly.

    projects 191  environment 142  conserve 128  courts 90  corporate 89
    records 86    advocacy 64      organizing 60  spending 60
    financial 29  people 28        osint 14

---

## Round 33 — twenty new countries

**93 countries · 32 subnational regions · 24 international bodies · 376 entries ·
0 validation problems.**

Egypt, Morocco, Tunisia, Senegal, Mali, Cameroon, Mozambique, Malawi, Zimbabwe,
Botswana, Namibia, Sri Lanka, Nepal, Cambodia, Myanmar, Jordan, Syria, Iraq,
Azerbaijan, Kazakhstan.

Taken from the CBD focal point list, using only entries where that list gives an
explicit institutional website — no domain inferred from an e-mail address, which
is the rule the whole country directory has been built under.

Several are here for what they demonstrate rather than what they publish:

- **Syria.** ICARDA's genebank was evacuated from Aleppo and became the first
  withdrawal ever made from the Svalbard vault. That is the clearest
  demonstration anywhere of why duplicated seed storage exists, and the map's
  seed-protection lens argues for it constantly.
- **Iraq and Jordan.** Both sit in the wheat and barley centre of origin, which
  is discussed far less than the maize one. Iraq's seed system was substantially
  reorganised under occupation — a documented case of seed law rewritten from
  outside.
- **Botswana.** Beef exports to the EU make its position on GM feed commercially
  consequential in a way its neighbours' is not.
- **Egypt.** The largest wheat importer in the world. What an importer of that
  size accepts sets the standard exporters have to meet — leverage importing
  states rarely use.
- **Nepal.** Seed supply depends heavily on Indian imports, so decisions made in
  Delhi are inherited. A common and under-examined situation.
- **Myanmar.** Recorded so the gap is visible rather than absent. A country with
  no functioning register is a different thing from a country not yet added, and
  the entry says which this is.

    projects 213  environment 146  conserve 137  corporate 95  courts 90
    records 86    advocacy 64      organizing 60  spending 60
    financial 29  people 28        osint 14

Roughly 95 countries still have no entry. The remaining ones are mostly small
island states and territories where the focal point list gives a ministry but no
website, which is precisely the case the no-guessing rule exists for.

---

## Round 34 — the defensive half

**93 countries · 32 subnational regions · 24 international bodies · 395 entries ·
0 validation problems.**

Nineteen entries, all seed banks, farmer seed networks and testing capacity. The
map has been strong on how to fight a permit and thin on the thing it repeatedly
tells people to do first: get clean seed somewhere safe. `conserve` went 137 →
168 and is now the second-largest lens.

The ones that carry an argument:

- **Ethiopia — Biodiversity Institute.** One of the oldest and largest genebanks
  in Africa, built before most countries had one, in a centre of origin for
  coffee, sorghum, teff and durum wheat. It is the working model everything in
  the seed lens argues for.
- **Peru — Parque de la Papa.** Six Quechua communities conserving over a
  thousand native potato varieties **in the field, governed by the communities
  themselves** rather than by an institution holding seed on their behalf. That
  is farmers' rights exercised rather than legislated, inside the potato's centre
  of origin.
- **Syria — ICARDA.** The Aleppo evacuation and the first withdrawal ever made
  from Svalbard. Every argument for duplicating a line in more than one place was
  tested here, in public, and the duplication worked.
- **Philippines — IRRI.** Rice accounted for roughly a third of all recorded GM
  contamination incidents despite no GM rice being commercially grown anywhere,
  and the global rice backup sits in Los Baños.
- **Nigeria — IITA.** Bt cowpea was approved in Nigeria; the world's cowpea
  diversity is held in the same country. That makes the contamination question
  immediate rather than theoretical.
- **France — Kokopelli.** Prosecuted for selling varieties not on the official
  catalogue, and took it to the European Court of Justice. Whether a seed may be
  sold at all if it is not registered is the quiet foundation under everything
  else on this map.
- **UK — Heritage Seed Library.** Varieties that can no longer legally be sold
  because registration lapsed, distributed to members instead. The clearest
  demonstration that seed law removes varieties from circulation quietly, without
  anyone deciding they were bad.

One entry is marked medium-trust and commentary for a structural reason:
**Brazil's Embrapa develops engineered crops and also runs the reference
laboratories used to detect them.** That is a fact about how the Brazilian system
is arranged, and the entry says so without making it an accusation about anyone
in it.

    projects 214  conserve 168  environment 156  corporate 96  courts 91
    records 86    organizing 66  advocacy 65     spending 60
    financial 29  people 28      osint 14

---

## Round 35 — a marker in the wrong hemisphere, and two fixes

**AfricanLII was pinned in Sydney.** Reported, and correct. The body was called
"Free legal information networks" and I placed it at AustLII's coordinates
because AustLII hosts the LII infrastructure — so the entry for African law sat
off the coast of New South Wales.

Split into two bodies: **AfricanLII in Cape Town**, where it is hosted, and
**WorldLII in Sydney**, where it genuinely is.

**Auditing the rest found five more of the same kind.** Every one was a body
named after a *network* or a *category* rather than a place, so the pin drifted
to whichever member came to mind:

    Strategic & public-interest litigation   London      → Eugene, Oregon (ELAW)
    Gene editing & synthetic biology firms   Cambridge MA → Washington DC (SEC)
    The four — agricultural biotech majors   Frankfurt   → Leverkusen (Bayer)
    Global farmer & food-sovereignty         Paris       → Barcelona (GRAIN)
    Independent GM testing                   Luxembourg  → Ispra (the EURL lab)

The rule now applied: **a body sits where its lead entry actually is.**

**A build-time pin audit enforces it.** Expected coordinates for the seven
corrected bodies, plus a check that no body has impossible coordinates or sits at
null island. The build fails rather than shipping a marker in the wrong
hemisphere again.

**New goal 11b: "Change the law through legislation."** Step 11 already existed
but was labelled "Go after the rule itself", which does not read as *change the
law*, and it only covered the litigation route. 11 is now explicitly the courts
route; 11b is the legislative one — bans, moratoria, labelling, seed rights.

Its hint gives the entry points in order of difficulty (municipal declaration →
regional moratorium → labelling or coexistence rule → national prohibition →
constitutional provision) and notes that almost every one began with people who
had no standing and no lawyer. It closes on what beat what: **Vermont's labelling
law survived industry litigation and was ended by Congress instead** — which
tells you where the fight moves once you start winning.

**Pill saturation reduced.** `#24548c` → `#3d5673`, borders `#3a6fae` →
`#567192`, applied across `.chip.on`, `.ps-pill.on`, `.pt-pill.on`,
`.best-pill.on` and `.skpill.on`.

21 intents, 21 selectable options, every one mapping both ways.

---

## Round 36 — resources grouped by goal, not by lens

**A unit's resource box now groups by intention**, in the same order the
"What are you trying to do?" menu runs. Previously it grouped by lens, which is a
taxonomy of *source types* — useful for filtering, wrong for reading. Open a
country now and it reads: find the record → read the assessment → locate the
site → request what was withheld → who owns it → the money → the officials →
past cases → change the law → find allies → secure seed.

Three decisions inside it:

- **The order is read off the menu at runtime**, not duplicated in a constant.
  Add or move a goal and the popups follow automatically; the two cannot diverge.
- **Entries repeat across goals.** A court database serves "find past cases" and
  "change the law through the courts". Filing it under one would hide it from the
  step where someone actually needs it, so it appears in both and each count is
  the count for that group.
- Anything matching no goal falls into **"Everything else here"** rather than
  vanishing.

Tested against real data: the US box produces 17 goal groups from 24 resources,
Brazil 13 from 10, Kenya 7 from 4.

### An escaping bug, caught by the validator

The first version emitted `\\'collapsed\\'` into a single-quoted JavaScript
string — a literal backslash that terminates the string early. `Unexpected
identifier 'collapsed'`. Rewritten to build the handler with `\u0027`, which the
parser resolves after the string closes and which cannot be mangled by escaping
levels. Third time a quoting error has reached the output; the syntax check has
caught every one.

### Seventeen more entries

Filling the goals that were thinnest now that the popup is organised by them —
FOI routes, land registries and integrity bodies. `records` 86 → 103,
`people` 28 → 34, `financial` 29 → 34.

- **South Africa's PAIA** reaches **private bodies** where the record is needed
  to exercise a right. That is rare in the world, and a company holding safety
  data it will not publish is exactly the case the provision was written for.
- **Chile's Consejo para la Transparencia** — the seed-multiplication site
  question was decided there, on transparency grounds, not in a biosafety forum.
- **New Zealand's LINZ Data Service** publishes national parcel geometry free and
  downloadable. Almost nowhere else can you map a drift radius without paying per
  title.
- **South Africa's deeds registry** entry says what it does *not* cover:
  communal land under traditional tenure, a large share of the country. Where
  tenure is communal the neighbour with standing is an institution, not a
  titleholder.
- **Brazil's sanctions list** — a two-minute check on whether an applicant is
  already barred from public contracting.

**93 countries · 25 international bodies · 412 entries · 0 validation problems.**

    projects 217  conserve 168  environment 156  records 103  courts 99
    corporate 97  organizing 66  advocacy 65     spending 61
    people 34     financial 34   osint 15

---

## Round 37 — pivot: industry-primary

The map is no longer a toolkit for opposing releases. It is a map of the
industry. The accountability material is gone rather than demoted.

**Twelve facets replace the twelve lenses:** Seed & Traits · Gene Editing &
Synthetic Biology · DNA Synthesis & Sequencing · Contract Research &
Manufacturing · Laboratory Animals · Livestock, Aquaculture & Pets · Insects,
Microbes & Open Release · De-extinction & Conservation Biotech · Human Clinical &
Therapeutic · Assisted Reproduction · Money & Backers · Rules, Records &
Advocacy. 51 sub-filters.

**Every entry now has a fixed three-part description** — WHAT the organisation
is and does, WHERE it sits in the chain, WHY it matters. The third part is the
argument, and it is written from the documented position rather than from
characterisation: market share, published terms, incident record, the structure
of the arrangement. Enforced at build time — a missing section fails validation.

**The goal menu became a navigation menu.** The map no longer tells anyone what
to do, so the options name parts of the industry rather than tasks. The angle
selector ("with your wallet / with media tactics / with your legal skills") is
deleted outright — it only made sense on a campaign map.

**The tour is rewritten**, 8 steps, running the chain backwards from the thing
you can see: the narrow top, the synthesis layer nobody maps, who actually does
the work, what it is done to, applied to people, what sets the pace, and the
machinery around it. The old worked example — seven steps of campaign advice —
is gone.

**Data rebuilt from scratch: 12 countries, 46 entries**, every facet populated.
The 412 accountability entries are not merged in; this is a different map.

Entries carrying the most: Bayer selling both the tolerant seed and the herbicide
it tolerates; Twist and IDT as the layer where capability is actually gated, by
company policy rather than statute; Addgene requiring an institutional account,
which is the real barrier between the public and this technology; Charles River
both breeding the animals and running the studies performed on them; Jackson
Laboratory's catalogue as a product list where every entry is a lineage bred to
be ill; ViaGen cloning pets with no biosafety framework engaged at any point;
Oxitec's self-limiting claim tested by the Jacobina genotyping; Colossal
reframing extinction as reversible on behalf of a company that would own the
result; Casgevy curing a disease most prevalent in Africa at $2.2m a patient;
Orchid selling polygenic embryo scores that the underlying statistics cannot
support.

### Process note

Four panel rewrites were attempted in one script; the last anchor failed and
Python discarded all four, because the file write comes at the end. Split into
four scripts, each writing independently. That is the third time an aborted
multi-edit script has silently reverted good work in this project.
