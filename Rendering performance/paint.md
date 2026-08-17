[[Rendering performance/layout]] [[Rendering performance/composite]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# paint

> Pixel-filling stage after layout — text, colors, borders, shadows, images recorded into layers for compositing.

```txt
        paint ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Checks whether you can rank CSS property cost (layout vs paint vs composite) …

## Sources
- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Reduce the scope and complexity of style calculations](https://web.dev/articles/reduce-the-scope-and-complexity-of-style-calculations) — overview

## Key Concepts
- **Core:** Once geometry is known, paint builds draw lists (and rasters) for visible con…

## Technical Details
```
Layout complete
    │
    ▼
Paint records (fill, stroke, text, images)
    │
    ▼
Layers → Composite (GPU)
```

| Cheap (composite) | Medium (paint) | Expensive (layout + paint) |
|-------------------|----------------|----------------------------|
| `transform`, `opacity` | `background-color`, `box-shadow` | `width`, `top`, `font-size` |

```css
.animated { will-change: transform; } /* sparingly */
```

```javascript
function updateVisual(state) {
  requestAnimationFrame(() => {
    el.style.transform = `translateX(${state.x}px)`;
  });
}
```

1. Rendering → Paint flashing
2. Layers panel — promotion and memory
3. Performance — Paint / Raster slices

| Symptom | Check | Fix |
|---------|-------|-----|
| Full-screen green flash | Broad selectors / stacking | Narrow invalidation; avoid hover on `*` |
| Memory climb | Too many layers | Remove excess `will-change` |
| Blurry text after move | Subpixel transform | Snap to integer pixels when possible |
| Scroll jank + fixed background | `background-attachment: fixed` | Pseudo-element layer instead |

## Mistakes to Avoid
- **Mistake:** `will-change` on everything
- **Mistake:** Profiling only desktop — mobile GPUs amplify paint cost
- **Mistake:** Ignoring print stylesheets

## Pros/Cons or Trade-offs
- **Pro:** Paint-only updates are cheaper than layout when geometry is stable.
- **Con:** Pretty effects (huge blurs/shadows) are still expensive — especially on mobile GPUs.

## Comparison
- vs [[Rendering performance/composite]]: paint draws into layers; composite merges layers.
- vs [[Rendering performance/INP]]: paint time is part of presentation delay after an interaction.


### Use cases
- Hover states on a dense data grid: `box-shadow` on every cell repainted huge …
