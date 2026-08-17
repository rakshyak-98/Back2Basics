[[react hooks]] [[React Architecture]] [[RSC (React Server Component boundaries)]] [[React State management]] [[React build]] [[React code smells]]

# React Application Architecture for Production

> Production React needs error boundaries, env config, observability, auth session handling, and deployable build artifacts — not just components.

```txt
        React Application  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers move past todo apps into failure handling, config, and how you k…

## Sources
- [Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) — deep-dive
- [Start a React project](https://react.dev/learn/start-a-new-react-project) — overview

## Key Concepts
- **Error boundaries:** isolate feature crashes.
- **Config:** public env vs server secrets.
- **Observability:** client error reporting + web vitals.
- **Auth session:** refresh/expiry without full page death.


- **Core:** Production architecture adds operational seams: errors, feature flags, secret…

## Technical Details
- Checklist: error boundary per route → query cache defaults → CSP/headers with…

## Mistakes to Avoid
- **Mistake:** No error boundary anywhere
- **Mistake:** Baking prod API keys into the client bundle

## Pros/Cons or Trade-offs
- **Pro:** Failures degrade gracefully.
- **Con:** Too many boundaries hide bugs if you never alert.

## Comparison
- vs [[React Architecture]]: production adds ops; architecture is module/state shape.


### Use cases
- Checkout route wraps payment widget in an error boundary so a third-party scr…
