[[Architectures]] [[System Architecture]]

# H3 (Hexagonal Hierarchical Spatial Index)

> H3 maps lat/lng to hexagon IDs — bucket nearby points for density, surge, and spatial joins. **Uber**.

```txt
        H3 (Hexagonal Hier ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** H3 shows spatial indexing literacy

## Sources
- [Uber blog — H3](https://www.uber.com/blog/h3/) — overview
- [H3 docs](https://h3geo.org/docs/) — deep-dive

## Key Concepts
```txt
lat,lng ──► H3 index (res N) ──► aggregate / join / heatmap
                 │
                 ├─ parent (coarser)
                 └─ children (finer)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Cell** | One hexagon bucket | “We count events per cell.” |
| **Resolution** | Cell size knob | “Higher res = smaller hexes.” |
| **k-ring** | Neighbor cells | “Surge looks at ring around the rider.” |
| **Compact** | Merge children → parent | “Store less for large areas.” |

## Technical Details
```python
import h3
cell = h3.latlng_to_cell(37.77, -122.42, 9)
neighbors = h3.grid_disk(cell, 1)
parent = h3.cell_to_parent(cell, 7)
```

| Knob | Why it matters |
|------|----------------|
| Resolution | Too coarse hides hotspots; too fine = sparse counts |
| `grid_disk` | Neighbor queries without GIS joins |
| Same res in joins | Don’t join res-8 to res-10 blindly |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty heatmaps | Res too fine / few events | Coarser res or longer window |
| Edge artifacts | Polygon ≠ hex cover | Use polyfill; accept boundary fuzz |
| Join mismatch | Different resolutions | Normalize to one res |
| Slow polyfill | Huge polygons | Simplify geom; lower res |

## Mistakes to Avoid
- **Mistake:** Hex ≠ exact geography
- **Mistake:** Resolution drift

## Pros/Cons or Trade-offs
- **Trade-off:** Legal parcel boundaries — use real GIS polygons.
- **Trade-off:** One-off distance between two points — haversine is enough.
