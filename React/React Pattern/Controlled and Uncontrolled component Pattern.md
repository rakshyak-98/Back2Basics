[[react hooks]] [[React State management]] [[React Architecture]] [[React pattern categorisation]] [[Component Presentational Pattern]] [[Composite pattern]]

# Controlled and Uncontrolled component Pattern

> Controlled inputs take value+onChange from React state; uncontrolled inputs use DOM state via refs.

```txt
        Controlled and Unc ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask which composition pattern fits the API you want

## Sources
- [Controlled and Uncontrolled component Pattern docs](https://react.dev/reference/react-dom/components/input) — deep-dive
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
- Reach for Controlled and Uncontrolled component Pattern when the component AP…
