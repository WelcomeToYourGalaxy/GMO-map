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

---

## Round 38

- Title back to **Live Global Genetic Frontlines Map**.
- The "What this is" material moved out of the help panel and into the **Global
  Wire** intro, which now opens the map and names all twelve facets in prose.
- The help panel now begins at "Every entry says the same three things".
  Deleted: "argued from the documented position rather than asserted", the
  Trust-and-voice sentence, the "What this map does not do" paragraph.
  "Clicking empty ocean" replaced with clicking the first name in the place row.
- **The tour is removed** — button and content. The walkthrough text was
  delivered in the reply instead.
- **Facility dots removed** (`SETS=[]`). Town halls, courthouses and government
  offices are civic buildings, not industry sites. The layer, its filters and
  its legend remain in the engine, so a facility set can be restored later if a
  genuinely industrial one is built.
- **Lens pills recoloured** to the same light blue as the source-type pills
  (`#7fa8cc` on `#9dc0dd`, dark text), and the index Expand-all / Collapse-all
  controls matched to it.
- **Release layer untouched.** All 14 source families survive the pivot,
  including the `contamination` family for escapes and unauthorised releases,
  plus 19 organism types and 5 overlays. Both harvesters unchanged.

### Wire coverage: 30 feeds to 79

Almost every region read zero because the feed list was 30 mostly-English
sources. Now 79, across **20 query languages** — Arabic, Chinese (simplified and
traditional), Dutch, English, French, German, Hindi, Indonesian, Italian,
Japanese, Korean, Polish, Portuguese, Romanian, Russian, Spanish, Swedish, Thai,
Turkish, Vietnamese — targeting **37 countries** directly.

Structure: publisher feeds, then topic queries in English, then one region-
targeted query per major territory, then non-English queries per language market.
Regional Mongabay editions added for Latin America, Brazil, India and francophone
Africa.

The harvester now reads the language from the feed URL's `hl=` parameter rather
than the feed's `<language>` element, which Google News endpoints do not reliably
set — so the language filter will populate properly for the first time.

---

## Round 39 — overlays expanded to eight

GMO-free zones, protected areas and genebanks kept rather than dropped, and
reframed for an industry map rather than removed from it:

- **GMO-free zones** are the negative space — the places the industry has been
  kept out of, and therefore a direct measure of where its expansion met a limit.
- **Protected areas** are the receiving environment: what sits next to a trial
  site, and what a gene-flow question is actually about.
- **Genebanks** are the industry's raw material. Commercial breeding starts from
  landraces and wild relatives held in trust by public institutions, which is the
  least-discussed subsidy the industry receives.

Three added: **field trial density**, **regulatory regime by country**, and
**seed & breeding infrastructure**. Eight total, all colours distinct.

`overlays/README.md` rewritten with a source and a build route for each, ordered
by how easily each can be built. Two notes worth carrying:

- **Field trial density is buildable today** from `projects.json` alone —
  aggregate by state, emit one polygon per unit. No external source, and it
  refreshes whenever the harvester runs.
- **Regulatory regime is the highest-value one to build.** It classifies each
  country by how it decides what counts as a regulated organism, and it is the
  layer that explains why an empty area on this map can mean deregulation rather
  than absence.

---

## Round 40

**Facilities section removed from the key box.** The toggle, the hint and the
type filters are gone; `#facFilter` stays hidden in the DOM so the layer can be
restored if an industrial facility set is ever built.

**All toggled pills on one light blue.** `.chip.on`, `.skpill.on`, `.ps-pill.on`,
`.pt-pill.on`, `.best-pill.on` and `.wire-tab.on` were drifting apart again after
each edit, so the recolour is now a blanket swap applied after the rule list
rather than a per-rule entry. Zero dark-blue pills remain.

**Two overlays built from real geometry** — `harvest/build_overlays.py`.

`trials.geojson` aggregates `projects.json` by state and draws the counts on the
actual US state polygons already embedded in `index.html` as `SUBGEO`. No
external source, and it regenerates whenever the release harvester runs. It
currently shows one state, because `projects.json` holds only the five curated
records; run the APHIS harvester and it fills.

`regime.geojson` classifies each country by how it decides what counts as a
regulated organism — technique-based, trait-based, or a carve-out that moves a
class outside registration entirely — dissolved from the same embedded admin-1
geometry into one shape per country. 36 of 71 classified countries have geometry
in `SUBGEO`; the other 35 are named in the run output rather than approximated,
and an unshaded country means "not classified here", never "no rules".

The other six overlays need geometry this repo does not hold. The generator says
so and does not invent them.

**Industry entries: 46 → 71**, 13 countries, every facet populated, zero
validation problems.

    seed 30  editing 18  synthesis 18  money 14  rules 13  animals 13
    clinical 12  cro 11  repro 9  livestock 8  wild 8  deextinct 4

Entries carrying an argument this round: Bayer's FieldView, where the agronomic
recommendation comes from the company selling the inputs; Benson Hill as the
pattern rather than the company — independent trait developers exit into one of
four buyers, so consolidation is the funding model's assumed endpoint; the Broad
Institute converting publicly funded research into an exclusive agricultural
licence; Thermo Fisher with visibility across the whole field that no regulator
has; GenScript, where an order placed in one country, made in another and used in
a third is overseen by none; Genus editing at breeding-stock level so a trait
propagates through national herds without any farmer deciding; AquaGen, where
farmed salmon genetics reach wild populations with no engineered organism
involved at all; Agragene as a warning about reading concentration off a permit
count; Cooper Surgical, where one faulty media batch reaches embryos in hundreds
of clinics at once; bluebird bio withdrawing an approved cure from a continent
over price.

---

## Round 41 — the retry was retrying the wrong thing

The push race fix from round 27 worked as designed and still failed:

    push rejected (attempt 1) - rebasing onto origin/main
    CONFLICT (content): Merge conflict in wire.json
    error: could not apply d58c6e4... wire: refresh

**Rebasing a wholesale-generated file can only ever conflict.** `wire.json` is
rewritten end to end on every run, so when two runs finish close together git has
two complete rewrites of the same file and no basis for merging them. The retry
loop was correct about *when* to act and wrong about *what to do*.

Both workflows now do this instead: on a rejected push, `fetch` and
`reset --hard origin/main`, then **re-run the harvester against the remote's
version** and commit fresh. Nothing is lost, because the harvesters already
merge with whatever is on disk — the wire keeps a 120-day archive and dedupes on
link, and the release harvester merges the curated file in front. Three attempts.

**And a `concurrency: group: commit-main` on both**, so they queue behind each
other instead of racing. That removes most conflicts before they can happen; the
reset-and-re-harvest loop is the backstop for the rest.

The releases workflow now also runs `build_overlays.py` and commits
`overlays/trials.geojson`, so the trial-density layer refreshes with the data it
is built from rather than going stale the moment the release layer updates.

### Unrelated warning in the same log

    Node.js 20 is deprecated ... actions/checkout@v4, actions/setup-python@v5
    are being forced to run on Node.js 24

Informational. Both actions still work; the runner is substituting a newer Node.
Worth bumping the action versions eventually, but nothing is broken and I have
not verified which major versions are current, so I have not guessed at them.

---

## Round 42

**Release dots lightened.** The scale ramp sat at 15–19% lightness, which is
close to invisible against a dark basemap. Same hue progression — cool for the
smallest work through to warm for the largest — at 57–62% lightness:

    5 largest  #e0724a      4  #c07aa8      3  #d4c15e
    2          #8fc46a      1 smallest  #5cc6bd

**Industry entries: 71 → 90**, 13 → 20 countries. New: India, Argentina, Israel,
Singapore, Denmark, plus deeper China, Japan, Brazil, Germany, Australia, Canada.

The ones carrying an argument:

- **Sanatech Seed (Japan)** — the GABA tomato, the first gene-edited food sold at
  retail through a *notification* route rather than an approval, including free
  seedlings to home gardeners. A carve-out's working demonstration: a product in
  domestic gardens with no risk assessment on file anywhere.
- **Regional Fish Institute (Japan)** — gene-edited sea bream and puffer sold as
  food, through the same route. AquAdvantage salmon took two decades to approve
  in the United States; these reached plates without that fight, because the
  technique used placed them outside the scheme. Same category of product,
  opposite outcome, decided by how the change was made rather than what it does.
- **Novonesis (Denmark)** — enzymes from engineered microbes used in the
  production of a very large share of processed food. Processing aids are
  generally unlabelled because the enzyme does not remain in the product, so the
  largest everyday contact between the public and engineered organisms happens
  invisibly by regulatory design, and almost nobody in the GM debate argues about
  it.
- **Mahyco (India)** — the Bt cotton licence and the royalty dispute that
  followed it through price controls, litigation and legislation. The clearest
  case anywhere of a trait fee meeting a smallholder economy.
- **Syngenta Group China** — industrial policy, regulatory approval and
  commercial gain inside one state structure. A different arrangement from
  anywhere else on this map, rarely examined in those terms.
- **Bioceres (Argentina)** — HB4 wheat, approved first in an exporting country
  and then in the countries that buy from it. How one national approval becomes a
  fact importers must accommodate.
- **Singapore Food Agency** — first to approve cultivated meat, because an
  import-dependent state has no domestic farm lobby to satisfy.

**20 countries · 90 entries · 0 validation problems.**

    seed 38  editing 31  rules 26  money 18  synthesis 18  clinical 16
    cro 15   animals 13  livestock 12  repro 9  wild 8  deextinct 4

---

## Round 43 — the thin facets

**21 countries · 108 entries · 0 validation problems.** Eighteen added, weighted
entirely to the four weakest facets: **deextinct 4 → 12, wild 8 → 16, repro
9 → 18, livestock 12 → 19.** No facet is now below 12.

    seed 41  editing 33  rules 28  money 24  livestock 19  synthesis 18
    repro 18  clinical 17  wild 16  cro 15  animals 13  deextinct 12

Four entries do work the map could not do before:

**San Diego Zoo's Frozen Zoo.** The largest wildlife cell bank in the world,
sampled since the 1970s for research, and now the material basis for every
cloning and genetic-rescue project involving a vertebrate. An institutional
archive that quietly became a supply chain for a commercial field that did not
exist when the sampling started, with no framework governing who may use it for
what.

**GloFish.** The first engineered animal sold to the public anywhere, in pet
shops since 2003, and still the most numerous by units. Millions of engineered
vertebrates have sat in domestic aquariums for two decades, bought as decoration,
with escapes into Brazilian streams documented. The quietest large-scale release
of engineered animals that has ever happened, and it happened through pet shops.

**Novonesis was last round's version of this; the World Mosquito Program is this
round's hardest case.** Wolbachia mosquitoes released at city scale across more
than a dozen countries, with randomised-trial evidence of reduced dengue. It is
the strongest counter-case to any blanket position against open release, and the
entry says so — while keeping the governance question about a modification
designed to persist indefinitely, which stays open regardless of the outcome. A
map that cannot accommodate this is not describing the field accurately.

**The American Chestnut Foundation.** Engineering proposed for deliberate,
permanent release into wild forest by a conservation charity, with no recall
mechanism by design — and then withdrawn when the line's problems emerged and the
sponsoring organisation reversed its own position. That is what independent
scrutiny working looks like, and it is rarer than either side of this argument
usually admits.

Two structural observations that came out of writing this batch, now in the
entries themselves: reproductive technology was normalised on cattle at volumes
dwarfing the human sector long before the human debate started (Trans Ova), and
agricultural biologicals are following the seed sector's consolidation curve a
generation later, visibly enough to name now rather than after it completes.

---

## Round 44 — industry entities become map points

**Organisations are no longer resource-list entries. They are markers.** Click
one and its own description opens: what it is, where it sits in the chain, why it
matters. There is no per-country resources box — `trackerdata.json` ships as
`{}`, so nothing opens on a country click.

`harvest/build_industry_points.py` converts all 108 entries to points. Every
coordinate is the organisation's headquarters or principal site at **city
level**, and every record is `precise:false`, because a corporate headquarters is
not where the work happens and the dashed ring means exactly that. Coordinates
live in one `PLACES` table so a wrong pin is a one-line fix.

**Escapes are now on the map — past as well as present.** Fifteen documented
incidents in `harvest/escape_records.json`, hand-compiled, because the GM
Contamination Register logged 396 incidents across 63 countries between 1997 and
2013 and then stopped, and nothing replaced it. There is no feed to harvest.

The record includes the ones this map has been describing in prose without
placing: **GloFish established in Atlantic Forest streams in Minas Gerais** — the
pet trade as a release pathway, no application, no assessment, no monitoring;
Oregon creeping bentgrass, where 62 of 585 plants tested were still resistant
three years into mitigation; transgenes in Oaxacan maize landraces; the Jacobina
mosquito introgression; StarLink; LLRICE 601; Triffid flax found in exports eight
years after deregistration; Bt10, where a company could not tell its own lines
apart for four years; feral canola in North Dakota carrying stacked traits nobody
bred; GM petunias sold worldwide for years and found by accident; Roundup Ready
wheat volunteering in Oregon with the cause never established.

Each entry says the same three things as every other point, and each carries the
same caveat: it was found and reported, which is a different thing from every
incident that happened.

**27 source families now**, twelve industry facets plus escapes plus the release
registers, so the key box's source filter separates all three kinds of point.

**128 points total**: 108 industry, 15 escapes, 5 curated releases. All 128 map
to a valid source family and a valid organism type; zero unmapped.

    industry_seed 15   industry_editing 15   escape 15   industry_livestock 11
    industry_repro 11  industry_synthesis 9  industry_wild 9  industry_rules 8
    industry_deextinct 7  industry_animals 6  industry_clinical 6
    industry_money 6   ogtr 5   industry_cro 5

### A near miss

Appending the new families to `PJ_SRC` dropped the closing brace on the last
original entry, and the emitted line then had a duplicated terminator. Caught by
the build failing rather than by producing something subtly wrong. Separately, a
line-numbered edit aimed at the trackerdata loader would have overwritten
`LENSLABEL`; reading the target line first caught it, as it has every time.

---

## Round 45 — a plain-language introduction on the wire

The wire panel now opens with an introduction to the subject before it describes
the map. Written for someone who knows nothing about this, at the reading level
of a curious child, and carried by figures rather than adjectives.

The sequence: what an engineered seed is · plants do not stay put · three escape
cases with numbers (Oregon 62 of 100 plants three years into a cleanup, North
Dakota over 75% of roadside canola with some carrying two traits nobody bred,
Mexican wild cotton going from 0% to 60% in ten years) · what changed in those
plants, found seventeen years after the crop went on sale by researchers asking
something else.

Then three additions requested for this round:

**The organisms get no say.** A seed does not choose to exist, or where, or when.
Everything else alive arrives through parents and a place that shaped its kind
over a very long time; these arrive because a company decided which trait would
sell. It is a short paragraph and it is the only part of the map that speaks for
the organism rather than about it.

**Who decided, and what they chose to build.** Four companies. 94% of engineered
area in three crops, 81% in three countries, three firms holding 36% of live US
release authorisations and one holding 19% alone. Almost all of it is weedkiller
tolerance and built-in insecticide — both sell chemicals, both come with a patent
that ends seed saving. The same sale earns twice.

**Population growth is not being addressed, so the "feeds the world" defence does
not hold.** By 2035 about 40% of cereals will be eaten by people, roughly a third
goes to livestock, the rest to fuel and industry. Only about 7% of soy is eaten
by people; cotton is not food. 645 million faced hunger in 2025 and 2.7 billion
could not afford a healthy diet — a problem of prices, wars and roads, not of
grain existing. Demand is treated as a given to sell into rather than a thing
anyone is addressing, which means the benefits only read as benefits if today's
farming is accepted as the floor. Widen the frame and the ledger reads
differently. **Until the companies steering it change direction, the honest
baseline is the damage, not the yield.**

