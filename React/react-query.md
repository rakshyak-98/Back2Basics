[[React]] [[react cache]] [[Redux/Redux createApi]] [[Optimizing performance]]

# react-query (TanStack Query)

> Client library for server state — cache, dedupe, refetch, and mutate with one `QueryClient`.

```txt
        react-query (TanSt ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers separate server state vs client UI state and ask when Context, R…

## Sources
- [Wikipedia — react-query](https://en.wikipedia.org/wiki/react-query) — overview

## Key Concepts
- **Server state:** Data that lives on an API — “Not form open/closed — that’s client state.”
- **staleTime:** How long data is fresh — “No refetch until stale.”
- **gcTime:** How long unused cache is kept — “Was `cacheTime` — garbage collection.”
- **invalidate:** Mark stale + refetch — “After POST, invalidate the list key.”

## Technical Details
```txt
useQuery(key, fn) → QueryCache
useMutation → invalidate / setQueryData → subscribers re-render
```

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

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Refetch every focus | `refetchOnWindowFocus` + `staleTime: 0` | Raise `staleTime` or disable focus refetch |
| Cache gone after Ctrl+F5 | In-memory cache | Expected; add persister if needed |
| Soft reload keeps data | DevTools still shows cache | Clear site data to wipe |
| Duplicate network calls | Different keys / no shared client | One `QueryClientProvider`; normalize keys |
| Mutation UI stale | No invalidate | `invalidateQueries` / `setQueryData` |

- **Mistake:** **Not a backend cache**
- **Mistake:** **Don’t put client UI flags in Query**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **No shared server data**
- **Con / skip when:** **Offline-first local DB**

## Real-World Applications
- **Scenario:** Apply react-query (TanStack Query) in feature code where the Key Concepts mat…
