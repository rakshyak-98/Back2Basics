[[Redux]] [[Redux toolkit]] [[Redux/Redux createSlice]]

# redux toolkit features

> RTK’s toolkit map — store, slices, thunks, Query, entities, selectors — what each is for.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** RTK is Redux with batteries — `configureStore` defaults, `createSlice` + Immer, async via `createAsyncThunk` or RTK Query, lists via entity adapters.

```txt
configureStore
  ├─ createSlice (+ Immer)
  ├─ createAsyncThunk / createApi
  ├─ createEntityAdapter
  └─ createSelector
```

### Interview map (words you can say)

| Feature | Job in one line |
|---------|-----------------|
| **configureStore** | Store + thunk + DevTools + checks |
| **createSlice** | Reducer + actions in one object |
| **Immer** | “Mutate” drafts safely |
| **extraReducers** | React to thunks / other slices |
| **createAsyncThunk** | pending/fulfilled/rejected trio |
| **createApi** | Cache HTTP; generate hooks |
| **createEntityAdapter** | Normalized id→entity maps |
| **createSelector** | Memoized derived state |

## Standard config / commands

```ts
const store = configureStore({ reducer: { todos: todosReducer, [api.reducerPath]: api.reducer },
  middleware: (gDM) => gDM().concat(api.middleware) })

const todosSlice = createSlice({
  name: 'todos',
  initialState: adapter.getInitialState(),
  reducers: { /* Immer drafts */ },
  extraReducers: (b) => { b.addCase(load.fulfilled, (s, a) => adapter.setAll(s, a.payload)) },
})
```

| Use when | Reach for |
|----------|-----------|
| Feature local state | `createSlice` |
| One-off async | `createAsyncThunk` |
| REST/GraphQL cache | `createApi` |
| Large collections | `createEntityAdapter` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Boilerplate explosion | Hand-written actions | `createSlice` |
| Non-serializable warning | Date/class in state | Store ISO strings / ids |
| Duplicate fetches | Hand thunks everywhere | RTK Query |
| List perf / messy CRUD | Array scans | Entity adapter |

---

## Gotchas

> [!WARNING]
> **RTK Query cache ≠ createSlice** — don’t mirror server lists in both without a sync plan.

> [!WARNING]
> **Entity adapters need stable ids** — missing `id` breaks upserts.

---

## When NOT to use

- **Local ephemeral UI** — `useState`.
- **No shared client cache need** — server components / simple fetch may suffice.

---

## Related

[[Redux toolkit]] [[Redux/Redux createSlice]] [[Redux/Redux createAsyncThunk]] [[Redux/Redux createApi]] [[Redux/Immutability in Redux]]
