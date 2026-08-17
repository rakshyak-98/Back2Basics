[[react hooks]] [[React State management]] [[React Architecture]] [[Compound Components 1]] [[React pattern categorisation]] [[Separate functional logic from persentation components]]

# Compound Components

> Parent and children components share implicit state (often Context) for a flexible API.





## Interview Relevance
Interviewers ask which composition pattern fits the API you want — and what breaks when you force the wrong one.

## Sources
- [Compound Components docs](https://react.dev/learn/passing-data-deeply-with-context) — deep-dive
- [React Learn](https://react.dev/learn) — overview

## Key Concepts
- **Modern default:** custom hooks for logic reuse.
- **Keep for APIs:** compound components / providers when the JSX API matters.

## Technical Details
See also sibling notes under `React Pattern/` and [[React design patterns]].

## Real-World Applications
Reach for Compound Components when the component API needs that composition style; otherwise prefer hooks.

## Pros/Cons or Trade-offs
- **Pro:** Shared vocabulary in code reviews.
- **Con:** Forcing a pattern where a simple hook suffices.

## Comparison
- vs [[react hooks]]: hooks share logic; these patterns shape component APIs.

## Mistakes to Avoid
- Introducing HOCs in greenfield 2026 code without a library constraint.
- Provider for high-frequency changing values.
