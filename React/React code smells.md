[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React code smells

> Recurring anti-patterns — prop drilling chaos, effect-as-lifecycle cargo cult, derived state duplication — that signal design debt.

```txt
        React code smells ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers drop a smell and ask you to refactor: derived state, effects for…

## Sources
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — deep-dive
- [Managing State](https://react.dev/learn/managing-state) — overview

## Key Concepts
- **Derived state:** storing what you can compute from props.
- **Effect for calculate:** syncing state that should be render-time math.
- **Mega context:** one provider for unrelated values causing wide re-renders.


- **Core:** Code smells are maintainability warnings: the app works but the structure wil…

## Technical Details
| Smell | Refactor |
|-------|----------|
| `useEffect` to set state from props | Compute during render |
| 12 boolean `useState`s | `useReducer` or state machine |
| Fetch in five children | Lift to query with shared key |

## Mistakes to Avoid
- **Mistake:** Adding Redux to “fix” prop drilling of two levels
- **Mistake:** Silencing exhaustive-deps to keep a smell compiling

## Pros/Cons or Trade-offs
- **Pro:** Naming smells creates a shared review vocabulary.
- **Con:** Obsessing over purity slows delivery on throwaway UI.

## Comparison
- vs [[Optimizing performance]]: smells are design; perf is measured cost.


### Use cases
- Profile form stored `fullName` in state and updated it in an effect from `fir…
