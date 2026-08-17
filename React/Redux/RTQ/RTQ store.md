[[react hooks]] [[React State management]] [[React Architecture]] [[RTQ Toolkit]] [[RTQ tags]] [[redux store architecture]]

# RTK Query store wiring

> Add RTK Query reducer and middleware to configureStore so generated hooks work.

```txt
        RTK Query store wi ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want action → reducer → store → subscribe data flow, immutabilit…

## Sources
- [RTK Query store wiring](https://redux-toolkit.js.org/rtk-query/overview) — deep-dive
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
- Use RTK Query store wiring when your app’s Redux layer needs that capability
