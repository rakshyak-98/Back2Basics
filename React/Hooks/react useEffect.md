[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# react useEffect

> Synchronize a component with an external system after render — subscriptions, network, non-React widgets.

```txt
        react useEffect ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers hammer dependency arrays, cleanup, and “you might not need an ef…

## Sources
- [useEffect](https://react.dev/reference/react/useEffect) — deep-dive
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — deep-dive

## Key Concepts
- **Deps:** re-run when listed values change.
- **Cleanup:** unsubscribe / abort.
- **Not for:** transforming props into state that can be computed.


- **Core:** `useEffect` runs after paint to connect React to something outside React

## Technical Details
```tsx
useEffect(() => {
  const id = setInterval(() => tick(), 1000)
  return () => clearInterval(id)
}, [tick])
```

## Mistakes to Avoid
- **Mistake:** Missing deps / disabling eslint blindly
- **Mistake:** Fetching without a query library in every component

## Pros/Cons or Trade-offs
- **Pro:** Explicit external sync points.
- **Con:** Effect sprawl recreates lifecycle soup.

## Comparison
- vs `useLayoutEffect`: layout runs before paint for DOM measure.


### Use cases
- Chat socket subscribed in an effect; abort/unsubscribe on room id change.
