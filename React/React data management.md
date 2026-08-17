[[react hooks]] [[React State management]] [[data fetching component]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]]

# React data management

> Decide where data lives — server cache, URL, local UI state, or a global client store — and keep those roles separate.

```txt
        React data managem ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers draw the line between server state and client state

## Sources
- [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) — deep-dive
- [Managing State](https://react.dev/learn/managing-state) — overview

## Key Concepts
- **Server state:** [[react-query]] / RTK Query.
- **URL state:** filters, page, selected id.
- **Client UI state:** modals, drafts — `useState` / [[zustand]].
- **Cross-feature client:** [[Redux]] when justified.


- **Core:** Data management assigns each piece of state an owner: remote cache, router, c…

## Technical Details
- Decision cheat sheet:

| Data | Home |
|------|------|
| `/api/users` list | Query library |
| `?tab=billing` | Router search params |
| Modal open | Local state |
| Multi-step wizard draft shared across routes | Store |

## Mistakes to Avoid
- **Mistake:** Mirroring every query result into Redux
- **Mistake:** Storing auth tokens in a persistence middleware without XSS thre…

## Pros/Cons or Trade-offs
- **Pro:** Clear ownership reduces sync bugs.
- **Con:** Too many tools without conventions confuse newcomers.

## Comparison
- vs [[React State management]]: state management is the client mechanisms


### Use cases
- Admin table: filters in the URL, rows in TanStack Query, row-selection in com…
