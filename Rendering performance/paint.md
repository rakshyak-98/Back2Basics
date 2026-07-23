[[Rendering performance/layout]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# Paint (repaint)

> Fill pixels after layout — text, colors, borders, shadows — **often split into layers for compositing**.

## Mental model

After [[Rendering performance/layout]], **paint** records **draw lists** per layer (what to draw where). GPU **composite** merges layers. Changing paint-only properties skips layout but still repaints.

```
Layout complete
    │
    ▼
Paint records (fill, stroke, text, images)
    │
    ▼
Layers → Composite (GPU)
```

Paint involves: text glyphs, backgrounds, borders, box-shadows, images — everything visible after geometry is known.

Changing a **layout property** forces layout **then** paint. Changing **color** often paint-only.

## Standard config / commands

### Property cost (rule of thumb)

| Cheap (composite) | Medium (paint) | Expensive (layout+paint) |
|-------------------|----------------|---------------------------|
| `transform`, `opacity` | `background-color`, `box-shadow` | `width`, `top`, `font-size` |

### Reduce paint area

```css
.animated {
  will-change: transform; /* promote layer — use sparingly */
}

.fixed-header {
  transform: translateZ(0); /* legacy layer hint — prefer will-change */
}
```

### DevTools paint debugging

1. **Rendering** → **Paint flashing** (green flashes = repaints)
2. **Layers** panel — see promoted layers, memory cost
3. **Performance** trace — **Paint** and **Raster** slices

### Optimize large shadows and blurs

```css
/* Heavy — repaints large region */
.card { box-shadow: 0 0 60px rgba(0,0,0,.5); filter: blur(20px); }

/* Lighter — pseudo-element with opacity animation on transform */
```

### `requestAnimationFrame` for visual updates

```javascript
function updateVisual(state) {
  requestAnimationFrame(() => {
    el.style.transform = `translateX(${state.x}px)`;
  });
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Full-screen green flash | Whole page repaints | Reduce layer count; fix hover rules on `*` |
| Memory climb | Too many layers | Remove excessive `will-change` |
| Text blurry after animate | Subpixel transform | Snap to integer px |
| Scroll jank with fixed bg | `background-attachment: fixed` | Use pseudo-element layer |
| Canvas + DOM overlap | Duplicate paint | Single surface or isolate iframe |

## Gotchas

> [!WARNING]
> **`will-change` on everything** — each layer consumes GPU memory; mobile OOM and worse perf.

- **Invalidation propagates** — parent opacity change may repaint children.
- **`border-radius` + overflow** — expensive clipping paths.
- **Print styles** — separate paint path; don't profile screen only for print bugs.

## When NOT to use

- Don't micro-optimize paint on static marketing pages with no interaction — [[Rendering performance/INP]] and LCP dominate.

## Related

[[Rendering performance/layout]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Flash of Unstyled Content]]