It closes on the line the whole map rests on: the strongest objection is not that
a gene is dangerous, but that the decision cannot be taken back.

763 words, with a rule separating the argument from the description of the map
beneath it.

### A note on the figures

Everything quoted has a source in the document it came from, with one exception
flagged there and repeated here: the 94% / 81% concentration figures are a
second-hand citation and were marked "verify against ISAAA/industry figures
before publishing". They are in the panel because they are the standard figures
in this argument, but they are the two most worth checking before this goes
anywhere public.

---

## Round 46 — the two guides, linked from the map

Both PDFs are in `guides/` and linked as buttons at the foot of the wire panel's
argument, immediately before the rule that separates the argument from the
description of the map. That is the natural place: someone who has just read why
this matters is at the point of asking what to do.

    guides/how-to-stop-a-release.pdf        28 pages
    guides/how-to-change-the-industry.pdf   26 pages

Each button carries a title and a short description of what is inside, so the
choice between them is obvious without opening either: **guide 1 is one
application**, guide 2 is **the rules rather than the permit**.

The descriptions are written from what the guides show rather than from a
summary of them — the five steps that run at once rather than in order, where the
tilt shows in a permit file, the four permit stages and the deadline on each, how
far capture reaches and what sits outside it, and the question underneath
everything: whether the thing is legally a GMO at all, because redrawing that
definition closes every door above it at once.

**A note on those descriptions.** The PDFs' text streams would not extract here,
so I wrote the button copy from the figures visible in the conversation and from
what you said each guide covers, not from reading the full documents. If either
description misstates what is in a guide, that is why, and it is a two-line fix.

The buttons are styled to match the light-blue pill palette rather than
introducing a new accent.

---

## Round 47

**152 points: 127 industry, 20 escapes, 5 curated releases.** Zero unmapped.

    industry_seed 21   escape 20   industry_editing 15   industry_rules 12
    industry_livestock 11  industry_repro 11  industry_synthesis 10
    industry_wild 9    industry_deextinct 9  industry_cro 8
    industry_animals 8 industry_clinical 7   industry_money 6   ogtr 5

**Nineteen industry entries**, opening seven new countries: Mexico, South Africa,
Nigeria, Kenya, Italy, Poland, Thailand.

The theme running through most of them is the **demand side**, which the map had
barely touched. Engineered crops are overwhelmingly not eaten by people — they
become animal feed — so the companies deciding what goes into feed determine most
of the actual demand for engineered traits, and they are almost entirely absent
from public argument, which stays fixed on the supermarket shelf. Charoen
Pokphand, Nutreco, JBS and Grupo Bimbo are here for that reason. A buyer
specification does more to shape what gets planted than most approval decisions
do, and none of it is public.

Two others worth naming:

- **WuXi AppTec.** Western legislative attempts to restrict reliance on it made
  the dependency explicit: much of the drug pipeline of the countries that
  regulate this industry is developed and made by a company those countries do
  not regulate. The contract layer is where national oversight quietly stops.
- **Dabeinong.** China's approvals since 2023 have created a fifth centre of
  trait ownership outside the four Western majors, state-supported and deployed
  by state decision. The standard account of this industry as four Western firms
  is going out of date.
- **UK Home Office animal statistics.** A large share of licensed procedures are
  for *breeding and maintaining* genetically altered lines rather than for
  experiments — animals created and killed to sustain a line. That distinction
  appears in these statistics and almost nowhere else, and it is the clearest
  available measure of what the model-organism trade costs.

**Five more escape records, 15 → 20.** Chosen because each one shows a different
failure mode rather than another instance of the same:

- **Gujarat 2001** — Bt cotton growing before India had approved any GM crop, and
  approved the following year. Approval followed adoption. Once a trait is in the
  ground at scale, the decision becomes whether to criminalise existing farmers,
  which is not what the framework was built to decide.
- **Japanese ports** — feral canola along the haulage routes between ports and
  crushing plants, in a country that grows none. Every plant arrived by falling
  off a truck. Assessment concerns what happens around a field; it has nothing to
  say about spillage in transit.
- **Petunias, second wave** — further engineered varieties found on sale four
  years after a worldwide recall that was treated as complete. Vegetatively
  propagated lines traded informally between breeders persist in a system nobody
  monitors.
- **Australian certified seed** — engineered traces inside the certification
  system itself. Coexistence policy assumes a grower can choose; that depends on
  certified seed being what the label says, and tolerances are a percentage, not
  zero.
- **Wheat, third find** — Washington and Montana, years after Oregon, cause
  established in none of the three. Whatever is moving this material has operated
  for over a decade since the programme that created it shut down.

---

## Round 48

**The guides moved out of the wire and into their own pull-down panel**, sitting
at the top of the right rail directly above the lens box. Click the header to
open or close it; the caret rotates. They were at the foot of the wire argument,
which meant scrolling past 763 words to find them.

**169 points: 144 industry, 20 escapes, 5 curated.** Zero unmapped.

    industry_seed 22   escape 20   industry_editing 17   industry_rules 16
    industry_livestock 13  industry_repro 13  industry_synthesis 10
    industry_cro 10    industry_animals 10  industry_deextinct 10
    industry_wild 9    industry_clinical 7  industry_money 7   ogtr 5

**Seventeen entries, ten new countries**: Russia, Turkey, Ukraine, Indonesia,
Viet Nam, Colombia, Sweden, Finland, Ireland, UAE.

Several of them exist to complicate the map's own argument rather than reinforce
it, which is the point:

- **Turkey** permits GM feed imports under an approved-event list while
  prohibiting cultivation with criminal penalties. That is what most cultivation
  bans actually amount to — the ban is real, the exposure continues, and the gap
  between those two facts is where most public argument about bans goes wrong.
- **Russia** banned cultivation in 2016 and kept funding the research. Not a
  contradiction: a state deciding it wants the capability without the imports.
- **Colombia** — the thing that produced nationwide strikes was **seed
  certification law**, not biosafety law. Worth marking, because seed law is
  where most of this industry's control actually sits and it almost never gets
  the attention.
- **New Zealand's Predator Free 2050** has a strong case for genetic predator
  control, a capable research base, and still has not authorised it — partly
  because Māori consultation raised questions about who decides for a species
  that the programme could not answer. A country taking the consent question
  seriously enough to slow itself down.
- **Sweden's SLU** advocates treating edited crops as conventional on the grounds
  that the alternative locks small public breeders out. That is a real argument
  and it is also the argument the largest companies benefit from most. The entry
  holds both halves.
- **Solar Foods** makes protein from carbon dioxide, hydrogen and electricity. If
  that works at scale, the land argument underpinning most defences of engineered
  agriculture weakens — while concentrating food production into industrial
  facilities owned by whoever built them, which is a different distribution of
  control from farming, not obviously a better one.
- **Gulf sovereign wealth** has no exit deadline and no electorate where it
  invests. A materially different kind of money entering this industry, growing
  while the venture cycle contracts.

Also **Cyagen**, where a researcher commissions an animal that does not yet exist
to a written specification and it arrives as a product with a lead time; and the
**National Primate Research Centers**, where chronic supply scarcity is what makes
the international trade lucrative and the smuggling prosecutions predictable.

---

## Round 49 — one file to upload

Adding entries was touching five files a session. It now touches one.

**All 169 hand-built points are embedded in `index.html`** as `PJ_SEED` —
industry organisations and the entire escape record. They are written by hand
rather than harvested, so they belong in the file rather than in a data file a
workflow overwrites.

**The loader merges instead of replacing.** It still fetches `projects.json` for
whatever the harvesters produced, and unions it into the embedded set keyed on
`url + name`, so a record cannot appear twice. Three consequences worth having:

- Adding entries changes `index.html` and nothing else.
- The map works with no fetch at all — open the file from disk, or embed it
  anywhere, and every point is still there. That was the original design
  principle for these builds and it had quietly stopped being true.
- A failed fetch degrades to "the embedded set only" rather than to a seed stub.
  The old fallback was an empty array.

**`projects.json` is now machine-maintained only**, holding harvested releases
plus the five curated records. `aphis_releases.py` no longer merges the industry
and escape files into it, which would have produced every point twice.

Verified by running the page's own merge against both files: 169 embedded plus 5
fetched gives 169 merged, zero duplicates, zero unmapped source families.

`index.html` grew from 2.28 MB to 2.33 MB. Given it already carries an embedded
world plate and the subnational geometry, 50 KB for the entire dataset is a good
trade for never having to think about which files are in sync.

---

## Round 50 — three marker shapes, and sixteen more entries

**The three kinds of point now look different.** They shared one layer and one
shape, so an organisation and a release authorisation read identically.

    Square    an organisation, at its headquarters or principal site
    Diamond   a documented escape, where the material was found
    Circle    a release authorisation from an official register

Shape carries this rather than colour, because colour is already carrying rated
scale and there was no second channel to spend. Filled means a real coordinate;
outlined and faint means the source published none. A corporate headquarters is
always outlined, because it is not where the work happens.

The legend section is rewritten to match, and now says what each shape means
before explaining the fill.

**185 embedded points: 160 industry, 20 escapes, 5 curated.** Zero problems.

    industry_rules 26  industry_seed 24  escape 20  industry_editing 18
    industry_synthesis 13  industry_livestock 13  industry_repro 13
    industry_cro 10  industry_animals 10  industry_deextinct 10
    industry_wild 9  industry_clinical 7  industry_money 7  ogtr 5

**Sixteen entries, twelve new countries**: Pakistan, Bangladesh, Ethiopia, Ghana,
Uruguay, Paraguay, Chile, Spain, Portugal, Romania, Egypt, plus more Canada.

Several of these say something the map could not say before:

- **Chile grows engineered crops that Chileans may not plant.** It is the
  counter-season multiplication hub for the northern hemisphere seed industry,
  and the site locations were withheld as commercial confidence until the
  transparency council ordered otherwise.
- **Paraguay is the third case of adoption preceding approval**, after India and
  Brazil. In each, the regulator's eventual decision was whether to legalise what
  was already in the ground. That is a ratification rather than an assessment,
  and it is how a large share of the world's engineered crop area arrived.
- **Ethiopia wrote one of the strictest biosafety laws in the world** — strict
  liability, criminal penalties — and then amended it. The strict law was
  achievable, and it was reversed through the same channels that write the loose
  ones.
- **Ghana's approval and its ten-year prison term for infringing breeders' rights
  arrived through the same legislative period, from the same advisory sources.**
  Approval and seed criminalisation are usually discussed separately; there they
  are one process.
- **Uruguay traces every individual cow from birth to slaughter.** A country that
  can do that cannot claim seed traceability is technically impossible. The
  capability exists; it is not applied to seed.
- **Portugal publishes its GM planting register parcel by parcel; Spain does
  not** — two neighbours under the same EU framework, so the difference is a
  national choice rather than a legal constraint.
- **Bio-Rad** makes the detection instruments, and the entry names why they do
  not help: event-specific tests exist for approved transgenic events and
  generally not for gene-edited organisms, because there is no inserted sequence
  to target. The instruments are capable; the reference material is missing, and
  that is a consequence of deregulation rather than of chemistry.
- **Aldevron and IDT sit inside the same conglomerate**, which is invisible from
  either name. Two of the largest suppliers of genetic raw materials, one
  corporate decision-maker, no biosafety authority above it.

`index.html` is 2.35 MB and remains the only file this round changed.

---

## Round 51

**205 embedded points: 180 industry, 20 escapes, 5 curated.** Zero problems, no
duplicates, every description carrying all three sections.

    industry_rules 31  industry_seed 24  escape 20  industry_editing 18
    industry_synthesis 14  industry_repro 14  industry_livestock 13
    industry_cro 12  industry_wild 12  industry_animals 11
    industry_clinical 11  industry_deextinct 10  industry_money 10  ogtr 5

Twenty entries, weighted to the facets that were thinnest: **clinical 7 → 11,
money 7 → 10, wild 9 → 12, cro 10 → 12.** New countries: Malaysia, Peru, Austria,
Czechia.

The entries carrying an argument:

- **Intellia.** In-vivo CRISPR — edited inside the patient rather than in cells
  removed and returned. An in-vivo edit cannot be recalled from a body any more
  than a released organism can be recalled from a field. It is somatic, so not
  inherited, but the irreversibility argument this map makes about the
  environment applies to a person, and it applies first to the people in early
  trials.
- **Roche / Genentech.** Genentech made the first recombinant human insulin,
  which is where medical and agricultural biotechnology parted company in the
  public mind. The same technique applied to a drug became uncontroversial;
  applied to a crop it did not. That divergence is about who benefits and who was
  asked, not about the science.
- **Flagship Pioneering** creates companies rather than funding them. When a fund
  originates the company, the commercial thesis precedes the science instead of
  following it — which is the clearest available answer to why this industry
  builds what it builds.
- **Leaps by Bayer** holds positions in agriculture, gene therapy *and*
  reproductive health. The facets on this map are more joined up at the ownership
  level than anywhere else, and almost no account of agricultural biotechnology
  connects a seed company to a fertility clinic.
- **Verily's Debug programme.** Automated mass rearing turns releasing tens of
  millions of insects into an engineering problem rather than a biological one.
  The constraint stops being capacity and becomes only permission, which puts far
  more weight on the permission than the systems granting it were built for.
- **Greenlight.** RNA pesticides fall outside GMO frameworks because nothing
  living is modified, and outside conventional pesticide assumptions because the
  mechanism is sequence-specific. The product is on the market while the category
  is still being argued about.
- **Genomics England.** Participants consented to research; the commercial access
  arrangements were designed afterwards. Newborn sequencing raises this map's
  recurring question in another form — a person whose genome is read before they
  can be asked.
- **China's NHC.** The only jurisdiction where the germline prohibition arrived
  through prosecution rather than anticipatory legislation. A different kind of
  deterrent resting on a different kind of authority.
- **Czechia.** Farmers abandoned Bt maize because buyers would not pay for it,
  not because it was prohibited. The market door working with no regulator
  involved at all.
- **Peru.** A moratorium framed around protecting native agrobiodiversity rather
  than safety, extended twice, now running to 2035. The centre-of-origin argument
  carried into law and held there for over a decade.

`index.html` at 2.37 MB, and again the only file this round changed.

---

## Round 52

**223 embedded points: 198 industry, 20 escapes, 5 curated**, across 175 distinct
places. Zero problems, no duplicates, no impossible coordinates.

    rules 41  seed 28  escape 20  editing 18  synthesis 14  repro 14
    livestock 13  cro 12  animals 12  wild 12  deextinct 12
    clinical 11  money 11  ogtr 5

Eighteen entries, seventeen new countries: Cuba, Bolivia, Ecuador, Costa Rica,
Tanzania, Zambia, Greece, Hungary, Morocco, Taiwan, Saudi Arabia, plus additions
to the Philippines, Norway, China, Germany, the UK and the US.

This batch is mostly about **what states have actually tried**, which the map was
thin on:

- **Cuba** is the clean test of whether the objection is to the technology or to
  who owns it. A fully state-owned sector: no patent holder, no royalty, no seed
  contract, no shareholder. The consent, containment and irreversibility
  questions survive intact; the ownership ones vanish. Being able to see that
  separation is worth an entry on its own.
- **Bolivia** has constitutional protection for native seed, a rights-of-nature
  statute, and roughly a million hectares of engineered soy. The widest gap on
  this map between what a country's law says and what is in its fields.
- **Ecuador** wrote the prohibition into its constitution in 2008. Enforcement
  has been contested and imports continue. A constitutional clause is harder to
  remove than a decree and no easier to enforce — the practical lesson for anyone
  pursuing that route.
