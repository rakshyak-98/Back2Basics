<!-- note-strategy: operational -->
[[React]] [[Redux]] [[Redux/Redux createSlice]] [[Redux/Redux createApi]]

# Redux toolkit

> Official Redux batteries — `configureStore`, `createSlice`, Immer, thunks, and optional RTK Query with less boilerplate.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** RTK is how you write Redux in 2024+ — slices generate actions, Immer lets “mutating” reducers, store comes with sane middleware.

```txt
createSlice → reducer + actions
configureStore → store (+ thunk, checks)
createApi → optional server cache
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **createSlice** | Reducer + action creators | “One file owns the feature state.” |
| **configureStore** | Store factory | “Defaults beat hand `createStore`.” |
| **Immer** | Draft mutations | “Writable syntax, immutable result.” |
| **RTK Query** | Data fetching layer | “Caching/deduping like React Query.” |

## Standard config / commands

```ts
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    incremented(state) { state.value += 1 },
  },
})

export const store = configureStore({
  reducer: { counter: counterSlice.reducer },
})
export const { incremented } = counterSlice.actions
export type RootState = ReturnType<typeof store.getState>
```

| Knob | Why it matters |
|------|----------------|
| `getDefaultMiddleware()` | Keep thunk when customizing |
| `serializableCheck` | Catch bad state shapes in dev |
| Slice `name` | Prefixes action types |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Thunks rejected as non-plain | Middleware overridden | `.concat` onto defaults |
| Unexpected mutation errors | Wrote outside slice / non-draft | Only mutate drafts in reducers |
| Action type typos | Hand-written strings | Use slice action creators |
| Boilerplate returning | Not using slices/Query | Adopt RTK patterns |

---

## Gotchas

> [!WARNING]
> **Replacing middleware array** drops thunk and checks — always extend defaults.

> [!WARNING]
> **Don’t fight Immer** — returning a new object *and* mutating the draft incorrectly yields odd state.

---

## When NOT to use

- **No shared client state** — skip Redux entirely.
- **Only remote cache** — TanStack Query alone may be enough.

---

## Related

[[Redux]] [[Redux/Redux createSlice]] [[Redux/Redux createAsyncThunk]] [[Redux/Redux createApi]] [[Redux/Redux Thunk]]
