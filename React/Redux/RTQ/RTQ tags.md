[[react hooks]] [[React State management]] [[React Architecture]] [[RTQ Toolkit]] [[RTQ store]]

# RTK Query tags

> Cache tags for invalidation — mark entities provided/invalidated so lists refetch correctly.





## Interview Relevance
Interviewers want action → reducer → store → subscribe data flow, immutability, and why Redux Toolkit is the default path.

## Sources
- [RTK Query tags](https://redux-toolkit.js.org/rtk-query/usage/automated-refetching) — deep-dive
- [Redux getting started](https://redux.js.org/introduction/getting-started) — overview

## Key Concepts
- **Data flow:** dispatch → middleware → reducer → subscribers.
- **Modern path:** Redux Toolkit; avoid hand-written switch statements for new code.

## Technical Details
Prefer official RTK APIs documented at the Sources link. Cross-link [[Redux/Redux concept and data flow]] and [[Redux toolkit]].

## Real-World Applications
Use RTK Query tags when your app’s Redux layer needs that capability; keep server lists in RTK Query or TanStack Query.

## Pros/Cons or Trade-offs
- **Pro:** Centralized, debuggable updates with DevTools.
- **Con:** Ceremony — skip Redux for local UI-only state.

## Comparison
- vs [[zustand]]: Redux for large shared client graphs + middleware; Zustand for minimal stores.

## Mistakes to Avoid
- Mutating state outside Immer drafts.
- Caching server entities only in slices without a query layer.
- Persisting secrets to localStorage.
