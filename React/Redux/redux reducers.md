[[Redux]] [[Redux/Immutability in Redux]] [[Redux/Redux createSlice]] [[Redux concept and data flow]]

# redux reducers

> **Pure functions** `(state, action) => newState` — only place state shape changes — **Redux fundamentals**.

---

## Mental model

```txt
(prevState, action) → nextState
```

Rules:

1. **No side effects** — no API, `Date.now()`, random, DOM.
2. **No mutate arguments** — return new references for changed branches.
3. **Same action + state → same next state** — enables DevTools time travel.

```txt
Why pure?
  Same action dispatched twice → identical result
  Replay log in prod → reproduce bug
```

RTK **`createSlice`** uses Immer — you **mutate draft** inside reducer, Immer produces immutable next state ([[Redux/Redux createSlice]]).

---

## Standard config / commands

### Plain reducer (legacy)

```javascript
const initialState = { count: 0 };

function counter(state = initialState, action) {
  switch (action.type) {
    case "counter/incremented":
      return { ...state, count: state.count + 1 };
    default:
      return state;
  }
}
```

### createSlice (RTK — preferred)

```typescript
const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    incremented(state) {
      state.value += 1; // Immer draft — OK here only
    },
  },
});
```

### combineReducers

```typescript
const rootReducer = combineReducers({
  counter: counterReducer,
  auth: authReducer,
});
```

Each key manages its slice independently.

### Extra reducers for async thunk

```typescript
extraReducers: (builder) => {
  builder.addCase(fetchUser.fulfilled, (state, action) => {
    state.user = action.payload;
  });
},
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| State reference unchanged, UI stale | Mutated nested object in plain reducer | Spread clone or use createSlice |
| Undefined state after action | Missing default param / wrong key | `state = initialState`; match action type |
| Random test failures | Impure reducer (API inside) | Move async to [[Redux/redux middleware]] |
| Immer error in plain reducer | push on frozen state | Switch to createSlice or deep clone |
| Whole tree resets | Returned wrong shape | Return only slice shape in nested reducer |

---

## Gotchas

> [!WARNING]
> **API call inside reducer** — same action could yield different states → breaks replay and tests.

> [!WARNING]
> **Shallow copy trap** — `{ ...state, nested: state.nested }` shares nested reference; clone nested when changing it.

---

## When NOT to use

- **Server cache normalization** — RTK Query manages its own reducer slice.
- **Ephemeral UI** — modal open flag rarely belongs in Redux ([[React State management]]).
- **Derived data** — compute in selector (`createSelector`), don't store duplicate fields.

---

## Related

[[Redux]] · [[Redux/Immutability in Redux]] · [[Redux/Redux createSlice]] · [[Redux/redux middleware]] · [[Redux concept and data flow]]
