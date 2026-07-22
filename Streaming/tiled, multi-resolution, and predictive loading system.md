[[Streaming]] [[Buffer cache]] [[file descriptors]] [[webSocket]]

# tiled, multi-resolution, and predictive loading system

> Deep-zoom / tiled media streaming: pyramid levels, viewport fetch, and prefetch — maps, PDF viewers, microscopy, satellite imagery.

---

## Mental model

```txt
Full image 16k×16k — never ship whole file to client

        Level 0 (1 tile)
       /    |    \
   Level 1 (2×2)
       …
   Level N (256×256 tiles at full resolution)

Client viewport → compute visible tile (z, x, y) → fetch only those + neighbors
```

**Multi-resolution pyramid:** each zoom level is downsampled by 2×; tiles are fixed size (256 common in Deep Zoom, TMS, Slippy map conventions).

**Predictive loading:** prefetch ring around viewport in pan direction; cancel in-flight fetches on rapid zoom change.

**Formats:** DZI (Deep Zoom), IIIF (`/info.json` + `{region}/{size}/{rotation}/{quality}.jpg`), map `{z}/{x}/{y}.png`, MBTiles offline bundle.

---

## Standard config / commands

### Tile coordinate math (Web Mercator / slippy)

```javascript
function lonLatToTile(lon, lat, z) {
  const n = 2 ** z;
  const x = Math.floor((lon + 180) / 360 * n);
  const latRad = lat * Math.PI / 180;
  const y = Math.floor((1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2 * n);
  return { z, x, y };
}
```

### Viewport → tile list

```javascript
function tilesForBounds(bounds, z, tileSize = 256) {
  const min = lonLatToTile(bounds.west, bounds.north, z);
  const max = lonLatToTile(bounds.east, bounds.south, z);
  const tiles = [];
  for (let x = min.x; x <= max.x; x++)
    for (let y = min.y; y <= max.y; y++)
      tiles.push({ z, x, y });
  return tiles;
}
```

### CDN / cache headers

```nginx
location ~ ^/tiles/(?<z>\d+)/(?<x>\d+)/(?<y>\d+)\.webp$ {
  add_header Cache-Control "public, max-age=31536000, immutable";
  # Tiles content-addressed or versioned by dataset id: /v3/tiles/...
}
```

### IIIF request (standard in cultural heritage / medical imaging)

```txt
GET {base}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}
Example: /image/abc/full/800,/0/default.jpg
```

### Client prefetch pattern

```javascript
const cache = new Map(); // key: `${z}/${x}/${y}`
const inflight = new Map();

async function loadTile(z, x, y, priority = 'high') {
  const key = `${z}/${x}/${y}`;
  if (cache.has(key)) return cache.get(key);
  if (inflight.has(key)) return inflight.get(key);

  const p = fetch(`/tiles/${z}/${x}/${y}.webp`, { priority })
    .then(r => r.blob())
    .then(blob => { cache.set(key, blob); inflight.delete(key); return blob; });
  inflight.set(key, p);
  return p;
}

// On pan end: prefetch 1-tile halo in velocity direction
```

### Server generation (pyramid build)

```bash
# vips / gdal / imagemagick — run offline in batch job
vips dzsave huge.tif output --tile-size 256 --overlap 0 --suffix .webp
# Output: output.dzi + output_files/
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank tiles at zoom | Missing pyramid level | Regenerate z range; verify maxZoom in metadata |
| Wrong tile positions | Y axis flip (TMS vs XYZ) | `y_tms = (2^z - 1) - y_xyz` |
| 404 storm on pan | Bounds math off-by-one | Unit test tile coverage; clamp x/y |
| Memory crash mobile | Unbounded cache Map | LRU cap; revokeObjectURL; WebGL texture pool limit |
| Slow zoom | Fetching full res too early | Clamp max native zoom; overzoom last level with CSS |
| Stale tiles after update | CDN immutable | Version path `/dataset-v4/tiles/...` |
| CORS on tile CDN | Image canvas tainted | `crossOrigin="anonymous"` + ACAO header |

---

## Gotchas

> [!WARNING]
> **HTTP/1.1 connection limit** — hundreds of tile requests parallelize poorly; HTTP/2, domain sharding (legacy), or sprite sheets for small sets.

> [!WARNING]
> **Retina displays** — may need `@2x` tile size or higher z; clarify in API contract.

> [!WARNING]
> **Predictive fetch on metered data** — respect `navigator.connection.saveData`.

> [!WARNING]
> **Security on dynamic tiles** — signed URLs or auth cookie; tiles leak data if guessable x/y/z.

---

## When NOT to use

- **Images < 2000px** — single responsive `srcset` sufficient.
- **Video** — HLS/DASH segment streaming, not static tile pyramid.
- **Vector maps at scale** — MVT (Mapbox Vector Tiles) not raster pyramid.

---

## Related

[[Buffer cache]] · [[Animation]] · [[Frontend Datastructure]] · [[Nginx internals]] · [[Configuration]]
