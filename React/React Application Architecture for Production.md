[[React]] [[RSC (React Server Component boundaries)]] [[React Architecture]]

# React Application Architecture for Production

> Structure a production React/Next app — feature folders, providers, and pick render strategy per page.

---

## Index

- [[#Context]]
- [[#Decision]]
- [[#Consequences]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Alternatives considered]]
- [[#Related]]

## Context

…

## Decision

We will … because …

## Consequences

**Positive:** …

**Negative / trade-offs:** …

## Mental model

**Say it in one breath:** Next.js wins when each route can choose SSR/SSG/CSR/RSC independently. Keep shared UI in `components`, domain in `features`, and wire one application-level provider tree.

```txt
pages/app (render strategy)
  → features/* (api, components, types, public index)
  → providers (one AppProvider)
  → lib / stores / utils
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Feature folder** | Vertical slice | “API + UI colocated; export only public surface.” |
| **Render strategy** | Per-page SSR/SSG/CSR | “Why teams pick Next.” |
| **providers/** | Compose contexts | “One wrapper in root layout.” |

## Standard config / commands

```txt
src/
  components/     # shared UI
  config/
  features/
    booking/
      api/
      components/
      types/
      index.ts    # public exports only
  layouts/
  lib/
  providers/      # → AppProvider
  stores/
  testing/
  types/
  utils/
```

```tsx
// providers/index.tsx
export function AppProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={qc}>
      <ThemeProvider>{children}</ThemeProvider>
    </QueryClientProvider>
  )
}
```

| Knob | Why it matters |
|------|----------------|
| `features/*/index.ts` | Prevents deep imports across features |
| `api/` inside feature | Keeps UI ↔ network boundary clear |
| Page-level render mode | Mix marketing SSG + app SSR |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Circular imports | Feature A imports B internals | Export via `index.ts` only |
| Provider order bugs | Auth under Query | Nest: theme → query → auth |
| Huge shared `components/` | Feature UI leaked up | Move into `features/x/components` |
| Wrong cache/SSR mix | Page used client fetch only | Align with Next render mode |

---

## Gotchas

> [!WARNING]
> **“Everything in components/” becomes a junk drawer** — feature-scope first.

> [!WARNING]
> **Multiple Providers without a single AppProvider** — root layout becomes unreadable.

---

## When NOT to use

- **Tiny marketing site** — flat folders beat ceremony.
- **No SSR needs** — Vite SPA may be enough; don’t force Next.

---

## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

## Related

[[React Architecture]] [[RSC (React Server Component boundaries)]] [[React project configuration]] [[Managing complex component structure]]
