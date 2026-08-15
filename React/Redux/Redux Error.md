[[react hooks]] [[React State management]] [[React Architecture]] [[Immutability in Redux]] [[Redux]] [[Redux State sync with localstorage]]

# Redux Error

> How errors surface in Redux apps — rejected thunks, error slices, and middleware crash reporters.

## Interview Relevance

Interviewers want action → reducer → store → subscribe data flow, immutability, and why Redux Toolkit is the default path.

## Sources

- [Redux Error](https://redux-toolkit.js.org/api/createAsyncThunk) — deep-dive
- [Redux getting started](https://redux.js.org/introduction/getting-started) — overview

## Key Concepts

- **Data flow:** dispatch → middleware → reducer → subscribers.
- **Modern path:** Redux Toolkit; avoid hand-written switch statements for new code.

## Technical Details

Prefer official RTK APIs documented at the Sources link. Cross-link [[Redux/Redux concept and data flow]] and [[Redux toolkit]].

## Real-World Applications

Use Redux Error when your app’s Redux layer needs that capability; keep server lists in RTK Query or TanStack Query.

## Pros/Cons or Trade-offs

- **Pro:** Centralized, debuggable updates with DevTools.
- **Con:** Ceremony — skip Redux for local UI-only state.

## Comparison

- vs [[zustand]]: Redux for large shared client graphs + middleware; Zustand for minimal stores.

## Mistakes to Avoid

- Mutating state outside Immer drafts.
- Caching server entities only in slices without a query layer.
- Persisting secrets to localStorage.
