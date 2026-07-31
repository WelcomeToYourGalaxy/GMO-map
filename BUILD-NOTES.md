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
