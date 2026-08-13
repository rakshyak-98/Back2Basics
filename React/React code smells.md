[[React]] [[Optimizing performance]] [[React Pattern/Component Presentational Pattern]]

# React code smells

> Patterns that make React apps hard to change — god components, prop drilling, and mirrored state.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Smell = structure that fights change. Fix by extracting hooks, colocating state, and deriving values instead of syncing them.

### Interview map (words you can say)

| Smell | Plain meaning | Fix you say |
|-------|---------------|-------------|
| **God component** | Logic + UI + fetch in one file | Custom hooks + presentational split |
| **Prop drilling** | Props hop 4+ layers unused mid-tree | Context or lift composition |
| **Mirrored state** | `useState(props.x)` then sync | Derive during render; key remount |
| **Effect for transform** | `useEffect` copies A→B | Compute `B` from `A` inline/`useMemo` |

## Standard config / commands

```tsx
// ❌ mirror props
const [name, setName] = useState(props.name)
useEffect(() => setName(props.name), [props.name])

// ✅ derive or remount
const name = props.name
// or <Editor key={props.id} initial={props.name} />
```

| Check | Healthy signal |
|-------|----------------|
| Component > ~200 lines / many concerns | Extract hook or child |
| Prop only forwarded | Composition or context |
| State equals props always | Delete state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Can’t find where state lives | God component / deep drill | Extract hook; document owners |
| Stale UI after prop change | Mirrored state | Derive or `key={id}` remount |
| Re-renders cascade | Context value identity | Split context; memo value |
| Untestable UI | Fetch inside leaf | Container/hook owns IO |

---

## Gotchas

> [!WARNING]
> **Context is not a state library** — huge provider values re-render everyone; split or use a store.

> [!WARNING]
> **`useMemo` doesn’t fix architecture** — memo over a god component hides the smell.

---

## When NOT to use

- **Greenfield tiny widgets** — don’t over-split a 30-line component.
- **Pass-through of 1–2 props** — drilling two levels is fine.

---

## Related

[[Optimizing performance]] [[React Pattern/Component Presentational Pattern]] [[React Pattern/Provider pattern]] [[Hooks/react useEffect]]
