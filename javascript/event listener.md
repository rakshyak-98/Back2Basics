[[javascript]] [[throttle]] [[Callback]]

# event listener

> Register a function for a DOM (or EventTarget) event — `addEventListener` / `removeEventListener` with the same function reference.

---

## Mental model

**Say it in one breath:** Target receives events; listeners run in registration order (capture then bubble phases). Remove with the **same** function reference.

```txt
capture ↓ … target … ↑ bubble
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **capture** | Downward phase | “`{ capture: true }`.” |
| **bubble** | Upward (default) | “Most click handlers.” |
| **once** | Auto-remove | “`{ once: true }`.” |
| **passive** | Can’t preventDefault | “Scroll perf on touch.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t remove listener | New function each time | Store named fn / AbortSignal |
| preventDefault ignored | Passive listener | Drop `passive` |
| Handler fires twice | React + DOM / double bind | Bind once; check Strict Mode |
| Memory leak | Never removed | Cleanup on unmount |

---

## Gotchas

> [!WARNING]
> **Anonymous functions** — `removeEventListener` won’t match a new arrow.

> [!WARNING]
> **Passive scroll listeners** — browsers may force passive; design accordingly.

---

## When NOT to use

- **React synthetic events** — prefer JSX `onClick` unless integrating non-React libs.
- **High-frequency raw handlers** — throttle/raf.

---

## Related

[[throttle]] [[Callback]] [[dataTransfer]]
