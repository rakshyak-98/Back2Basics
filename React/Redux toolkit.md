[[Redux]] [[Redux/Redux createSlice]] [[Redux/Redux createAsyncThunk]] [[Redux/Redux createApi]] [[React State management]]

# Redux Toolkit

> Official Redux batteries — `configureStore`, `createSlice`, Immer, and thunks without hand-written boilerplate.

## Interview Relevance

Interviewers treat RTK as the default Redux answer — expect `createSlice`, Immer drafts, and when to add RTK Query.

## Sources

- [Redux Toolkit — Getting started](https://redux-toolkit.js.org/introduction/getting-started) — deep-dive
- [Redux — RTK overview](https://redux.js.org/redux-toolkit/overview) — overview

## Key Concepts

- **configureStore:** store + DevTools + thunk middleware wired by default.
- **createSlice:** name + initial state + reducers → action creators generated.
- **Immer:** “mutate” drafts safely inside slice reducers.
- **createAsyncThunk / RTK Query:** async without hand-rolled action type strings.

## Technical Details

```ts
const store = configureStore({
  reducer: { todos: todosSlice.reducer, [api.reducerPath]: api.reducer },
  middleware: (gDM) => gDM().concat(api.middleware),
});
```

Prefer selectors (`createSelector`) for derived data instead of storing duplicate projections in the slice.

## Real-World Applications

Greenfield React app adopting Redux: start with RTK slices for client intent and RTK Query endpoints for server lists.

## Pros/Cons or Trade-offs

- **Pro:** Deletes classic boilerplate and footguns.
- **Con:** Still more moving parts than [[zustand]] for a single small store.

## Comparison

- vs hand-written Redux: RTK is the supported path; avoid new switch-based reducers.
- vs [[Redux/Redux createApi]]: RTK Query is the server-cache half of Toolkit.

## Mistakes to Avoid

- Disabling serializable checks to hide non-serializable secrets in state.
- Mixing raw `createStore` patterns with RTK without reason.
- Putting form keystroke state into the global store.
