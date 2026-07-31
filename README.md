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
│   └─ wire_harvest.py         RSS harvester → wire.json
├─ .github/workflows/
│   └─ wire.yml                runs the harvester every 6h and commits
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

The release harvesters are specified but not written. Start with **OGTR** — it
is the only register on Earth that publishes field-trial *site* locations, so it
is the only feed that yields solid dots rather than dashed rings on day one.
The full manifest is in `BUILD-NOTES.md`.

---

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
