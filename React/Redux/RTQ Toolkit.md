<!-- note-strategy: operational -->
[[Redux]] [[Redux/Redux createApi]] [[Redux/RTQ/RTQ store]]

# RTQ Toolkit

> RTK Query as the data cache — keyed queries, tag invalidation, optional persistence across refresh.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** RTK Query stores responses under `state[reducerPath].queries` keyed by endpoint+arguments. Mutations invalidate tags; hooks expose `data` / loading / error. Memory cache clears on full reload unless you persist.

```txt
useGetXQuery(args)
  → cache hit? return data
  → else fetch → cache → notify subscribers
mutation → invalidatesTags → refetch active queries
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Query key** | Endpoint + serialized args | “Same key → shared cache.” |
| **invalidateTags** | Force refetch | “After create/update/delete.” |
| **initiate** | Dispatch without hook | “`dispatch(api.endpoints.x.initiate())`.” |
| **refetchOnMountOrArgChange** | Freshness window | “Number = max age seconds.” |

## Standard config / commands

```ts
export const productApi = createApi({
  reducerPath: 'productApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['product'],
  refetchOnMountOrArgChange: 30,
  endpoints: (b) => ({
    getAll: b.query<Product[], void>({
      query: () => '/products',
      providesTags: ['product'],
    }),
  }),
})

// manual refresh
dispatch(productApi.util.invalidateTags(['product']))
```

| Knob | Why it matters |
|------|----------------|
| Sync into other slices | Prefer tags; or `fixedCacheKey` / listeners — don’t dual-write casually |
| Persist | `redux-persist` on `api.reducerPath` if reload must keep cache |
| `transformResponse` | Normalize before cache |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Refetch every mount | `refetchOnMountOrArgChange: true` | Use number or false |
| Stale after mutation | Missing invalidate | Wire tags |
| Cache gone after F5 | Expected memory | Persist or accept refetch |
| Polling dead | No `setupListeners` | See [[Redux/RTQ/RTQ store]] |
| Dual state drift | Slice + Query copy | Single source of truth |

---

## Gotchas

> [!WARNING]
> **RTK Query does not auto-write your auth slice** — sync explicitly if tokens live elsewhere.

> [!WARNING]
> **Persisting Query blindly** — can serve stale secured data; whitelist carefully.

---

## When NOT to use

- **Websocket-only live feeds** — streaming updates pattern or different store.
- **Local-only CRUD** — `createEntityAdapter` slice.

---

## Related

[[Redux/Redux createApi]] [[Redux/RTQ/RTQ store]] [[Redux/RTQ/RTQ tags]] [[Redux/redux persist]] [[react-query]]
