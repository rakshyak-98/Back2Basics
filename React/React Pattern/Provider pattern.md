[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Composite pattern]]

# Provider pattern

> Put a value in Context.Provider so deep children read it without prop drilling.

## Interview Relevance

Interviewers ask which composition pattern fits the API you want — and what breaks when you force the wrong one.

## Sources

- [Provider pattern docs](https://react.dev/learn/passing-data-deeply-with-context) — deep-dive
- [React Learn](https://react.dev/learn) — overview

## Key Concepts

- **Modern default:** custom hooks for logic reuse.
- **Keep for APIs:** compound components / providers when the JSX API matters.

## Technical Details

See also sibling notes under `React Pattern/` and [[React design patterns]].

## Real-World Applications

Reach for Provider pattern when the component API needs that composition style; otherwise prefer hooks.

## Pros/Cons or Trade-offs

- **Pro:** Shared vocabulary in code reviews.
- **Con:** Forcing a pattern where a simple hook suffices.

## Comparison

- vs [[react hooks]]: hooks share logic; these patterns shape component APIs.

## Mistakes to Avoid

- Introducing HOCs in greenfield 2026 code without a library constraint.
- Provider for high-frequency changing values.
