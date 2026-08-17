[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[Rendering performance/critical rendering path]] [[NodeJS/Event Loop]]

# INP

> Interaction to Next Paint — Core Web Vital for responsiveness: how long from click/tap/key until the next frame shows feedback.

```txt
        INP ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Replaced FID as the responsiveness Core Web Vital (2024)

## Sources
- [web.dev — Interaction to Next Paint (INP)](https://web.dev/articles/inp) — deep-dive
- [web.dev — Optimize INP](https://web.dev/explore/how-to-optimize-inp) — deep-dive
- [web-vitals library](https://github.com/GoogleChrome/web-vitals) — overview

## Key Concepts
- **Full interaction latency:** input delay + event handling + presentation (style/layout/paint) until next p…
- **vs FID:** FID measured only first-input delay
- **Thresholds (CWV):** ≤ 200 ms good; 200–500 ms needs improvement; > 500 ms poor (p75 field).
- **Long tasks:** main-thread work > ~50 ms delays input


- **Core:** INP summarizes how quickly the page responds to user interactions over the wh…

## Technical Details
```
User click
    │
    ▼ input queued
Main thread busy? ──yes──► input delay
    │
    ▼ event handlers run
    ▼ style / layout / paint scheduled
    ▼ next paint  ◄── INP ends here (feedback frame)
```

```javascript
import { onINP } from 'web-vitals';

onINP((metric) => {
  // metric.value in ms; send to analytics with metric.id
  console.log('INP', metric.value, metric.entries);
});
```

- Common fixes (priority order):

```javascript
function yieldToMain() {
  return new Promise((r) => setTimeout(r, 0));
}

requestIdleCallback(() => heavyAnalytics());
const worker = new Worker('/worker.js');
```

| Source | Use |
|--------|-----|
| CrUX / Search Console | Real-user INP (field) |
| Performance panel | Find long tasks and INP breakdown |
| Lighthouse | Lab proxy — not the official field score |

- Framework patterns: React `startTransition` for non-urgent updates

## Mistakes to Avoid
- **Mistake:** Optimizing only LCP/CLS and ignoring click handlers
- **Mistake:** Calling `preventDefault` then doing heavy work before any visual…
- **Mistake:** Trusting Lighthouse alone for INP — ship field monitoring

## Pros/Cons or Trade-offs
- **Pro:** Captures real “UI felt dead” moments better than FID.
- **Con:** Pages with few interactions may lack INP in reports — not always a bug.

## Comparison
- vs LCP: LCP is loading; INP is interaction
- vs [[Rendering performance/refresh rate]]: frame budget explains jank during animation


### Use cases
- E-commerce filter click: sync JSON parse + re-render of 5k DOM nodes → INP sp…
