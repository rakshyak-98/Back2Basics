[[Javascript]] [[JavaScript/Garbage Collection]]

# Weak map

> `WeakMap` keys are objects held weakly — if nothing else references the key, the entry can be GC’d.

## Interview Relevance

WeakMap questions check ephemeral metadata without preventing GC — versus Map leaks.

## Sources

- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts

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

## Technical Details

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

## Pros/Cons or Trade-offs

- **Need key listing / size** — Map.
- **Primitive keys** — Map or object.

## Mistakes to Avoid

> [!WARNING]
> **Values can keep keys alive** — if `value` points at `key`, GC won’t help.

> [!WARNING]
> **Not for caches of strings/URLs** — use Map + LRU eviction.

| Symptom | Check | Fix |
|---------|-------|-----|
| TypeError on set | primitive key | Box or use Map |
| Need to iterate | wrong structure | Use Map |
| Entry “missing” | key GC’d | Expected if no other refs |
| Leak still | value references key | Break cycle |

