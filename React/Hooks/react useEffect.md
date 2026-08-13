[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# react useEffect

> react useEffect shapes how React applications compose UI, state, and side effects in production.

## What this is

Hooks are functions whose names start with `use` and attach stateful logic to function components. React matches hook calls to fiber state by call order, which is why hooks must run at the top level of every render and never inside conditions or loops ([React Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks)).

## Operating it

```tsx
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id); // cleanup on dep change or unmount
}, [tick]);
```

| Check | Action |
|-------|--------|
| Stale closure in effect | List every reactive value in the dependency array or refactor to a ref |
| Effect runs every render | Remove state updates that rewrite dependencies each pass |
| Missing cleanup | Return a dispose function for subscriptions, timers, and listeners |

## What breaks first

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Invalid hook call warning | Hook outside component or duplicate React copies | Call hooks only from components/custom hooks; dedupe `react` in bundle |
| Hydration mismatch | Server HTML differs from client render | Fix conditional rendering; avoid `Date.now()` in SSR output |
| State updates but UI stale | Mutation without setter | Use immutable updates; Redux Toolkit uses Immer but raw React state needs new references |

## Recall

What breaks first in production if `react useEffect` is misused — bundle size, stale UI, or hydration errors?

## Related

[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

## Sources

- [React — useEffect](https://react.dev/reference/react/useEffect)
