[[React Architecture]] [[React design patterns]] [[React data management]] [[zustand]]

# Ad hoc system (React context)

> A **one-off, purpose-built** solution for a single feature — fast locally, expensive globally if it becomes the default pattern — **Fowler (refactoring)** applied to frontend.

---

## Mental model

"Ad hoc" (Latin: *for this*) = code shaped for **one screen or sprint**, not a reusable platform.

```txt
Quick fix: prop drill 3 levels + local useState
Ad hoc "system": copy-paste same fetch/cache logic in 5 routes
Platform: shared QueryClient, design tokens, routing layout
```

In React codebases, ad hoc systems appear as:

| Smell | Example |
|-------|---------|
| Duplicate fetch logic | Each page rolls its own `useEffect` + axios |
| Global `window` hacks | Event bus on `window` for cross-tree talk |
| One-off Context | `ThemeContext` + `CartContext` + `ModalContext` per feature |
| Inline business rules | 200-line component with no extraction |

Fine for **prototypes and experiments**; toxic when it becomes production architecture without review.

---

## Standard config / commands

### When ad hoc is acceptable

```tsx
// Spike / internal tool — explicit TTL in comment
export function AdminExportButton() {
  const [busy, setBusy] = useState(false);
  // ADHOC: direct fetch until export API stabilizes (ticket ENG-1234)
  const onClick = () => {
    setBusy(true);
    fetch("/api/v1/export-legacy").finally(() => setBusy(false));
  };
  return <button disabled={busy} onClick={onClick}>Export</button>;
}
```

### Graduation path (ad hoc → maintainable)

1. **Extract hook** — `useExport()` with error/loading contract.
2. **Centralize server state** — RTK Query / TanStack Query ([[React data management]]).
3. **Document boundary** — ADR or ticket linking replacement.

```tsx
// After graduation
function useExport() {
  return useMutation({ mutationFn: () => api.post("/api/v2/export") });
}
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Same bug in many pages | Copy-paste ad hoc fetch | Single hook or RTK endpoint |
| State desync across tabs | Ad hoc localStorage writes | [[Redux/Redux State sync with localstorage]] or Query persist |
| Un-testable components | Logic in JSX | Extract pure functions / hooks |
| "Works on my machine" env | Hardcoded URLs | [[React project config]] env vars |
| Performance death by Context | Ad hoc Provider tree | [[zustand]] or colocate state |

---

## Gotchas

> [!WARNING]
> **Ad hoc Context for server data** — no cache, dedupe, or stale-while-revalidate; use [[react-query]] / RTK Query instead.

> [!WARNING]
> **Temporary flags live forever** — `// TODO` ad hoc paths become critical prod paths without tests.

---

## When NOT to use

- **Shared across 3+ features** — invest in [[React Architecture]] and [[React data management]].
- **Auth, billing, permissions** — never one-off; centralize and audit.
- **Design system components** — use tokens + shared library, not inline styles per screen.

---

## Related

[[React Architecture]] · [[Managing complex component structure]] · [[React data management]] · [[React Pattern/Summary pattern]] · [[zustand]]
