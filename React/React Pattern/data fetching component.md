[[React Pattern]] [[Hooks/react useEffect]] [[react-query]]

# data fetching component

> Ways a component loads remote data — classic `useEffect`, Suspense `use()`, or a cache library.

## Mental model

**Say it in one breath:** Client fetch either owns loading state yourself (`useEffect`) or suspends until a promise resolves (`use` + Suspense). Production apps usually outsource cache to React Query / RTK Query.

```txt
useEffect: mount → fetch → setState → render
use()+Suspense: render → throw promise → fallback → resolve → render
library: hook → cache key → dedupe / retry / stale
```

### Interview map (words you can say)

| Approach | Plain meaning | Say in interview |

| **useEffect fetch** | Manual loading/error | “Fine for demos; races need abort.” |
| --- | --- | --- |
| **use() + Suspense** | Read promise in render | “Needs cache so promise identity is stable.” |
| **react-query / RTKQ** | Cached keyed requests | “Deduping and invalidation included.” |

## Standard config / commands

```tsx
// Classic
useEffect(() => {
  const c = new AbortController()
  fetch('/api/user', { signal: c.signal })
    .then((r) => r.json())
    .then(setUser)
  return () => c.abort()
}, [])

// Suspense (promise must be cached — don’t create inline every render)
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise)
  return <div>{user.name}</div>
}
```

| Knob | Why it matters |

| Abort | Prevents stale setState |
| --- | --- |
| Stable promise | `use()` without cache refetches forever |
| Cache key | Library dedupe |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Infinite Suspense loop | New promise each render | Module/cache the promise |
| Race on param change | No abort | AbortController / query key |
| Double fetch Strict Mode | Dev double mount | Idempotent + abort |
| No shared cache | Hand fetch in 5 trees | [[react-query]] |

## Gotchas

> [!WARNING]
> **`use(fetch())` inline is wrong** — fetch must be memoized/cached by key.

> [!WARNING]
> **Suspense doesn’t replace error UI** — still need Error Boundaries.

## When NOT to use

- **Mutations / POST** — event handlers, not mount effects.
- **SSR-critical data** — load on the server / RSC when possible.

## Related

[[Hooks/react useEffect]] [[Data Fetching HOC component]] [[react-query]] [[Redux/Redux createApi]]
