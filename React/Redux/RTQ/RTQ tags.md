[[Redux/RTQ Toolkit]] [[Redux/Redux createApi]] [[API handling]] [[react-query]] [[React data management]]

# RTQ tags

> RTK Query **cache labels** — `providesTags` on queries, `invalidatesTags` on mutations — automatic refetch graph — **RTK Query docs**.

---

## Mental model

Each cached query entry can **provide** tags `{ type, id? }`. Mutations **invalidate** tags → RTK refetches all queries that provided matching tags.

```txt
getPosts query   providesTags: [{ type: 'Post', id: 'LIST' }, { type: 'Post', id: 1 }, ...]
updatePost mut   invalidatesTags: [{ type: 'Post', id: 1 }]
→ getPost(1) and list queries refetch
```

Without tags, mutations leave **stale lists** until manual `dispatch(api.util.invalidateTags(...))`.

Internal shape (debug):

```txt
provided: {
  tags: { Post: { __internal_without_id: ['getAllPosts(undefined)'] } },
  keys: { 'getAllPosts(undefined)': [{ type: 'Post' }] }
}
```

**Providing** a tag = "this cache entry depends on tag X" → invalidating X drops/refetches it.

---

## Standard config / commands

```typescript
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Post", "User"],
  endpoints: (build) => ({
    getPosts: build.query<Post[], void>({
      query: () => "/posts",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Post" as const, id })),
              { type: "Post", id: "LIST" },
            ]
          : [{ type: "Post", id: "LIST" }],
    }),
    getPost: build.query<Post, string>({
      query: (id) => `/posts/${id}`,
      providesTags: (_r, _e, id) => [{ type: "Post", id }],
    }),
    updatePost: build.mutation<Post, Partial<Post> & { id: string }>({
      query: ({ id, ...body }) => ({ url: `/posts/${id}`, method: "PATCH", body }),
      invalidatesTags: (_r, _e, { id }) => [{ type: "Post", id }, { type: "Post", id: "LIST" }],
    }),
  }),
});
```

### Optimistic update (optional)

```typescript
async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
  const patchResult = dispatch(
    api.util.updateQueryData("getPost", id, (draft) => { Object.assign(draft, patch); })
  );
  try { await queryFulfilled; } catch { patchResult.undo(); }
}
```

Register `api.middleware` and `api.reducer` in store ([[Redux/RTQ Toolkit]]).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| List stale after create | Mutation missing `LIST` invalidation | `invalidatesTags: [{ type: 'Post', id: 'LIST' }]` |
| Too many refetches | Broad `{ type: 'Post' }` without id | Narrow id-specific invalidation |
| Tag not in tagTypes | Typo / missing registration | Add to `tagTypes` array |
| Query never refetches | `providesTags` omitted | Add providesTags to query endpoint |
| Flash empty during refetch | `keepUnusedDataFor` | Tune cache lifetime; optimistic update |

---

## Gotchas

> [!WARNING]
> **Invalidate everything** — `{ type: 'Post' }` without id invalidates **all** Post queries — expensive on large apps.

> [!WARNING]
> **Tags without LIST id** — creating item won't refresh collection views.

---

## When NOT to use

- **One-off read never mutated** — skip tags; static `keepUnusedDataFor`.
- **Real-time push** — WebSocket patch + `updateQueryData` may beat blind invalidation ([[webSocket]]).
- **Non-Redux app** — TanStack Query `queryKey` invalidation is the parallel ([[react-query]]).

---

## Related

[[Redux/RTQ Toolkit]] · [[Redux/Redux createApi]] · [[API handling]] · [[React data management]] · [[Redux/redux middleware]]
