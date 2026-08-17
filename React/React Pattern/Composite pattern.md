[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# Composite pattern

> Treat individual components and groups uniformly — trees of UI nodes composed recursively.

```txt
        Composite pattern ──┬── Why it matters
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
- [Composite pattern docs](https://react.dev/learn/thinking-in-react) — deep-dive
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
- Reach for Composite pattern when the component API needs that composition sty…
