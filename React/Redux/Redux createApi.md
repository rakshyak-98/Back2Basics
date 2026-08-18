[[Redux]] [[Redux/RTQ Toolkit]] [[Redux/RTQ/RTQ store]]

# Redux createApi

> Define endpoints once — RTK Query builds reducer, middleware, cache keys, and React hooks.

## Mental model

**Say it in one breath:** `createApi` describes how to talk to your backend. Queries cache by endpoint+arguments; mutations invalidate tags so lists refetch. Hooks are React sugar over the same API slice.

```txt
createApi({ baseQuery, tagTypes, endpoints })
  → api.reducer + api.middleware
  → useXQuery / useYMutation
  → providesTags / invalidatesTags
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **fetchBaseQuery** | Thin fetch wrapper | “Set `baseUrl` + `credentials`.” |
| --- | --- | --- |
| **providesTags** | Mark cached data | “This list is `Users`.” |
| **invalidatesTags** | Bust related cache | “POST then refetch list.” |
| **ApiProvider** | Mini store for demos | “Use real store in apps.” |
| **Lazy query** | Fetch on demand | “`useLazyGetXQuery`.” |

## Standard config / commands

```ts
export const cartApi = createApi({
  reducerPath: 'cartApi',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_BASE_URL,
    credentials: 'include', // cookies off by default (same-origin)
  }),
  tagTypes: ['Cart'],
  endpoints: (builder) => ({
    fetchCart: builder.query<CartItem[], void>({
      query: () => '/cart',
      providesTags: ['Cart'],
    }),
    addItem: builder.mutation<CartItem, CartItem>({
      query: (item) => ({ url: '/cart', method: 'POST', body: item }),
      invalidatesTags: ['Cart'],
    }),
  }),
})
export const { useFetchCartQuery, useAddItemMutation } = cartApi
```

| Knob | Why it matters |

| `credentials: 'include'` | Send cookies cross-site/same-site as needed |
| --- | --- |
| `tagTypes` | Required before provide/invalidate |
| Lazy vs auto | Mount-time vs button-click fetch |
| `transformResponse` | Shape before cache |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Cookies missing | Default credentials | Set `credentials: 'include'` |
| List stale after POST | No tags | `providesTags` / `invalidatesTags` |
| Hook undefined | Wrong import path | `@reduxjs/toolkit/query/react` |
| Duplicate requests | New args object each render | Stabilize args / serialize |
| Browser shows cached 200 | HTTP cache vs RTKQ | Different layers — check Network |

## Gotchas

> [!WARNING]
> **`ApiProvider` + existing Provider** — don’t nest two Redux stores; mount the api on your store.

> [!WARNING]
> **Cache dies on full reload** — memory only unless you persist.

## When NOT to use

- **Non-cached RPC fire-and-forget** — plain thunk may be simpler.
- **GraphQL-heavy Apollo shops** — don’t run two caches without need.

## Related

[[Redux/RTQ Toolkit]] [[Redux/RTQ/RTQ store]] [[Redux/RTQ/RTQ tags]] [[Redux/Redux createAsyncThunk]]
