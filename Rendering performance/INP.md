[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[Rendering performance/critical rendering path]] [[NodeJS/Event Loop]]

# INP

> Interaction to Next Paint — Core Web Vital for responsiveness: how long from click/tap/key until the next frame shows feedback.

## Interview Relevance

Replaced FID as the responsiveness Core Web Vital (2024). Interviewers want: what INP measures, good/needs-improvement thresholds, and how you fix long tasks vs presentation delay.

## Sources

- [web.dev — Interaction to Next Paint (INP)](https://web.dev/articles/inp) — deep-dive
- [web.dev — Optimize INP](https://web.dev/explore/how-to-optimize-inp) — deep-dive
- [web-vitals library](https://github.com/GoogleChrome/web-vitals) — overview

## Core Definition

INP summarizes how quickly the page responds to user interactions over the whole visit. Field data typically uses a high percentile (commonly p75); lab tools approximate but CrUX / Search Console are the ranking-facing signal.

## Key Concepts

- **Full interaction latency:** input delay + event handling + presentation (style/layout/paint) until next paint — not just “JS finished.”
- **vs FID:** FID measured only first-input delay; INP watches (essentially) all click/tap/key interactions and includes processing + paint.
- **Thresholds (CWV):** ≤ 200 ms good; 200–500 ms needs improvement; > 500 ms poor (p75 field).
- **Long tasks:** main-thread work > ~50 ms delays input — same class of problem as a blocked [[NodeJS/Event Loop|event loop]], but in the browser.

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

Common fixes (priority order):

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

Framework patterns: React `startTransition` for non-urgent updates; virtualize long lists; avoid layout thrashing in click handlers (see [[Rendering performance/layout]]).

## Real-World Applications

E-commerce filter click: sync JSON parse + re-render of 5k DOM nodes → INP spikes on mobile. Fix: virtualize, defer analytics, paint an optimistic selected state immediately.

## Pros/Cons or Trade-offs

- **Pro:** Captures real “UI felt dead” moments better than FID.
- **Con:** Pages with few interactions may lack INP in reports — not always a bug.

## Comparison

- vs LCP: LCP is loading; INP is interaction — a fast hero image does not fix an 800 ms click handler.
- vs [[Rendering performance/refresh rate]]: frame budget explains jank during animation; INP is interaction → next paint, including JS delay.

## Mistakes to Avoid

- Optimizing only LCP/CLS and ignoring click handlers.
- Calling `preventDefault` then doing heavy work before any visual feedback — show optimistic UI first.
- Trusting Lighthouse alone for INP — ship field monitoring.
