[[Rendering performance/paint]] [[Rendering performance/composite]] [[Rendering performance/refresh rate]] [[Rendering performance/INP]] [[css/Animation]]

# layout

> Browser geometry pass (reflow) — compute sizes and positions after style, before paint.

```txt
        layout ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Staff frontend reviews probe layout thrashing (`offsetWidth` read/write lo…

## Sources
- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Avoid large, complex layouts](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing) — deep-dive
- [MDN — CSS containment](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment) — overview

## Key Concepts
- **Global-ish cost:** one width change can ripple through descendants (and sometimes ancestors) → t…
- **Forced synchronous layout:** reading geometry (`offsetWidth`, `getBoundingClientRect`) after DOM writes fl…
- **Skip layout when possible:** animate `transform` / `opacity` so the compositor handles motion (see [[Rende…
- **Containment:** `contain: layout` / `content-visibility: auto` limits how far reflow spreads …


- **Core:** Layout turns the render tree into a box model: where each element sits and ho…

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

- DevTools: Performance → Layout events

## Mistakes to Avoid
- **Mistake:** `getBoundingClientRect()` in hot scroll/input paths without cach…
- **Mistake:** `contain: strict` everywhere
- **Mistake:** Animating `top`/`left` for motion that `transform` could handle

## Pros/Cons or Trade-offs
- **Pro:** Correct responsive geometry — essential for documents and complex UI.
- **Con:** Easy to accidentally schedule every frame under interaction load → hurts [[Rendering performance/INP]].

## Comparison
- vs [[Rendering performance/paint]]: layout decides boxes; paint fills them.
- vs CLS: layout shifts that are visible to users become CLS; same engine stage, different metric.


### Use cases
- Dashboard with expandable rows: measuring each row height while writing style…
