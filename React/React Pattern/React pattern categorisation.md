[[react hooks]] [[React Architecture]] [[Component Presentational Pattern]] [[Composite pattern]] [[Controlled and Uncontrolled component Pattern]] [[Provider pattern]]

# React pattern categorisation

> Map of React composition patterns — when to reach for hooks, compound components, providers, or legacy HOCs.

```txt
        React pattern cate ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask which composition pattern fits the API you want

## Sources
- [React pattern categorisation docs](https://react.dev/learn) — deep-dive
- [React Learn](https://react.dev/learn) — overview

## Key Concepts
- **Modern default:** custom hooks for logic reuse.
- **Keep for APIs:** compound components / providers when the JSX API matters.

## Technical Details
- See also sibling notes under `React Pattern/` and [[React design patterns]].

## Mistakes to Avoid
- **Mistake:** Introducing HOCs in greenfield 2026 code without a library const…
- **Mistake:** Provider for high-frequency changing values

## Pros/Cons or Trade-offs
- **Pro:** Shared vocabulary in code reviews.
- **Con:** Forcing a pattern where a simple hook suffices.

## Comparison
- vs [[react hooks]]: hooks share logic; these patterns shape component APIs.


### Use cases
- Reach for React pattern categorisation when the component API needs that comp…
