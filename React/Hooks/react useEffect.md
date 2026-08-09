[[Hooks]] [[react hooks]] [[Optimizing performance]]

# react useEffect

> Run side effects after paint — fetch, subscriptions, DOM — keep render pure.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Interview map (words you can say)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Render computes UI. `useEffect` runs after that commit when deps change; cleanup runs before the next effect and on unmount.

```txt
render (pure) → commit DOM → useEffect(fn)
fn deps change → cleanup() → fn() again
unmount → cleanup()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Deps array** | When to re-run | “`[]` = mount once; omit = every render (rare).” |
| **Cleanup** | Undo the effect | “Abort fetch, remove listener, clear timer.” |
| **Strict Mode** | Dev double-invoke | “Mount→cleanup→mount — proves cleanup works.” |

## Standard config / commands

```tsx
useEffect(() => {
  const c = new AbortController()
  fetch('/api', { signal: c.signal })
    .then((r) => r.json())
    .then(setData)
    .catch((e) => { if (e.name !== 'AbortError') console.error(e) })
  return () => c.abort()
}, [])
```

| Deps | When it runs |
|------|----------------|
| `[]` | After first paint only |
| `[a, b]` | When `a` or `b` changes (shallow) |
| cleanup return | Before re-run + unmount |

Effects in one component run **in source order**.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Infinite loop | Effect sets state that’s a dep | Remove dep or derive without effect |
| Stale props/state | Missing dep | Add dep or use functional update / ref |
| Double fetch in dev | Strict Mode | Idempotent + abort cleanup |
| Race: old response wins | No abort | AbortController on cleanup |
| Sync A→B in effect | Derived data | Compute in render / `useMemo` |

---

## Gotchas

> [!WARNING]
> **Don’t use effects for derived state** — `fullName = first + last` belongs in render.

> [!WARNING]
> **Mutating POSTs** — prefer event handlers; GET-on-mount is the common effect case.

---

## When NOT to use

- **Transforming props → state** — derive or remount with `key`.
- **Data fetching at scale** — [[react-query]] owns cache/dedupe better.

---

## Related

[[react hooks]] [[react-query]] [[Optimizing performance]] [[useRef]]
