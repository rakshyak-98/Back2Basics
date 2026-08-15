[[Rendering performance/paint]] [[Rendering performance/layout]] [[Rendering performance/critical rendering path]] [[css/Animation]]

# composite

> Compositing merges painted layers into the final frame — the cheap last step when animations only change transform or opacity.

## Interview Relevance

Frontend performance interviews ask why `transform` / `opacity` stay smooth while `top` / `width` jank: compositor-only properties skip layout and paint.

## Sources

- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — deep-dive
- [web.dev — Stick to compositor-only properties](https://web.dev/articles/stick-to-compositor-only-properties) — overview

## Core Definition

After layout and paint, the browser (often on a compositor thread / GPU) stacks layers in z-order. Updates that only change how layers are combined can avoid redoing geometry and pixel fill.

## Key Concepts

- **Layers:** painted surfaces that can move independently → more layers can mean less full-frame paint, but cost memory and management.
- **Compositor-only properties:** typically `transform` and `opacity` (and some filters, depending on browser) → ideal for scroll-linked and UI motion.
- **Promotion:** `will-change: transform` or 3D translate hints can put an element on its own layer → helps hot animations; hurts if overused.
- **Overlap / order:** correct stacking matters for overlapping UI — compositor applies layers in the right order every frame.

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

Factors that hurt compositing performance:

1. Too many promoted layers (GPU memory, bookkeeping).
2. Animating properties that force layout or paint every frame.
3. Large overlapping layers that still invalidate frequently.

## Real-World Applications

Mobile nav drawer and toast animations: animate `transform`/`opacity` so scrolling and gestures stay responsive even when the main thread is busy.

## Pros/Cons or Trade-offs

- **Pro:** Smooth motion with a small main-thread budget — critical on mid-tier phones.
- **Con:** Layer explosion from blanket `will-change` — memory pressure and sometimes worse jank.

## Comparison

- vs [[Rendering performance/paint]]: paint fills pixels into layers; composite combines layers.
- vs [[Rendering performance/layout]]: layout computes geometry; composite should not need new geometry for transform-only moves.

## Mistakes to Avoid

- Animating `top`/`left` “because CSS” — forces layout + paint every frame.
- Putting `will-change: transform` on every card — promote only what moves.
- Assuming composite fixes [[Rendering performance/INP]] — long JavaScript still blocks input handling.
