[[react hooks]] [[React Application Architecture for Production]] [[RSC (React Server Component boundaries)]] [[React State management]] [[React build]] [[React code smells]]

# React Architecture

> How a React app is sliced — routes, features, shared UI, server vs client state, and infrastructure boundaries.





## Interview Relevance
Interviewers sketch boxes: routing, features, API client, auth — and ask where state lives and what must not cross the RSC boundary.

## Sources
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [Server Components](https://react.dev/reference/rsc/server-components) — deep-dive

## Core Definition
React architecture is the map of modules and runtime boundaries so features can ship without tangling data fetching and UI.

## Key Concepts
- **Layers:** routes → features → shared UI → infra (API, auth).
- **State split:** server cache vs client UI state ([[React data management]]).
- **Boundaries:** mark client files with use client only where interactivity needs it.

## Technical Details
```txt
app/          # routes
features/     # product domains
shared/ui/    # design system
infra/api/    # HTTP client
```

## Real-World Applications
B2B dashboard: each product area is a feature module; auth session in a thin provider; lists via TanStack Query.

## Pros/Cons or Trade-offs
- **Pro:** Clear ownership and code-split points.
- **Con:** Premature micro-folder structures slow small apps.

## Comparison
- vs [[React Application Architecture for Production]]: production adds observability, error boundaries, env, CI.

## Mistakes to Avoid
- Global Redux for all server data.
- Importing server-only secrets into client components.
