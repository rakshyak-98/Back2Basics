[[Architectures]]

# H3 (Hexagonal Hierarchical Spatial Index)

> H3 maps lat/lng to hexagon IDs — bucket nearby points for density, surge, and spatial joins. **Uber**.

## Mental model

**Say it in one breath:** Pick a resolution; every point becomes a hex cell id; neighbors and parents/children are cheap.

```txt
lat,lng ──► H3 index (res N) ──► aggregate / join / heatmap
                 │
                 ├─ parent (coarser)
                 └─ children (finer)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Cell** | One hexagon bucket | “We count events per cell.” |
| --- | --- | --- |
| **Resolution** | Cell size knob | “Higher res = smaller hexes.” |
| **k-ring** | Neighbor cells | “Surge looks at ring around the rider.” |
| **Compact** | Merge children → parent | “Store less for large areas.” |

## Standard config / commands

```python
import h3
cell = h3.latlng_to_cell(37.77, -122.42, 9)
neighbors = h3.grid_disk(cell, 1)
parent = h3.cell_to_parent(cell, 7)
```

| Knob | Why it matters |

| Resolution | Too coarse hides hotspots; too fine = sparse counts |
| --- | --- |
| `grid_disk` | Neighbor queries without GIS joins |
| Same res in joins | Don’t join res-8 to res-10 blindly |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Empty heatmaps | Res too fine / few events | Coarser res or longer window |
| Edge artifacts | Polygon ≠ hex cover | Use polyfill; accept boundary fuzz |
| Join mismatch | Different resolutions | Normalize to one res |
| Slow polyfill | Huge polygons | Simplify geom; lower res |

## Gotchas

> [!WARNING]
> **Hex ≠ exact geography** — coastlines and political borders won’t match cell edges.

> [!WARNING]
> **Resolution drift** — mixing res in one metric doubles or splits counts.

## When NOT to use

- **Legal parcel boundaries** — use real GIS polygons.
- **One-off distance between two points** — haversine is enough.

## Related

[[Architectures]] [[System Architecture]]
