[[react hooks]] [[React Application Architecture for Production]] [[RSC (React Server Component boundaries)]] [[React State management]] [[React build]] [[React code smells]]

# React Architecture

> How a React app is sliced — routes, features, shared UI, server vs client state, and infrastructure boundaries.

```txt
        React Architecture ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers sketch boxes: routing, features, API client, auth

## Sources
- [Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [Server Components](https://react.dev/reference/rsc/server-components) — deep-dive

## Key Concepts
- **Layers:** routes → features → shared UI → infra (API, auth).
- **State split:** server cache vs client UI state ([[React data management]]).
- **Boundaries:** mark client files with use client only where interactivity needs it.


- **Core:** React architecture is the map of modules and runtime boundaries so features c…

## Technical Details
```txt
app/          # routes
features/     # product domains
shared/ui/    # design system
infra/api/    # HTTP client
```

## Mistakes to Avoid
- **Mistake:** Global Redux for all server data
- **Mistake:** Importing server-only secrets into client components

## Pros/Cons or Trade-offs
- **Pro:** Clear ownership and code-split points.
- **Con:** Premature micro-folder structures slow small apps.

## Comparison
- vs [[React Application Architecture for Production]]: production adds observability, error bounda…


### Use cases
- B2B dashboard: each product area is a feature module
