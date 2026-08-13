<!-- note-strategy: operational -->
[[React]] [[React code smells]] [[react hooks]] [[useRef]]

# Optimizing performance

> Cut wasted re-renders and expensive work — measure first, then memoize or split.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A function component re-renders when it mounts, when its parent re-renders, or when a hook says state/context changed. Memoization keeps referential equality so children can skip work.

```txt
parent render → child render (default)
memo(child) + stable props → skip child
useMemo/useCallback → stable references for deps
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Re-render** | Function runs again | “Not always bad — cheap renders are fine.” |
| **`React.memo`** | Skip if props shallow-equal | “Helps pure leaves under hot parents.” |
| **`useMemo`** | Cache computed value | “For expensive derive, not every object.” |
| **`useCallback`** | Memoize function identity | “Same as `useMemo(() => fn, deps)`.” |

## Standard config / commands

```tsx
const value = useMemo(() => heavy(list), [list])
const onSelect = useCallback((id: string) => setId(id), [])

const Row = React.memo(function Row({ item, onSelect }: Props) {
  return <li onClick={() => onSelect(item.id)}>{item.name}</li>
})
```

| Knob | Why it matters |
|------|----------------|
| Profiler / why-did-you-render | Prove waste before memo |
| Stable deps | Empty deps = mount-only identity |
| Split context | Huge provider values bust memo |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Typing lag in list | Profiler: which component | Virtualize; memo rows; stable callbacks |
| memo child still renders | New object/array/fn props | `useCallback` / hoist constants |
| `useMemo` “not working” | Dep is new reference each time | Fix upstream identity, not more memo |
| Effect thrash | Unstable deps | Memoize or move deps |

---

## Gotchas

> [!WARNING]
> **`useMemo` compares references, not deep content** — new `{}` every render defeats it.

> [!WARNING]
> **Memo tax** — comparing props costs CPU; don’t wrap everything.

---

## When NOT to use

- **Fast leaves** — optimize after measuring.
- **Premature `useCallback` everywhere** — adds noise without a memoized child/effect dep need.

---

## Related

[[React code smells]] [[useRef]] [[Hooks/react useEffect]] [[react hooks]]
