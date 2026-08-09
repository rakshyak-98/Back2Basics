[[Redux]] [[Redux toolkit]] [[Redux/Redux createAsyncThunk]]

# Redux Thunk

> Middleware that lets action creators return functions — put async work (fetch, delay) next to dispatch.

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

**Say it in one breath:** Plain Redux actions are sync objects. A thunk is a function `(dispatch, getState) => …` that can await APIs then dispatch real actions. RTK’s `configureStore` includes thunk by default.

```txt
UI → dispatch(thunkFn) → thunk middleware runs fn
                              ├─ await api
                              └─ dispatch({ type, payload })
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Thunk** | Function-as-action | “I return a function that later dispatches.” |
| **Side effect** | I/O outside reducers | “Reducers stay pure; thunks own fetch.” |
| **RTK default** | Thunk already installed | “No need to `applyMiddleware(thunk)` with RTK.” |

## Standard config / commands

```ts
// Hand-written thunk
const loadUser = (id) => async (dispatch, getState) => {
  dispatch({ type: 'user/pending' })
  const data = await api.getUser(id)
  dispatch({ type: 'user/fulfilled', payload: data })
}

// Prefer RTK helper
export const loadUser = createAsyncThunk('user/load', async (id) => api.getUser(id))
```

| Knob | Why it matters |
|------|----------------|
| `getDefaultMiddleware()` | Already has thunk + immutability checks |
| Custom middleware | Spread defaults then `.concat(logger)` — don’t drop thunk |
| `createAsyncThunk` | Pending/fulfilled/rejected for free |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Actions must be plain objects” | Thunk middleware missing | Use RTK store or add `redux-thunk` |
| Race: old response wins | No abort / ignore | AbortController or requestId check |
| Double fetch | Multiple mounts dispatch | Dedup in thunk or use RTK Query |
| Non-serializable in state | Put Promise/Map in reducer | Keep async results as plain data |

---

## Gotchas

> [!WARNING]
> **Overriding middleware without defaults** — `middleware: [logger]` drops thunk. Use `getDefaultMiddleware().concat(logger)`.

> [!WARNING]
> **Thunk ≠ saga** — complex cancel/retry flows may want RTK Query or a dedicated async layer.

---

## When NOT to use

- **Server/cache state** — [[react-query]] / [[Redux/Redux createApi]] fit better than hand thunks.
- **Sync UI toggles** — plain actions / `createSlice` reducers.

---

## Related

[[Redux/Redux createAsyncThunk]] [[Redux toolkit]] [[Redux/Redux concept and data flow]]
