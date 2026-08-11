[[React data management]] [[zustand]] [[Redux]] [[react hooks]] [[react-query]]

# React State management

> **Where** state lives — local UI, lifted, context, zustand, Redux, server cache — pick by lifetime and audience — **Kent C. Dodds (state colocation)**.

---

## Mental model

```txt
UI ephemeral (open modal)     → useState colocated
Shared UI (theme, wizard)   → Context / zustand
Server data (API lists)     → TanStack Query / RTK Query
Global client + time-travel → Redux Toolkit (narrow cases)
URL state (filters, tab)    → searchParams / router
```

You can **derive** values in render — don't duplicate state:

```tsx
const fullName = `${first} ${last}`; // not useState unless user edits fullName directly
```

Decision tree:

```txt
Need server cache?     YES → Query/RTK Query ([[React data management]])
Else need global UI?   YES → [[zustand]] (simple) or Redux (middleware/devtools)
Else                   useState / useReducer in feature
```

---

## Standard config / commands

### Local + derived

```tsx
function FilterList({ items }: { items: Item[] }) {
  const [q, setQ] = useState("");
  const filtered = useMemo(
    () => items.filter((i) => i.name.includes(q)),
    [items, q]
  );
  return (/* input + list */);
}
```

### useReducer for complex transitions

```tsx
type State = { step: number; data: FormData };
type Action = { type: "next" } | { type: "patch"; field: string; value: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "next": return { ...state, step: state.step + 1 };
    case "patch": return { ...state, data: { ...state.data, [action.field]: action.value } };
    default: return state;
  }
}
```

### Server state (don't put in Redux by default)

```tsx
const { data: user } = useQuery({ queryKey: ["me"], queryFn: fetchMe });
```

See [[zustand]] for client-global pattern; [[Redux]] when you need audit middleware across many features.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stale list after POST | Server state not invalidated | Query invalidate / RTK tags |
| Context re-render entire tree | Value not memoized | Split context; zustand selectors |
| Two sources of truth | Same entity in Redux + Query | Single owner — usually Query |
| Lost state on refresh | Expected for RAM | Persist or URL encode |
| Infinite update loop | setState in render | Derive or useEffect deps |

---

## Gotchas

> [!WARNING]
> **useEffect to sync props → state** — prefer key remount or controlled pattern.

> [!WARNING]
> **Redux for form field focus** — colocate; global store noise.

---

## When NOT to use

- **Everything in Redux** — 2017 pattern; server cache belongs in Query.
- **Context for high-frequency updates** — perf cliff; use zustand/external store.
- **Global store for one screen** — local state until second consumer exists.

---

## Related

[[React data management]] · [[zustand]] · [[Redux]] · [[react-query]] · [[referential equality]]
