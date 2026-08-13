[[react hooks]] [[React State management]] [[React Architecture]] [[react style inside component]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# RSC (React Server Component boundaries)

> RSC (React Server Component boundaries) shapes how React applications compose UI, state, and side effects in production.

## What this is

React Server Components run on the server and serialize their output for the client bundle boundary. Files marked `"use client"` become client components that can hold state and browser APIs; keeping server components at the leaves of data-fetching trees reduces JavaScript shipped to browsers.

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `RSC (React Server Component boundaries)` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[React State management]] [[React Architecture]] [[react style inside component]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

## Sources

- [React — Server Components](https://react.dev/reference/rsc/server-components)
