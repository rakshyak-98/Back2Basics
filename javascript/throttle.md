[[javascript]] [[event listener]] [[promise]] [[web worker]] [[Optimizing performance]]

# throttle

> Run a function at most once per time window — drop or coalesce extra calls (scroll, resize, mousemove).

## Interview Relevance

Interviewers use **throttle** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **throttle**, **debounce**, **leading/trailing**.

## Sources

- [CSS-Tricks — Debouncing and Throttling](https://css-tricks.com/debouncing-throttling-explained-examples/) — overview
- [Wikipedia — throttle](https://en.wikipedia.org/wiki/throttle) — overview

## Key Concepts

- **throttle:** Max frequency — Fire regularly while active.
- **debounce:** After pause — Search box after typing stops.
- **leading/trailing:** Edge of window — Fire immediately and/or at end.

## Technical Details

```txt
events: |||||│|||| → throttle → |    |    |
debounce waits for silence then fires once
```

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
|------|----------------|
| `requestAnimationFrame` | Visual updates synced to paint |
| Libraries (lodash) | Leading/trailing options |
| Cancel on unmount | Clear timers in React |

## Real-World Applications

In production APIs and tooling, **throttle** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Throttle ≠ debounce** — interviewers love this distinction; **React** — memoize throttled fn; don’t recreate each render.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Run a function at most once per time window — drop or coalesce extra calls (scro…).
- **Con / when not:** **Rare clicks** — no need.
- **Con / when not:** **Must process every event** — queue instead of drop.

## Comparison

vs [[event listener]]: know when each applies — do not treat them as interchangeable. vs [[promise]]: know when each applies — do not treat them as interchangeable. vs [[web worker]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Throttle ≠ debounce** — interviewers love this distinction.
- **React** — memoize throttled fn; don’t recreate each render.
- **UI jank still:** check Window too small / heavy fn; fix: Raise ms; lighten handler
- **Missed last event:** check Leading-only throttle; fix: Add trailing call
- **Used debounce for scroll:** check Wrong tool; fix: Throttle scroll; debounce input
- **Stale `this`:** check Lost context; fix: Arrow or bind
