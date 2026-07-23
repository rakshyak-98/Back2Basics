[[zustand]] [[expressjs]] [[Event Loop]] [[webSocket]] [[JWT authentication]]

# React data management

> Decision tree: **server state vs client state** — where TanStack Query, RTK Query, Zustand, and Context belong — **staff-level frontend architecture**.

---

## Mental model

Split state by **source of truth** and **lifecycle**:

```txt
                    ┌─ Server state ─────────────────────────────┐
                    │  API/DB owns it; UI is a cache             │
                    │  Tools: TanStack Query, RTK Query, SWR       │
                    └────────────────────────────────────────────┘
                    ┌─ Client state ─────────────────────────────┐
                    │  UI-only: modals, filters, wizard step     │
                    │  Tools: useState, Zustand, URL searchParams  │
                    └────────────────────────────────────────────┘
                    ┌─ URL state ────────────────────────────────┐
                    │  Shareable, bookmarkable: ?page=2&sort=date│
                    └────────────────────────────────────────────┘
```

| Question | If yes → |
|----------|----------|
| Can another user/tab see different value for same screen? | Server state |
| Lost on refresh OK / should restore from API? | Server state |
| Pure UI (drawer open, selected tab)? | Client state |
| Should back button restore it? | URL state |
| Needs optimistic update + rollback? | Query mutation + optional client cache |

**Anti-pattern:** fetch in `useEffect` + `useState` + manual loading flags — you rebuilt React Query poorly.

---

## Standard config / commands

### Decision tree (quick)

```txt
1. Data from HTTP/GraphQL?
   YES → TanStack Query (default) or RTK Query (already on Redux)
   NO  → 2

2. Shared across many components, not from server?
   YES → [[zustand]] (medium) or useState lifted (small)
   NO  → 3

3. Should URL reflect it?
   YES → searchParams / router state
   NO  → local useState

4. Form with validation?
   → React Hook Form + server submit via Query mutation

5. Real-time push?
   → Query cache invalidate on [[webSocket]] event; don't duplicate in Zustand
```

### TanStack Query baseline

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['orders', orderId],
  queryFn: () => fetchOrder(orderId),
  staleTime: 30_000,
});

const mutation = useMutation({
  mutationFn: updateOrder,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['orders'] }),
});
```

### Zustand for UI shell

```typescript
// [[zustand]] — sidebar, theme, multi-step wizard step
const step = useWizard((s) => s.step);
```

### RTK Query (Redux shops)

```typescript
// When: existing Redux, time-travel debug, unified middleware
const { data } = useGetOrderQuery(orderId);
// Client slice for UI-only alongside
```

### Context — narrow use

```txt
✓ Theme, i18n, auth identity (read-mostly)
✓ Dependency injection (rare)
✗ High-frequency updates (re-renders all consumers)
✗ Server lists / pagination
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stale list after mutation | invalidateQueries / tag invalidation | Add onSuccess invalidation; optimistic update |
| Double fetch on mount | Strict Mode + no dedupe | Query dedupes by key — remove duplicate useEffect fetch |
| Global loading spinner forever | queryKey mismatch | Align keys between list/detail |
| State lost on refresh | Client-only Zustand | Persist or fetch from server |
| Two sources of truth | Same entity in Zustand + Query | Single source — Query cache; UI flags only in Zustand |
| SSR hydration flash | fetch on client only | prefetch in loader / dehydrate QueryClient |
| Redux boilerplate fatigue | RTK for everything | Server → Query; UI → Zustand slice |

---

## Gotchas

> [!WARNING]
> **Copy server data into Zustand** — sync bugs on refetch; derive from Query cache with selectors.

> [!WARNING]
> **normalize by hand** — if you need entity graphs across screens, RTK Query cache or normalized Query patterns — not scattered useState.

> [!WARNING]
> **Context for "global store"** — performance cliff at scale; fine for 2–3 low-churn values.

> [!WARNING]
> **URL as only store for sensitive filters** — leaks in logs/referrers; sanitize.

> [!WARNING]
> **WebSocket + Query** — patch cache with `setQueryData` instead of parallel Zustand copy.

---

## When NOT to use

| Tool | Skip when |
|------|-----------|
| **Redux/RTK** | Greenfield app with no complex client workflows |
| **Zustand** | Data belongs to server; use Query |
| **React Query** | Static site, no remote data |
| **Jotai/Recoil** | Team lacks atom graph debugging experience — default to Query + Zustand |

---

## Related

[[zustand]] [[expressjs]] [[Event Loop]] [[webSocket]] [[JWT authentication]] [[Session Storage]]
