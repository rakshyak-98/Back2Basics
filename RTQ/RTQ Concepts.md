[[matcher]] [[Prisma]]

# RTQ concepts (Redux Toolkit Query)

> Data-fetching layer on Redux Toolkit — define API endpoints once, get generated hooks, caching, and invalidation instead of hand-rolled thunks.

```txt
        RTQ concepts (Redu ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want cache tags/invalidation, generated hooks vs slices, and whe…

## Sources
- [Redux Toolkit — RTK Query](https://redux-toolkit.js.org/rtk-query/overview) — deep-dive

## Key Concepts
- **`createApi`:** endpoints + base query → reducer, middleware, hooks.
- **Cache keys:** args define cache entries.
- **Tags:** invalidate related queries after mutations.
- **Generated hooks:** `useGetXQuery` / `useLazy…` for components.

## Technical Details
```js
export const api = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Hotel"],
  endpoints: (build) => ({
    getHotel: build.query({
      query: (id) => `hotels/${id}`,
      providesTags: (r, e, id) => [{ type: "Hotel", id }],
    }),
  }),
});
```

- `configureStore` must add the API reducer and middleware

## Mistakes to Avoid
- **Mistake:** Forgetting to add API middleware (queries hang/no-op)
- **Mistake:** Over-fetching without tags — stale screens after writes
- **Mistake:** Duplicating the same remote state in hand-written slices

## Pros/Cons or Trade-offs
- **Pro:** Less boilerplate than custom thunks + normalization for REST.
- **Con:** Complex graphs may still need normalized stores or GraphQL clients.

## Comparison
- vs React Query: similar caching ideas; RTK Query lives inside Redux.
- vs [[matcher]]: matchers customize slice reactions to RTKQ actions.


### Use cases
- Booking UIs: list/detail queries share tags so a mutation refreshes the right…

- **Example:** After update hotel mutation, `invalidatesTags: [{ type: 'Hotel',…
