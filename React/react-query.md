[[React]] [[react cache]] [[Redux/Redux createApi]]

# react-query (TanStack Query)

> Client library for server state — cache, dedupe, refetch, and mutate with one `QueryClient`.

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

**Say it in one breath:** Declare “this key fetches with this fn”; Query owns caching, background refetch, retries, and sharing across components. Cache lives in browser RAM (per tab) unless you add a persister.

```txt
useQuery(key, fn) → QueryCache
useMutation → invalidate / setQueryData → subscribers re-render
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Server state** | Data that lives on an API | “Not form open/closed — that’s client state.” |
| **staleTime** | How long data is fresh | “No refetch until stale.” |
| **gcTime** | How long unused cache is kept | “Was `cacheTime` — garbage collection.” |
| **invalidate** | Mark stale + refetch | “After POST, invalidate the list key.” |

## Standard config / commands

```tsx
const qc = new QueryClient({
  defaultOptions: { queries: { staleTime: 30_000, retry: 1 } },
})

function Todos() {
  const { data, isPending, error } = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then((r) => r.json()),
  })
  // …
}
```

| Knob | Why it matters |
|------|----------------|
| Stable `queryKey` | Identity of cache entry |
| `staleTime` | Stops refetch storms on focus/mount |
| Persist plugin | Survive soft reload (still client-side) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Refetch every focus | `refetchOnWindowFocus` + `staleTime: 0` | Raise `staleTime` or disable focus refetch |
| Cache gone after Ctrl+F5 | In-memory cache | Expected; add persister if needed |
| Soft reload keeps data | DevTools still shows cache | Clear site data to wipe |
| Duplicate network calls | Different keys / no shared client | One `QueryClientProvider`; normalize keys |
| Mutation UI stale | No invalidate | `invalidateQueries` / `setQueryData` |

---

## Gotchas

> [!WARNING]
> **Not a backend cache** — RAM only unless persisted; hard refresh destroys it.

> [!WARNING]
> **Don’t put client UI flags in Query** — modals/toggles belong in React state.

---

## When NOT to use

- **No shared server data** — plain `useEffect` + fetch may suffice for one-off.
- **Offline-first local DB** — IndexedDB/SQLite sync layer, not Query alone.

---

## Related

[[react cache]] [[Redux/Redux createApi]] [[Optimizing performance]]
