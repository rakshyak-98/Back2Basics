[[React State management]] [[React pattern categorisation]] [[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]]

# React design patterns

> Reusable composition strategies — compound components, providers, hooks, controlled inputs — chosen for the API you want.





## Interview Relevance
Interviewers ask which pattern fits a use case and what you’d avoid in modern React.

## Sources
- [Context](https://react.dev/learn/passing-data-deeply-with-context) — overview
- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive

## Core Definition
Design patterns in React are composition recipes for sharing behavior and structuring component APIs.

## Key Concepts
- **Hooks:** default for shared logic.
- **Compound components:** flexible parent/child APIs ([[React Pattern/Compound Components]]).
- **Provider:** dependency injection via Context ([[React Pattern/Provider pattern]]).
- **Controlled/uncontrolled:** form input ownership.

## Technical Details
See leaf notes under `React Pattern/` for worked examples; prefer hooks over new HOCs/render props.

## Real-World Applications
Design-system Tabs implemented as compound components with shared context for active index.

## Pros/Cons or Trade-offs
- **Pro:** Predictable APIs across the codebase.
- **Con:** Pattern zoo without guidance wastes time.

## Comparison
- vs [[React Pattern/React pattern categorisation]]: categorisation is the map; this is the rationale.

## Mistakes to Avoid
- Using HOCs for new code when a hook suffices.
- Context for high-frequency values without splitting.
