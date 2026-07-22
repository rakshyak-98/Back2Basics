[[css]] [[JavaScript]] [[webSocket]]

# Animation

> Browser animation performance: stay on the **compositor** (transform/opacity), avoid **layout thrash** — **Paul Lewis / high-performance animations** + Chrome rendering pipeline.

---

## Mental model

Rendering pipeline (simplified):

```txt
JS → Style → Layout → Paint → Composite
         ↑              ↑
    expensive       cheaper if layer promoted
```

| Property change | Typical path | Cost |
|-----------------|--------------|------|
| `transform`, `opacity` | Composite only (if promoted) | **Low** — GPU-friendly |
| `color`, `box-shadow` | Paint | Medium |
| `width`, `height`, `top`, `left`, `margin` | Layout → Paint → Composite | **High** — layout thrash |

**Compositor layer:** promoted element gets own texture; GPU translates/scales/ fades without reflowing neighbors.

**Layout thrash:** read geometry (`offsetHeight`, `getBoundingClientRect`) then write style in interleaved loop → forced synchronous layout (FSL) every iteration.

```txt
BAD:  for each el: el.style.width = el.offsetWidth + 1 + 'px'
GOOD: batch reads → batch writes (or use transform)
```

**`will-change`:** hints promotion; overuse → memory blowup (each layer = texture RAM).

---

## Standard config / commands

### Prefer compositor-friendly CSS

```css
.card {
  /* Animate these */
  transition: transform 200ms ease, opacity 200ms ease;
  will-change: transform; /* remove after animation ends in JS */
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.95;
}

/* Avoid animating layout props */
/* transition: width 200ms;  ← triggers layout every frame */
```

### FLIP technique (layout change without jank)

```javascript
const first = el.getBoundingClientRect();
// DOM change that would layout...
const last = el.getBoundingClientRect();
const dx = first.left - last.left;
const dy = first.top - last.top;
el.style.transform = `translate(${dx}px, ${dy}px)`;
el.style.transition = 'none';
requestAnimationFrame(() => {
  el.style.transition = 'transform 200ms ease';
  el.style.transform = '';
});
```

### Batch DOM reads/writes

```javascript
// Read phase
const heights = items.map(el => el.offsetHeight);
// Write phase
items.forEach((el, i) => { el.style.height = `${heights[i]}px`; });
```

### DevTools checks

```txt
Chrome Performance → enable "Screenshots" + "Layout Shift"
Look for purple "Layout" blocks during animation
Rendering tab → "Paint flashing" / "Layer borders"
```

### `requestAnimationFrame` for JS-driven animation

```javascript
function tick(t) {
  el.style.transform = `translateX(${progress(t)}px)`;
  if (!done) requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Janky scroll-linked animation | Main thread long tasks | Move to transform; offload work; `passive: true` listeners |
| Fan spin / GPU memory spike | Layer count | Remove excess `will-change`; avoid promoting huge elements |
| Animation stutters every N ms | GC or layout in loop | Profile Performance tab; eliminate FSL |
| Works desktop, dies mobile | Too many paints / layers | Reduce blur/shadow animation; simplify |
| `position: fixed` jank during scroll | Compositor + scroll mismatch | `transform: translateZ(0)` sparingly; check containing block |
| CLS after animation | Layout-affecting exit | Animate transform/opacity; reserve space |

---

## Gotchas

> [!WARNING]
> **`will-change: transform` on everything** — mobile Safari/Chrome may exhaust GPU memory; toggle only during active animation.

> [!WARNING]
> **Animating `filter: blur()`** — expensive paint every frame; use pre-blurred asset or limit duration.

> [!WARNING]
> **`height: auto` transitions** — cannot interpolate smoothly without JS measurement → layout thrash.

> [!WARNING]
> **Third-party widgets** forcing layout in scroll handlers — audit with Performance → Bottom-Up → "Layout".

---

## When NOT to use

- **Reduced motion users** — respect `prefers-reduced-motion: reduce`; provide instant state change.
- **Critical path LCP element** — don't animate hero image/container until after LCP.
- **Heavy box-shadow on large lists** — paint cost scales with pixels; use border or static shadow image.

---

## Related

[[scss]] · [[JavaScript]] · [[web capabilities]] · [[Progressive search functionality]]
