[[javascript]] [[event listener]] [[promise]]

# throttle

> Run a function at most once per time window — drop or coalesce extra calls (scroll, resize, mousemove).

## Mental model

**Say it in one breath:** Throttle = rate limit. Debounce = wait until quiet. Don’t confuse them.

```txt
events: |||||│|||| → throttle → |    |    |
debounce waits for silence then fires once
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **throttle** | Max frequency | “Fire regularly while active.” |
| --- | --- | --- |
| **debounce** | After pause | “Search box after typing stops.” |
| **leading/trailing** | Edge of window | “Fire immediately and/or at end.” |

## Standard config / commands

```js
function throttle(fn, ms) {
  let last = 0
  return (...args) => {
    const now = Date.now()
    if (now - last >= ms) {
      last = now
      fn(...args)
    }
  }
}
window.addEventListener('scroll', throttle(onScroll, 100))
```

| Knob | Why it matters |

| `requestAnimationFrame` | Visual updates synced to paint |
| --- | --- |
| Libraries (lodash) | Leading/trailing options |
| Cancel on unmount | Clear timers in React |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| UI jank still | Window too small / heavy fn | Raise ms; lighten handler |
| Missed last event | Leading-only throttle | Add trailing call |
| Used debounce for scroll | Wrong tool | Throttle scroll; debounce input |
| Stale `this` | Lost context | Arrow or bind |

## Gotchas

> [!WARNING]
> **Throttle ≠ debounce** — interviewers love this distinction.

> [!WARNING]
> **React** — memoize throttled fn; don’t recreate each render.

## When NOT to use

- **Rare clicks** — no need.
- **Must process every event** — queue instead of drop.

## Related

[[event listener]] [[web worker]] [[Optimizing performance]]
