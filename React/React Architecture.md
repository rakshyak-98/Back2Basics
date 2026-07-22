[[React Application Architecture for Production]] [[React data management]] [[react routes]] [[RSC (React Server Component boundaries)]] [[API handling]]

# React Architecture

> How you **split UI, state, data, and boundaries** so the app scales past one team — **Kent C. Dodds / React docs / production postmortems**.

---

## Mental model

Layers (top → bottom):

```txt
Routes / layouts          → URL → screen composition
Feature modules           → domain folders (cart/, billing/)
UI components             → dumb, reusable
State                     → server (Query/RTK) vs client (zustand/local)
Infrastructure            → api client, auth, error boundaries, i18n
```

Core challenges when building production React:

| Challenge | Mitigation |
|-----------|------------|
| **Server vs client state** | [[React data management]] — don't duplicate API in Redux |
| **Bundle size** | Code-split routes ([[react routes]]); lazy `React.lazy` |
| **Auth/session** | Central guard + token refresh ([[JWT authentication]]) |
| **Error isolation** | Route-level error boundaries |
| **SSR/RSC boundaries** | [[RSC (React Server Component boundaries)]] — `"use client"` minimal |
| **Testing** | Summary hooks + presentational views |
| **Env/config drift** | [[React project config]] typed env |

```txt
Bad:  every page imports axios + Redux + Context for same POST
Good: RTK Query endpoint + generated hook + route loader
```

---

## Standard config / commands

### Feature folder layout

```txt
src/
  app/           # providers, router, store
  features/
    billing/
      api.ts
      hooks/
      components/
      routes.tsx
  shared/        # Button, Modal — no feature imports upward
```

### App shell

```tsx
// app/Providers.tsx
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ReduxProvider store={store}>
        <ErrorBoundary FallbackComponent={PageCrash}>
          {children}
        </ErrorBoundary>
      </ReduxProvider>
    </QueryClientProvider>
  );
}
```

### Route-based code splitting

```tsx
const Billing = lazy(() => import("../features/billing/routes"));
// <Suspense fallback={<Skeleton />}><Billing /></Suspense>
```

Document **data flow ADR** when choosing Redux vs Query vs zustand ([[React State management]]).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Circular imports | Feature ↔ shared leak | Enforce dependency rule (eslint-plugin-import) |
| Hydration mismatch | Client-only APIs in RSC | Move to client leaf |
| Global re-render storm | Context at root | Colocate; selectors ([[zustand]]) |
| Inconsistent API errors | Per-page handling | Normalized error type in [[API handling]] |
| Slow initial load | No split | Route lazy + analyze bundle ([[React build]]) |

---

## Gotchas

> [!WARNING]
> **Premature micro-frontends** — fix module boundaries inside monorepo first.

> [!WARNING]
> **Redux for every GET** — cache belongs in Query ([[react-query]]); Redux for true client global state.

---

## When NOT to use

- **Marketing one-pager** — Vite + few components; skip feature folders.
- **Embedded widget** — isolate bundle, minimal router.
- **Copy-paste architecture from blog** — match team size and release cadence.

---

## Related

[[React Application Architecture for Production]] · [[React data management]] · [[Managing complex component structure]] · [[react routes]] · [[React build]]