- **Costa Rica** — a majority of cantons declared themselves GM-free through
  municipal votes while national authorisations continued. Subnational refusal
  accumulating into a de facto national position with no national law changing.
- **Tanzania** adopted strict liability, and industry bodies campaigned against
  it explicitly as a barrier to investment. That is a clear statement of how much
  the *absence* of a liability rule is worth to them everywhere else.
- **Greece** is one of nineteen EU states and regions that opted out
  territory-wide. A mechanism designed to enable cultivation by letting objectors
  step aside produced near-continental exclusion instead.
- **Norway's Gene Technology Act** requires sustainability, societal benefit and
  ethics to be weighed alongside safety — the only major framework that puts them
  in the statute. Australia's regulator is barred from considering benefit at
  all. How much a regulator may think about is a drafting decision.
- **Golden Rice** is the strongest case the industry has: genuinely
  public-interest, over two decades to reach a field, then lost its permits on
  monitoring grounds rather than on safety. Both things are true at once, and the
  entry says so.
- **China National Seed Group.** One state holding company owns both a global
  agrochemical major and China's domestic seed champion. No competition authority
  anywhere has jurisdiction over the combination.

### Two process notes

An editing slip left a stray `"url" and` expression inside the Norway entry,
which would have silently discarded the description string. Caught by importing
the module and asserting all three description sections before use, rather than
by the build.

The PLACES extension regex failed against escaped unicode in the anchor, so
eighteen entries built with no coordinates and the script listed them. Fixed by
locating the closing brace by line number and inserting there. The script naming
its own misses is what made that a thirty-second fix.

---

## Round 53 — the three kinds finally behave as three kinds

**Independent toggles.** One checkbox was turning everything off together. There
are now three, under the layer toggle: Industry, Escapes, Releases. Turning
releases off leaves 218 of 223 points drawn.

**Own colours.** All three were sharing one ramp, so shape was doing the work
alone. Now:

    Industry   gold        #f2d06b → #c08c38
    Escapes    red-magenta #ef6a5a → #a8479f
    Releases   green-blue  #8fc46a → #8f9fd0

Fifteen values, all fifteen distinct. Each ramp still runs light-to-dark with
rated scale, so colour carries two things without either being ambiguous.

**Own sizes.** Releases draw at 0.62 of base radius, escapes at 0.95,
organisations at 1.25. An authorisation is one decision; an organisation is the
thing making thousands of them.

Legend rewritten to say all of it, including that each kind has its own checkbox.

### Intro rewrites

- **The wild cotton paragraph is replaced with the ecological consequences.**
  Fewer ant species; the plants that lost their guards took the worst caterpillar
  damage measured; the ones paying for guards they do not need spend sugar they
  would otherwise put into seed. Then it follows outward: ants carry seeds and
  turn soil, which decides what else grows there, and parasitic wasps that were
  never a target came out 35% lighter after eating caterpillars containing the
  insecticide. Closing on the point that does the work — nobody has a list of
  what any plant is connected to, so the tests come back clean because the tests
  cover what somebody thought to test.
- **The chemical link is now explained rather than asserted**, in four short
  paragraphs a novice can follow: how a weedkiller kills a plant, what the spare
  bacterial copy does, and then the sentence you asked for verbatim — **"the
  point is that you can spray the whole field — crop and weeds together — and
  only the weeds die."** Then why that makes the seed worth buying only if you
  also buy the spray, that Bayer sells both, that the trait creates the market
  for the chemical rather than competing with it, and that the patent turns what
  farmers did free for ten thousand years into a yearly bill. It ends by naming
  the consequence: that is why these two traits exist and drought tolerance and
  better nutrition do not.
- **Two paragraphs removed** — the "not feeding people" statistics and the
  population-growth paragraph after it.

Wire lead is now 891 words. It went up rather than down: two paragraphs came
out, but explaining the chemical link properly and following the ecology outward
cost more than the statistics they replaced. That is the right trade for a reader
starting from nothing.

---

## Round 54 — one timeout skipped every harvester after it

    could not fetch CFIA dataset: <urlopen error timed out>
    ##[error]Process completed with exit code 1.

**APHIS never ran.** Neither did the industry points or the overlay builder. A
GitHub Actions `run:` block executes under `bash -e`, so the first non-zero exit
status aborts the whole step — and `cfia_approvals.py` called `sys.exit(1)` when
it could not reach open.canada.ca. Every script after it was skipped silently.

Three fixes, each addressing a different layer of the same mistake:

**1. Retry with backoff in both fetchers.** Four attempts, 5s / 10s / 15s apart,
timeout raised from 120s to 180s. Government endpoints time out; that is a normal
condition, not an outage.

**2. An unreachable source exits 0, not 1.** `cfia_approvals.py` now warns and
returns, leaving the existing `cfia_records.json` in place. `aphis_releases.py`
does the same when nothing is harvested. Neither should be a build failure — the
previous data stays and the next run tries again.

**3. Each harvester isolated in the workflow.** Every call now ends in
`|| echo "!! … failed - continuing"`, in both workflows, so one source being
unreachable cannot take down the rest. `git add` gained `--ignore-errors` for the
same reason: a file a failed harvester never wrote would otherwise abort the step
on a first run.

### Verified rather than assumed

Reproduced the exact failure — patched `fetch` to raise, ran `main()` — and
confirmed it now returns normally with status 0, prints the warning to stderr,
and leaves the existing file alone. Before the fix that path called
`sys.exit(1)`; after it, `returncode: 0 -> step continues`.

The general lesson is worth keeping: **a script that is correct on its own can
still be wrong inside `bash -e`.** Exiting non-zero to signal "I could not do my
job" is right for a command line and wrong for one step in a pipeline of
independent tasks, and nothing in the script's own tests would ever show it.

---

## Round 55 — wire lead edits

Every requested change applied and verified individually:

- **"What this is about, briefly" deleted** — it opens on the substance now.
- **The two ant paragraphs merged into one generic paragraph** on ecological
  consequences. It no longer runs on ants and caterpillars as a story; it states
  the general point — every wild plant sits inside a web of arrangements with
  other species, and a change entering at one point comes out at others nobody
  was watching — then anchors it with three measured results: fewer defending
  insect species and the worst feeding damage of any group tested; parasitic
  wasps 35% lighter after eating prey containing the insecticide; introgressed
  wild cotton holding less genetic variety than its neighbours. Closes on the
  line that carries it: nobody holds a list of what any organism is connected to,
  so the tests come back clean because the tests cover what somebody thought to
  test.
- **"Every other living thing arrives through parents…" deleted.**
- **The three firms are now named**: Bayer, Syngenta and Pioneer hold 36%, Bayer
  alone 19%. The four majors are named too, since the paragraph already asserted
  "four companies" without saying which.
- **The weedkiller-mechanism sentence deleted**, and the spray line moved up to
  close the "one of two things" paragraph, reworded to **"The point with the
  first is…"**.
- **"That is what makes the seed worth buying…" deleted**; the Bayer-sells-both
  lines now follow the spray line directly.
- **"Who decided." heading deleted.**
- **"The organisms get no say" moved** to its own paragraph after the
  drought-tolerance line, where it now closes the argument.
- **"The strongest objection is the simplest…" deleted.**

Wire lead is 771 words, down from 891.

---

## Round 56 — the missing material, folded in

Everything listed as absent last round is now in, without a new section for each.

**A fairness passage now opens the argument**, immediately after the first
paragraph, and then turns. It concedes what is actually true: insect-resistant
cotton substantially reduced broad-spectrum spraying in several countries, and
those sprays killed bees, birds and farm workers; the unsafe-to-eat claim has not
held up in decades of testing and leading with it gets everything else dismissed;
engineered crops are not one thing; and even the damage depends on the baseline,
since no-till erodes less soil than ploughing and more than leaving the land
alone.

Then the turn, carrying the six arguments that survive: irreversibility,
contamination of centres of origin, absent liability, thin monitoring, absent
consent, and seed ownership moving to patent holders. **None of them require
proving an organism is dangerous, and together they outweigh the credits.**
Putting the strongest version of the other side first is what makes the rest
readable as an argument rather than a pitch.

**Folded into existing paragraphs**, no new headings:

- Canola seed staying viable in soil about three years, so the soil keeps
  refilling after planting stops.
- Roadside spraying not removing the resistant plants but everything competing
  with them.
- The Oregon grass crossing into two other grass species, one a different genus
  entirely; the product pulled, the company fined $500,000, and the grass still
  out there.
- Mexican wild cotton listed vulnerable, with gene flow from crops named as the
  main threat.
- Effects not being consistent: 55% more seed in wild sunflower, no advantage in
  rice.
- No untouched version left to measure against once the genes are in — the
  question stops being answerable at the moment it becomes urgent.
- **No undo**, restored as the closing line: most farm damage stops when the
  farming stops; genes in a wild breeding population do not.

**Three things needed explaining before they could be used, so they got a
paragraph each:**

- **The "shelf of spare parts" framing**, and why it is wrong — the variety in a
  wild population is what it has left after thousands of years of storms and
  droughts, and narrowing it takes away the range of answers the population can
  still give.
- **The refuge system** — what it is, why it works, and why escaped plants break
  it: scattered, next to no refuge, often making far less toxin, which is a weak
  dose in an unplanned place and precisely the condition resistance spreads
  fastest under. Closing on the fact that organic farmers lose the same
  insecticide if it fails.
- **The "feeds the world" rebuttal** — where the grain actually goes, the hunger
  figures being about prices rather than supply, and the gap between what is said
  and what is planted.

Wire lead is 1,572 words across 16 paragraphs, up from 771. It is long for a
panel. It is also now the whole argument rather than a summary of one, and the
material that was missing was the material that made it hold together.

---

## Round 57 — key box list, and the wire lead cut back

**Key box.** The layer toggle now reads **"All map points"**, and the three kind
checkboxes stack vertically underneath it instead of running together on one
line.

**Wire lead: 1,062 words across 13 paragraphs**, down from 1,572. Every edit
applied and checked individually; twenty-one assertions, all passing.

Structural moves:

- The spray line now closes the **opening** paragraph, immediately after the two
  trait types are named — which is where it does the most work, since it explains
  the first one at the moment it is introduced.
- The whole fairness block is gone as a block. What survives of it runs as one
  sentence of concession before the turn: cotton did reduce broad-spectrum
  spraying, sprays killed bees, birds and farm workers, the unsafe-to-eat claim
  has not held up — **"Plants do not stay where you put them though."**
- The four surviving arguments moved into the ecology paragraph, so they land on
  the evidence rather than standing alone as a list.
- Liability and seed ownership moved into the patent paragraph, where the
  mechanism they describe actually sits.
- The three crops line moved beside the feedlot sentence; the hunger figures
  moved to the end of that paragraph.
- The refuge explanation is replaced by four plain sentences: engineered plants
  spread out of fields, cross-breed in ditches, make less toxin than the
  original, and a weak dose in an unplanned place is the condition resistance
  spreads fastest under.

Deleted outright: the "shelf of spare parts" paragraph, the refuge paragraph, the
"feeds the world" opening, "Now look at what they chose to build", "Nobody holds
a list…", "Most damage from farming stops…", and the utilitarian phrasing about
what answers a population can still give.

Two things now say **why** rather than asserting:

- **Contamination**, in one clause — crop pollen crosses into wild relatives and
  the engineered gene stays in the wild population and passes down it.
- **Certification**, in one sentence — a neighbouring organic farm whose crop
  tests positive loses the certification its price depends on, and carries the
  loss itself.
- **The patent**, expanded to say what it covers: the plant itself and everything
  grown from it, which is why the contract forbids replanting.

### One judgement call worth flagging

The instruction was to open with "Although insect-resistant cotton did…" *and* to
end that sentence's successor with "though". Both together would concede twice in
one breath. It is written as a flat statement of the credits followed by
"Plants do not stay where you put them though" — which keeps both elements and
lets the "though" carry the turn.

---

## Round 58 — wire lead line edits

Twenty wording and structure changes, each verified individually. 1,062 → 1,034
words; the argument is now 8 paragraphs, down from 10, with the map description
following the rule.

Structure:
- **"Plants do not stay where you put them though"** moved to open the escape
  paragraph rather than close the concession one, so the turn happens at the top
  of the evidence instead of the bottom of the credit.
- **The Bayer-sells-both lines merged** into the end of the four-companies
  paragraph. They were the conclusion of that paragraph standing on their own.
- **The resistance paragraph condensed to one clause** inside the measured-
  examples list: insecticide-producing plants that escape and cross-breed in
  ditches make less toxin than the original, a weak dose in an unplanned place
  being precisely the condition under which insect resistance spreads fastest.
  It was a paragraph explaining a mechanism; it is now a finding sitting beside
  the other findings.
- **Contamination folded into the same list** rather than sitting after it, with
  the wild cotton figures as its example rather than as separate items.

Wording, all as specified: "sprays that killed"; "Pollen blows and cross
pollinates with wild species"; "And, canola seed stays alive… refilling with
their seeds"; "And that's not the end of it"; "a web of relationships"; the
commas removed around "and that were never a target of anything"; "Worse yet,"
opening the irreversibility clause; "are rarely asked" in the present tense;
"yearly bill; seed ownership"; "Meanwhile, nobody is liable"; "a problem of
prices, wars and roads, not of grain existing"; "They arrive because".

The close is now **"And, worst of all, the organisms themselves have no say."**

---

## Round 59 — the wire's real bug, and the yield argument corrected

### Why almost every region read zero

**The country-name table was English-only.** "Deutschland" does not match
"Germany"; "中国" does not match "China". The wire queries in twenty languages and
could tag headlines in one of them.

Worse, the first attempt at fixing it made things silently wrong rather than
merely empty. `slug()` stripped everything non-ASCII, so a Chinese, Japanese,
Korean, Cyrillic, Thai, Devanagari, Bengali or Arabic headline was reduced to
punctuation — and then short Latin fragments matched against the remains and
**tagged them all as the United States.** An empty region filter is a visible
failure; a filter full of wrong countries is not.

Three fixes:

1. **`slug()` keeps every script.** Accents fold; letters stay.
2. **`_has_name()` matches by script.** Word boundaries for space-delimited
   writing, plain substring for the ones that do not use spaces — Thai, Lao,
   Khmer, Myanmar, CJK, kana and hangul. A boundary test can never fire on a
   Chinese headline, because there are no boundaries in it.
3. **Native and localised names added**, 163 name forms → 561, plus the inflected
   forms that actually appear in headlines: России rather than Россия,
   Polsce rather than Polska, Česku, României, Magyarországon, Україні,
   Ελλάδας. Slavic and Greek names decline; the nominative alone never
   matches.

Tested against 26 headlines across every query language: **25 correct**, both
deliberate negatives correctly untagged. Before the fix, 12 of 12 non-English
tests were wrong.

On the empty language dropdown: language is read from each feed URL's `hl=`
parameter, which is set on every regional and non-English query. Once the
harvester runs with this build, the dropdown fills from the items themselves.

### The yield argument was wrong

"Neither trait moves grain from a feedlot to a person or lowers the price of
vegetables" asserted something the traits partly do — insect resistance protects
harvests from pest losses, so it does put more grain in the system.

Replaced with the argument that actually holds: **both built traits protect a
harvest that already exists**, from weeds and from pests, on land already farmed
well enough to grow a crop. Neither raises what a plant can yield, and neither
reaches the fields where yield is lowest, because those fields fail for lack of
water and soil rather than for lack of weeding. That is why the traits that were
not built — drought tolerance, poor-soil yield, iron and vitamin A — are the ones
that would have mattered.

