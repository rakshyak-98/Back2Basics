[[javascript]] [[throttle]] [[Callback]] [[dataTransfer]]

# event listener

> Register a function for a DOM (or EventTarget) event — `addEventListener` / `removeEventListener` with the same function reference.

```txt
        event listener ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **event listener** to check whether you can explain the mech…

## Sources
- [MDN — addEventListener](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) — deep-dive
- [Wikipedia — event listener](https://en.wikipedia.org/wiki/event_listener) — overview

## Key Concepts
- **capture:** Downward phase — `{ capture: true }`.
- **bubble:** Upward (default) — Most click handlers.
- **once:** Auto-remove — `{ once: true }`.
- **passive:** Can’t preventDefault — Scroll perf on touch.

## Technical Details
```txt
capture ↓ … target … ↑ bubble
```

```js
const onClick = (e) => console.log(e.target)
el.addEventListener('click', onClick)
el.removeEventListener('click', onClick)

el.addEventListener('touchstart', onTouch, { passive: true })
```

| Knob | Why it matters |
|------|----------------|
| Same ref to remove | Inline arrows can’t remove |
| `AbortSignal` | `addEventListener(..., { signal })` batch cancel |
| Delegation | Listen on parent for dynamic kids |

## Mistakes to Avoid
- **Mistake:** **Anonymous functions**
- **Mistake:** **Passive scroll listeners**
- **Mistake:** **Can’t remove listener:** check New function each time
- **Mistake:** **preventDefault ignored:** check Passive listener
- **Mistake:** **Handler fires twice:** check React + DOM / double bind
- **Mistake:** **Memory leak:** check Never removed; fix: Cleanup on unmount

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Register a function for a DOM (or EventTarget) event — `addEventListener` / `rem…).
- **Con / when not:** **React synthetic events**
- **Con / when not:** **High-frequency raw handlers** — throttle/raf.

## Comparison
- vs [[throttle]]: know when each applies


### Use cases
- In production APIs and tooling, **event listener** shows up whenever teams sh…
