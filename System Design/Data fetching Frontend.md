<!-- note-strategy: operational -->
[[System Design]] [[cache system]] [[ETAG or IF MATCH]] [[Real-time Subscription]]

# Data fetching Frontend

> Frontend data fetching — load remote state into the UI with caching, dedupe, and clear loading/error paths (not ad-hoc `useEffect` soup).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Treat the server as source of truth; the client holds a cache keyed by query. Deduplicate in-flight requests; invalidate on mutations.

```txt
UI → query hook → cache → network → API
         ↑ invalidate / setQueryData
```

| Layer | Job |
|-------|-----|
| API service module | URLs, auth headers, typed errors |
| Cache (React Query/SWR) | Stale-while-revalidate |
| UI | Loading / empty / error states |

---

## Standard config / commands

```ts
// Conceptual React Query
const { data, error, isLoading } = useQuery({
  queryKey: ['user', id],
  queryFn: () => api.getUser(id),
  staleTime: 30_000,
})

useMutation({
  mutationFn: api.updateUser,
  onSuccess: () => qc.invalidateQueries({ queryKey: ['user', id] }),
})
```

| Knob | Why |
|------|-----|
| `staleTime` | Avoid refetch storms |
| `retry` | Flaky mobile nets |
| Suspense/boundaries | Consistent UX |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Double fetch StrictMode | Effect without cache | Use Query/SWR; or abort |
| Stale UI after POST | No invalidate | Invalidate/setQueryData |
| Waterfalls | Serial awaits | Parallel + consolidate endpoints |
| Auth flicker | Race token refresh | Single refresh mutex |
| CORS only in browser | See CORS note | Fix API headers |

---

## Gotchas

> [!WARNING]
> **`useEffect` fetch without cleanup** — setState on unmounted; race on id change.

> [!WARNING]
> **Cache key incompleteness** — missing filter ⇒ wrong data reuse.

> [!WARNING]
> **Global state for server data** — duplicates cache responsibility.

---

## When NOT to use

- **Fully static site** — bake data at build.
- **Local-only UI state** — form drafts stay in component state.
- **Binary streaming media** — players/MSE, not JSON hooks.

---

## Related

[[cache system]] [[Real-time Subscription]] [[Authentication web application]] [[ETAG or IF MATCH]]
