[[presentation layer]] [[Service Layer]] [[React Application Architecture for Production]] [[feature flag]]

# frontend layered architecture

> Frontend layers separate UI, state, and API access — so screens don’t each reinvent fetching and rules.

```txt
        frontend layered a ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Frontend layering interviews check whether UI, state, and API access stay sep…

## Sources
- [React — Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [Martin Fowler — Presentation Domain Separation](https://martinfowler.com/eaaCatalog/presentationDomainSeparation.html) — deep-dive

## Key Concepts
```txt
Pages/Views → State (hooks/store) → API client → Backend
     ↑ presentational
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Presentational** | Dumb UI | “Props in, events out.” |
| **Container / hook** | Wiring + fetch | “Owns loading/error.” |
| **API module** | HTTP + DTO map | “One place for endpoints.” |
| **Server state** | Remote cache | “react-query / RTK Query.” |

## Technical Details
```ts
// data layer
export const getOrder = (id: string) => api.get<OrderDto>(`/orders/${id}`)

// feature hook
export function useOrder(id: string) {
  return useQuery({ queryKey: ['order', id], queryFn: () => getOrder(id) })
}

// view
export function OrderPage({ id }: { id: string }) {
  const { data, isLoading } = useOrder(id)
  if (isLoading) return <Spinner />
  return <OrderView order={data} />
}
```

| Knob | Why it matters |
|------|----------------|
| Query keys | Cache correctness |
| Error boundaries | One crash ≠ white screen |
| Feature folders | Colocate UI + hook + api |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Fetch in every leaf | Network waterfall | Lift to route/loader |
| Stale UI after mutate | Cache not invalidated | Invalidate query key |
| God context | Whole app rerenders | Split stores / query |
| Business rules only in UI | Pricing in React | Enforce on API too |

## Mistakes to Avoid
- **Mistake:** Prop drilling “layers”
- **Mistake:** Duplicated clients

## Pros/Cons or Trade-offs
- **Trade-off:** Marketing static page — no need for stores and API modules.
- **Trade-off:** Tiny widget — one component + fetch is fine until it grows.
