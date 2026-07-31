# GMO-map

A live global map of the paper trail behind the genetic-engineering industry —
the registers where releases are applied for and consented, the dossiers behind
them, the record of what has escaped, the patents asserted over living material,
and the people and institutions holding the arrangement to account.

Not an argument against the science. An argument about a decision procedure that
runs on a commercial timetable, on self-generated evidence, with liability that
does not reach the harm and enforcement that cannot cross a border.

---

## Repo layout

Everything `index.html` fetches is **relative to itself**, so nearly all of it
sits flat at the root. One real subfolder.

```
GMO-map/
├─ index.html                  the map — must be at root for Pages
├─ .nojekyll                   stops Pages' Jekyll pass touching the files
├─ trackerdata.json            per-country resource directory
├─ projects.json               release layer  (or projects.json.gz — see below)
├─ wire.json                   news wire archive
├─ wire_climate.json           optional second wire stream (absent = ignored)
├─ legmap_sub.json             optional subnational resources
├─ overlays/                   context overlay polygons — see overlays/README.md
├─ harvest/
│   ├─ wire_harvest.py         RSS harvester → wire.json
│   ├─ aphis_releases.py       APHIS release permits → projects.json
│   ├─ projects_curated.json   hand-written records, merged by the above
│   ├─ bch_focal_points.py     CBD focal-point list → trackerdata stubs
│   └─ check_links.py          link rot + staleness report
├─ .github/workflows/
│   ├─ wire.yml                runs the wire harvester every 6h and commits
│   └─ releases.yml            runs the APHIS harvester weekly and commits
├─ <country>.md / .pdf         optional per-country guides, ROOT level
└─ BUILD-NOTES.md              what was built, what's stubbed, what's next
```

Two things load from other repos and need nothing here:
administrative boundaries from `WelcomeToYourGalaxy/cgaz-boundaries`, and
facility dots from `WelcomeToYourGalaxy/executive-map`.

**Deploy:** Settings → Pages → source `main`, folder `/ (root)`.

---

## The data files

| file | state | notes |
|---|---|---|
| `trackerdata.json` | **seeded** | 18 countries, 35 entries, all verified |
| `projects.json` | **seeded** | 5 records, transcribed from OGTR licence pages |
| `wire.json` | empty `[]` | fills on the first workflow run |
| `wire_climate.json` | absent | optional; the map skips it silently |
| `legmap_sub.json` | absent | optional; the map skips it silently |
| `overlays/*.geojson` | absent | map prints "— not yet available", which is true |

### `projects.json`

```json
{ "projects": [ {
  "name": "...", "source": "ogtr:DIR-201", "type": "GM wheat field trial",
  "lat": -34.34, "lng": 138.92, "state": "South Australia",
  "precise": false, "impact": 2,
  "company": "...", "size": "1 site, max 2 ha/yr",
  "status": "Licence issued", "date": "2024-05-01",
  "url": "https://...", "desc": "...",
  "deadline": "2026-09-30"
} ] }
```

- `source` must start with a `PJ_SRC` key (`bch`, `ogtr`, `aphis`, `eu_release`,
  `cfia`, `ctnbio`, `conabia`, `geac`, `nzepa`, `oecd_biotrack`, `isaaa`,
  `contamination`, `clinical`, `seed`) — a `key:id` suffix is fine.
- `impact` 1–5 drives dot size and colour.
- `precise: false` draws a dashed ring. Use it whenever the register gives a
  district rather than a site — which is most of the time.
- `status` decides the consent-phase filter: anything matching
  *issued / granted / approved / permitted / construction* counts as consented,
  everything else as in review.
- `deadline` (optional) raises the countdown banner on the popup.
- `type` + `name` + `desc` feed the organism classifier.

If the file outgrows GitHub's size limit, commit `projects.json.gz` instead —
the loader tries the gzip first and handles both hosting behaviours.

### `wire.json`

A flat array. `iso` and `region` can be left empty; the map geo-tags from the
headline at render time.

```json
[ { "name": "GMWatch", "title": "...", "link": "https://...",
    "date": "2026-07-30T09:12:00+00:00", "snippet": "...",
    "iso": "", "region": "", "lang": "en", "sig": 0 } ]
```

---

## Harvesters

`harvest/wire_harvest.py` runs now — it reads the feed list straight out of
`index.html` so the feeds live in one place, merges with the existing archive so
a feed outage can't truncate it, dedupes on link, and keeps 120 days.

```bash
python3 harvest/wire_harvest.py     # stdlib only, no dependencies
```

`harvest/bch_focal_points.py` parses the CBD Secretariat's official BCH national
focal point list (`cbd.int/doc/lists/bch-fp.pdf`, 189 countries) into per-country
trackerdata stubs. It needs `pypdf`. It deliberately keeps only the institution
name and the institution's published website — the source PDF also carries named
officials, direct e-mail addresses and phone numbers, and the script asserts none
of that survives into its output. The stubs are a review queue: a human writes
the CAN / CAN'T / FOR description before anything is merged.

Note that bch.cbd.int itself is a JavaScript application and returns nothing to a
fetcher, which is why the PDF is the route.

`harvest/aphis_releases.py` harvests US environmental-release authorisations
from the APHIS BRS public data files — two CSVs, updated every business day,
public domain. It keeps only records with a `Rel -` component (import and
interstate movement are not releases), drops withdrawn, denied, superseded and
expired records, and drops anything past its expiration date.

```bash
python3 harvest/aphis_releases.py --dry-run   # summary, writes nothing
python3 harvest/aphis_releases.py             # writes projects.json
```

Hand-written records for registers with no bulk file live in
`harvest/projects_curated.json` and are merged in front of the harvested ones.
Edit them there, not in `projects.json`, which is overwritten on every run.

**A correction worth recording:** earlier notes here recommended starting with
OGTR, because it is the only register that publishes field-trial *site*
locations. That recommendation was made without checking, and it is wrong —
`ogtr.gov.au` disallows automated access in its robots.txt. Its records remain
the best in the world to read by hand; they cannot be harvested. APHIS
explicitly publishes a bulk file for reuse, so that is where the layer starts.
The rest of the manifest is in `BUILD-NOTES.md`.

---

## Keeping it true

Every entry carries a `checked` date, and the map shows it under each entry:
plain grey under a year, amber over a year, rust over two with "re-verify before
relying on it". This exists because 300+ hand-written entries go stale quietly —
registers move, agencies reorganise, and nothing about a stale entry looks wrong.

```bash
python3 harvest/check_links.py               # check every URL, report rot
python3 harvest/check_links.py --stale-only  # no network, just verification ages
python3 harvest/check_links.py --update-dates  # stamp today on entries that resolved
```

`--update-dates` is the weaker check and the tool says so: a URL resolving is not
the same as an entry being accurate. A ministry can be reorganised without its
domain moving. Treat the date as "this link worked", and re-read the description
when the amber turns up.

## Honest gaps, carried into the UI

- Contained use is under-recorded everywhere: most lab work is notified, not
  licensed, and notifications are rarely published individually.
- Gene-edited organisms are increasingly invisible by design. Where a
  jurisdiction has moved editing techniques outside GMO registration, there is
  no record to harvest — the absence of a dot means the law stopped requiring
  one. This is the largest structural gap and it is growing.
- Coordinates are the exception. Expect dashed rings to outnumber solid dots.
- The human side — germline, embryo selection, IVF and assisted reproduction —
  is not a release register and is not forced into the release layer. It lives
  in the lenses and the index.
- No coverage percentage is claimed anywhere. No dataset holds the true global
  count, so any figure would be invented.
