[[react hooks]] [[React Architecture]] [[RSC (React Server Component boundaries)]] [[React State management]] [[React build]] [[React code smells]]

# React Application Architecture for Production

> Production React needs error boundaries, env config, observability, auth session handling, and deployable build artifacts — not just components.





## Interview Relevance
Interviewers move past todo apps into failure handling, config, and how you keep SSR/CSR deploys safe.

## Sources
- [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) — deep-dive
- [Start a React project](https://react.dev/learn/start-a-new-react-project) — overview

## Core Definition
Production architecture adds operational seams: errors, feature flags, secrets, monitoring, and release strategy around the UI tree.

## Key Concepts
- **Error boundaries:** isolate feature crashes.
- **Config:** public env vs server secrets.
- **Observability:** client error reporting + web vitals.
- **Auth session:** refresh/expiry without full page death.

## Technical Details
Checklist: error boundary per route → query cache defaults → CSP/headers with host → sourcemaps in error tool → health of API base URL per environment.

## Real-World Applications
Checkout route wraps payment widget in an error boundary so a third-party script failure does not blank the whole SPA.

## Pros/Cons or Trade-offs
- **Pro:** Failures degrade gracefully.
- **Con:** Too many boundaries hide bugs if you never alert.

## Comparison
- vs [[React Architecture]]: production adds ops; architecture is module/state shape.

## Mistakes to Avoid
- No error boundary anywhere.
- Baking prod API keys into the client bundle.
