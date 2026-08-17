[[react hooks]] [[React State management]] [[React Architecture]]

# Optimizing performance

> Cut wasted React work — fewer re-renders, smaller bundles, lighter lists — measure before memoizing everything.

```txt
        Optimizing perform ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want profiling evidence, then targeted fixes (`React.memo`, virt…

## Sources
- [Render and Commit](https://react.dev/learn/render-and-commit) — overview
- [React.memo](https://react.dev/reference/react/memo) — deep-dive

## Key Concepts
- **Render cost:** parent state updates re-render children unless memoized/isolated.
- **Lists:** virtualize long lists; stable keys.
- **Code split:** `lazy` + Suspense for rare routes.


- **Core:** Performance work targets unnecessary renders, expensive calculations, and ove…

## Technical Details
| Tool | Use |
|------|-----|
| React Profiler | Find expensive commits |
| `memo` / `useMemo` | After proving re-render cost |
| Windowing (e.g. react-window) | Thousands of rows |

## Mistakes to Avoid
- **Mistake:** Wrapping every component in `memo`
- **Mistake:** Unstable inline objects as props defeating memo

## Pros/Cons or Trade-offs
- **Pro:** Measured fixes improve INP/TBT.
- **Con:** Premature memo adds complexity and stale-deps bugs.

## Comparison
- vs [[react cache]]: cache is server/dedupe; this note is client render cost.


### Use cases
- Settings page re-rendered a 5k-row table on every keystroke
