[[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# Layout (reflow)

> Browser calculates geometry — sizes and positions of elements — **render pipeline stage between style and paint**.

## Mental model

**Layout** (reflow) computes where boxes go. One element's size can ripple up and down the tree — **layout is often global** within a subtree.

```
Style recalc → Layout → Paint → Composite
                  ↑
        triggered by geometry-changing properties
        (width, height, font-size, offsetTop read+write, …)
```

| Triggers layout | Usually skips layout |
|-----------------|----------------------|
| `width`, `height`, `padding`, `border` | `transform`, `opacity` |
| DOM insert/remove | `filter` (may paint only) |
| Font load | `will-change: transform` |
| Reading `offsetWidth` after write | compositor-only animations |

Example: `<body>` width change reflows descendants.

## Standard config / commands

### Avoid layout thrashing (read/write interleave)

```javascript
// Bad — forces sync layout each iteration
els.forEach(el => {
  el.style.width = el.offsetWidth + 10 + 'px';
});

// Good — batch reads, then writes
const widths = els.map(el => el.offsetWidth);
els.forEach((el, i) => { el.style.width = widths[i] + 10 + 'px'; });
```

### Prefer transform for movement

```css
.moved {
  transform: translateX(100px); /* compositor thread, no layout */
}
```

### CSS containment (limit reflow scope)

```css
.card {
  contain: layout style paint;
}
```

### `content-visibility` (defer off-screen layout)

```css
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

### DevTools

- **Performance** → **Layout** events in flame chart
- **Rendering** tab → **Layout Shift Regions** (CLS related)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Jank on scroll | Sticky + height reads | `passive: true` listeners; avoid layout in scroll |
| ResizeObserver loop error | Feedback resize | Debounce; don't set size from observer blindly |
| Slow list filter | Re-layout 10k nodes | Virtual list; `key` stability |
| CLS on font swap | Layout shift metric | `size-adjust`, reserve space |
| Animation stutters | Animating `top/left` | Switch to `transform` |

## Gotchas

> [!WARNING]
> **`getBoundingClientRect()` in hot path** forces layout if DOM dirty — cache per frame.

- **Tables** — auto layout is expensive; fixed table-layout or flex/grid for perf-critical UI.
- **Subpixel rounding** — repeated layout can cause 1px jitter in responsive designs.
- **iframe** — layout in child doesn't always isolate parent cost.

## When NOT to use

- Don't `contain: strict` on everything — breaks positioning (`position: fixed` descendants).

## Related

[[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]