The paragraph now opens on it: **"Keep in mind that these two traits — surviving
a weedkiller, and producing an insecticide — were built over drought tolerance
and better nutrition."**

Plus the line edits: the concession merged into the escape paragraph; "In Oregon,
for example"; "And the spreading is not the end of it" restored; the wild cotton
clauses split on a semicolon; the resistance clause rewritten in full; "Worse
yet, containment has demonstrably failed, and escapes are irreversible"; "found
only by accident"; the Bayer lines moved to open the patent paragraph; "a problem
of profiteering, not of grain existing".

---

## Round 60 — the wire's other two bugs, both mine

The harvester fix last round was necessary and not sufficient. Two more, both
introduced by earlier builds rather than present in the source.

**The language dropdown never populated.** `_wireBuildLangOptions` uses a local
`opts` string, declared on source line 1673. A `put(1673, …)` from an earlier
round replaced that declaration with the options loop — so `opts` was undeclared,
reading it threw a ReferenceError on every call, and the select was never filled.
That is exactly the reported symptom: the filter worked, and there was nothing in
it. The put is retargeted to 1674, which is the loop. The duplicated loop that
edit also left behind is gone.

Exercised the fixed builder directly: five items in three languages produce
`All languages / English (2) / Spanish (1) / Chinese (1) / Unknown (1)`.

**The browser-side tagger had the same ASCII-only bug as the harvester.**
`_wireSlug` stripped everything outside `a-z0-9`, so the client fallback could
not read a non-Latin headline either — which matters for every item archived
before the harvester was fixed. Now `[^\p{L}\p{N}\p{M}]`, keeping letters,
numbers and combining marks, with the same script-aware matching as the
harvester: substring for Thai, Lao, Khmer, Myanmar, CJK, kana and hangul, word
boundaries for everything else.

`\p{M}` matters more than it looks: `normalize('NFD')` splits Devanagari matras
and Hangul syllables apart, and without marks in the keep-set "भारत" became
"भ रत". Tested with both sides slugged, as the real code does: **9 of 9 across
German, Chinese, Russian, Thai, Korean, Hindi, Arabic, Portuguese, and a
deliberate negative.**

Applied as post-assembly text replacements rather than line-numbered puts,
because both functions are generated by earlier edits and have no stable source
line — which is what produced the `opts` bug in the first place.

### Text edits

The wild cotton clause rewritten as a single flowing sentence; "there is no
undoing it, ever"; "Measured examples so far:"; and the honest expansion of what
is not known — **"comes out at many others nobody has been watching and
quantifying or even defining in the first place. Simply put, nobody knows the
real impacts, both now and in the future."**

The yield-and-hunger paragraph is deleted. Wire lead 1,099 → 952 words, 10 → 9
paragraphs.

---

## Round 61 — why the subregions were still empty

The reference map you sent has the answer, and it is not a tagging bug this time.
Two things it does that this harvester did not.

**1. It reads the map's own admin-1 taxonomy.** My hand-written subregion tables
covered 16 countries. The map carries admin-1 geometry for **46**, embedded in
`index.html` as `SUBGEO`, and the panel lists a row for every one of those
regions. A region the harvester cannot name can never be tagged, so every row it
did not know about read 0 permanently.

`_load_map_subregions()` now parses SUBGEO at run time: **1,062 region terms
across 46 countries**, matched on the region name and on its bare form without
the administrative suffix, because a headline says "Bavaria" and not "Freistaat
Bayern". The canonical name is used verbatim, since a near-miss on spelling
produces a row that can never match.

**2. It asks for each place by name.** This is the real fix, and it is the one I
had missed entirely. The global feeds only tag a region when a headline happens
to name it — so adding feeds could never populate the panel, no matter how many.
The reference queries every region individually.

Added the same per-region pass, against **GDELT** rather than Google News for the
reason the reference states in its own comment: this is hundreds of requests in
one run, and RSS throttles hard at that volume, "which is why nearly every region
came back empty while a handful of large ones succeeded". GDELT is built for
programmatic access, indexes non-English media, and needs no key. 1,157 places
are queryable; the pass is capped (`--regions N`, default 400) and can be skipped
with `--no-regions`.

### What I could not verify

**GDELT returns 403 from this sandbox**, whose egress allowlist does not include
the host. The request shape follows the reference implementation, which works in
CI. I have not seen it return a single article here, and I am not going to claim
otherwise.

So the run now prints, and warns loudly on stderr if every request failed:

    WARNING: every GDELT request failed. The region and subregion counts will
    stay near zero, because the global feeds only tag a region when a headline
    happens to name it.

If that warning appears in the workflow log, the per-region source is being
blocked rather than the tagging being wrong, and the next thing to try is the
reference's Google News fallback tier.

### Guides open in the map now

Clicking a guide opens an overlay over the map — title bar, **Download PDF**
button, close button, Escape to dismiss, click-outside to dismiss. The iframe
source is cleared on close so the PDF stops rendering behind the map. Opens at
`#view=FitH` so it lands readable rather than at whatever the browser's viewer
defaults to.

### Text edits

"watching, quantifying, or even defining in the first place" with the
"simply put" sentence removed; "and that weren't targeted in the first place";
a comma before "with gene flow"; "insect resistance **to it** spreads fastest";
a full stop before "Monitoring is thin"; and the close is now **"the organisms
themselves have no say in all of this. A seed does not choose to be born, where,
or when."**

---

## Round 62

**Colours.** The selected lens pill set `#081657` **inline**, which beats every
stylesheet rule — which is why it stayed dark navy while every other active pill
had already gone light blue. It now matches the consent-phase pills exactly. The
"All map points" checkbox used the old dark `--accent` while the three kind
checkboxes under it were light blue; both now use `#7fa8cc`.

**Help panel restructured.** The map key and Reading the markers now follow The
map directly. The Global Wire sub-paragraph is deleted. "Every entry says the
same three things" moved into the middle of the map paragraph, between where you
are and clicking a name to go back up.

Deleted: "The largest marker, because an organisation is the thing making
thousands of decisions" and "The smallest, because it is one decision". The
outlined-headquarters line now says why rather than asserting it: **it is an
office, and the laboratories, plants and fields the company runs are somewhere
else entirely.**

**Animal experimentation facilities: 15 entries, animals facet 12 → 27.** 238
points total.

The honest framing, which is in the entries: **there is no global register of
these.** The USDA publishes an annual list of registered facilities, the UK Home
Office publishes establishment licences and procedure statistics, the EU has
ALURES across 27 countries. None covers the world, none shares categories, and
**mice, rats and birds bred for research are excluded from the US Animal Welfare
Act's definition of an animal** — which is the overwhelming majority of animals
used and the great majority of genetically altered ones. So this is a curated set
of the largest and best-documented facilities, not a survey, and the entries say
so.

What the batch establishes:

- **The UK and EU count animals bred and killed to maintain engineered lines
  separately from experimental use.** Nowhere else publishes that number, so
  nowhere else can say what the model-organism trade costs.
- **Charles River's own site list is the nearest thing to a map of the industry's
  physical footprint that exists** — because no regulator publishes one, in any
  country.
- **The primate dependency.** Chinese export suspension in 2020 raised prices
  several-fold and stalled Western programmes, which showed how completely the
  rest of the world depends on breeding capacity in one country. Rarely discussed
  as a dependency.
- **The Biomedical Primate Research Centre has survived repeated parliamentary
  attempts to wind it down.** A facility outlasting explicit political pressure
  to close says more about how entrenched this work is than any statistic.

---

## Round 63 — law, lobbying, and named people

**255 points: 230 industry, 20 escapes, 5 curated.** Seventeen entries.

**Law and patents.** The regulatory firms that draft what agencies read, the
USPTO full-text search and the Patent Trial and Appeal Board where CRISPR
ownership was actually decided, the EPO opposition register, No Patents on Seeds,
the EU Transparency Register, and Euroseeds. Two points these carry:

- **The claims are the property, not the abstract.** A patent naming a specific
  construct and one reaching any plant containing a gene variant look identical
  on the front page.
- **Any person may oppose a European patent for nine months after grant**, with
  no standing requirement and no lawyer needed to file. Polling across several
  European countries finds large majorities against patents on seeds. It is the
  widest gap on this map between how much support a position has and how few
  people act on it.

**Named individuals.** Everyone included is a public figure in a public role, and
every entry describes the role and the documented decisions attached to it — not
the person. Where conduct has been adjudicated, the finding is cited as a
finding.

- **Bayer Crop Science leadership.** Companies get argued with as if they were
  weather. A division has a head with a public name and a stated remit, and mail
  to a named executive is answered differently from mail to a company.
- **The Broad and the Innovative Genomics Institute**, as the two sides of the
  foundational patent dispute. Both did publicly funded work; the agricultural
  rights ended up exclusively licensed either way. **The individuals are not the
  problem; the arrangement that converts their work into an exclusive licence is,
  and it operated identically regardless of who won.**
- **Doudna's institute runs an explicit access-and-affordability programme.** The
  strongest critique of gene-therapy pricing comes from inside the field, which
  is worth citing precisely because it cannot be dismissed as illiteracy.
- **He Jiankui.** The only completed case of heritable human genome editing. The
  scientific response was a moratorium with no legal force, issued by people who
  were not the ones proceeding. What stopped it was a criminal prosecution — which
  matters everywhere on this map that self-governance is offered as sufficient.

    rules 51  seed 30  animals 27  editing 21  escape 20  synthesis 14
    repro 14  livestock 13  deextinct 13  cro 12  wild 12  clinical 12
    money 11  ogtr 5

### On "until coverage is 100%"

It cannot get there, and the notes should say so rather than implying an
asymptote. There are thousands of seed companies, hundreds of CROs, tens of
thousands of fertility clinics and laboratories, and no complete register of any
of them exists in any country. A census is not available to anyone, at any
budget.

What is achievable is completeness of **structure**: every facet populated, every
chokepoint named, every mechanism shown at least once with a real example. On
that measure the map is close. On headcount it is a sample, and the honest thing
is to keep saying which one it is.

---

## Round 64 — repo audit

The uploaded repo is in good shape. Four things.

### The wire works

    2,359 items | 940 country-tagged | 397 subregion-tagged across 83 subregions
    613 from GDELT | 41 language values

GDELT ran fine in CI, which is what could not be verified from the sandbox. The
per-region pass is doing exactly what it was added to do.

### One bug it exposed

**GDELT reports a language NAME, not a code**, and the harvester truncated it to
two characters. So `sp`, `ch`, `po` and `ge` appeared alongside the proper
`es`/`zh`/`pt`/`de` from the RSS feeds — the dropdown listed several languages
twice, under codes that are not ISO codes at all. `po` also collided Portuguese
with Polish.

Fixed with a name-to-code map in the harvester. `tidy_repo.py` repairs the 282
items already committed; it deliberately leaves `po` alone, because after the
fact there is no way to tell which of the two languages it was and guessing would
be worse than leaving it unlabelled.

### index.html is three rounds behind

The repo has 223 points; the current build has 255. Missing: the animal
facilities including ALURES, the law firms and named individuals, the in-page
guide viewer, the lens pill colour fix, and two wire-text edits.

`harvest/build_industry_points.py` is also behind, and `industry_source.json` /
`industry_points.json` are at 144 rather than 230.

### Four stray files

    bch_focal_points.py       duplicate of harvest/bch_focal_points.py
    check_links.py            duplicate of harvest/check_links.py
    guides/?                  1 byte, an upload artefact
    overlays/README (2).md    duplicate of overlays/README.md

`tidy_repo.py` removes them, and only removes the two root scripts after
confirming byte-for-byte that the `harvest/` copies are identical.

### What projects.json should look like, confirmed

    365 records: 360 harvested APHIS + 5 curated OGTR

Correct. The map merges it with the 223 embedded points and yields 583 with no
duplicates, which is the round-49 architecture working as intended.

---

## Round 65

**274 points: 249 industry, 20 escapes, 5 curated.** Nineteen entries into the
two facets thinnest against their real size: **cro 12 → 20, repro 14 → 23.**

    rules 51  seed 30  animals 27  repro 23  editing 21  cro 20  escape 20
    synthesis 15  livestock 13  deextinct 13  clinical 13  wild 12
    money 11  ogtr 5

The entries carrying something:

- **IQVIA** designs and runs the trial *and* sells analytics built on prescription
  and claims data covering hundreds of millions of people. Neither business is
  regulated with the other in view.
- **Parexel** as the pattern: most large CROs are now private-equity owned, so
  **the organisation running the trials a regulator reads publishes less about
  itself than the sponsor does.** That is the wrong way round.
- **Catalent**, bought by Novo Holdings — a manufacturer serving many sponsors
  now owned by one of them, so every other client's supply runs through a
  competitor's asset.
- **ICON** owns both the trials and the sites that host them, which removes a
  check that existed when sites were independent.
- **HFEA's add-on ratings** are the only case anywhere of a regulator publicly
  rating the extras clinics sell. Most are rated red or amber and they continue
  to be sold — which shows precisely how far publication gets you without a power
  to prohibit.
- **Cooper Surgical's culture media recall.** One defective batch reaches embryos
  in hundreds of clinics at once and cannot be undone. Clinic-level oversight
  cannot see a supplier selling into every clinic — the same blind spot the
  contract-manufacturing facet has.
- **Monash IVF** is listed rather than private-equity held, which forces
  disclosure the others avoid: cycle volumes, revenue per cycle, and the market
  announcements that follow an incident. The clearest available view of the
  commercial mechanics of a fertility business.
- **Celltrion** for the point biosimilars make on their own: they are the one
  part of this industry where prices fall, and they exist because patents expire.

**`.github/workflows/tidy.yml`** added — a `workflow_dispatch`-only job that runs
`tidy_repo.py` from GitHub itself, so no local clone is needed. Delete it and
`tidy_repo.py` after the run.

---

## Round 66

**293 points: 268 industry, 20 escapes, 5 curated.** Twenty-one entries into the
facets that were thinnest after the last round: **money 11 → 15, wild 12 → 15,
clinical 13 → 15, livestock 13 → 17, synthesis 15 → 18, deextinct 13 → 15.**

    rules 51  seed 30  animals 27  repro 23  editing 22  cro 20  escape 20
    synthesis 18  livestock 17  wild 15  deextinct 15  clinical 15
    money 15  ogtr 5

The entries that carry something new:

- **The International Gene Synthesis Consortium.** It is voluntary, its
  membership is a minority of world capacity, and no government requires any of
  it. **The most consequential control point in this entire industry is a trade
  association's code of practice.** Stated as a fact about governance, not a
  prediction about misuse.
- **Codex DNA / Telesis Bio** is why that matters now rather than eventually.
  Order screening only works while orders are placed; a benchtop synthesiser
  moves the capability inside the building and the voluntary regime has nothing
  left to inspect.
- **Benchling** sees the design before the synthesis company sees the order and
  long before a regulator sees an application. Nothing requires it to look.
- **Sterile Insect Technique.** Radiation-sterilised insects cannot reproduce at
  all; engineered self-limiting insects reduce that to a probability. The older
  technique is the benchmark any release should be argued against, and it is the
  comparison the industry rarely puts alongside its own.
- **Blackstone Life Sciences.** Royalty financing attaches a permanent claim on a
  medicine's revenue before approval, which is one reason prices do not fall
  after development cost is recovered.
- **The Gelsinger record.** Every safeguard in the clinical facet exists because
  of a specific death in 1999, and the investigation found unreported adverse
  events and undisclosed financial interests. **The reforms followed the harm
  rather than preceding it**, which is the pattern this map documents everywhere.
- **The RAC archive.** Protocol-by-protocol public review of human gene transfer
  existed for forty-five years and was ended on the grounds the field had
  matured. The archive is the benchmark for judging what replaced it.
