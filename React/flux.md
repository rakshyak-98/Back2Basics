<!-- note-strategy: operational -->
[[React]] [[Redux]]

# flux

> Unidirectional data flow for UI apps — action in, store updates, view re-renders (no two-way binding loops).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** View dispatches an action → dispatcher fans out → stores update → views subscribe and re-render. Data moves one way.

```txt
View → Action → Dispatcher → Store(s) → View
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Action** | “Something happened” payload | “Intent, not a DOM event.” |
| **Dispatcher** | Single hub for actions | “Stores register; hub broadcasts.” |
| **Store** | State + domain logic | “Only stores mutate app state.” |
| **Unidirectional** | No child→parent magic writes | “Easier to replay and debug.” |

## Standard config / commands

Today you rarely install classic Flux — [[Redux]] / RTK is the common Flux descendant:

```ts
dispatch({ type: 'todos/add', payload: text })
// reducer → new state → connected view
```

| Piece | Job |
|-------|-----|
| Actions | Describe intent |
| Stores / reducers | Own state transitions |
| Views | Read state, dispatch only |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| View doesn’t update | Store emit / subscription | Ensure store notifies; React binds correctly |
| State changes mysteriously | Side writes outside actions | Route all mutations through actions |
| Circular updates | Store A triggers B triggers A | Break cycle; one owner per fact |
| Hard to test | Logic in views | Move rules into stores/reducers |

---

## Gotchas

> [!WARNING]
> **Flux ≠ Redux** — Redux = single store + pure reducers; classic Flux allows multiple stores + dispatcher.

> [!WARNING]
> **Two-way binding habits** — mutating state from deep children without actions recreates the spaghetti Flux fixed.

---

## When NOT to use

- **Local ephemeral UI** (open/closed tooltip) — component state is enough.
- **Server cache** — prefer [[react-query]] / RTK Query over inventing Flux stores for HTTP.

---

## Related

[[Redux]] [[Redux toolkit]] [[Redux/Redux concept and data flow]]
