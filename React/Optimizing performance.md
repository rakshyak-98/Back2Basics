[[react hooks]] [[React State management]] [[React Architecture]]

# Optimizing performance

> Cut wasted React work — fewer re-renders, smaller bundles, lighter lists — measure before memoizing everything.

## Interview Relevance

Interviewers want profiling evidence, then targeted fixes (`React.memo`, virtualization, code split) — not blanket memo.

## Sources

- [Render and Commit](https://react.dev/learn/render-and-commit) — overview
- [React.memo](https://react.dev/reference/react/memo) — deep-dive

## Core Definition

Performance work targets unnecessary renders, expensive calculations, and oversized JS payloads — guided by the Profiler.

## Key Concepts

- **Render cost:** parent state updates re-render children unless memoized/isolated.
- **Lists:** virtualize long lists; stable keys.
- **Code split:** `lazy` + Suspense for rare routes.

## Technical Details

| Tool | Use |
|------|-----|
| React Profiler | Find expensive commits |
| `memo` / `useMemo` | After proving re-render cost |
| Windowing (e.g. react-window) | Thousands of rows |

## Real-World Applications

Settings page re-rendered a 5k-row table on every keystroke — isolate input state and virtualize the table.

## Pros/Cons or Trade-offs

- **Pro:** Measured fixes improve INP/TBT.
- **Con:** Premature memo adds complexity and stale-deps bugs.

## Comparison

- vs [[react cache]]: cache is server/dedupe; this note is client render cost.

## Mistakes to Avoid

- Wrapping every component in `memo`.
- Unstable inline objects as props defeating memo.
