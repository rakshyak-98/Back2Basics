[[React data management]] [[expressjs]] [[Event Loop]] [[webSocket]] [[Session Storage]]

# Zustand

> Minimal client-state library for React — store outside the component tree with selective subscriptions — **when Redux is overkill**.

```txt
        Zustand ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers separate server state vs client UI state and ask when Context, R…

## Sources
- [Zustand documentation](https://docs.pmnd.rs/zustand/getting-started/introduction) — deep-dive
- [Zustand GitHub](https://github.com/pmndrs/zustand) — overview

## Key Concepts
- **Note:** Zustand holds state in a **vanilla store** (works without React). Components …

| Pattern | API |
|---------|-----|
| **Simple store** | `create((set) => ({ count: 0, inc: () => set(s => ({ count: s.count+1 })) }))` |
| **Selector** | `useStore(s => s.count)` — re-render only when `count` changes |
| **Outside React** | `useStore.getState().inc()` in event handlers, middleware |
| **Slices** | Multiple `create` stores or combine with middleware |

- **Note:** **Server state** (API data, cache, stale-while-revalidate) belongs in **TanSt…

## Technical Details
```txt
┌─────────────┐     subscribe(selector)     ┌─────────────┐
│  Component  │ ◄──────────────────────── │ Zustand     │
└─────────────┘                             │ store       │
       │ dispatch set()/actions              └──────┬──────┘
       └──────────────────────────────────────────►│
```

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

- On server: **new store per request**.
- On client: hydrate once from serialized snapshot or accept flash.

## Mistakes to Avoid
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

- **Mistake:** **Zustand for API cache**
- **Mistake:** **SSR singleton leak**
- **Selector object**::** → infinite renders without `useShallow`
- **Mistake:** **persist + sensitive data**
- **Mistake:** **Testing**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Server-fetched lists with cache invalidation**
- **Con / skip when:** **Complex event-sourced domain**
- **Con / skip when:** **Cross-tab sync requirements**

## Real-World Applications
- **Scenario:** Apply Zustand in feature code where the Key Concepts match
