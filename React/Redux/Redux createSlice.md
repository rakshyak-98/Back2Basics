[[Redux]] [[Redux toolkit]] [[Redux/Immutability in Redux]]

# Redux createSlice

> One RTK call that builds a reducer, action creators, and action types for a feature slice — Immer drafts inside.

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

**Say it in one breath:** Name the slice, give `initialState` and `reducers`; RTK emits `actions` and a `reducer` you mount on the store.

```txt
createSlice({ name, initialState, reducers })
  → slice.actions.foo(payload)
  → slice.reducer
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Slice** | Feature state + reducers | “Colocated instead of giant switch.” |
| **PayloadAction** | Typed action payload | “`action.payload` is T.” |
| **extraReducers** | React to other actions/thunks | “Listen to async lifecycle.” |

## Standard config / commands

```ts
const todosSlice = createSlice({
  name: 'todos',
  initialState: { items: [] as { id: string; text: string; done: boolean }[] },
  reducers: {
    added(state, action: PayloadAction<string>) {
      state.items.push({ id: crypto.randomUUID(), text: action.payload, done: false })
    },
    toggled(state, action: PayloadAction<string>) {
      const t = state.items.find((i) => i.id === action.payload)
      if (t) t.done = !t.done
    },
  },
})
export const { added, toggled } = todosSlice.actions
export default todosSlice.reducer
```

| Knob | Why it matters |
|------|----------------|
| `name` | Prefixes `todos/added` |
| Draft mutation | Immer → immutable next state |
| `prepare` callback | Customize payload (ids, meta) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Action no-ops | Wrong reducer key on store | Mount `todos: todosReducer` |
| Type errors on payload | Missing `PayloadAction<T>` | Annotate reducer args |
| Async not handled | Only sync reducers | `extraReducers` + `createAsyncThunk` |
| Mutation outside slice | Changed state in component | Dispatch an action instead |

---

## Gotchas

> [!WARNING]
> **Don’t spread the whole action into state** — pick `payload` fields you need.

> [!WARNING]
> **`name` collisions** across slices make DevTools harder — keep names unique.

---

## When NOT to use

- **Remote-only CRUD** — consider [[Redux/Redux createApi]] instead of hand slices.
- **Ephemeral local UI** — `useState`, not a slice.

---

## Related

[[Redux toolkit]] [[Redux/Redux createAsyncThunk]] [[Redux/Immutability in Redux]]
