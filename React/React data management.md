[[react hooks]] [[React State management]] [[Data Fetching HOC component]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]]

# React data management

> Decide where data lives — server cache, URL, local UI state, or a global client store — and keep those roles separate.

## Interview Relevance

Interviewers draw the line between server state and client state; mixing them is a common senior-filter fail.

## Sources

- [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) — deep-dive
- [Managing State](https://react.dev/learn/managing-state) — overview

## Core Definition

Data management assigns each piece of state an owner: remote cache, router, component, or global store — not one bucket for everything.

## Key Concepts

- **Server state:** [[react-query]] / RTK Query.
- **URL state:** filters, page, selected id.
- **Client UI state:** modals, drafts — `useState` / [[zustand]].
- **Cross-feature client:** [[Redux]] when justified.

## Technical Details

Decision cheat sheet:

| Data | Home |
|------|------|
| `/api/users` list | Query library |
| `?tab=billing` | Router search params |
| Modal open | Local state |
| Multi-step wizard draft shared across routes | Store |

## Real-World Applications

Admin table: filters in the URL, rows in TanStack Query, row-selection in component state.

## Pros/Cons or Trade-offs

- **Pro:** Clear ownership reduces sync bugs.
- **Con:** Too many tools without conventions confuse newcomers.

## Comparison

- vs [[React State management]]: state management is the client mechanisms; data management includes server/URL.

## Mistakes to Avoid

- Mirroring every query result into Redux.
- Storing auth tokens in a persistence middleware without XSS threat modeling.
