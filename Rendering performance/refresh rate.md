[[Rendering performance/INP]] [[Rendering performance/layout]] [[Rendering performance/paint]] [[Rendering performance/composite]] [[Operating System/context switching]]

# refresh rate

> Display cadence in hertz — frames must be ready before vsync or the user sees stutter; 60 Hz ≈ 16.7 ms budget.

## Interview Relevance

Separates “we animate in JS” from real-time budgets: can you do the math for 60/120 Hz, use `requestAnimationFrame`, and explain why mobile CPU throttle breaks desktop-smooth animations?

## Sources

- [web.dev — Rendering performance](https://web.dev/articles/rendering-performance) — overview
- [MDN — Window.requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) — deep-dive
- [Wikipedia — Refresh rate](https://en.wikipedia.org/wiki/Refresh_rate) — overview

## Core Definition

The panel refreshes at a fixed (or variable) rate. The browser aims to produce a new frame for each refresh. If JavaScript + style + layout + paint miss the deadline, frames drop and motion looks like jank.

## Key Concepts

- **Frame period:** `1000 / Hz` ms — hard ceiling before vsync.
- **Practical JS budget:** leave headroom for rendering and the browser — ~10 ms of script at 60 Hz is a common rule of thumb, less at 120 Hz.
- **`requestAnimationFrame`:** schedules work for the next frame; pauses in background tabs → correct hook for visual updates.
- **Variable refresh:** ProMotion / VRR can change cadence for power — don’t assume a fixed 16.7 ms forever.

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

Testing: enable high refresh on device; Chrome Rendering → FPS meter; CPU 4× throttle for mobile simulation.

| Symptom | Check | Fix |
|---------|-------|-----|
| Stuttering animation | Long tasks > frame period | Split work; compositor-only props |
| 30 FPS on 120 Hz panel | Every other frame missed | Reduce paint/layout per frame |
| Background tab “slow” | rAF throttled | Pause on `visibilitychange` — expected |
| `setInterval(16)` drift | Not vsync-aligned | Use `requestAnimationFrame` |

## Real-World Applications

Canvas game loop or drag-and-drop preview: drive positions in `requestAnimationFrame`, keep per-frame work under budget, and move decorative motion to `transform` on the compositor.

## Pros/Cons or Trade-offs

- **Pro:** Clear numeric target for animation and scroll work.
- **Con:** Desktop headroom lies — same site fails on mid-tier Android at 4× throttle.

## Comparison

- vs [[Rendering performance/INP]]: refresh rate is continuous frame cadence; INP is interaction → next paint latency.
- vs vsync in native games: web apps go through the browser compositor — different tear/latency controls.

## Mistakes to Avoid

- Equating `setInterval(16)` with vsync — it drifts and ignores display timing.
- Judging smoothness only with DevTools docked open — the dock itself slows JS.
- Doing heavy layout every rAF tick for large DOM — batch or virtualize.
