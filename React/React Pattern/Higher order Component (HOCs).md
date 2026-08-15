[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# Higher-order Component (HOCs)

> Function that takes a component and returns an enhanced component — classic reuse before hooks.

## Interview Relevance

Interviewers ask which composition pattern fits the API you want — and what breaks when you force the wrong one.

## Sources

- [Higher-order Component (HOCs) docs](https://legacy.reactjs.org/docs/higher-order-components.html) — deep-dive
- [React Learn](https://react.dev/learn) — overview

## Key Concepts

- **Modern default:** custom hooks for logic reuse.
- **Keep for APIs:** compound components / providers when the JSX API matters.

## Technical Details

See also sibling notes under `React Pattern/` and [[React design patterns]].

## Real-World Applications

Reach for Higher-order Component (HOCs) when the component API needs that composition style; otherwise prefer hooks.

## Pros/Cons or Trade-offs

- **Pro:** Shared vocabulary in code reviews.
- **Con:** Forcing a pattern where a simple hook suffices.

## Comparison

- vs [[react hooks]]: hooks share logic; these patterns shape component APIs.

## Mistakes to Avoid

- Introducing HOCs in greenfield 2026 code without a library constraint.
- Provider for high-frequency changing values.
