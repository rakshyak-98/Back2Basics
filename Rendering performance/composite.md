[[Rendering performance/paint]] [[Rendering performance/layout]] [[Rendering performance/critical rendering path]] [[css/Animation]]

# composite

> Compositing merges painted layers into the final frame — the cheap last step when animations only change transform or opacity.

```txt
        composite ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Frontend performance reviews ask why `transform` / `opacity` stay smooth w…

## Sources
- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Stick to compositor-only properties](https://web.dev/articles/stick-to-compositor-only-properties) — overview

## Key Concepts
- **Core:** After layout and paint, the browser (often on a compositor thread / GPU) stac…

## Technical Details
```
Style → Layout → Paint → Composite → pixels on screen
                              ↑
              transform/opacity-only updates can jump here
```

| Prefer for animation | Avoid for 60 fps motion |
|----------------------|-------------------------|
| `transform: translate/scale/rotate` | `top`, `left`, `margin` |
| `opacity` | `width`, `height`, `padding` |

```css
.drawer {
  transform: translateX(0);
  transition: transform 200ms ease;
  will-change: transform; /* only while animating / known hot path */
}
```

- Factors that hurt compositing performance:

1. Too many promoted layers (GPU memory, bookkeeping).
2. Animating properties that force layout or paint every frame.
3. Large overlapping layers that still invalidate frequently.

## Mistakes to Avoid
- **Mistake:** Animating `top`/`left` “because CSS”
- **Mistake:** Putting `will-change: transform` on every card
- **Mistake:** Assuming composite fixes [[Rendering performance/INP]]

## Pros/Cons or Trade-offs
- **Pro:** Smooth motion with a small main-thread budget — critical on mid-tier phones.
- **Con:** Layer explosion from blanket `will-change` — memory pressure and sometimes worse jank.

## Comparison
- vs [[Rendering performance/paint]]: paint fills pixels into layers; composite combines layers.
- vs [[Rendering performance/layout]]: layout computes geometry


### Use cases
- Mobile nav drawer and toast animations: animate `transform`/`opacity` so scro…
