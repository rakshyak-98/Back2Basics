[[Javascript]] [[JavaScript/Garbage Collection]]

# Weak map

> `WeakMap` keys are objects held weakly — if nothing else references the key, the entry can be GC’d.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Attach private metadata to objects without preventing GC; no iteration, no string keys.

```txt
WeakMap: object key → value   (key not kept alive by the map)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Weak ref** | Doesn’t keep key alive | “No memory leak from the map.” |
| **No enumerate** | Can’t list keys | “Privacy + GC freedom.” |
| **vs Map** | Strong keys | “Map keeps keys alive.” |
| **Private data** | Per-object store | “Before `#private` fields.” |

---

## Standard config / commands

```js
const meta = new WeakMap()
meta.set(el, { clicks: 0 })
meta.get(el).clicks++
```

| Knob | Why it matters |
|------|----------------|
| Object keys only | Primitives throw |
| WeakSet | Presence without values |
| FinalizationRegistry | Optional cleanup hooks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| TypeError on set | primitive key | Box or use Map |
| Need to iterate | wrong structure | Use Map |
| Entry “missing” | key GC’d | Expected if no other refs |
| Leak still | value references key | Break cycle |

---

## Gotchas

> [!WARNING]
> **Values can keep keys alive** — if `value` points at `key`, GC won’t help.

> [!WARNING]
> **Not for caches of strings/URLs** — use Map + LRU eviction.

---

## When NOT to use

- **Need key listing / size** — Map.
- **Primitive keys** — Map or object.

## Related

[[JavaScript/Garbage Collection]] [[Javascript]]
