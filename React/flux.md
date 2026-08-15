[[react hooks]] [[React State management]] [[React Architecture]]

# Flux

> Early Facebook unidirectional data pattern — actions → dispatcher → stores → views — ancestor of Redux.

## Interview Relevance

Interviewers may ask Flux vs Redux: single store, pure reducers, and immutability habits.

## Sources

- [Flux overview](https://facebook.github.io/flux/) — overview
- [Redux prior art](https://redux.js.org/understanding/history-and-design/prior-art) — deep-dive

## Core Definition

Flux enforces one-way data flow so views don’t mutate shared stores ad hoc; Redux refined it into a single store and pure reducers.

## Key Concepts

- **Action:** plain object describing intent.
- **Dispatcher:** central hub (Flux) / store.dispatch (Redux).
- **Store:** holds state; views subscribe.

## Technical Details

Conceptual flow: `View → Action → Dispatcher → Store → View`.

## Real-World Applications

Historical React apps used Flux libraries; modern code usually uses Redux Toolkit or simpler stores.

## Pros/Cons or Trade-offs

- **Pro:** Predictable updates vs two-way binding chaos.
- **Con:** Classic Flux boilerplate is heavy vs RTK.

## Comparison

- vs [[Redux]]: Redux is a Flux-inspired library with a single store and middleware ecosystem.

## Mistakes to Avoid

- Calling Flux and Redux interchangeable without noting single-store and Immer/RTK differences.