- **Alnylam** for the distinction the map keeps returning to: RNA interference
  wears off when dosing stops. A reversible therapy and a permanent edit are not
  one category, and treating them as one loses the only feature that matters for
  consent.
- **FDA's animal register** distinguishes approvals from enforcement discretion —
  the agency deciding not to act rather than deciding a product is safe. The two
  look identical from outside.
- **Hendrix Genetics and Topigs Norsvin.** Global poultry and pig genetics are
  controlled by a handful of firms, so a few breeding decisions propagate into
  billions of animals. Concentration tighter than in seed, attracting a fraction
  of the attention.

### A small bug

`Nature's SAFE` failed to geocode because the coordinate table used a curly
apostrophe and the entry a straight one. Caught because the builder names its own
misses rather than silently dropping them — the same design that made the
eighteen-entry miss in round 52 a thirty-second fix.

---

## Round 67

**311 points: 286 industry, 20 escapes, 5 curated.** Nineteen entries across
twelve countries, including four new: Serbia, Bulgaria, Sri Lanka, plus more
Denmark and Japan.

    rules 56  seed 35  animals 27  editing 26  repro 23  synthesis 21
    cro 20  escape 20  livestock 17  clinical 16  wild 15  deextinct 15
    money 15  ogtr 5

The entries carrying an argument:

- **Beam and Prime Medicine.** Each generation of editing tool is offered as the
  answer to the previous one's off-target problem. That is progress, and it is
  also an admission: **the earlier tools had the problem while they were being
  used on people, and were described as precise at the time.** Prime editing then
  writes new sequence without inserting a transgene, which puts it outside
  regulatory categories drawn around inserting foreign DNA — by construction.
- **Arcadia Biosciences.** A company can now design its product to fall outside
  the definition rather than pass through it. The regulatory question is answered
  at the design stage, before any application exists, which is not how any of
  these frameworks assumed products would be developed.
- **Zymergen.** Raised very large sums, went public, failed to commercialise, was
  absorbed. The venture model rewards claims that outrun results, and the
  correction arrives as a share price rather than a retraction — the literature
  behind such a company is not revisited when it fails.
- **New England Biolabs.** The least examined chokepoint in the chain: **no
  screening regime, voluntary or otherwise, covers who may buy a Cas nuclease,
  and it is sold from a catalogue.**
- **Element and Ultima.** Instrument competition is driving cost per genome down,
  and below a certain price population-scale sequencing becomes the default — at
  which point the consent and retention questions arrive for everybody at once.
- **Florimond Desprez.** Independent breeders cannot pay licence fees at scale or
  retain patent attorneys, so they abandon projects rather than risk
  infringement. The patent argument is usually framed as farmers against
  companies; it is also companies against companies.
- **DLF Seeds.** Grasses are wind-pollinated, perennial, outcrossing and planted
  near wild relatives — the worst containment profile of any crop group, and the
  one the Oregon escape happened in. The commercial pressure to engineer them did
  not go away because one release failed.
- **Serbia.** EU accession requires alignment with a framework that permits
  authorised GM products, so a national prohibition becomes a trade negotiation
  rather than a domestic decision. The same mechanism that operated on Mexico,
  arriving by a different route.
- **Bulgaria** writes buffer distances into statute, which concedes that pollen
  travels. Most frameworks avoid conceding it by leaving distances to guidance.
- **Sri Lanka.** Labelling in importing countries is enforced by border testing,
  which needs laboratory capacity most importing countries do not have. A rule
  that cannot be tested for exists on paper — and that is the ordinary condition
  rather than the exception.
- **The African Union model law.** A model law spreads a regulatory approach
  across dozens of countries in one act of drafting, long before any application
  appears. Whoever writes the model decides more than any national committee.
- **WHO's genome editing framework** recommends a registry, whistleblowing
  mechanisms and a prohibition on heritable editing. None of it binds anybody,
  and the one case that has happened was stopped by a national criminal court.

### Workflows

Only `releases.yml` and `wire.yml` belong in `.github/workflows/` permanently.
`tidy.yml` is a one-off: run it, then delete it and `tidy_repo.py` together.

---

## Round 68

**332 points: 307 industry, 20 escapes, 5 curated**, across 218 distinct places.
Twenty-one entries. Every facet now at 16 or above except the harvested release
family.

    rules 60  seed 36  editing 27  animals 27  synthesis 23  repro 23
    cro 20  money 20  escape 20  livestock 19  clinical 19  wild 17
    deextinct 16  ogtr 5

The ones that carry something:

- **Regeneron Genetics Center.** Millions of exomes sequenced through health
  system partnerships. Participants consented to research; the dataset is a
  corporate asset that outlasts the study, the consent form and often the health
  system that gathered it. **This is the human counterpart of the germplasm
  question the seed facet raises.**
- **The insertional oncogenesis record.** Inserting genetic material into a
  genome can land it somewhere that matters — the reason gene therapy stalled in
  the 2000s, and it recurred with newer vectors. The field's answer is better
  vectors, which is the same answer as last time. The risk is disclosed,
  monitored, accepted, and carried by patients.
- **Moderna's individualised cancer therapies.** A therapy designed for one
  person cannot be trialled the way a product is. **Regulators are being asked to
  approve a manufacturing process rather than a medicine**, which is a different
  question from the one every framework on this map was built to answer.
- **ICER.** Its value-based benchmarks for several gene therapies came in well
  below the launch price, and the therapies launched at the higher figure anyway.
  The clearest demonstration that pricing here is set by what a market will bear
  rather than by any assessment of worth.
- **NIH RePORTER.** Answers the question the industry's materials avoid: how much
  was paid for publicly. A record showing public funds, a university and a
  commercial partner on one project is the documented start of nearly every
  licence this map complains about.
- **BARDA.** Public funding of manufacturing capacity produces privately owned
  plants, and the terms on which the public can later use what it paid for are
  whatever the original contract said.
- **Guangzhou Wolbaki.** Release programmes are limited by rearing capacity, and
  capacity is being built where labour and land are cheapest. A map of open
  release covering only Oxitec and the World Mosquito Program is missing where
  the insects are actually produced.
- **Argentina's INASE.** Seed law permits farm-saved seed, so the companies
  collect through private contracts and testing at delivery points instead.
  **When a law does not give a company what it wants, the contract does — and the
  contract is not public.**
- **Mexico's CONAHCYT** is the one case on this map of a state research body
  producing the evidence a government used to *restrict* an industry. Everywhere
  else the equivalent institutions produce the evidence used to permit one.
- **Fonterra.** A cooperative of that size deciding against a trait removes the
  market for it across an entire national sector, with no regulator involved.
- **Revive & Restore's black-footed ferrets** worked, and depended entirely on
  tissue banked decades earlier by people with no idea what it would be used for.
  The case for cryobanking is made there — and so is the case that sampling
  choices made now decide what is possible later.

**Alliance for Science** is listed at low trust: philanthropic money funding
public argument rather than research, training fellows from countries where
approval decisions are pending. Legitimate advocacy, and an input into those
decisions. It is a voice, not a record, and the trust filters exclude it as one.

---

## Round 69

**356 points: 326 industry, 25 escapes, 5 curated**, across 227 places. Twenty
industry entries and **five new escape records — the first addition to that layer
since it was built.**

    rules 61  seed 37  editing 28  animals 27  escape 25  synthesis 24
    livestock 23  repro 23  cro 22  money 22  clinical 21  deextinct 20
    wild 18  ogtr 5

### The escape record, 20 → 25

Three of the five are about organisms nothing engineered, which is the point:

- **Farmed salmon genetics in wild Norwegian rivers.** Farmed ancestry found in a
  large majority of assessed wild populations, river by river, over decades.
  **Nothing here was genetically engineered** — the genetics are the product of
  intensive selection, and they entered wild populations through routine escape.
  It is the clearest measured example of the process this map argues about for
  crops, and it exists only because one country funded the monitoring.
- **Atlantic salmon naturalised in Patagonia**, from escapes running to hundreds
  of thousands of fish per incident, in a country with no native salmon. No
  biosafety framework was engaged at any point, because nothing was engineered.
- **Petunias, a third wave** after two clearance operations each treated as
  complete. The recurrence measures the monitoring rather than the plant.
- **Ukraine** — the fourth case of adoption preceding approval after India,
  Brazil and Paraguay. Consistent enough now to treat as the normal route: the
  register records what was asked for, not what is in the ground.
- **GM maize found growing in Mexico** despite the constitutional prohibition.
  Imported grain intended for food can be planted, and some of it is. **A
  prohibition on planting does not control seed that arrives as food** — the gap
  every import-and-prohibit country on this map has, and almost none tests for.

### Industry entries

- **Cibus** is the concrete case behind an abstract point made three rounds ago:
  its Canadian canola is the CFIA register entry with no OECD identifier. A
  commercial product in the field that the international tracking system cannot
  name.
- **Advarra.** Commercial ethics review boards are legal, accredited, efficient —
  and selected and paid by the sponsor whose protocol they review. The structural
  conflict is identical to the one in safety studies, and here it applies to the
  body whose entire function is protecting participants.
- **MHRA's accelerated pathway.** Regulators now compete to be chosen. That is
  stated policy rather than an accusation, and it exerts steady downward pressure
  on how demanding any one of them can be.
- **Norway's marine research institute** runs the only systematic long-term
  monitoring of genetic introgression from farmed into wild animals anywhere.
- **Syncona** is included as a counter-example to this map's own
  venture-timeline argument: patient capital exists, is publicly listed, and
  whether it produces different products is testable rather than assumed.
- **The European Investment Bank.** Public capital reaching this industry as
  lending carries none of the disclosure the grant channel has.
- **SUNY ESF's chestnut programme** published performance problems with its own
  line, and the sponsoring conservation organisation withdrew support as a
  result. Self-reported adverse findings from a developer are rare enough here to
  mark wherever they occur.

---

## Round 70

**374 points: 344 industry, 25 escapes, 5 curated.** Eighteen entries.

    rules 65  seed 43  editing 29  animals 29  repro 26  escape 25
    synthesis 24  livestock 23  cro 22  clinical 22  money 22
    deextinct 21  wild 18  ogtr 5

Carrying something:

- **UPOV 1991.** The single instrument that has done most to change what a farmer
  may legally do with a harvest, spreading through trade negotiation rather than
  domestic debate. **Most people affected by it have never heard of it.**
- **Codex Alimentarius.** A voluntary guideline becomes effectively binding once
  trade law treats departure from it as an obstacle needing justification. That
  is the mechanism behind the Mexico ruling, named here as a mechanism.
- **EFSA's GMO opinions** run to hundreds of pages and are open for public
  comment for thirty days after publication. Almost nobody comments. **The most
  consequential open door on this map and the one least walked through.**
- **India's ART Act.** Commercial surrogacy was prohibited and the market moved
  to countries with weaker rules. **A national prohibition on a cross-border
  service relocates it rather than ending it**, and the people most exposed move
  with it.
- **Corteva's seed treatments.** Treated seed is often outside pesticide-use
  reporting because nothing is sprayed, so the area treated is not recorded
  anywhere. One of the largest insecticide applications in world agriculture and
  among the least documented.
- **Verve Therapeutics.** Every argument for accepting an irreversible edit rests
  on the alternative being worse. Applied to a condition already managed by daily
  tablets, that argument has to be made differently — and the eligible population
  is orders of magnitude larger.
- **The Donor Sibling Registry** exists because the clinics did not build it. The
  sibling groups it has surfaced are the primary public evidence that family
  limits are not working, assembled by the people affected rather than by any
  regulator.
- **Enza Zaden and Bejo.** A handful of firms in one Dutch province breed most of
  what the world eats fresh. Geographic concentration nobody treats as a
  vulnerability, invisible from any national statistic.
- **Egypt's grain tenders.** Purchase specifications from the world's largest
  wheat buyer function as regulation, written by a purchasing agency rather than
  a biosafety authority.
- **Beck's Hybrids.** Independent retailers license the same traits as everyone
  else, so visible competition at the point of sale sits on a trait layer with
  almost none. **What looks like a choice of companies is a choice of bags.**

### Weebly embed

`weebly-embed.html` added: an iframe pointing at the GitHub Pages URL, sized at
85vh with a 520px floor so it survives short windows and phones. An iframe rather
than a paste because the map is a 2.5 MB single file with its own scripts and
styles — pasted into a Weebly page it would collide with the theme's CSS and
Weebly would strip much of what it needs. The file carries a full-bleed variant
and a fallback link in comments.

### A caught artefact

One coordinate line emerged malformed — a fragment of unrelated text spliced into
a float literal. `ast.parse` caught it before the build ran. Worth noting because
it was not a logic error or a bad anchor: it was corruption in generated text,
and only the syntax check would have found it.

---

## Round 71

**393 points: 363 industry, 25 escapes, 5 curated.** Nineteen entries. Every
facet now at 20 or above except the harvested release family.

    rules 67  seed 43  editing 32  animals 29  clinical 26  repro 26
    money 25  escape 25  synthesis 24  cro 24  deextinct 24  livestock 23
    wild 20  ogtr 5

The entries that carry something:

- **Pivot Bio's PROVEN.** Applied across millions of US acres, it is one of the
  largest deliberate releases of an engineered organism in history by area — and
  it generates no entry in any biosafety register, because a soil microbe applied
  to seed is not a plant and is not planted. **The scale and the invisibility are
  facts about the same product.**
- **Rothamsted's aphid-repellent wheat.** The trait worked in the glasshouse and
  failed in the field, and the institute published that. It is the single best
  answer to the claim that laboratory performance predicts field performance, and
  it came from the developer.
- **Japan's PMDA.** Conditional approval lets regenerative medicine products be
  marketed on preliminary evidence; at least one was later withdrawn when
  confirmatory data did not arrive. **It is the working experiment in whether
  early access or evidence should come first, and the results are being generated
  on patients.**
- **NMDP.** Ex-vivo gene therapy needs transplant-grade infrastructure. A therapy
  requiring it cannot reach anywhere that lacks it regardless of price — for the
  sickle cell therapies that means most of the affected population, and **the
  barrier is hospitals rather than money.**
- **Index fund ownership.** Most people with a pension are part-owners of this
  industry through funds they never chose stock by stock. That is the mechanism
  that makes shareholder pressure possible at all, and the same fact cuts both
  ways — the map now says so.
- **ViaGen's Przewalski's horses.** Commercial pet cloning built the capability
  conservation cloning now uses. The capacity exists because a consumer market
  paid to develop it.
- **BioRescue.** Biotechnology deployed after every other option failed, on a
  subspecies driven to two individuals by poaching. Whatever it demonstrates
  about the technology, it demonstrates more about what made it necessary.
- **Poland.** Prohibiting the marketing of GM seed achieves a cultivation ban
  without invoking the biosafety framework at all — because seed law is where the
  practical control sits.
- **China's seed industry programme.** Seed sovereignty pursued as industrial
  policy by the world's largest agricultural producer, with the state as
  investor, regulator and customer at once.

### A coordinate caught before it shipped

Gates Ag One was geocoded to (63.7467, -68.5170) labelled "St Louis" — which is
in the Canadian Arctic. Fixed, and then a spot-check ran every entry whose stated
place matches a known city against that city's real position: **0 mismatches
across 367 entries.** Worth having as a standing check, since a plausible-looking
pair of floats is the one kind of error nothing else in the pipeline would catch.

---

## Round 72

**414 points: 384 industry, 25 escapes, 5 curated.** Twenty-one entries.

    rules 70  seed 50  editing 37  animals 31  clinical 28  repro 28
    money 25  escape 25  synthesis 24  cro 24  deextinct 24  livestock 23
    wild 20  ogtr 5

