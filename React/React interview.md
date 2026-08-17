[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React interview

> What strong React interviews probe — hooks rules, state placement, RSC boundaries, and debugging re-renders — with crisp trade-offs.

```txt
        React interview ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** This note is the study map: expect hooks, state vs server cache, keys/lists, …

## Sources
- [React Learn](https://react.dev/learn) — overview
- [React Reference](https://react.dev/reference/react) — deep-dive

## Key Concepts
- **Core:** React interviews reward precise mental models (render → commit → effects) and…

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
