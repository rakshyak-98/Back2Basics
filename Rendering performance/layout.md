[[Rendering performance/paint]] [[Rendering performance/composite]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# layout

> Browser geometry pass (reflow) — compute sizes and positions after style, before paint.

## Interview Relevance

Staff frontend interviews probe layout thrashing (`offsetWidth` read/write loops), why `transform` beats `top`, and CSS containment / `content-visibility` for large pages.

## Sources

- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Avoid large, complex layouts](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing) — deep-dive
- [MDN — CSS containment](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment) — overview

## Core Definition

Layout turns the render tree into a box model: where each element sits and how large it is. Changing geometry can force reflow of a whole subtree — often the most expensive step before paint.

## Key Concepts

- **Global-ish cost:** one width change can ripple through descendants (and sometimes ancestors) → treat layout as potentially O(tree).
- **Forced synchronous layout:** reading geometry (`offsetWidth`, `getBoundingClientRect`) after DOM writes flushes pending layout immediately → thrashing when done in a loop.
- **Skip layout when possible:** animate `transform` / `opacity` so the compositor handles motion (see [[Rendering performance/composite]]).
- **Containment:** `contain: layout` / `content-visibility: auto` limits how far reflow spreads or defers off-screen work.

## Technical Details

```
Style recalc → Layout → Paint → Composite
                  ↑
        geometry-changing properties and DOM size changes
```

| Triggers layout | Usually skips layout |
|-----------------|----------------------|
| `width`, `height`, `padding`, `border` | `transform`, `opacity` |
| DOM insert/remove | many `filter` cases (still may paint) |
| Font load / size | compositor-only animations |
| Read `offsetWidth` after write | batched reads then writes |

```javascript
// Bad — forces sync layout each iteration
els.forEach((el) => {
  el.style.width = el.offsetWidth + 10 + 'px';
});

// Good — batch reads, then writes
const widths = els.map((el) => el.offsetWidth);
els.forEach((el, i) => {
  el.style.width = widths[i] + 10 + 'px';
});
```

```css
.card { contain: layout style paint; }
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
.moved { transform: translateX(100px); }
```

DevTools: Performance → Layout events; Rendering → Layout Shift Regions (CLS-related).

## Real-World Applications

Dashboard with expandable rows: measuring each row height while writing styles caused jank. Batching measurements and using `content-visibility` on off-screen panels fixed scroll FPS.

## Pros/Cons or Trade-offs

- **Pro:** Correct responsive geometry — essential for documents and complex UI.
- **Con:** Easy to accidentally schedule every frame under interaction load → hurts [[Rendering performance/INP]].

## Comparison

- vs [[Rendering performance/paint]]: layout decides boxes; paint fills them.
- vs CLS: layout shifts that are visible to users become CLS; same engine stage, different metric.

## Mistakes to Avoid

- `getBoundingClientRect()` in hot scroll/input paths without caching per frame.
- `contain: strict` everywhere — breaks `position: fixed` descendants and sticky patterns.
- Animating `top`/`left` for motion that `transform` could handle.
