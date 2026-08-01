# Context overlays

Areas, not points. Off by default in the map key. Filenames must match the `k`
values in `PJ_OVERLAYS` inside `index.html`.

Format: a plain `FeatureCollection`. The popup reads `properties.name` (falling
back to `NAME`, then `title`), so give every feature one.

```json
{ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "properties": { "name": "Mesoamerican centre \u2014 maize (indicative)" },
      "geometry": { "type": "Polygon", "coordinates": [[[-104,22],[-96,22],[-96,15],[-104,15],[-104,22]]] } }
  ] }
```

---

## The eight layers, and where each comes from

Ordered by how easily each can actually be built.

### `trials.geojson` — Field trial density
**Buildable today, from data you already have.** Aggregate `projects.json` by
state or country and emit one polygon per unit with a count in `properties.name`.
No external source needed, and it updates whenever the harvester runs. Start
here: trials precede cultivation by years, so this is the nearest thing to a
forward view of where the industry's footprint will spread.

### `protected.geojson` — Protected areas & wild-relative habitat
**Ready-made.** The World Database on Protected Areas via Protected Planet
(`protectedplanet.net`), maintained by UNEP-WCMC and IUCN, downloadable by
country. Enormous — clip and simplify hard before committing. Attribution is
required and commercial redistribution restricted; check the terms.

### `genebanks.geojson` — Genebanks & seed collections
**Ready-made, but points.** Genesys (`genesys-pgr.org`) and FAO WIEWS publish
institute records with coordinates. Points render as markers rather than filled
areas, which looks different from the rest — either accept that or buffer them
into small circles on export.

### `regime.geojson` — Regulatory regime by country
**Must be built, and worth the most.** One shaded world layer classifying each
country by how it decides what counts as a regulated organism: by technique, by
trait, or not at all. Sources are the national frameworks already described in
the map's own entries, plus the Cartagena Protocol party list. Join to country
boundaries and dissolve. This is the layer that explains why the map looks
different in different places — and why an empty area can mean deregulation
rather than absence.

### `cultivation.geojson` — Approved GM cultivation area
**Must be built.** No dataset holds this as geometry. Country level can be
assembled from national approval registers joined to country boundaries.
Sub-nationally it exists only where an agricultural census publishes it — USDA
NASS is the main example. Anything finer would be estimated; don't ship it as
though it were measured.

### `infrastructure.geojson` — Seed & breeding infrastructure
**Must be built, by hand.** Where the industry physically is rather than where
its products grow: the Hawaiian seed nurseries, counter-season multiplication in
Chile and Argentina, the Dutch vegetable-breeding cluster. Concentrated in very
few places. Company site listings and agricultural statistics are the sources;
there is no register.

### `centres_origin.geojson` — Centres of crop origin & diversity
**Must be built.** No canonical polygon file exists. Vavilov's centres have
several competing versions, and the modern quantitative treatment (Khoury et al.
2016, *Proc. R. Soc. B*) defines regions by country and subregion rather than by
geometry. Take those definitions, join to country or admin-1 boundaries,
dissolve, and put **"indicative"** in every feature name — it reaches the popup,
and these boundaries are genuinely contested.

### `gmofree.geojson` — GMO-free zones & regional bans
**Must be built.** The GMO-free Regions network (`gmo-free-regions.org`) holds
the European directory; US county bans are documented individually. Neither
publishes geodata. Geocode declarations against admin-1/admin-2 boundaries, and
record the declaring body and date in the feature name, because these lapse and
get overturned.

---

**These files are deliberately absent from the repo.** A missing overlay makes
the map print "— not yet available" beside the toggle, which is accurate. An
empty `FeatureCollection` would render a silent no-op layer that looks like data.
Ship a file only once it holds real geometry.
