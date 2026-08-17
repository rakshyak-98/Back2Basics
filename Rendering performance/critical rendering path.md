[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/composite]] [[Rendering performance/INP]]

# critical rendering path

> Ordered browser work that turns HTML, CSS, and JavaScript bytes into the first pixels — optimize it to show content sooner.

```txt
        critical rendering ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Classic web performance question: DOM → CSSOM → render tree → layout → paint …

## Sources
- [web.dev — Critical Rendering Path](https://web.dev/articles/critical-rendering-path) — deep-dive
- [web.dev — Render-tree Construction, Layout, and Paint](https://web.dev/articles/critical-rendering-path/render-tree-construction) — deep-dive

## Key Concepts
- **Core:** The critical rendering path is the minimum sequence of network and CPU steps …

## Technical Details
```
HTML ──► DOM ──┐
               ├──► Render tree ──► Layout ──► Paint ──► Composite
CSS  ──► CSSOM ┘
JS (sync) can block HTML parse and delay CSSOM/DOM progress
```

- Pipeline checklist:

1. Build DOM from HTML.
2. Build CSSOM from CSS (and apply).
3. Combine into render tree (visible nodes only).
4. [[Rendering performance/layout|Layout]] — box sizes and positions.
5. [[Rendering performance/paint|Paint]] — fill draw lists / rasters.
6. [[Rendering performance/composite|Composite]] — layers to screen.

- Measurement: Chrome Performance / Lighthouse

## Mistakes to Avoid
- **Mistake:** Giant blocking CSS for the whole site on every route
- **Mistake:** Sync `<script>` in `<head>` without `defer`/`async` when order a…
- **Mistake:** Ignoring CSSOM

## Pros/Cons or Trade-offs
- **Pro:** Shared mental model for both first load and subsequent frames.
- **Con:** Over-inlining CSS/JS bloats HTML — hurts caching and can slow repeat visits.

## Comparison
- vs [[Rendering performance/INP]]: CRP is mostly about first (and subsequent) rendering pipeline
- vs resource waterfalls: network timing feeds the CRP but is not the whole path


### Use cases
- Marketing landing page: inline critical CSS for above-the-fold, defer non-cri…
