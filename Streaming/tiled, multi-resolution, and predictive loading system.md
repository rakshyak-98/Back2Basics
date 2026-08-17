[[Streaming]] [[Buffer cache]] [[file descriptors]] [[webSocket]] [[Animation]] [[Frontend Datastructure]] [[Nginx internals]] [[Configuration]]

# tiled, multi-resolution, and predictive loading system

> tiled, multi-resolution, and predictive loading system — full image 16k×16k — never ship whole file to client

```txt
        tiled, multi-resol ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers ask about tiled, multi-resolution, and predictive loading system…

## Sources
- [Wikipedia — tiled, multi-resolution, and predictive loading system](https://en.wikipedia.org/wiki/tiled%2C_multi-resolution%2C_and_predictive_loading_system) — overview

## Key Concepts
- **Note:** **Multi-resolution pyramid:** each zoom level is downsampled by 2×

- **Note:** **Predictive loading:** prefetch ring around viewport in pan direction

- **Note:** **Formats:** DZI (Deep Zoom), IIIF (`/info.json` + `{region}/{size}/{rotation…

## Technical Details
```txt
Full image 16k×16k — never ship whole file to client

        Level 0 (1 tile)
       /    |    \
   Level 1 (2×2)
       …
   Level N (256×256 tiles at full resolution)

Client viewport → compute visible tile (z, x, y) → fetch only those + neighbors
```

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

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Blank tiles at zoom | Missing pyramid level | Regenerate z range; verify maxZoom in metadata |
| Wrong tile positions | Y axis flip (TMS vs XYZ) | `y_tms = (2^z - 1) - y_xyz` |
| 404 storm on pan | Bounds math off-by-one | Unit test tile coverage; clamp x/y |
| Memory crash mobile | Unbounded cache Map | LRU cap; revokeObjectURL; WebGL texture pool limit |
| Slow zoom | Fetching full res too early | Clamp max native zoom; overzoom last level with CSS |
| Stale tiles after update | CDN immutable | Version path `/dataset-v4/tiles/...` |
| CORS on tile CDN | Image canvas tainted | `crossOrigin="anonymous"` + ACAO header |

- **Mistake:** **HTTP/1.1 connection limit**
- **Mistake:** **Retina displays**
- **Mistake:** **Predictive fetch on metered data**
- **Mistake:** **Security on dynamic tiles**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Images < 2000px**
- **Con / skip when:** **Video**
- **Con / skip when:** **Vector maps at scale**

## Real-World Applications
- **Scenario:** Used wherever tiled, multi-resolution, and predictive loading system sits in …
