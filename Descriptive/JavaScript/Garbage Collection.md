[[Javascript]] [[JavaScript/Weak map]] [[JavaScript/Call stack]]

# Garbage Collection

> GC reclaims heap objects your program can’t reach — you don’t `free()`, but you can still leak via lingering references.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Reachability from roots (stack, globals) keeps objects alive; engines use generational GC and can pause briefly.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Memory climbs | heap snapshot | Break retainer paths |
| Detached DOM nodes | listeners/closures | Remove listeners; null refs |
| Worker retain | open ports | Close MessagePorts |
| GC pauses | huge heaps | Smaller objects; pool wisely |

---

## Gotchas

> [!WARNING]
> **Closures capture more than you think** — accidental retain of big objects.

> [!WARNING]
> **Global caches without bounds** — classic process leak.

---

## When NOT to use

- **Manual arena allocators in WASM** — different story.
- **Trying to force GC for correctness** — fix references instead.

## Related

[[JavaScript/Weak map]] [[JavaScript/Call stack]] [[Heap memory]]
