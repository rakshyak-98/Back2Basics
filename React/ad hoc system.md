[[react hooks]] [[React State management]] [[React Architecture]] [[Data Fetching HOC component]]

# ad hoc system

> One-off state and fetch wiring scattered across components — works in a spike, fights you in production.

## Interview Relevance

Interviewers contrast disciplined data/state boundaries with ad-hoc effects and prop drilling to see if you have tasted scale.

## Sources

- [React — Thinking in React](https://react.dev/learn/thinking-in-react) — overview
- [React — Managing State](https://react.dev/learn/managing-state) — deep-dive

## Core Definition

An ad hoc React system means each feature invents its own fetch, cache, and event wiring instead of shared patterns (hooks, query clients, stores).

## Key Concepts

- **Local invention:** Every screen has its own `useEffect` fetch + loading flag.
- **No shared client:** Headers, base URL, and error mapping copied per file.
- **Prop drilling / random Context:** Cross-cutting state appears without a clear owner.

## Technical Details

Smell checklist:

| Smell | Prefer instead |
|-------|----------------|
| `useEffect` + `fetch` in 10 screens | [[react-query]] |
| Modal + user + cart all in one Context | Split stores / [[zustand]] slices |
| Copy-pasted loading spinners | Shared Suspense / query status UI |

## Real-World Applications

MVP ships with fetch-in-effect everywhere; the first multi-page feature forces a migration to TanStack Query and a thin API module.

## Pros/Cons or Trade-offs

- **Pro:** Fast for prototypes and throwaway demos.
- **Con:** Race conditions, duplicate requests, and inconsistent error UX at team scale.

## Comparison

- vs [[React Architecture]]: architecture names owners and boundaries; ad hoc leaves each file to invent them.

## Mistakes to Avoid

- Calling a working spike “done” without extracting the API/query layer.
- Adding Redux “for structure” while still fetching ad hoc in components.
