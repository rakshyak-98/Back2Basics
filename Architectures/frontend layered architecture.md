[[presentation layer]] [[Service Layer]] [[React Application Architecture for Production]]

# frontend layered architecture

> Frontend layers separate UI, state, and API access — so screens don’t each reinvent fetching and rules.

---

## Mental model

**Say it in one breath:** Views render; hooks/stores hold UI state; an API/data layer talks to the backend — keep side effects out of leaf components.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Fetch in every leaf | Network waterfall | Lift to route/loader |
| Stale UI after mutate | Cache not invalidated | Invalidate query key |
| God context | Whole app rerenders | Split stores / query |
| Business rules only in UI | Pricing in React | Enforce on API too |

---

## Gotchas

> [!WARNING]
> **Prop drilling “layers”** — deep trees without a data layer still couple everything.

> [!WARNING]
> **Duplicated clients** — three axios instances with three auth headers.

---

## When NOT to use

- **Marketing static page** — no need for stores and API modules.
- **Tiny widget** — one component + fetch is fine until it grows.

## Related

[[presentation layer]] [[React Application Architecture for Production]] [[feature flag]]
