<!-- note-strategy: operational -->
[[React]] [[React Pattern/Component Presentational Pattern]] [[React Pattern/Provider pattern]]

# Separate functional logic from presentation components

> Keep domain rules out of JSX — you should be able to swap GUI for CLI without rewriting the rules.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Pure domain code computes; presentation only renders props and fires callbacks. If swapping the UI would force rewriting business rules, separation failed.

```txt
Domain (pure)  →  ViewModel / hooks  →  Presentational UI
     ↑                    ↑
  testable            thin glue
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MVC** | Model + View + Controller bridge | “Controller can still mix concerns.” |
| **MVP** | Passive view, presenter mediates | “View knows nothing about the model.” |
| **MVVM** | View binds to View-Model | “Formatting lives in VM, not DOM code.” |

## Standard config / commands

```tsx
// domain — no React
export function cartTotal(items: { price: number; qty: number }[]) {
  return items.reduce((s, i) => s + i.price * i.qty, 0)
}

// glue
function useCartVm(items: Item[]) {
  return { total: cartTotal(items), count: items.length }
}

// presentation — props only
function CartSummary({ total, count }: { total: number; count: number }) {
  return <p>{count} items · ${total}</p>
}
```

| Pattern | Who owns logic |
|---------|----------------|
| Container / Presentational | Container fetches & maps; presentational is dumb |
| Custom hooks | Logic reusable without a “container” component |
| Provider | Shared domain state injected; UI stays thin |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t unit-test totals | Logic inside JSX | Extract pure functions |
| Same rule duplicated in web + mobile | Coupled to DOM | Shared domain module |
| “Dumb” view still imports API | Fetch in presentational | Move fetch to hook/container |
| Hard to swap design system | Domain in styled components | Props in; no business imports |

---

## Gotchas

> [!WARNING]
> **Presentational ≠ zero hooks** — local UI state (open/closed) is fine; domain rules are not.

> [!WARNING]
> **MV\* labels don’t save you** — the swap-UI test matters more than the acronym.

---

## When NOT to use

- **Tiny throwaway screens** — three lines of logic don’t need a domain layer.
- **UI-only chrome** — no domain rules; keep it in the component.

---

## Related

[[React Pattern/Component Presentational Pattern]] [[React Pattern/Higher order Component (HOCs)]] [[React Pattern/Provider pattern]] [[React code smells]]
