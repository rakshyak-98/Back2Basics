[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React code smells

> Recurring anti-patterns — prop drilling chaos, effect-as-lifecycle cargo cult, derived state duplication — that signal design debt.





## Interview Relevance
Interviewers drop a smell and ask you to refactor: derived state, effects for transforms, or giant contexts.

## Sources
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — deep-dive
- [Managing State](https://react.dev/learn/managing-state) — overview

## Core Definition
Code smells are maintainability warnings: the app works but the structure will fight the next change.

## Key Concepts
- **Derived state:** storing what you can compute from props.
- **Effect for calculate:** syncing state that should be render-time math.
- **Mega context:** one provider for unrelated values causing wide re-renders.

## Technical Details
| Smell | Refactor |
|-------|----------|
| `useEffect` to set state from props | Compute during render |
| 12 boolean `useState`s | `useReducer` or state machine |
| Fetch in five children | Lift to query with shared key |

## Real-World Applications
Profile form stored `fullName` in state and updated it in an effect from `first`+`last` — remove state, concatenate in render.

## Pros/Cons or Trade-offs
- **Pro:** Naming smells creates a shared review vocabulary.
- **Con:** Obsessing over purity slows delivery on throwaway UI.

## Comparison
- vs [[Optimizing performance]]: smells are design; perf is measured cost.

## Mistakes to Avoid
- Adding Redux to “fix” prop drilling of two levels.
- Silencing exhaustive-deps to keep a smell compiling.
