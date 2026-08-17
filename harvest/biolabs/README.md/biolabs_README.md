# Global BioLabs captures go here

BSL4 and BSL3+ laboratories worldwide, from the Global BioLabs project at
King's College London and the Schar School of Policy and Government.

## Why this is a folder of captures rather than a download

There is no file to download. The published report gives counts and country
scores and names no laboratory. The interactive map holds the facilities as a
Mapbox vector tileset, so there is nothing in the project's own repository to
read either.

The records are pulled out of the rendered map. `queryRenderedFeatures` returns
only what is currently drawn, so one capture misses whole continents - the first
one taken had 25 countries and no United States at all. Several captures from
different viewports are merged here, and the harvester deduplicates by name and
coordinates.

## How to capture

Open <https://global-biolabs.github.io/> directly, not the Squarespace page that
frames it. Open the browser console (F12). If Chrome refuses a paste, type
`allow pasting` first. Then run:

```js
(async () => {
  ['bsl4','bsl3plus','absl4','rbsl4'].forEach(l=>map.setLayoutProperty(l,'visibility','visible'));
  const seen = new Map();
  const views = [[-100,40],[20,20],[120,20],[0,0],[-60,-20],[140,-25]];
  for (const c of views) {
    map.jumpTo({center:c, zoom:2});
    await new Promise(r=>setTimeout(r,4000));
    map.queryRenderedFeatures({layers:['bsl4','bsl3plus','absl4','rbsl4']})
      .forEach(x=>{
        const k = x.layer.id+'|'+(x.properties.Name||'')+'|'+x.geometry.coordinates.join(',');
        if(!seen.has(k)) seen.set(k, {layer:x.layer.id, ...x.properties,
          lng:x.geometry.coordinates[0], lat:x.geometry.coordinates[1]});
      });
    console.log(c, 'running total', seen.size);
  }
  const rows = [...seen.values()];
  console.log('TOTAL:', rows.length);
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([JSON.stringify(rows)],{type:'application/json'}));
  a.download='biolabs.json'; a.click();
})();
```

Drop the downloaded file in this folder under any name. Adding a capture never
loses an earlier one; the harvester merges everything present.

## What to check

The current two captures give 154 facilities in 37 countries. The report counts
69 BSL4 and 57 BSL3+ facilities, and a facility can carry more than one level,
so a total in this range is right. A capture that returns markedly fewer
countries was taken before the tiles finished loading - wait longer between
hops rather than accepting it.
