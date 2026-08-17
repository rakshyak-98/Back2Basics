[[react hooks]] [[React State management]] [[React Architecture]] [[react-query]] [[Component Presentational Pattern]] [[Compound Components]]

# data fetching component

> A data-fetching component loads remote data and renders a view — in modern React the preferred pattern is a custom hook plus a presentational component, with TanStack Query owning server cache state.

---

## Why It Matters

Before hooks, teams used class components with `componentDidMount`, render-prop data fetchers, and Higher-Order Components like `withData(UserList)`. Today the pattern is: **hook owns fetch + cache**, **component owns JSX**. Reviewers still ask about separation of concerns, loading/error states, and cache invalidation — the data-fetching component pattern is the architectural boundary between "how we get data" and "how we show it."

---

## Sources

- [TanStack Query — React Overview](https://tanstack.com/query/latest/docs/framework/react/overview) — Server state as a first-class cache with stale-while-revalidate, deduplication, and background refetch.
- [React — You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — Why fetching in `useEffect` without a cache layer causes race conditions and duplicate requests.
- [React — Separating Events from Effects](https://react.dev/learn/separating-events-from-effects) — When effects are appropriate vs event handlers for data loading.

---

## Key Concepts

### Modern pattern (hook + presentational)

```txt
useUsers() hook          UserList component
├── queryKey             ├── calls useUsers()
├── queryFn (fetch)      ├── renders loading / error / data
├── staleTime            └── no fetch logic inside JSX
└── cache (TanStack Query)
```

| Layer | Responsibility |
|-------|----------------|
| **Query hook** | Fetch, cache, retry, dedupe, background refresh |
| **Presentational component** | Loading skeleton, error banner, empty state, data table |
| **Container (optional)** | Wire hook to component when testing demands separation |

### Legacy patterns (know for maintenance)

| Pattern | Era | Issue |
|---------|-----|-------|
| Class `componentDidMount` fetch | Pre-hooks | No cache; race conditions on prop change |
| Render props `<DataFetcher render={...}/>` | 2017–2019 | Callback hell; hard to compose |
| HOC `withUsers(UserList)` | 2016–2018 | Wrapper hell; lost static types |
| `useEffect` + `useState` | Hooks early | Duplicate fetches; no deduplication |

---

## Technical Details

### Recommended: custom hook + component

```tsx
// hooks/useUsers.ts
import { useQuery } from '@tanstack/react-query';

export function useUsers(status?: string) {
  return useQuery({
    queryKey: ['users', status],
    queryFn: () =>
      fetch(`/api/users?status=${status ?? ''}`).then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      }),
    staleTime: 60_000,
  });
}

// components/UserList.tsx
export function UserList({ status }: { status?: string }) {
  const { data, isLoading, error, refetch } = useUsers(status);

  if (isLoading) return <Skeleton rows={5} />;
  if (error) return <ErrorBanner message={error.message} onRetry={refetch} />;
  if (!data?.length) return <EmptyState label="No users found" />;

  return (
    <table>
      <tbody>{data.map(u => <tr key={u.id}><td>{u.name}</td></tr>)}</tbody>
    </table>
  );
}
```

### Suspense boundary (React 18+)

```tsx
function UserListSuspended() {
  const { data } = useSuspenseQuery({ queryKey: ['users'], queryFn: fetchUsers });
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Parent:
<ErrorBoundary fallback={<ErrorPage />}>
  <Suspense fallback={<Skeleton />}>
    <UserListSuspended />
  </Suspense>
</ErrorBoundary>
```

### Presentational / container split (when testing demands it)

```tsx
// Pure — easy to test with mock data
export function UserTable({ users, onSelect }: { users: User[]; onSelect: (id: string) => void }) {
  return <table>...</table>;
}

// Container — wires hook to presentational
export function UserTableContainer() {
  const { data, isLoading, error } = useUsers();
  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner error={error} />;
  return <UserTable users={data} onSelect={id => navigate(`/users/${id}`)} />;
}
```

---

## Mistakes to Avoid

- Fetching in `useEffect` without abort/cleanup — race when props change quickly.
- Putting fetch logic inline in JSX — untestable and mixes concerns.
- Mirroring query cache into Redux or Zustand — two sources of truth.
- No error boundary or error UI — white screen on network failure.
- Ignoring `staleTime` — refetch on every mount causes unnecessary load.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Clear separation: hook = data, component = view | Two files for simple lists |
| TanStack Query handles cache, retry, dedup | Learning curve for query keys and invalidation |
| Presentational components easy to test | Over-abstraction for one-off pages |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[React State management]] | Data fetching is server-state ownership within broader state architecture |
| [[Compound Components]] | Composition pattern for UI structure, not data loading |
| [[Component Presentational Pattern]] | Same split — container/hook fetches, presentational renders |

---

## Use cases

- Admin user table: `useUsers(status)` hook + `UserTable` presentational component.
- Product detail page: `useProduct(id)` with Suspense boundary and skeleton fallback.
- Dashboard widgets: parallel `useQuery` calls with independent loading states per card.
