[[react hooks]] [[React State management]] [[React Architecture]] [[Data Fetching HOC component]] [[React pattern categorisation]] [[Component Presentational Pattern]]

# data fetching component

> Component whose job is to load remote data and pass it to a view — prefer hooks/query libraries today.

## Interview Relevance

Interviewers ask which composition pattern fits the API you want — and what breaks when you force the wrong one.

## Sources

- [data fetching component docs](https://tanstack.com/query/latest/docs/framework/react/overview) — deep-dive
- [React Learn](https://react.dev/learn) — overview

## Key Concepts

- **Modern default:** custom hooks for logic reuse.
- **Keep for APIs:** compound components / providers when the JSX API matters.

## Technical Details

See also sibling notes under `React Pattern/` and [[React design patterns]].

## Real-World Applications

Reach for data fetching component when the component API needs that composition style; otherwise prefer hooks.

## Pros/Cons or Trade-offs

- **Pro:** Shared vocabulary in code reviews.
- **Con:** Forcing a pattern where a simple hook suffices.

## Comparison

- vs [[react hooks]]: hooks share logic; these patterns shape component APIs.

## Mistakes to Avoid

- Introducing HOCs in greenfield 2026 code without a library constraint.
- Provider for high-frequency changing values.
