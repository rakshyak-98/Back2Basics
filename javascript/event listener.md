[[javascript]] [[throttle]] [[Callback]] [[dataTransfer]]

# event listener

> Register a function for a DOM (or EventTarget) event — `addEventListener` / `removeEventListener` with the same function reference.





## Interview Relevance
Interviewers use **event listener** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **capture**, **bubble**, **once**, **passive**.

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

## Real-World Applications
In production APIs and tooling, **event listener** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Anonymous functions** — `removeEventListener` won’t match a new arrow; **Passive scroll listeners** — browsers may force passive; design accordingly.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Register a function for a DOM (or EventTarget) event — `addEventListener` / `rem…).
- **Con / when not:** **React synthetic events** — prefer JSX `onClick` unless integrating non-React libs.
- **Con / when not:** **High-frequency raw handlers** — throttle/raf.

## Comparison
vs [[throttle]]: know when each applies — do not treat them as interchangeable. vs [[Callback]]: know when each applies — do not treat them as interchangeable. vs [[dataTransfer]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Anonymous functions** — `removeEventListener` won’t match a new arrow.
- **Passive scroll listeners** — browsers may force passive; design accordingly.
- **Can’t remove listener:** check New function each time; fix: Store named fn / AbortSignal
- **preventDefault ignored:** check Passive listener; fix: Drop `passive`
- **Handler fires twice:** check React + DOM / double bind; fix: Bind once; check Strict Mode
- **Memory leak:** check Never removed; fix: Cleanup on unmount
