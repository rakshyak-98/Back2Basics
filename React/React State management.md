[[react hooks]] [[React Architecture]] [[React design patterns]] [[data fetching component]] [[zustand]] [[Redux]] [[react-query]] [[RSC (React Server Component boundaries)]]

# React State management

> React state management is the discipline of choosing where each piece of application data lives — local UI state, shared client store, server cache, or URL — and using the smallest mechanism that keeps the UI consistent.

---

## Why It Matters

Reviewers and architects ask this constantly: "Why Context here and not Zustand? Why TanStack Query and not Redux for server data?" Wrong choices produce re-render storms (Context holding fast-changing values), duplicated caches (Redux mirroring query results), or security holes (tokens in localStorage). The modern answer is not one library — it is **assigning each datum an owner** and picking tools matched to update frequency and sharing scope.

---

## Sources

- [React — Managing State](https://react.dev/learn/managing-state) — Official guide to local state, lifting state, Context, and reducer patterns with decision criteria.
- [TanStack Query — React Overview](https://tanstack.com/query/latest/docs/framework/react/overview) — How server state differs from client state and why a dedicated cache layer exists.
- [Redux — Three Principles](https://redux.js.org/understanding/thinking-in-redux/three-principles) — When a predictable global store is justified and what problems it solves.
- [Zustand documentation](https://docs.pmnd.rs/zustand/getting-started/introduction) — Minimal global client store with selector-based subscriptions to avoid Context re-render issues.

---

## Key Concepts

### The four homes for data

| Data type | Owner | Tool | Update frequency |
|-----------|-------|------|------------------|
| **Server state** | Remote API | TanStack Query, RTK Query, SWR | Changes on server; stale-while-revalidate |
| **URL state** | Browser address bar | React Router `searchParams`, Next.js router | Shareable, bookmarkable filters and tabs |
| **Local UI state** | Component | `useState`, `useReducer` | Ephemeral — modals, form drafts, hover |
| **Shared client state** | Cross-route client | Context (low-freq), Zustand, Redux | Theme, cart, auth session, wizard progress |

```txt
                    ┌── Server cache (react-query)
                    ├── URL (?tab=billing&page=2)
User-visible data ──┤── Local UI (useState)
                    └── Global client (zustand / Redux)
```

### Decision rules

1. **Start local** — `useState` until two distant components need the same value.
2. **Context for low-frequency** — theme, locale, auth identity that changes rarely. Never Context for mouse position or scroll offset.
3. **Query library for server data** — never mirror `/api/users` into Redux manually.
4. **Zustand or Redux for shared client** — cart, multi-step wizard state shared across routes.
5. **URL for shareable filters** — table sort, pagination, selected tab.

---

## Technical Details

### Local state — single component

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Context — theme (low-frequency)

```tsx
const ThemeContext = createContext<'light' | 'dark'>('light');

function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  return (
    <ThemeContext.Provider value={theme}>
      <Layout onToggle={() => setTheme(t => t === 'light' ? 'dark' : 'light')} />
    </ThemeContext.Provider>
  );
}
```

### Server state — TanStack Query

```tsx
function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 60_000,
  });
  if (isLoading) return <Spinner />;
  if (error) return <ErrorBanner error={error} />;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### Shared client — Zustand with selectors

```tsx
import { create } from 'zustand';

const useCart = create<{ items: Item[]; add: (i: Item) => void }>((set) => ({
  items: [],
  add: (item) => set(s => ({ items: [...s.items, item] })),
}));

// Component only re-renders when items change — not on unrelated store updates
const count = useCart(s => s.items.length);
```

### URL state — filters in search params

```tsx
const [searchParams, setSearchParams] = useSearchParams();
const page = Number(searchParams.get('page') ?? '1');
setSearchParams({ page: String(page + 1), tab: 'billing' });
```

### Decision cheat sheet

| Need | Tool |
|------|------|
| One form field | `useState` |
| Theme / locale | Context |
| Product list from API | TanStack Query |
| Cart across pages | Zustand or Redux |
| Admin table filters | URL search params |
| Multi-step wizard shared across routes | Zustand |
| Auth token (prefer httpOnly cookie) | Server session — not client store |

---

## Mistakes to Avoid

- Context for high-frequency changing values — every consumer re-renders on every change.
- Mirroring every query result into Redux — two sources of truth, sync bugs guaranteed.
- Storing auth tokens in Redux persist middleware without XSS threat modeling.
- Redux Toolkit + TanStack Query for the same entity list — pick one owner.
- Global event bus for all application state — untraceable data flow.

---

## Pros/Cons or Trade-offs

| Approach | Pro | Con |
|----------|-----|-----|
| Local `useState` | Simplest; no dependencies | Prop drilling at scale |
| Context | Built-in; good for theme/locale | Re-render cost on frequent updates |
| TanStack Query | Caching, dedup, background refresh | Learning curve; not for client-only state |
| Zustand | Minimal API; selector subscriptions | Another dependency; team conventions needed |
| Redux | DevTools; middleware ecosystem | Boilerplate; overkill for small apps |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[data fetching component]] | Data fetching is one slice of data management — server cache ownership |
| [[react hooks]] | Hooks are the mechanism; this note is the architecture decision |
| [[Redux]] | Redux is one tool for shared client state — not for server cache |
| [[RSC (React Server Component boundaries)]] | Server Components fetch on server — different from client cache |

---

## Use cases

- E-commerce: product pages powered by TanStack Query; cart in Zustand; checkout step in URL; modal open state local.
- Admin dashboard: filters in URL (`?status=open&page=2`); table rows in Query; row selection in component state.
- Design system: theme and density in Context; component-internal hover/ focus in `useState`.
