[[react hooks]] [[React State management]] [[React Architecture]] [[Immutability in Redux]] [[Redux]] [[Redux Error]]

# Redux createSlice

> Define name, initial state, reducers — RTK generates action creators and case reducers with Immer.

```txt
        Redux createSlice ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want action → reducer → store → subscribe data flow, immutabilit…

## Sources
- [Redux createSlice](https://redux-toolkit.js.org/api/createSlice) — deep-dive
- [Redux getting started](https://redux.js.org/introduction/getting-started) — overview

## Key Concepts
- **Data flow:** dispatch → middleware → reducer → subscribers.
- **Modern path:** Redux Toolkit; avoid hand-written switch statements for new code.

## Technical Details
- Prefer official RTK APIs documented at the Sources link.
- Cross-link [[Redux/Redux concept and data flow]] and [[Redux toolkit]].

## Mistakes to Avoid
- **Mistake:** Mutating state outside Immer drafts
- **Mistake:** Caching server entities only in slices without a query layer
- **Mistake:** Persisting secrets to localStorage

## Pros/Cons or Trade-offs
- **Pro:** Centralized, debuggable updates with DevTools.
- **Con:** Ceremony — skip Redux for local UI-only state.

## Comparison
- vs [[zustand]]: Redux for large shared client graphs + middleware; Zustand for minimal stores.


### Use cases
- Use Redux createSlice when your app’s Redux layer needs that capability