Carrying something:

- **Charles River's horseshoe crab reagent.** A wild animal harvested at scale
  for the endotoxin test every injectable medicine depends on — and a recombinant
  replacement exists, works, and is in the US pharmacopoeia. Adoption has been
  slow because the old test is what everyone is used to. **Here the engineered
  substitute is the option that spares the animals, and inertia is what keeps it
  from being used.** The map is better for containing a case that cuts this way.
- **Editas.** The first in-vivo human gene editing trial, discontinued for
  commercial rather than safety reasons. Participants accepted an irreversible
  procedure in a programme that was then stopped because the market was too
  small — a risk of trial participation nobody consents to explicitly.
- **Orchard Therapeutics.** For ultra-rare disease the eligible population is a
  few hundred children worldwide, so the price per patient becomes extraordinary
  by arithmetic rather than by choice. **That is the honest version of the pricing
  argument, and it does not apply to the larger indications where the same prices
  are charged.**
- **Perfect Day.** The protein is identical to the dairy version and the
  engineered organism is removed in processing, so nothing requires a label. One
  of the largest routes by which engineered-organism products reach households,
  and the least visible.
- **Impossible Foods** is unusual for being open about it, and the disclosure has
  cost it with part of its own natural-foods constituency. A product marketed on
  environmental grounds and opposed on genetic ones — shown rather than resolved.
- **McCain and Simplot as processors.** Processor specification is why the
  engineered potato has had a limited market: the buyers declined it and growers
  plant what buyers will take. The market door, documented, in a crop where it
  was decisive.
- **Alfalfa.** Perennial, bee-pollinated far beyond any buffer, stands persisting
  for years — the crop where coexistence rules written around annual
  self-pollinating plants fit worst, approved for release anyway.
- **The WTO SPS Committee.** Members raise 'specific trade concerns' about each
  other's approval timelines and the record is public. **The clearest
  documentation anywhere of pressure applied to regulators from outside their own
  country.**
- **ISO's biotechnology committee.** Standards committees are open to
  participation and almost nobody outside industry participates. A definition
  settled there propagates into national regulation years later without anyone
  having argued about it in public.
- **CIP in Peru.** A centre of origin, the world's largest potato genebank and a
  national GMO moratorium in one place — and the biofortified sweetpotato work
  happened there, conventional breeding delivering the nutrition trait the
  engineered pipeline is criticised for not delivering.
- **The Ethiopian Biodiversity Institute** insisted on material transfer terms
  and benefit sharing decades before the Nagoya Protocol. That precedent came
  from a low-income country protecting its own material, not from an
  international negotiation.
- **ICBA in Dubai.** The traits this map notes as absent from commercial
  pipelines — salinity, drought, poor-soil yield — are being worked on there,
  largely by conventional breeding on public and philanthropic money, at a
  fraction of the resources going into the two commercial traits.

The coordinate/place check ran clean: **0 mismatches across 388 entries.**

---

## Round 73 — the index and the lens buttons were dead

Two real bugs, both with the same root cause, both mine.

**Since round 44, `trackerData` ships as `{}`.** That was correct — entries became
map points and the per-country resources box was removed. But `buildIndexData()`
and the whole lens/sub-filter system still read `trackerData`. So the index built
from an empty object and **every lens button filtered a set with nothing in it.**
The single stray row you saw was the last thing left in that structure.

Two fixes:

1. **`buildIndexData()` now reads `PJ_SEED`** — 431 rows, every point, labelled by
   kind: Organisation, Escape, Release authorisation.
2. **`pjPasses()` now honours the lens and sub-filter selection**, so clicking a
   facet filters the map as well as the index. Release records carry no facet
   tags, so they show when the lens is "all" and hide once a facet is chosen — a
   facet is a claim about the industry, not about a permit.

For either to work the points had to carry the fields they were stripped of in
the round-44 conversion: `tags`, `kind`, `voice`, `trust`, `skind`.
`build_industry_points.py` now carries all five.

Verified by running the shipped `buildIndexData` against the shipped `PJ_SEED`:
**431 rows, all 12 lenses represented**, and the lens filter tested on the map
(all → 431 points, seed → 114, clinical → 72, sub-filter `seed:majors` → 15).

**One invalid tag found on the way.** `people:professional`, from the law-firm
batch, is not one of the 51 sub-filters — it had been passing because recent
validation checked source families rather than tags. Replaced, and every tag in
every module now checked against the map's real taxonomy: **920 tags, 0 invalid.**

### Colours

Help-panel section headings (`.hl-sec`, both rules) and the "jump to a part of
the industry" menu now use the same light blue as the lens pills and layer
checkboxes.

### Entries

**431 points: 401 industry, 25 escapes, 5 curated.** Eighteen entries.

    rules 72  seed 56  editing 41  animals 31  clinical 30  repro 28
    synthesis 25  money 25  escape 25  cro 24  livestock 24  deextinct 24
    wild 21  ogtr 5

- **Hybrid wheat.** Hybridisation achieves what a patent achieves without needing
  one: the saved seed simply does not perform. **The oldest mechanism on this map
  for making a farmer buy every year, and it requires no law at all.**
- **Short-stature corn** is an adaptation to a climate producing stronger storms.
  The industry is selling adaptation to conditions its own input-intensive model
  contributes to.
- **Enlist** is the treadmill made visible in a product line — tolerance to a
  second chemical sold because the first stopped working, and the reintroduced
  older herbicides drift further than the one they replace.
- **Ohalo and Inari.** One alters how genomes combine without changing a
  sequence; the other makes dozens of simultaneous edits. Carve-outs written
  around single small changes that could plausibly have arisen naturally do not
  obviously reach either, and **no framework has drawn a line at a number.**
- **Novo Nordisk and Biocon together.** Recombinant insulin is fifty years old
  with long-expired patents, and the price rose anyway because three firms supply
  nearly all of it — while Biocon's biosimilars sell far cheaper. **Age and
  expired patents do not produce low prices; competition does.**
- **Moolec.** A soy plant containing pig protein is not covered by any labelling
  scheme built around allergens, dietary restriction or religious observance.
- **Oxford Nanopore's field sequencers** are the one technology here that
  materially helps the people checking rather than the people releasing.
- **CIMMYT.** Its standard material agreement keeps the world's maize and wheat
  diversity available and unpatentable in the form supplied — the main thing
  standing against the enclosure the rest of this map documents, and it depends
  on funding rather than on any law.
- **MASIPAG** does both halves: hundreds of farmer-selected rice varieties in
  circulation, and the litigation that revoked the Golden Rice permits. **An
  opposition that also produces seed is a different proposition.**

---

## Round 74 — why the subregions were still empty

The per-region pass was working. It was only ever reaching the same third of the
places, every run.

### The bug

`uniq[:cap]` sliced the target list **after countries had been added to the
front**. So each run queried 97 countries plus the alphabetically earliest ~300
subregions — ARG, AUS, AUT, BEL, BGD, BGR, BOL, BRA — **and nothing past roughly
"D" was ever queried at all.** Same slice every run, forever. That is exactly the
shape of what you were seeing: many regions filled, most subregions at zero.

### Three fixes

**Order.** Subregions go first now. Countries already pick up coverage from the
global feeds; subregions almost never do, and they are the ~1,060 rows reading
zero.

**Rotation.** The window advances every six hours, which is the wire's cron
interval — stateless and deterministic, so two runs in the same slot agree and
consecutive runs do not repeat. Simulated against the real target list:

    targets: 1,157 (1,060 subregions first, then 97 countries)
      after run 1: 400 covered (35%)
      after run 2: 800 covered (69%)
      full sweep after 3 runs (18 hours)

Because `wire.json` keeps a 120-day archive, coverage accumulates rather than
rotating away.

**Widening.** A place with no matching story in 90 days is not necessarily a
place with nothing to report — it may be a quiet quarter in a small region. Three
tiers now, tried in order until one returns something: 90 days on the topic
terms, 365 days on the same terms, then 365 days on a broader set. **The widest
tier still carries topic terms.** A bare place-name query returns whatever merely
mentions the place, which is how a region filter fills with irrelevant stories
and becomes worse than empty.

**And a budget**, because three tiers across 400 places is up to 1,200 requests.
Tier 1 always runs for every place; the widening tiers draw on a pool of
`cap × 2.2`. Without it a quiet week — when almost everything escalates — would
triple the request count and the runtime.

### Verified

Exercised the whole pass with GDELT stubbed at a 20% hit rate reachable only on
the widest tier: **400 places → 1,200 calls → 73 distinct subregions filled**,
every item carrying both `iso` and `region`, budget holding with 80 left.

And the names match: **every one of the panel's 1,060 subregion rows is a name
the harvester can now write, exactly — 100%, zero mismatches.** A near-miss on
spelling produces a row that can never fill, so this is the check that matters
most.

Only `harvest/wire_harvest.py` changed. Re-run the wire workflow; the panel
should fill over the next three runs rather than all at once.

---

## Round 75 — the Register is recoverable

Twelve wire-lead edits applied, each verified.

### The finding that matters

The GM Contamination Register stopped in 2013 and I had been treating it as
lost. It is not. **The whole dataset survives as open-access supplementary data**:

    Price B & Cotter J (2014). International Journal of Food Contamination 1:5
    doi:10.1186/s40550-014-0005-8 — CC BY

Additional file 1 is the incident table: all 396 incidents across 63 countries.
`harvest/contamination_register.py` recovers it. It does not hard-code a download
URL — supplementary URLs move, DOIs do not — so it fetches the article, finds the
supplement link, follows it, and says exactly which step failed if the layout
changes rather than writing a silently empty file. Country-level positions only;
rows it cannot place are dropped rather than guessed at. Every record carries the
CC BY attribution in its description.

New source family `escape:register`, separate from the hand-written `escape`
family, because the two are not the same kind of record: the Register gives
one-line summaries at country level, the hand-written entries carry the detail.
Both are diamonds; the filter separates them.

Blocked from the sandbox by the egress allowlist, so the fetch is unverified
here. The parser is not: exercised offline against rows shaped like the published
table, it produces well-formed records with all three description sections, real
coordinates, and the attribution.

### What I got wrong before

I said the Register could not be added. It can. **The right question was not
whether the site still works but whether the data was ever published elsewhere**,
and it was, in the paper describing it.

---

## Round 76 — two more sources recovered

### OGTR, looked at again

There is no bulk download. But there is an **interactive crop field trial map**
carrying licence, holder, crop, trait, area, location and status. An interactive
map is driven by a data endpoint, so the data exists in machine-readable form
whether or not a download is advertised.

`harvest/ogtr_trials.py` finds that endpoint rather than assuming a URL, and
**checks robots.txt first, every run**. Earlier rounds recorded OGTR as off
limits on the strength of robots.txt; the right way to act on that is to ask the
file each time rather than to remember an answer. If it refuses, the script says
so and exits 0.

From the sandbox it refuses — correctly, since the allowlist blocks robots.txt
and `RobotFileParser` treats an unreadable file as a refusal. **So I still do not
know OGTR's real answer.** The run will print it.

Worth having if it works: every other release record on this map is
`precise:false`, sitting at a country or state fallback because the register
published no location. **OGTR publishes real coordinates.** These would be the
only release points on the map that sit where the thing actually is — and the
entry says why that matters: it removes the usual argument against publishing
locations everywhere else.

### Animal facilities, pieced together

`harvest/animal_facilities.py` harvests the USDA annual reports — one point per
registered US research facility with the species counts it declared, at state
level. New source family `animals:facility`.

It is the only facility-level count published anywhere, and every record says
what it is missing: **mice, rats and birds bred for research are excluded from
the Animal Welfare Act's definition of an animal.** They are the overwhelming
majority of animals used and the great majority of genetically altered ones. The
UK and EU figures are national totals rather than facility lists, so they stay as
the hand-written entries already on the map.

### Both are discovery-based and both say what failed

Neither hard-codes a download URL. APHIS reorganises its data pages and
supplementary URLs move; a hard-coded path fails silently a year later. Both
name the step that failed and tell you what to update. Both exercised offline
against realistically shaped rows: coordinates outside the expected bounds are
rejected, unplaceable rows are dropped rather than guessed, and every emitted
record carries all three description sections.

**29 source families now.** All route correctly.

---

## Round 77 — two crawlers, and a correction

### GMO-free zones

`harvest/gmofree_zones.py`. The site publishes one page per country with no
export, no API and no single table, so walking it is the only route. It reads the
**index** for country links rather than hard-coding a list, honours robots.txt,
runs one request at a time with a delay, and skips-and-names failures rather than
retrying into the ground.

Declarations are matched against the map's **own SUBGEO admin-1 names**, so a hit
lands on a row the panel already lists. Municipal declarations sit below admin-1
and are counted and reported rather than forced onto a region they do not fit.

### USDA FAS

`report_type=28` is the wrong filter — it is a broad category and still returns
tens of thousands. **The series is identified by its title.**
`harvest/fas_biotech.py` filters on the title, keeps the newest report per
country, and handles the search returning either JSON or HTML, because FAS has
served it both ways.

Two outputs, deliberately separate:

- **The report index** — country, year, title, URL. Reliable, and useful alone: a
  per-country list of where the official account of that country's biotech
  position is written down.
- **`area_candidates`** — best-effort regex hits from report prose. **Never merged
  into the index**, and the run prints how many reports it could read a figure
  from and how many it could not. The reports are written by different attachés
  in different years; figures appear in tables, sentences and footnotes with no
  fixed form. Presenting a number for every country would imply they were all
  found the same way.

**A bug caught in testing.** The crop-context window looked 60 characters ahead,
which attributed "55.2 million hectares of biotech crops, of which soybean..." to
soybean — when that figure is the national total. The crop that qualifies a figure
precedes it, so the window now looks backward only. Retested: the total comes
back with no crop, and the 34.9M correctly attaches to soybean.

### A correction on geoBoundaries

The GitHub Download-ZIP of geoBoundaries contains **no geometry** — every
`.geojson` is ~130 bytes of Git LFS pointer, because the ZIP button does not
resolve LFS. Use the API or the LFS media URLs. CGAZ ADM0 is 401 MB regardless,
which is a fetched file rather than an embedded one.

**And the regime overlay needs no file at all**: the map already fetches cgaz
boundaries at runtime, so a classification table applied to them replaces the
1.1 MB `regime.geojson`.

### Centres of origin needs no digitising

I said it would. It does not. Khoury et al. 2016 defines its 23 eco-geographic
regions **purely by country membership** — Table S2 lists the countries in each,
Table S1 maps crops to regions, both on Dryad at doi:10.5061/dryad.s08t2. The
overlay is country polygons dissolved into 23 groups: same technique as the
regime layer, same geometry, no licensed source and no digitising.

**Three of the five overlays are now country-level joins onto boundaries the map
already loads** — regime, centres of origin, and cultivation area.

---

## Round 78 — the concurrency group was dropping scheduled runs

    Canceling since a higher priority waiting request for commit-main exists

Both workflows shared  so they would queue
instead of racing. **GitHub only lets one run WAIT per group** — a newer queued
run cancels the waiting one. So whenever releases queued behind wire, that wire
run was dropped entirely rather than delayed.

Each workflow now has its own group. The push race the shared group was guarding
against is already handled better by the retry added in round 41: on a rejected
push the job resets to origin/main and re-harvests. That is robust to
collisions, so serialising the two bought nothing and cost scheduled runs.

---

## Round 79

**450 points: 420 industry, 25 escapes, 5 curated.** Nineteen entries.
Coordinate/place check clean across 425.

    rules 75  seed 60  editing 45  animals 33  clinical 31  repro 30
    money 27  synthesis 26  escape 25  cro 24  livestock 24  deextinct 24
    wild 21  ogtr 5

