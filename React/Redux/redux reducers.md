[[react hooks]] [[React State management]] [[React Architecture]] [[Immutability in Redux]] [[Redux]] [[Redux Error]]

# redux reducers

> redux reducers shapes how React applications compose UI, state, and side effects in production.

## What this is

Redux centralizes application state in a single store updated through dispatched actions and pure reducers. Redux Toolkit is the recommended integration path: `configureStore`, `createSlice`, and `createAsyncThunk` replace hand-written action types and boilerplate ([Redux Toolkit overview](https://redux.js.org/redux-toolkit/overview)).

## When to choose it

**Server state** (API payloads, pagination, cache) → TanStack Query or RTK Query.
**Client UI state** (modal open, form drafts) → `useState` or [[zustand]].
**Cross-feature client state** → Redux only when many views need the same synchronous snapshot.

## Operating it

```ts
const slice = createSlice({
  name: 'todos',
  initialState: { items: [], status: 'idle' },
  reducers: {
    added(state, action) { state.items.push(action.payload); },
  },
});
```

Prefer selectors (`createSelector`) for derived data instead of storing duplicate projections in the slice.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `redux reducers` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[Immutability in Redux]] [[Redux]] [[Redux Error]]

## Sources

- [Redux — Redux Toolkit overview](https://redux.js.org/redux-toolkit/overview)
