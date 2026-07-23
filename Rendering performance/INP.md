[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[NodeJS/Event Loop]]

# INP (Interaction to Next Paint)

> Core Web Vital measuring responsiveness — latency from user input to next frame paint — **replaces FID (2024)**.

## Mental model

**INP** captures **worst-case** (or high percentile) delay between interaction (click, tap, key) and when the browser **paints the next frame** showing feedback. Target: **≤ 200 ms** good, **200–500 ms** needs improvement, **> 500 ms** poor.

```
User click
    │
    ▼ input queued
Main thread busy? ──yes──► delay (long task)
    │
    ▼ event handler runs
    ▼ style/layout/paint scheduled
    ▼ next paint ◄── INP measures this gap
```

Unlike **FID** (first input only), INP considers **all interactions** during page lifetime (field data p75).

## Standard config / commands

### Measure in production (web-vitals library)

```javascript
import { onINP } from 'web-vitals';

onINP((metric) => {
  console.log('INP', metric.value, metric.entries);
  // Send to analytics: metric.id, metric.navigationType
});
```

### Chrome DevTools

1. **Performance** panel → record → interact → find **Long tasks** (> 50 ms).
2. **Performance insights** → INP breakdown (input delay, processing, presentation delay).

### Common fixes (priority order)

```javascript
// 1. Break long tasks
function yieldToMain() {
  return new Promise(r => setTimeout(r, 0));
}

// 2. Defer non-urgent work
requestIdleCallback(() => heavyAnalytics());

// 3. Offload CPU
const worker = new Worker('/worker.js');
```

### Framework patterns

- React 18 **Transitions** — mark updates non-urgent (`startTransition`)
- Virtualize long lists — don't render 10k DOM nodes on click filter
- Avoid synchronous layout read/write thrashing in click handlers

### Lab vs field

| Source | Use |
|--------|-----|
| **CrUX / Search Console** | Real user INP (28-day p75) |
| **Lighthouse** | Lab proxy — not official INP score |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| INP poor, LCP good | Long tasks on interaction | Profile click handler; split work |
| Spikes only mobile | Slower CPU, 4x throttling | Reduce JS; simplify DOM |
| After deploy regression | New sync JSON parse | Stream/chunk; Web Worker |
| Third-party widgets | Tag managers on click | Delay load; facade buttons |
| INP N/A in report | No interactions / bfcache | Normal for static pages |

## Gotchas

> [!WARNING]
> **Optimizing LCP alone won't fix INP** — hero image fast but 800 ms click handler still fails CWV.

- **SPA route change** counts as interaction — include in profiling.
- **preventDefault** on slow handler blocks native feedback — show instant optimistic UI.
- **100 ms input delay** from overlay capturing events — check z-index hit targets.

## When NOT to use

- Don't chase sub-50 ms INP on internal admin tools with 5 users — focus on critical revenue paths first.

## Related

[[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/refresh rate]] [[Descriptive/web development]]
