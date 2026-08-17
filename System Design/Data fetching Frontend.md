[[System Design]] [[cache system]] [[ETAG or IF MATCH]] [[Real-time Subscription]] [[Authentication web application]]

# Data fetching Frontend

> Frontend data fetching — load remote state into the UI with caching, dedupe, and clear loading/error paths (not ad-hoc `useEffect` soup).

```txt
        Data fetching Fron ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Query-cache keys, invalidation after mutations, waterfall avoidance, and auth…

## Sources
- TanStack Query / SWR documentation — overview
- [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) — HTTP caching related patterns — overview

## Key Concepts
- **Layers:** API module → cache (React Query/SWR) → UI states.
- **Stale-while-revalidate:** serve cache; refresh in background.
- **Invalidate on mutate:** keep UI coherent after POST/PATCH.
- **Complete query keys:** filters belong in the key.

## Technical Details
```txt
UI → query hook → cache → network → API
         ↑ invalidate / setQueryData
```

```ts
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
| staleTime | Avoid refetch storms |
| retry | Flaky mobile nets |
| Suspense/boundaries | Consistent UX |

| Symptom | Fix |
|---------|-----|
| Double fetch StrictMode | Use Query/SWR; abort |
| Stale UI after POST | Invalidate/setQueryData |
| Waterfalls | Parallel + consolidate endpoints |
| Auth flicker | Single refresh mutex |

## Mistakes to Avoid
- **Mistake:** `useEffect` fetch without cleanup / race on id change
- **Mistake:** Incomplete cache keys
- **Mistake:** Putting server data only in Redux without a fetch cache

## Pros/Cons or Trade-offs
- **Pro:** Deduped fetches; fewer loading bugs.
- **Con:** Cache-key mistakes show wrong data.
- **Trade-off:** server-state libraries vs global client stores for remote data.

## Comparison
- vs [[Real-time Subscription]]: push updates vs pull/query cache.
- vs [[cache system]]: browser/query cache is one cache layer.


### Use cases
- SPA dashboards, mobile web apps, and BFFs feeding typed hooks.
