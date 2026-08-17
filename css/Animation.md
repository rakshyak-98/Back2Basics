[[scss]] [[Flash of Unstyled Content]] [[tailwindcss]] [[Javascript]] [[web capabilities]]

# Animation

> Smooth UI motion comes from animating compositor-friendly properties (`transform`, `opacity`) — layout-thrashing width/top updates drop frames.

```txt
        Animation ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about CSS/JS animation to see if you know the render pipelin…

## Sources
- [web.dev — Stick to compositor-only properties](https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count) — deep-dive
- [MDN — `will-change`](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change) — overview
- [MDN — `prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — overview

## Key Concepts
- **Pipeline:** JS → Style → Layout → Paint → Composite
- **Compositor-friendly:** `transform`, `opacity` (with a layer) → typical interview “GPU-friendly” answ…
- **Layout thrash:** interleaved geometry reads (`offsetHeight`) and style writes → forced synchro…
- **`will-change`:** hints layer promotion → overuse burns GPU memory.
- **FLIP:** measure First/Last, invert with transform, Play


- **Core:** Browsers update pixels through a pipeline

## Technical Details
```txt
JS → Style → Layout → Paint → Composite
         ↑              ↑
    expensive       cheaper if layer promoted
```

| Property change | Typical path | Cost |
|-----------------|--------------|------|
| `transform`, `opacity` | Composite (if promoted) | Low |
| `color`, `box-shadow` | Paint | Medium |
| `width`, `height`, `top`, `left`, `margin` | Layout → Paint → Composite | High |

### Prefer compositor-friendly CSS

```css
.card {
  transition: transform 200ms ease, opacity 200ms ease;
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
  opacity: 0.95;
}

/* Avoid: transition: width 200ms; — layout every frame */
```

### FLIP sketch

```javascript
const first = el.getBoundingClientRect()
// DOM change that would reflow...
const last = el.getBoundingClientRect()
const dx = first.left - last.left
const dy = first.top - last.top
el.style.transform = `translate(${dx}px, ${dy}px)`
el.style.transition = 'none'
requestAnimationFrame(() => {
  el.style.transition = 'transform 200ms ease'
  el.style.transform = ''
})
```

### Batch reads/writes

```javascript
const heights = items.map((el) => el.offsetHeight)
items.forEach((el, i) => {
  el.style.height = `${heights[i]}px`
})
```

### Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Janky scroll-linked motion | Main-thread long tasks | Prefer transform; `passive` listeners |
| GPU memory spike | Layer count | Drop excess `will-change` |
| Stutters every N ms | Layout in the loop | Profile; eliminate forced sync layout |
| Fine on desktop, bad on mobile | Blur/shadow/paint area | Simplify effects |
| CLS after animation | Layout-affecting exit | Animate transform/opacity; reserve space |

## Mistakes to Avoid
- **Mistake:** Leaving `will-change: transform` on everything permanently
- **Mistake:** Animating `filter: blur()` on large areas every frame
- **Mistake:** Ignoring `prefers-reduced-motion`
- **Mistake:** Transitioning `height: auto` without a measured pixel height str…

## Pros/Cons or Trade-offs
- **Pro:** Compositor animations stay smooth under modest main-thread load.
- **Con:** Not every design can avoid layout (height accordion) — measure carefully or use FLIP.
- **Con:** Too many layers (`will-change`, large blurs) exhausts mobile GPUs.

## Comparison
- vs [[Flash of Unstyled Content]]: FOUC is first-paint styling
- vs JS timers (`setInterval`): `requestAnimationFrame` syncs to refresh


### Use cases
- Card hover lifts, route transition shells, and list reorder animations (FLIP)…

- **Example:** A kanban board measures card positions, then animates `transform…
