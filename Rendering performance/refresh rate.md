[[Rendering performance/INP]] [[Rendering performance/layout]] [[Rendering performance/paint]] [[Operating System/context switching]]

# Refresh rate

> Display hardware cadence — frames must be ready before vsync or user sees jank — **60 Hz ≈ 16.67 ms budget**.

## Mental model

Screen refreshes at fixed Hz (60, 90, 120, 144). Browser must produce a frame **before each vsync** or frame drops (stutter).

```
60 Hz → 1000/60 ≈ 16.67 ms per frame (hard ceiling)
120 Hz → 8.33 ms per frame

Browser target: complete JS + layout + paint within ~10 ms (60 Hz)
                 leaves headroom for compositor + system
```

Device refresh is constant; **app frame rate varies** — animation smooth only if work fits budget.

## Standard config / commands

### Frame budget math

| Refresh rate | Frame period | Practical JS budget |
|--------------|--------------|---------------------|
| 60 Hz | 16.67 ms | ~10 ms |
| 90 Hz | 11.1 ms | ~6–7 ms |
| 120 Hz | 8.33 ms | ~5 ms |

### `requestAnimationFrame` aligns to refresh

```javascript
function loop(ts) {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
// rAF fires ~once per frame, paused in background tabs
```

### Detect display refresh (experimental)

```javascript
if (window.screen?.refreshRate) {
  console.log('Hz', window.screen.refreshRate);
}
// matchMedia('(refresh-rate: 120hz)') — limited support
```

### High refresh rate testing

- Enable 120 Hz on device/emulator
- Chrome DevTools → **Rendering** → FPS meter
- Throttle CPU 4× to simulate mobile

### ProMotion / variable refresh

- iOS/macOS can vary refresh — don't assume fixed cadence for power saving.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Visible stutter in animation | Long tasks > frame period | Split work; compositor-only props |
| 30 FPS on 120 Hz panel | Every other frame missed | Profile; reduce paint cost |
| rAF runs but nothing moves | Logic bug vs display | Verify transform updates |
| Background tab slow | Browser throttles rAF | Expected — pause work on `visibilitychange` |
| VSync tear (games/native) | Full-screen exclusive | Web uses compositor — different stack |

## Gotchas

> [!WARNING]
> **Meeting 10 ms on desktop ≠ mobile** — same site at 4× CPU throttle may miss 16 ms budget.

- **`setInterval(16)` ≠ vsync** — use rAF for visual updates.
- **Layout + paint in rAF** every frame — OK for small DOM; batch static content.
- **DevTools open** slows JS — profile with closed dock when possible.

## When NOT to use

- Non-visual batch jobs — don't tie to rAF; use `setTimeout` or Worker.

## Related

[[Rendering performance/INP]] [[Rendering performance/layout]] [[Rendering performance/paint]] [[Descriptive/web development]]
