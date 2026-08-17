[[react hooks]] [[React State management]] [[React Architecture]] [[Immutability in Redux]] [[Redux Error]] [[Redux State sync with localstorage]] [[Redux toolkit]] [[flux]] [[zustand]]

# Redux

> Predictable client state container — actions dispatch to pure reducers that produce the next store snapshot.





## Interview Relevance
Interviewers want action → reducer → store → subscribe data flow, immutability, and why Redux Toolkit is the default path today.

## Sources
- [Redux Essentials](https://redux.js.org/tutorials/essentials/part-1-overview-concepts) — deep-dive
- [Redux Toolkit overview](https://redux.js.org/redux-toolkit/overview) — overview

## Key Concepts
- **Single store:** one state tree; slices combine via `configureStore`.
- **Actions:** plain objects describing intent; dispatch is the only write path.
- **Reducers:** pure `(state, action) => nextState` — RTK uses Immer drafts.
- **Selectors:** read/derive; avoid storing duplicate projections.
- **Server vs client:** API lists belong in RTK Query / TanStack Query — not hand-copied into slices.

## Technical Details
```ts
const slice = createSlice({
  name: 'todos',
  initialState: { items: [], status: 'idle' },
  reducers: {
    added(state, action) { state.items.push(action.payload); },
  },
});
```

Data flow: `UI → dispatch(action) → middleware → reducer → store → useSelector → UI`.

## Real-World Applications
Cross-feature client state (cart, multi-step draft, entitlements flags) shared by many routes — with DevTools time-travel during debugging.

## Pros/Cons or Trade-offs
- **Pro:** Debuggable unidirectional updates; mature middleware ecosystem.
- **Con:** Ceremony for local UI; overkill vs [[zustand]] or `useState` for small apps.

## Comparison
- vs [[zustand]]: Redux when you need strict patterns, middleware, and large shared graphs; Zustand when the store is small.
- vs [[flux]]: Redux is Flux-inspired with a single store and a simpler API.

## Mistakes to Avoid
- Mutating state outside Immer drafts (silent subscribe bugs).
- Mirroring every API response into slices instead of a query cache.
- Persisting secrets into `localStorage` via persist middleware.
