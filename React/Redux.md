<!-- note-strategy: operational -->
[[React]] [[flux]] [[Redux toolkit]] [[Redux/Redux Thunk]]

# Redux

> One predictable store for app state — dispatch actions, pure reducers return the next tree, views select slices.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** UI dispatches → reducers compute new state immutably → subscribers re-render. Prefer Redux Toolkit (`configureStore`, `createSlice`) over hand-rolled boilerplate.

```txt
Component → dispatch(action) → reducer → store → useSelector → Component
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Store** | Single state tree | “One source of truth for cross-cutting state.” |
| **Reducer** | `(state, action) => next` | “Pure — no fetch inside.” |
| **Dispatch** | Send an action | “The only way to request a change.” |
| **Selector** | Read a slice | “Keep components decoupled from shape.” |

## Standard config / commands

```bash
npm install @reduxjs/toolkit react-redux
```

```ts
const store = configureStore({ reducer: { user: userReducer } })
// App
<Provider store={store}><App /></Provider>
const user = useSelector((s: RootState) => s.user)
dispatch(userSlice.actions.logout())
```

| Knob | Why it matters |
|------|----------------|
| RTK defaults | Thunk + immutability/serializable checks |
| Slices | Colocate actions + reducer |
| RTK Query | Server cache without hand thunks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Component not updating | Selector identity / mutation | Return new refs; fix immutable updates |
| “Actions must be plain objects” | Missing thunk middleware | Use `configureStore` |
| Serializable warnings | Date/Map/class in state | Store plain data; ignore known actions |
| Too much re-rendering | Fat selectors / mapState | Narrow selectors; memoize |

---

## Gotchas

> [!WARNING]
> **Not everything belongs in Redux** — static config and local UI toggles often shouldn’t.

> [!WARNING]
> **Async stays out of reducers** — thunks/RTK Query/listeners own side effects.

---

## When NOT to use

- **Mostly server cache** — [[react-query]] may be enough.
- **Tiny apps** — `useState` / context until cross-route shared client state hurts.

---

## Related

[[Redux toolkit]] [[flux]] [[Redux/Redux createSlice]] [[Redux/Redux Thunk]] [[Redux/Redux createApi]]
