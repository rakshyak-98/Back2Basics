[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/composite]] [[Rendering performance/INP]]

# critical rendering path

> Ordered browser work that turns HTML, CSS, and JavaScript bytes into the first pixels — optimize it to show content sooner.

## Interview Relevance

Classic web performance question: DOM → CSSOM → render tree → layout → paint → composite. Interviewers want render-blocking insight (CSS, sync JS) and how you measure first paint / LCP.

## Sources

- [web.dev — Critical Rendering Path](https://web.dev/articles/critical-rendering-path) — deep-dive
- [web.dev — Render-tree Construction, Layout, and Paint](https://web.dev/articles/critical-rendering-path/render-tree-construction) — deep-dive

## Core Definition

The critical rendering path is the minimum sequence of network and CPU steps required to put pixels on screen for the current navigation. Shortening it improves first render and sets the stage for smooth updates later.

## Key Concepts

- **DOM:** parse HTML into a tree (bytes → tokens → nodes) → incremental as data arrives.
- **CSSOM:** parse CSS into a style tree → CSS is render-blocking for first paint of affected content.
- **Render tree:** DOM + CSSOM, excluding non-rendered nodes (`display: none`) → input to layout.
- **Layout / paint / composite:** geometry, pixels, layer merge — see sibling notes.
- **JavaScript:** sync scripts block parsing; they can also read/write DOM and force style work → schedule carefully.

## Technical Details

```
HTML ──► DOM ──┐
               ├──► Render tree ──► Layout ──► Paint ──► Composite
CSS  ──► CSSOM ┘
JS (sync) can block HTML parse and delay CSSOM/DOM progress
```

Pipeline checklist:

1. Build DOM from HTML.
2. Build CSSOM from CSS (and apply).
3. Combine into render tree (visible nodes only).
4. [[Rendering performance/layout|Layout]] — box sizes and positions.
5. [[Rendering performance/paint|Paint]] — fill draw lists / rasters.
6. [[Rendering performance/composite|Composite]] — layers to screen.

Measurement: Chrome Performance / Lighthouse; watch render-blocking resources, preload hints, and critical CSS strategies.

## Real-World Applications

Marketing landing page: inline critical CSS for above-the-fold, defer non-critical stylesheets, async non-essential scripts — first contentful paint drops without rewriting the design.

## Pros/Cons or Trade-offs

- **Pro:** Shared mental model for both first load and subsequent frames.
- **Con:** Over-inlining CSS/JS bloats HTML — hurts caching and can slow repeat visits.

## Comparison

- vs [[Rendering performance/INP]]: CRP is mostly about first (and subsequent) rendering pipeline; INP measures interaction → next paint latency across the visit.
- vs resource waterfalls: network timing feeds the CRP but is not the whole path — CPU parse/layout matter too.

## Mistakes to Avoid

- Giant blocking CSS for the whole site on every route.
- Sync `<script>` in `<head>` without `defer`/`async` when order allows.
- Ignoring CSSOM — “HTML is small” still waits on styles before first meaningful paint.
