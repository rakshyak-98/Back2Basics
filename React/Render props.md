[[React]] [[React Pattern/Higher order Component (HOCs)]] [[React Pattern/Provider pattern]]

# Render props

> Pass a function as a child/prop that receives state — the parent owns logic; the caller owns the UI.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Interview map (words you can say)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Component runs reusable logic, then calls `children(state)` or `render(state)` so the consumer decides markup.

```txt
<Mouse>
  {({ x, y }) => <Cursor x={x} y={y} />}
</Mouse>
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Render prop** | Function prop that returns UI | “Logic in wrapper; UI inverted to caller.” |
| **children as function** | Same idea with `children` | “Common React idiom before hooks.” |
| **vs HOC** | Composition vs wrap | “Render props avoid name clashes on props.” |

## Standard config / commands

```tsx
function CartProvider({ children }: { children: (api: CartApi) => React.ReactNode }) {
  const [cart, setCart] = useState<Item[]>([])
  const addItem = (item: Item) => setCart((c) => [...c, item])
  return <>{children({ cart, addItem })}</>
}

// Today: prefer a hook + optional context
function useCart() { /* … */ }
```

| Knob | Why it matters |
|------|----------------|
| Function identity | Inline `children={() => …}` re-creates each render |
| Context alternative | Avoid nesting hell for app-wide state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Nested pyramid | Many render-prop providers | Switch to hooks/context |
| Extra re-renders | New function child each time | Stabilize or use context |
| Prop name clash | `render` vs `children` | Pick one convention |
| Hard to type | Generics on render fn | Type the API object explicitly |

---

## Gotchas

> [!WARNING]
> **Hooks largely replaced this** — custom hooks are clearer for most logic reuse.

> [!WARNING]
> **Don’t mix with HOCs casually** — wrapping order and prop collisions get messy.

---

## When NOT to use

- **New code with hooks** — `useX()` is the default.
- **Simple prop passing** — no need for a render function.

---

## Related

[[React Pattern/Higher order Component (HOCs)]] [[React Pattern/Provider pattern]] [[react hooks]]
