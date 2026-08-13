<!-- note-strategy: operational -->
[[Javascript]] [[JavaScript/Garbage Collection]] [[Buffers]]

# The structured clone algorithm

> Structured clone deep-copies certain JS values for `postMessage`, IndexedDB, and friends — richer than JSON, still limited.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Clone transferable graphs (objects, maps, dates, arraybuffers); functions and DOM nodes don’t go.

```txt
value → structuredClone → independent copy
postMessage uses same algorithm (+ transfer list)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **structuredClone** | Deep copy API | “Better than JSON.parse(JSON.stringify).” |
| **Transfer** | Move ArrayBuffer | “Zero-copy to worker; sender loses it.” |
| **Non-cloneable** | functions, symbols (as keys issues) | “Throws DataCloneError.” |
| **vs JSON** | types preserved | “Date stays Date.” |

---

## Standard config / commands

```js
const copy = structuredClone(obj)
worker.postMessage(buf, [buf]) // transfer
```

| Knob | Why it matters |
|------|----------------|
| Transfer list | Performance for big buffers |
| Cycles | Clone supports cycles (JSON doesn’t) |
| Platforms | Older browsers need polyfills/libs |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| DataCloneError | functions / DOM | Strip or serialize manually |
| Buffer empty after post | transferred | Don’t use on sender after |
| Lost prototype | class instance | Rehydrate after clone |
| Slow clone | huge graph | Transfer buffers; shrink payload |

---

## Gotchas

> [!WARNING]
> **Class instances become plain objects** — methods gone.

> [!WARNING]
> **JSON mindset** — structured clone isn’t “any JS value.”

---

## When NOT to use

- **Need functions across realms** — redesign with messages.
- **Tiny POJOs** — JSON may be enough and more portable.

## Related

[[JavaScript/Garbage Collection]] [[Buffers]] [[worker]]
