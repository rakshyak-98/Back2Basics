[[Rendering performance/layout]] [[Rendering performance/composite]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# paint

> Pixel-filling stage after layout — text, colors, borders, shadows, images recorded into layers for compositing.





## Interview Relevance
Checks whether you can rank CSS property cost (layout vs paint vs composite) and debug repaints with paint flashing / Layers in DevTools.

## Sources
- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Reduce the scope and complexity of style calculations](https://web.dev/articles/reduce-the-scope-and-complexity-of-style-calculations) — overview

## Core Definition
Once geometry is known, paint builds draw lists (and rasters) for visible content. Changing a paint-only property skips layout but still costs GPU/CPU work proportional to the invalidated area.

## Recall Cues
- Why do interviewers care about Checks whether you can rank CSS property cost (layout vs paint vs composite) and debug repaints with paint flashing / Layers in DevTools?
- What is step 1: Rendering → Paint flashing?
- What is step 2: Layers panel — promotion and memory?
- What is step 3: Performance — Paint / Raster slices?
- What mistake is **`will-change` on everything — layer memory blowups and sometimes slower scrolling**?
- What mistake is **Profiling only desktop — mobile GPUs amplify paint cost**?
- What mistake is **Ignoring print stylesheets — separate paint path when print bugs appear**?

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

DevTools:

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
- `will-change` on everything — layer memory blowups and sometimes slower scrolling.
- Profiling only desktop — mobile GPUs amplify paint cost.
- Ignoring print stylesheets — separate paint path when print bugs appear.

## Comparison
- vs [[Rendering performance/composite]]: paint draws into layers; composite merges layers.
- vs [[Rendering performance/INP]]: paint time is part of presentation delay after an interaction.

## Real-World Applications
Hover states on a dense data grid: `box-shadow` on every cell repainted huge regions. Switching to a border/outline on a single highlight layer cut paint time.

## Pros/Cons or Trade-offs
- **Pro:** Paint-only updates are cheaper than layout when geometry is stable.
- **Con:** Pretty effects (huge blurs/shadows) are still expensive — especially on mobile GPUs.
