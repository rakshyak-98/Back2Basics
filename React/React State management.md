[[React Architecture]] [[React data management]] [[React design patterns]] [[React pattern categorisation]] [[Redux State sync with localstorage]] [[react hooks]]

# React State management

> Choose mechanisms for client state — useState, Context, Zustand, Redux — matched to update rate and sharing needs.





## Interview Relevance
Interviewers force a choice among local state, Context, and external stores and judge whether you over-engineer.

## Sources
- [Managing State](https://react.dev/learn/managing-state) — deep-dive
- [Redux principles](https://redux.js.org/understanding/thinking-in-redux/three-principles) — overview

## Core Definition
State management is picking the smallest tool that keeps UI consistent where data is shared — and leaving server data to a cache library.

## Key Concepts
- **Local first:** `useState` / `useReducer`.
- **Deep pass without drilling:** Context (low-frequency).
- **Selective subscriptions:** [[zustand]] / Redux selectors.
- **Server data:** not these — use [[react-query]].

## Technical Details
| Need | Tool |
|------|------|
| One form | useState |
| Theme/locale | Context |
| Cart across pages | Zustand/Redux |
| Product list from API | Query lib |

## Real-World Applications
Theme in Context; cart in Zustand; product pages powered by TanStack Query.

## Pros/Cons or Trade-offs
- **Pro:** Right-sized tools keep cognitive load low.
- **Con:** Three stores without docs become tribal knowledge.

## Comparison
- vs [[React data management]]: state management ⊆ client side of data management.

## Mistakes to Avoid
- Context for mouse coordinates.
- Redux Toolkit plus mirrored TanStack cache for the same entities.
