[[React Pattern]] [[React code smells]] [[React Pattern/Provider pattern]]

# Component Presentational Pattern

> Split “how data is loaded” (container) from “how it looks” (presentational) — UI stays reusable and easy to test.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Container owns fetch/state/handlers; presentational component is mostly props → JSX.

```txt
CartContainer ──props──► CartView (pure-ish UI)
     │
  hooks / Redux / Query
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Container** | Data + behavior | “Wires the screen to APIs.” |
| **Presentational** | Props in, UI out | “Storybook-friendly; no fetch.” |
| **Modern take** | Custom hooks | “`useCart()` + dumb view replaces class containers.” |

## Standard config / commands

```tsx
function CartView({ items, total, onRemove }: Props) {
  return (
    <ul>
      {items.map((i) => (
        <li key={i.id}>
          {i.name} <button onClick={() => onRemove(i.id)}>x</button>
        </li>
      ))}
      <p>Total: {total}</p>
    </ul>
  )
}

function CartContainer() {
  const { items, total, remove } = useCart()
  return <CartView items={items} total={total} onRemove={remove} />
}
```

| Knob | Why it matters |
|------|----------------|
| Props-only view | Snapshot/visual tests without mocking network |
| Hook as container | Less nesting than wrapper components |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t reuse UI | Fetch inside view | Extract container/hook |
| Prop explosion | Too many props | Group into view-model object |
| Logic leaks into JSX | Inline business rules | Move to hook |
| Over-split noise | One-liner wrappers | Merge until pain returns |

---

## Gotchas

> [!WARNING]
> **Don’t cargo-cult folders** — `containers/` vs `components/` without a rule just adds hops.

> [!WARNING]
> **Presentational ≠ no hooks** — local UI state (open/closed) is fine in the view.

---

## When NOT to use

- **Tiny components** — splitting a 20-line widget wastes time.
- **RSC-first pages** — server component can be the “container.”

---

## Related

[[React code smells]] [[react-query]] [[React Pattern/Provider pattern]]
