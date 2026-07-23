[[React data management]] [[expressjs]] [[Event Loop]] [[webSocket]]

# Zustand

> Minimal client-state library for React — store outside the component tree with selective subscriptions — **when Redux is overkill**.

---

## Mental model

Zustand holds state in a **vanilla store** (works without React). Components **subscribe** to slices; only subscribers to changed keys re-render. No Provider required (unlike Context performance traps).

```txt
┌─────────────┐     subscribe(selector)     ┌─────────────┐
│  Component  │ ◄──────────────────────── │ Zustand     │
└─────────────┘                             │ store       │
       │ dispatch set()/actions              └──────┬──────┘
       └──────────────────────────────────────────►│
```

| Pattern | API |
|---------|-----|
| **Simple store** | `create((set) => ({ count: 0, inc: () => set(s => ({ count: s.count+1 })) }))` |
| **Selector** | `useStore(s => s.count)` — re-render only when `count` changes |
| **Outside React** | `useStore.getState().inc()` in event handlers, middleware |
| **Slices** | Multiple `create` stores or combine with middleware |

**Server state** (API data, cache, stale-while-revalidate) belongs in **TanStack Query / RTK Query** — not Zustand. See [[React data management]].

---

## Standard config / commands

### Basic store

```typescript
import { create } from 'zustand';

type CartStore = {
  items: string[];
  add: (id: string) => void;
  clear: () => void;
};

export const useCart = create<CartStore>((set) => ({
  items: [],
  add: (id) => set((s) => ({ items: [...s.items, id] })),
  clear: () => set({ items: [] }),
}));

// Component
function Badge() {
  const count = useCart((s) => s.items.length);
  return <span>{count}</span>;
}
```

### Immer (nested updates)

```typescript
import { immer } from 'zustand/middleware/immer';

export const useUI = create(
  immer<{ panels: Record<string, boolean>; toggle: (k: string) => void }>((set) => ({
    panels: {},
    toggle: (k) =>
      set((state) => {
        state.panels[k] = !state.panels[k];
      }),
  }))
);
```

### Persist (localStorage)

```typescript
import { persist } from 'zustand/middleware';

export const usePrefs = create(
  persist(
    (set) => ({ theme: 'light', setTheme: (t: string) => set({ theme: t }) }),
    { name: 'prefs-v1' }
  )
);
```

### SSR (Next.js) — critical pattern

```typescript
// store.ts — avoid sharing server singleton state across requests
import { createStore } from 'zustand/vanilla';

export const createCartStore = () =>
  createStore<CartStore>((set) => ({ /* ... */ }));

// per-request in RSC/App Router or getServerSideProps — never global on server
```

On server: **new store per request**. On client: hydrate once from serialized snapshot or accept flash.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Too many re-renders | Selector returns new object each time | Stable selector; `useShallow` for object picks |
| State wrong after navigation (SSR) | Global store on server | Per-request store factory |
| Hydration mismatch | persist rehydrates after first paint | `skipHydration`, render placeholder until rehydrated |
| Stale closure in action | Old state captured | Use functional `set(s => ...)` |
| Lost state on refresh | No persist middleware | persist or server as source of truth |
| DevTools empty | Missing middleware | `devtools` middleware in dev only |

```typescript
import { useShallow } from 'zustand/react/shallow';
const { a, b } = useStore(useShallow((s) => ({ a: s.a, b: s.b })));
```

---

## Gotchas

> [!WARNING]
> **Zustand for API cache** — reinventing React Query: no stale time, dedup, background refetch, error retry.

> [!WARNING]
> **SSR singleton leak** — user A's cart visible to user B — catastrophic; always isolate server stores.

> [!WARNING]
> **Selector object** — `useStore(s => ({ x: s.x, y: s.y }))` new ref every time → infinite renders without `useShallow`.

> [!WARNING]
> **persist + sensitive data** — localStorage is XSS-readable; don't persist tokens.

> [!WARNING]
> **Testing** — reset store between tests: `useCart.setState({ items: [] }, true)`.

---

## When NOT to use

- **Server-fetched lists with cache invalidation** — TanStack Query / RTK Query.
- **Complex event-sourced domain** — Redux Toolkit + RTK Query or explicit event store.
- **Cross-tab sync requirements** — add `BroadcastChannel` or use URL/server state.

---

## Related

[[React data management]] [[Event Loop]] [[Session Storage]] [[expressjs]]