Several of these exist to complicate the map rather than reinforce it:

- **The Nuffield Council** concluded in 2018 that heritable genome editing
  *could* be ethically acceptable in some circumstances. Citing them honestly
  means citing that. The map is more useful for holding a considered position it
  does not simply endorse.
- **UK Biobank.** Access by approved application rather than purchase, with
  analyses returned to the resource. That is materially different from a company
  owning a dataset outright, and it is the clearest available answer to what the
  alternative to enclosure looks like in human genomics.
- **IMPC** is knocking out every protein-coding gene in the mouse and publishing
  the phenotypes — the most systematic vertebrate engineering ever undertaken,
  publicly funded, openly documented. Both the best documentation in that facet
  and its largest single undertaking.
- **Norway's sovereign fund** publishes its ethical exclusions *with reasoning*.
  For anyone pursuing the shareholder route this map keeps pointing at, that is
  the worked example of a documented divestment argument.

And several that sharpen it:

- **Cargill.** Private, so it publishes far less than any listed company here,
  and it handles a very large share of the world's traded grain. **The single
  largest mover of engineered crop output discloses the least about it.** Read
  beside ADM, which is listed: the same activity is documented or not depending
  on whether shares are traded, not on policy.
- **The FDA Modernization Act** removed the statutory requirement to test drugs
  in animals. **The requirement is gone and the practice largely continues**,
  because regulators still expect the data and sponsors still supply it. A law
  changing and nothing changing is worth documenting precisely.
- **Organic Seed Alliance.** Most organic growers use conventional untreated seed
  under exemptions, because organic seed is unavailable in the varieties they
  need. Seed supply is a quieter lever on that sector than any biosafety rule.
- **Tome / programmable integration.** Carve-outs for gene editing rest on
  nothing foreign being added. Inserting a whole gene lands back inside the
  transgenic definition — **the first technique in years moving in that direction
  rather than out of it.**
- **Scribe.** Proteins designed rather than discovered are not covered by patents
  on naturally occurring systems, which is part of the point. The patent fight is
  being routed around by building tools that were never anyone's to claim.
- **ASTA** maintains the voluntary database gene-edited varieties are listed in
  where no notification is required. **The public record of what is planted is
  kept by the sector planting it** — a fact about the regulation, not the
  companies.

---

## Round 80 — organisation type

**Facets say what part of the industry a body works in. They never said what
KIND of body it is** — and a ministry, a committee, a company and a campaign
group are not the same thing to argue with.

Every industry point now carries an `otype`, **derived from its own name and base
record rather than hand-tagged**, so it stays consistent across 420 entries and
re-derives when entries change. Nine types, every point classified, none left
over:

    #f2c14e  Companies                    211
    #6fa8dc  Ministries & agencies         53
    #76c893  Institutes & universities     50
    #c9a227  Funds & foundations           25
    #9fb3c8  Registers & databases         25
    #4db6ac  Intergovernmental bodies      18
    #e08a5f  Trade associations            16
    #d96ba0  NGOs & campaigns              12
    #8e7cc3  Committees & councils         10

Industry squares are now coloured by type, with a checkbox and colour swatch per
type under the three kind toggles. Escapes and releases keep their own ramps,
because neither is an organisation — and the type filter is skipped for them
rather than hiding them when a type is switched off.

Classifier order matters and is commented: an IGO that is also a "commission"
reads as an IGO, and a company with "research" in its name does not become an
institute. Verified: 9 types, 9 distinct colours, 0 industry points unclassified,
and switching companies off leaves 239 of 450 drawn.

### Wire lead

Six edits, each verified. The roadside-spraying and canola-dormancy sentences
deleted; the concession and the escape cases merged into one paragraph; "Seeds
and pollen do not stay where you put them"; "watching or even defining"; **"Nobody
knows the true ecological impacts of all of these combined"** added after the
resistance clause; "And, worst of all, containment has demonstrably failed"; and
the close is now **"And, of course, the organisms themselves have no say in all of
this. They are born simply because a company decided which trait would sell, and
they are released into a world that had no part in the decision either — all
because the corporate couldn't learn its place."**

854 words, nine paragraphs, down from 1,034.

---

## Round 81 — harvest the facets that have registers

Asked to reach 100% across every facet. Hand-entry cannot: assisted reproduction
alone is tens of thousands of clinics. But that is the wrong method for the
facets with the worst ratios, **because three of them have registers.**

### Clinical, from sample to coverage

`harvest/clinical_sponsors.py`. ClinicalTrials.gov requires registration of
essentially every interventional trial run in or submitted to the US, and its v2
API is open and keyless. The script runs ten queries — "gene therapy" alone
misses cell therapy and editing trials that never use the phrase — dedupes on
NCT number, and aggregates **by sponsor**: one point per organisation, carrying
trial count, phase spread, recruiting status and the country of its most frequent
trial location.

That takes the clinical facet from ~31 hand-written entries, which was about 1%,
to whatever the register holds. New source family `clinical:sponsor`.

The entry text makes the point the register itself makes: **it exists because a
law requires it, after sponsors were found abandoning trials with unfavourable
results unpublished. Every other facet on this map is argued about with figures
the industry chose to release; this one is not.**

What it does not claim: to be the world. Trials run entirely outside the US
regulatory orbit may never register, and China is under-represented relative to
its actual programme. The output note says so.

Blocked from the sandbox by the allowlist, so the fetch is unverified. The
aggregation is not — exercised offline: 5 studies with a duplicate NCT collapse
to 4 unique across 3 sponsors, the unplaceable country is dropped rather than
guessed, phases and sponsor class map correctly.

### The honest position on 100%

Three facets can reach effective completeness for their scope, and all three by
harvester rather than by typing:

- **Escapes** — 25 → ~420 once `contamination_register.py` runs. Near-complete
  for 1997–2013.
- **Animals** — 33 → ~1,000 once `animal_facilities.py` runs. Complete for the US.
- **Clinical** — 31 → the register, once this one runs.

**None of the three has executed anywhere with real network yet.** They are worth
more than another twenty rounds of hand-entry, and they cost one workflow run.

The rest — seed, contract research, reproduction, money — have no register
anywhere, so those stay a sample however long I work on them, and the map should
keep saying which is which.

**30 source families.** All route correctly.

---

## Round 82 — wording, panel order, overlays

### "Escape" is gone

**The word framed the organism as a fugitive, which is the wrong relationship:
nothing chose to leave.** Replaced throughout with **spread**, and with narrower
words where they fit better — stray plants rather than escaped plants, dispersal
pathway rather than escape pathway, loss of containment rather than escape from
containment.

    Documented spread & unauthorised releases     (was: escapes)
    Spread & contamination                        (facet category)
    Red diamond — a documented case of spread or contamination
    <b>Spread</b> — what got out of the field       (kind toggle)

Swept across `escape_records.json`, all 22 entry modules, `build.py`, `facets.py`
and `content.py`. **46 instances of the string remain in the built file and every
one is accounted for**: 44 internal keys (`escape:crop`, `data-kind="escape"`,
`escape_records`), which are identifiers rather than prose, and 2 uses of the
Escape key. The wire's search terms keep the word deliberately — journalists
write it, so the feed has to match it.

**One bug the rename caused, and the builder caught it.** Renaming an entry broke
its `PLACES` key, so it silently failed to geocode and the map went 450 → 449
points. The builder names its own misses rather than dropping them quietly, which
is why that took thirty seconds instead of never being noticed.

### Help panel reordered

Now: **Reading the markers** → **The map key** → **The map** → Left rail → Right
rail. The two sentences about the world plate and the satellite cross-fade moved
up to open Reading the markers, which is where they belong — they describe what
you are looking at, not how to navigate it.

Deleted the place-name row sentence. Navigation now reads: **"Click any area
outside of the region, or the unit's name in the top-centre row, to go back up."**

### Click-outside-to-go-up already worked

Checked before changing anything. `map.on('click')` already steps up a level when
you click outside the current unit's boundary: at country level it returns to the
world, at sub-unit level it pops one level, and clicking a drawn sub-unit descends
instead. Nothing needed doing.

### Overlays on by default

They were opt-in because they used to be placeholders. Two are now built from
real geometry and the rest fail quietly when their file is absent, so there is
nothing left to protect the reader from. Checkboxes ship checked and a load
handler switches the layers on to match.

### The guide PDFs

The run-together words — "Thenational biosafetyregulator" — are in the **figure
images**, not the text layer, and the PDFs were produced by Qt with subsetted
fonts and no recoverable source. **I cannot fix them by editing the files.** They
would need regenerating from whatever produced the diagrams. Flagged rather than
attempted, because a half-repaired PDF is worse than a known-broken one.

---

## Round 83 — wording again, and seventeen entries

### Three more words out

**"Stray" and "loss of containment" imply the organism belonged somewhere and got
away. "Contamination" implies it dirtied something clean.** All three carry a
judgement about the organism rather than about the decision that moved it.

    stray plants          →  self-sown plants
    loss of containment   →  spread from the site
    contamination         →  unauthorised presence
    contaminated          →  carrying engineered material
    contaminate           →  put engineered genes into

**"GM Contamination Register" stays as written.** It is the register's actual
name, and renaming someone else's title would be a different kind of inaccuracy.

Eight instances remain in the built file, all accounted for: internal keys and
the wire's search terms, which keep the word because journalists write it and the
feed has to match.

**One thing the sweep broke and I caught.** It rewrote `cross-contamination`
inside a wire keyword list into `cross-unauthorised presence`, which would have
stopped that term matching anything. Restored. **A blanket replace across a file
that contains both prose and search terms will always do this** — the guard list
now protects proper names and term lists explicitly.

### On the guide figures

I looked for the script. The three transcripts in this workspace are all
GMO-map sessions and none contains it; the only guide-building code in them is
the per-country resistance PDFs from the original source map, which is a
different set. **If I wrote those two guides it was in another conversation, and
that conversation's build code is not here.** I can rebuild the two diagrams from
what is visible, or rebuild the guides properly if you point me at that session.

### Entries

**466 points: 436 industry, 25 spread records, 5 curated.** Seventeen entries into
the thinnest facets: wild 21 → 23, deextinct 24 → 27, cro 24 → 27, livestock
24 → 27.

    rules 77  seed 60  editing 45  animals 34  clinical 31  repro 30
    money 28  synthesis 27  cro 27  livestock 27  deextinct 27
    spread 25  wild 23  ogtr 5

- **RNA pesticides.** Nothing living is altered, so no biosafety framework
  applies; the mechanism is sequence-specific, so pesticide assumptions do not
  fit. **Both categories were built for something else, and the product sells
  while the question of which governs it stays open.**
- **GBIRd.** Islands are chosen for gene-drive mice because a drive should stay
  put. But mice reach islands on boats, which is how they arrived — so the
  containment argument rests on the same transport that defeated it before.
- **The Florida panther.** Genetic rescue that worked, decades ago, by moving
  animals rather than editing them. Any engineered rescue has to explain what it
  adds over translocation, and that comparison is rarely made explicit.
- **Emulate.** The law now permits non-animal methods and regulators still expect
  animal data. **The constraint stopped being legal and became conventional**,
  which is harder to change and gets far less attention.
- **Sexed semen.** Most dairy calves born are female and the male calves that
  were the by-product are simply not conceived. It reduces a welfare problem by
  removing the animals from existence — a real improvement, named precisely.
- **Testbiotech.** That a handful of staff constitute most of the independent
  technical scrutiny of EFSA dossiers in the world's largest import market is a
  fact about the scrutiny, not about them.
- **Kew's Millennium Seed Bank.** The wild relatives taking up engineered genes
  are the same material stored there. A bank of what a population used to be is
  the only reference a later change can be measured against.

---

## Round 84 — the wording fixed by hand, not by sweep

The previous blanket replace did real damage that only showed up on inspection.
**It rewrote a URL, two Google News search queries, and a technical term that had
nothing to do with genetic engineering.** Every instance is now handled
individually.

### Repaired — the swap should never have touched these

    http://www.unauthorised presenceregister.org/
      → http://www.gmcontaminationregister.org/          (a live URL)

    %22GM%20unauthorised presence%22
      → %22GM%20contamination%22                          (a search query)

    "gm unauthorised presence", "carrying engineered material"
      → "gm contamination", "contaminated"                (wire search terms)

    "...used to test injectable drugs and devices for bacterial
     unauthorised presence"
      → "...for bacterial contamination"

That last one is the horseshoe crab endotoxin test. **Bacterial contamination in
a sterility assay is a technical term about pathogens, not about engineered
organisms**, and the sweep had no business inside it.

### Applied — the new words, where they fit

    "...a combination nobody bred, made by self-sown plants breeding with
     each other."
      → "...made by breakout plants breeding with each other."

    "Spread & unauthorised presence"        → "Spread & cross-breeding"
    "🧬 Unauthorised presence & spread"     → "🧬 Cross-breeding & spread"
    "cat": "Unauthorised presence record"  → "cat": "Spread record"

    "Red diamond — a documented case of spread or unauthorised presence,
     placed where the material was found."
      → "...a documented case of spread or cross-breeding..."

    "The coexistence rules, the unauthorised presence disputes and the organic
     sector's losses are all documented there."
      → "...the cross-breeding disputes and the organic sector's losses..."

    "This is not unauthorised presence of a crop but of the source of the crop."
      → "This is not cross-breeding into a crop but into the source of
         the crop."

    "...where a unauthorised presence or drift claim is filed..."
      → "...where a cross-breeding or drift claim is filed..."

    "the difference between ‘we think there is unauthorised presence’ and a
     result that survives challenge"
      → "the difference between ‘we think there is GM material in this’ and a
         result that survives challenge"

    "the only dedicated global record of GM unauthorised presence and
     illegal-release incidents"
      → "...record of GM cross-breeding and illegal-release incidents"

    "cases of unauthorised presence"
      → "cases of cross-breeding and unapproved planting"

**Where "cross-bred" did not fit, it was not forced.** Several records are about
an unapproved variety turning up in a food supply or an export shipment, where
nothing cross-bred with anything — those read "unapproved planting" or say
plainly what was found. The category name pairs the two: **Spread &
cross-breeding**.

Zero instances of the old wording remain. 466 points, scripts clean.

---

## Round 85 — every revision, from the original

Diffed against the repo copy you uploaded rather than reciting from memory. That
surfaced **one string the earlier sweep had mangled and I had not caught**:

    "guarantee an accession is available to you, or that it is uncontaminated"
      → (broken)  "...or that it is uncarrying engineered material"
      → (fixed)   "...or that it is free of engineered genes"

`uncontaminated` is one word, so a replace on `contaminated` ate the prefix. It
was in a tool description in the panel copy — exactly the place the user asked me
to check, and exactly where my own scans had been looking only at the help panel
and wire lead rather than every prose block in the file.

### The complete list, original → final

**Panel and key copy**

    "Red diamond — a documented escape or contamination incident, placed where
     the material was found."
      → "Red diamond — a documented case of spread or cross-breeding, placed
         where the material was found."

    "...together with recorded escapes and unauthorised releases..."
      → "...together with recorded spread and unauthorised releases..."

    "Biosafety & Contamination + Interpretive — the independent scientists
     re-reading the dossier."
      → "Biosafety & Spread + Interpretive — ..."

    "...read the claims that would be asserted against a farmer whose crop is
     contaminated."
      → "...against a farmer whose crop is carrying engineered material."

    "CAN'T: guarantee an accession is available to you, or that it is
     uncontaminated."
      → "...or that it is free of engineered genes."

    "FOR: the difference between ‘we think there is contamination’ and a result
     that survives challenge is usually which method was used."
      → "...between ‘we think there is GM material in this’ and a result that
         survives challenge..."

    "CAN: show that escape is routine rather than exceptional."
      → "CAN: show that spread is routine rather than exceptional."

    "Courthouses — where a consent is challenged by judicial review, where a
     contamination or drift claim is filed..."
      → "...where a cross-breeding or drift claim is filed..."

    "This is also where the regulatory escape happens: organisms made by editing
     rather than insertion."
      → "This is also where the regulatory evasion happens: ..."

