[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# react useEffect

> Synchronize a component with an external system after render — subscriptions, network, non-React widgets.





## Interview Relevance
Interviewers hammer dependency arrays, cleanup, and “you might not need an effect” for derived state.

## Sources
- [useEffect](https://react.dev/reference/react/useEffect) — deep-dive
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — deep-dive

## Core Definition
`useEffect` runs after paint to connect React to something outside React; cleanup undoes that connection.

## Key Concepts
- **Deps:** re-run when listed values change.
- **Cleanup:** unsubscribe / abort.
- **Not for:** transforming props into state that can be computed.

## Technical Details
```tsx
useEffect(() => {
  const id = setInterval(() => tick(), 1000)
  return () => clearInterval(id)
}, [tick])
```

## Real-World Applications
Chat socket subscribed in an effect; abort/unsubscribe on room id change.

## Pros/Cons or Trade-offs
- **Pro:** Explicit external sync points.
- **Con:** Effect sprawl recreates lifecycle soup.

## Comparison
- vs `useLayoutEffect`: layout runs before paint for DOM measure.

## Mistakes to Avoid
- Missing deps / disabling eslint blindly.
- Fetching without a query library in every component.
