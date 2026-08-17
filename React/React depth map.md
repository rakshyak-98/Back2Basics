[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React depth map

> What strong React depth checks cover — hooks rules, state placement, RSC boundaries, and debugging re-renders.

```txt
        React depth map ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** This note is the study map — expect hooks, state vs server cache, keys/lists, …

## Sources
- [React Learn](https://react.dev/learn) — overview
- [React Reference](https://react.dev/reference/react) — deep-dive

## Key Concepts
- **Core:** React depth checks reward precise mental models (render → commit → effects) and…

## Technical Details
- Practice prompts:

1. Why can’t hooks be conditional?
2. When is Context the wrong tool?
3. How do you fix a hydration mismatch?
4. Redux vs Query vs Zustand — pick for a notifications dropdown.

## Mistakes to Avoid
- **Mistake:** Answering “useMemo everything.”
- **Mistake:** Claiming Redux is required for all apps

## Pros/Cons or Trade-offs
- **Pro:** Structured prep covers 80% of FE rounds.
- **Con:** Memorizing API lists without failure stories fails senior bars.

## Comparison
- Cross-link deep leaves: [[react hooks]], [[React State management]], [[RSC (React Server Componen…


### Use cases
- Whiteboard a notifications bell: unread count from query cache, dropdown open…