**Wire lead**

    "...a combination nobody bred, made by escaped plants breeding with
     each other."
      → "...made by breakout plants breeding with each other."

    "Worse yet, containment has demonstrably failed, and escapes are
     irreversible — there is no undoing it."
      → "And, worst of all, containment has demonstrably failed, and the spread
         is irreversible — there is no undoing it, ever."

    "...wild plant relatives at centres of origin are being contaminated, like
     introgressed wild cotton..."
      → "...introgressed wild cotton was found to hold less genetic variety than
         its unmodified neighbours..."

**Source families and layer labels**

    "Escapes & contamination"                → "Spread & cross-breeding"
    "Documented escapes & unauthorised releases"
                                             → "Documented spread & unauthorised releases"
    "Escapes — what got out"                 → "Spread — what got out of the field"
    "🧬 Contamination & escapes"              → "🧬 Cross-breeding & spread"
    "cat": "Contamination record"            → "cat": "Spread record"
    "Incidents where engineered material was found where it had not been
     authorised"                             → "Cases where..."

**Records**

    "GM Contamination Register — the global escape record"
      → "GM Contamination Register — the global record of spread"

    "The only dedicated global record of GM contamination and illegal-release
     incidents"
      → "...record of GM cross-breeding and illegal-release incidents"

    "Grass, transgene escape into wild relatives"
      → "Grass, transgene spread into wild relatives"
    "Ornamental fish, escape into wild waters"
      → "Ornamental fish, spread into wild waters"
    "Escaped, eradication abandoned"       → "Spread; eradication abandoned"
    "escaped from ornamental fish farms"   → "spread from ornamental fish farms"
    "escape from containment"              → "spread from the site"
    "routine escapes"                      → "routine losses from pens"
    "the pet trade as a release pathway"   → "the pet trade as a dispersal pathway"
    "contamination incident"               → "case of cross-breeding or unapproved planting"
    "This is not contamination of a crop but of the source of the crop"
      → "This is not cross-breeding into a crop but into the source of the crop"
    "the contamination disputes and the organic sector's losses"
      → "the cross-breeding disputes and the organic sector's losses"
    "accepting grain would contaminate its seed stock"
      → "accepting grain would put engineered genes into its seed stock"

**Deliberately unchanged**

    "GM Contamination Register"        the register's actual name
    gmcontaminationregister.org        a live URL
    "bacterial contamination"          a sterility term about pathogens, in the
                                       horseshoe-crab endotoxin entry
    wire search terms and stop-list    journalists write these words, so the
                                       feed has to match them
    escape:crop, data-kind="escape"    internal identifiers, never displayed
    e.key === 'Escape'                 the keyboard key

**69 occurrences remain in the built file and all 69 are in that last group.**
Zero prose.

### Guides

`how-to-change-the-industry.pdf` replaced with your revised version.
**`how-to-stop-a-release.pdf` is unchanged** — the only revised file uploaded was
the industry-and-law guide, so the release guide still has the run-together
words in its figures.

---

## Round 86 — the wire lead was only about farming

Eight new paragraphs after the no-say close, widening from GM agriculture to the
whole industry. **1,404 words, 17 paragraphs**, up from 855 and 9.

Written from the same position as the rest, and built to show rather than tell —
every paragraph carries a mechanism or a number rather than an adjective:

- **Synthesis.** A handful of companies write most of the world's made-to-order
  DNA and screen orders against a dangerous-sequence list **because they agreed
  among themselves to** — no government requires it, and a meaningful share of
  world capacity sits outside the group that agreed. Nothing at all covers who
  may buy the cutting proteins; they are sold from a catalogue.
- **The materials gate.** Plasmid repositories, cell-line banks and reagent
  suppliers all require a verified institutional account. **"You can read the
  method for nothing. You cannot buy the materials."**
- **Contractors.** The company named on a permit often did none of the work.
  Follow the contractors instead of the clients and the industry is far more
  concentrated than its company list suggests — dozens of sponsors, a handful of
  laboratories — and the safety evidence a regulator assesses was paid for by the
  applicant and produced by a contractor whose next contract depends on that same
  industry.
- **Animals as reagents.** Catalogues run to thousands of mouse strains, each a
  lineage bred to be ill in a particular way. Mice, rats and birds bred for
  research are not animals under the US Animal Welfare Act — the overwhelming
  majority used, counted nowhere. Then: **"Pet cloning engages no biosafety
  framework at any point, because nothing foreign was added and the rules have
  nothing to catch."**
- **Deliberate release.** Insects by the hundred million; microbes across
  millions of acres generating no register entry because a microbe on a seed is
  neither a plant nor planted; and gene drives designed to push a change through
  a wild population **"with nobody releasing anything ever again."**
- **Money.** Venture funds need an exit inside the life of the fund, which
  rewards speed and scale over caution. Public money pays for the underlying
  science and the results end up private property. Philanthropy is among the
  largest funders of deployment in low-income countries. Defence agencies fund
  work outside civilian biosafety oversight in every country that does it.
- **Rules.** Trade associations exist so positions no single company wants
  attributed to it can still be advanced. Whole classes of organism are being
  moved outside registration. **"That does not make them safer. It makes them
  unrecorded."**
- **The close**, which is also the answer to why regulators and registers are
  mapped as part of the industry rather than as a check on it: **"The same chain
  that ends in a salmon fillet ends in a gene therapy, and in an embryo."**

Zero banned words in the new text. Placement, div balance and script parsing all
verified.

**One thing worth recording about the insert.** The anchor failed first time
because the closing paragraph holds a literal ’ rather than a `\u2019` escape —
the same class of near-miss as the curly apostrophe that broke a `PLACES` key.
**Grep the target before anchoring on remembered text.**

---

## Round 87 — corrections to the corrections

### A misattribution I need to own

I listed this as a wording change I made:

    "wild plant relatives at centres of origin are being contaminated, like
     introgressed wild cotton, which was found to hold less genetic variety than
     its unmodified neighbours, and Mexican wild cotton, which is now listed as
     vulnerable with gene flow from crops being the main threat"
      → "introgressed wild cotton was found to hold less genetic variety than
         its unmodified neighbours, and Mexican wild cotton is now listed as
         vulnerable, with gene flow from crops being the main threat."

**It was not a contamination-wording change. It was the rewrite you asked for
directly in round 82**, and I folded it into the wording list where it did not
belong. The two happened in the same session and I conflated them.

### Contamination is not the same as spread — you were right

**Contamination covers three routes and only one is cross-breeding:**

1. **Cross-breeding** — pollen carries an engineered gene into a related plant
   (Oregon bentgrass, Oaxacan maize, wild cotton).
2. **Mixing** — no breeding at all; seed or grain physically mixed in storage,
   transport or handling (StarLink, Japanese port canola, Triffid flax, Bt10).
3. **Unapproved planting** — someone grew it without authorisation (Gujarat 2001,
   Ukraine, Brazil, Paraguay).

So "Spread record" was wrong. Corrected:

    "cat": "Spread record"    →  "cat": "Cross-breeding & mixing record"
    "Spread & cross-breeding" →  "Cross-breeding & drift"
    "🧬 Cross-breeding & spread"  →  "🧬 Cross-breeding & drift"
    "a documented case of spread or cross-breeding"
      → "a documented case of drift, cross-breeding or mixing"

### Drift where drift is better

**Drift** for pollen and seed on the move; **spread** kept for organisms that
establish and keep going on their own.

    "Grass, transgene spread into wild relatives"
      → "Grass, transgene drift into wild relatives"
    "Spread through transport rather than through cultivation"
      → "Drift through transport rather than through cultivation"

Unchanged, because the organism establishes rather than drifts: "Ornamental
fish, spread into wild waters", "spread from ornamental fish farms", and the
gene-drive language.

### The farmer sentence

The whole point of it is a farmer who never bought the seed, and my version lost
that:

    "read the claims that would be asserted against a farmer whose crop is
     carrying engineered material"
      → "...against a farmer whose crop picked up an engineered gene he
         never planted"

### Two reverts

    "Biosafety & Spread + Interpretive"
      → "Biosafety & Cross-breeding + Interpretive"      (names the family as named)

    "This is also where the regulatory evasion happens"
      → "This is also where the regulatory escape happens"

The second is about a rule being slipped, not an organism. **"Escape" is only
banned where it describes a living thing** — applying the ban to regulation was
over-correction.

    "This is not cross-breeding of a crop but of the source of the crop"
      → "This is not just cross-breeding into a crop but into the source of
         the crop"

---

## Round 88 — reverted, and a workflow ceiling

### The wording is back to the original

Everything reverted except **"escapes"** and **"escapees"**, which stay replaced.
Where a phrase contained "escapes", the rest of it reverted but that word did
not — so "Escapes & contamination" comes back as **"Spread & contamination"**.

Restored: contamination / contaminated / contaminate, escape / escaped, "escape
from containment", "escape pathway", "release pathway", and every sentence I had
rewritten around them. Gone entirely: breakout plants, self-sown, unauthorised
presence, cross-breeding, spread from the site, dispersal pathway, "free of
engineered genes", "carrying engineered material", and the drift substitutions.

Final audit: **0 occurrences of "escapes" or "escapees"; 35 contamination-family
words and 53 uses of escape/escaped back in place; 0 traces of the intermediate
wording.** 466 points, 0 problems.

Two near-misses on the way back, both the same class as before: the Norwegian
entry's name carries a `\u2014` escape in source rather than a literal dash, so
the revert missed it and the `PLACES` key went out of alignment again; and two
sentences lived in `escape_records.json` rather than a module. **Both were caught
by the builder naming its own misses and by checking each string after the
rebuild rather than trusting the replace count.**

### Why the run took over two hours

`releases.yml` had **no time bound anywhere** — not on the job, not on any step —
and I had added five new harvesters to it without one. Any of them can hang: the
GMO-free crawler sleeps between requests, the FAS harvester fetches report after
report, and the clinical sponsor harvester pages through ten queries against an
API that can be slow.

Two ceilings now:

- **`timeout-minutes: 35` on the job.** Nothing here is worth an unbounded wait,
  and **a job that never finishes also never commits what the earlier steps did
  get** — which is the real cost.
- **A `timeout Nm` on each of the ten harvester calls**, sized to what each
  should need: 8m for APHIS and the clinical sponsors, 6m for the two crawlers,
  4–5m for the rest, 2m for the builders. One slow source can no longer eat the
  whole budget, and each still ends in `|| echo "… failed or timed out —
  continuing"` so the run carries on and commits what it has.

---

## Round 88 — reverted, and the two-hour run explained

### Wording reverted in full

Every change from rounds 82–87 is back to the original, in both the panel copy
and the entry descriptions: escape, escapes, escaped, contamination,
contaminated, contaminate, "Escapes & contamination", "Contamination record",
"🧬 Contamination & escapes", "Escapes — what got out", "Biosafety &
Contamination + Interpretive", and every sentence listed in round 85.

**Zero instances of the replacement wording remain** — checked against the full
list: breakout plants, self-sown, unauthorised presence, cross-breeding & drift,
cross-breeding & mixing, free of engineered genes, spread from the site, "picked
up an engineered gene he never planted". All gone. 104 occurrences of
escape/contamination restored.

**Kept, because they were separate requests rather than wording changes:** the
"And, worst of all" opening, the wild-cotton sentence rewrite, "Nobody knows the
true ecological impacts of all of these combined", the new industry-wide section,
and "regulatory escape" (which was itself a revert).

The revert took four passes because the source files escape characters
differently — `\u2014` in some places and a literal em dash in others, the same
trap as the apostrophe. **Verify against the built file, not the source.**

### The two-hour run

**The version running in your repo is not the one I fixed.** The repo copy has:

    concurrency:
      group: commit-main        ← shared with the wire workflow
    (no timeout-minutes, no per-command timeouts)

The version in this batch has:

    concurrency:
      group: releases           ← its own group
    timeout-minutes: 35
    timeout 5m python3 harvest/cfia_approvals.py || echo "..."
    timeout 8m python3 harvest/aphis_releases.py || echo "..."
    ...ten commands, each individually capped

So the run showing over two hours is almost certainly **waiting, not working** —
sitting in the shared `commit-main` queue behind the wire job, which runs every
six hours. GitHub counts queue time as elapsed time. That is exactly the round-78
bug, and the fix is in `.github/workflows/releases.yml` in this batch, unuploaded.

Upload it and cancel the stuck run. If a future run genuinely does hang, the job
now dies at 35 minutes and the log names which harvester ate the time.

---

## Round 89 — escape → drift or spread, contamination untouched

Judged per instance rather than swapped wholesale, because the two words do not
mean the same thing:

**SPREAD** — an organism reached somewhere and kept going: bred, established,
built a population.

    "made by escaped plants breeding with each other"
      → "made by spreading plants breeding with each other"
    "The strongest documented case of transgene escape into wild plant
     communities anywhere"
      → "...transgene spread into wild plant communities anywhere"
    "escaped from ornamental fish farms and established breeding populations"
      → "spread from ornamental fish farms and established breeding populations"
    "Atlantic salmon...have escaped from Chilean farms in very large numbers"
      → "...have spread out of Chilean farms in very large numbers"
    "established itself through escape from containment nobody was required to
     design for permanence"
      → "...through spread out of pens nobody was required to design for
         permanence"
    "they entered wild populations through routine escapes over decades"
      → "...through routine spread out of pens over decades"
    "and escapes are irreversible"  →  "and the spread is irreversible"

**DRIFT** — pollen, seed or grain carried somewhere by wind, water or handling.
Material moved; nothing established.

    "a documented escape or contamination incident"
      → "a documented drift or contamination incident"
    "Escape through transport rather than through cultivation"
      → "Drift through transport rather than through cultivation"
    "Escape from a public research programme rather than a company trial"
      → "Drift from a public research programme rather than a company trial"
    "CAN: show that escape is routine rather than exceptional"
      → "CAN: show that drift is routine rather than exceptional"

**Labels name both, because the layer holds both.**

    "Escapes & contamination"                → "Spread, drift & contamination"
    "🧬 Contamination & escapes"             → "🧬 Contamination, drift & spread"
    "Documented escapes & unauthorised releases"
                                             → "Documented spread, drift &
                                                unauthorised releases"
    "GM Contamination Register — escapes & illegal releases"
                                             → "...— spread, drift & illegal
                                                releases"
    "Escapes — what got out"                 → "Spread & drift — what got out"
    "— the global escape record"              → "— the global drift and spread
                                                record"
    "Escaped, eradication abandoned"         → "Spread; eradication abandoned"
    "Norwegian Institute of Marine Research — escape monitoring"
                                             → "— spread monitoring"

**Left as "escape":** the regulatory sense — "This is also where the regulatory
escape happens" — which is about a rule being slipped rather than an organism,
plus every internal key, which is never displayed. **Two prose instances remain
and both are that.**

**Contamination is untouched: 35 occurrences, exactly as before.**

### The same bug again, in reverse

Renaming the Norwegian entry, I updated the `PLACES` coordinate key and not the
entry itself, so it failed to geocode and the map went 466 → 465. Last time the
mismatch ran the other way. **Both halves of a rename have to move together**, and
the builder naming its own misses is the only reason either was caught.
