[[Javascript]] [[JavaScript/Weak map]] [[JavaScript/Call stack]] [[Heap memory]]

# Garbage Collection

> GC reclaims heap objects your program can’t reach — you don’t `free()`, but you can still leak via lingering references.





## Interview Relevance
GC interviews cover reachability, mark-and-sweep intuition, and memory leak patterns in JS.

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [Garbage Collection — Wikipedia](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)) — overview

## Key Concepts
```txt
roots → reachable graph stays  |  unreachable → collect
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Reachability** | Still referenced | “Detach listeners/maps.” |
| **Mark-sweep / generational** | Common strategies | “Young objects die fast.” |
| **Leak** | Unintended retain | “Closures + detached DOM.” |
| **WeakMap** | Non-retaining keys | “Metadata without leaks.” |

## Technical Details
```js
// Chrome DevTools → Memory → heap snapshot / allocation timeline
el.removeEventListener('click', handler)
cache.delete(key)
```

| Knob | Why it matters |
|------|----------------|
| Heap snapshots | Find retainers |
| `--expose-gc` (node) | Force GC in experiments only |
| WeakRef | Advanced; don’t abuse |

## Pros/Cons or Trade-offs
- **Manual arena allocators in WASM** — different story.
- **Trying to force GC for correctness** — fix references instead.

## Mistakes to Avoid
> [!WARNING]
> **Closures capture more than you think** — accidental retain of big objects.

> [!WARNING]
> **Global caches without bounds** — classic process leak.

| Symptom | Check | Fix |
|---------|-------|-----|
| Memory climbs | heap snapshot | Break retainer paths |
| Detached DOM nodes | listeners/closures | Remove listeners; null refs |
| Worker retain | open ports | Close MessagePorts |
| GC pauses | huge heaps | Smaller objects; pool wisely |
