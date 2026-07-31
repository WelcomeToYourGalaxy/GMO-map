# Context overlays

Areas, not points. Off by default in the map key. Filenames must match the `k`
values in `PJ_OVERLAYS` inside `index.html`.

Format: a plain `FeatureCollection`. The popup reads `properties.name` (falling
back to `NAME`, then `title`), so give every feature one. Nothing else in the
properties is used.

```json
{ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "properties": { "name": "Mesoamerican centre \u2014 maize (indicative)" },
      "geometry": { "type": "Polygon", "coordinates": [[[-104,22],[-96,22],[-96,15],[-104,15],[-104,22]]] } }
  ] }
```

---

## Where each one comes from

Only one of the five exists as a ready-made download. The rest have to be built,
and the honest way to build them is by joining a published *list* to
administrative boundaries you already have.

### `protected.geojson` — Protected areas & wild-relative habitat
**Ready-made.** The World Database on Protected Areas, via Protected Planet
(`protectedplanet.net`). Authoritative, maintained by UNEP-WCMC and IUCN,
downloadable by country or globally. Enormous — clip to the countries you care
about and simplify hard before committing. Check the terms; attribution is
required and commercial redistribution is restricted.

### `genebanks.geojson` — Genebanks & seed collections
**Ready-made, but points.** Genesys (`genesys-pgr.org`) and FAO WIEWS both
publish institute records with coordinates. `L.geoJSON` will render points as
markers rather than filled areas, which looks different from the other four —
either accept that or buffer the points into small circles before export.

### `centres_origin.geojson` — Centres of crop origin & diversity
**Must be built.** There is no canonical polygon file. Vavilov's centres are a
historical construct with several competing versions, and the modern
quantitative treatment (Khoury et al. 2016, *Proc. R. Soc. B*, "Origins of food
crops connect countries worldwide") defines regions of diversity by country and
subregion rather than by geometry. So: take their region definitions, join to
country or admin-1 boundaries, dissolve. Put **"indicative"** in every feature
name — it reaches the popup, and these boundaries are genuinely contested.

### `gmofree.geojson` — GMO-free zones & regional bans
**Must be built.** The GMO-free Regions network (`gmo-free-regions.org`)
maintains the European directory of declared regions and municipalities; US
county cultivation bans are documented individually rather than centrally.
Neither publishes geodata. Geocode the declarations against admin-1/admin-2
boundaries. Record the declaring body and the date in the feature name, because
these lapse and get overturned.

### `cultivation.geojson` — Approved GM cultivation area
**Must be built, and hardest of the five.** No dataset holds this as geometry.
At country level it can be assembled from national approval registers joined to
country boundaries. Sub-nationally it exists only where an agricultural census
publishes it — USDA NASS is the main example. Anything finer than that would be
estimated, so don't ship it as if it were measured.

---

**These files are deliberately absent from the repo.** A missing overlay makes
the map print "— not yet available" beside the toggle, which is accurate. An
empty `FeatureCollection` would instead render a silent no-op layer that looks
like data. Ship a file only once it holds real geometry.
