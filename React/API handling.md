[[react hooks]] [[React State management]] [[React Architecture]]

# API handling

> How React apps call backends — fetch in effects or query libraries, handle loading/error, and keep server data out of UI stores.

## Interview Relevance

Interviewers ask where API calls live, how you cancel them, and why duplicating server payloads in Redux is usually wrong.

## Sources

- [React — Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) — overview
- [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview) — deep-dive

## Core Definition

API handling is the boundary between UI and HTTP: request lifecycle, cache, retries, and mapping responses into props — not putting every JSON field into global client state.

## Key Concepts

- **Fetch placement:** Prefer a data library ([[react-query]] / RTK Query) over ad-hoc `useEffect` + `useState` for lists and detail views.
- **Loading / error / empty:** Model all three explicitly; never leave the UI on a spinner forever.
- **Cancellation:** Abort in-flight requests on unmount or key change to avoid setState-after-unmount and race conditions.
- **Auth headers:** Centralize the client (interceptor) so tokens and CSRF stay in one place.

## Technical Details

```tsx
// Prefer query keys + cache over manual effect fetch
const { data, error, isPending } = useQuery({
  queryKey: ['user', id],
  queryFn: ({ signal }) => fetch(`/api/users/${id}`, { signal }).then(r => r.json()),
})
```

| Concern | Prefer |
|---------|--------|
| Server lists / detail | [[react-query]] or [[Redux/Redux createApi\|RTK Query]] |
| Ephemeral UI (modal open) | `useState` / [[zustand]] |
| Cross-feature client snapshot | [[Redux]] only when many views share it |

## Real-World Applications

Dashboard that loads `/api/orders` with stale-while-revalidate: show cached rows instantly, refetch in background, surface toast on error.

## Pros/Cons or Trade-offs

- **Pro:** Shared API client + query cache cuts duplicate requests and loading flicker.
- **Con:** Hand-rolled effects recreate caching/race bugs the libraries already solved.

## Comparison

- vs putting API JSON in [[Redux]]: use Redux for client intent; use a query layer for server cache ([[React data management]]).

## Mistakes to Avoid

- Fetching in every child without a shared cache (N identical GETs).
- Ignoring AbortController / query cancellation on rapid navigation.
- Treating HTTP errors as empty data instead of an error state.
