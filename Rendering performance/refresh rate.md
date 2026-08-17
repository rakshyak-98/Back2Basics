[[Rendering performance/INP]] [[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/composite]] [[Operating System/context switching]]

# refresh rate

> Display cadence in hertz — frames must be ready before vsync or the user sees stutter; 60 Hz ≈ 16.7 ms budget.

```txt
        refresh rate ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Separates “we animate in JS” from real-time budgets: can you do the math for …

## Sources
- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — overview
- [MDN — Window.requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) — deep-dive
- [Wikipedia — Refresh rate](https://en.wikipedia.org/wiki/Refresh_rate) — overview

## Key Concepts
- **Frame period:** `1000 / Hz` ms — hard ceiling before vsync.
- **Practical JS budget:** leave headroom for rendering and the browser
- **`requestAnimationFrame`:** schedules work for the next frame
- **Variable refresh:** ProMotion / VRR can change cadence for power


- **Core:** The panel refreshes at a fixed (or variable) rate

## Technical Details
| Refresh rate | Frame period | Practical main-thread budget |
|--------------|--------------|------------------------------|
| 60 Hz | 16.67 ms | ~10 ms |
| 90 Hz | 11.1 ms | ~6–7 ms |
| 120 Hz | 8.33 ms | ~5 ms |

```
60 Hz  → finish work before ~16.7 ms or drop a frame
120 Hz → ~8.3 ms — same app code may fail without profiling
```

```javascript
function loop(ts) {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
```

```javascript
if (window.screen?.refreshRate) {
  console.log('Hz', window.screen.refreshRate);
}
```

- Testing: enable high refresh on device

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuttering animation | Long tasks > frame period | Split work; compositor-only props |
| 30 FPS on 120 Hz panel | Every other frame missed | Reduce paint/layout per frame |
| Background tab “slow” | rAF throttled | Pause on `visibilitychange` — expected |
| `setInterval(16)` drift | Not vsync-aligned | Use `requestAnimationFrame` |

## Mistakes to Avoid
- **Mistake:** Equating `setInterval(16)` with vsync
- **Mistake:** Judging smoothness only with DevTools docked open
- **Mistake:** Doing heavy layout every rAF tick for large DOM

## Pros/Cons or Trade-offs
- **Pro:** Clear numeric target for animation and scroll work.
- **Con:** Desktop headroom lies — same site fails on mid-tier Android at 4× throttle.

## Comparison
- vs [[Rendering performance/INP]]: refresh rate is continuous frame cadence
- vs vsync in native games: web apps go through the browser compositor


### Use cases
- Canvas game loop or drag-and-drop preview: drive positions in `requestAnimati…
