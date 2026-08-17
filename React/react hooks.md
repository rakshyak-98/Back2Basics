[[React]] [[Hooks/react useEffect]] [[useRef]] [[Optimizing performance]] [[React Pattern/Higher order Component (HOCs)]]

# react hooks

> Functions that let function components hold state and side effects — call them at the top level, same order every render.

```txt
        react hooks ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want Rules of Hooks, dependency arrays, and when a custom hook b…

## Sources
- [React — Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive
- [React — Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) — overview

## Key Concepts
- **Rules of Hooks:** Top-level, same order — “Enables React to match state to calls.”
- **Custom hook:** `useX` composing hooks — “Share logic without HOCs.”
- **Deps:** When effects/memos refresh — “Declare everything you read — or justify.”

## Technical Details
```txt
useState  → UI state
useEffect → after paint side effects
useRef    → mutable box, no re-render
useMemo / useCallback → stable values/fns
useContext → read provider
```

```tsx
function useWindowWidth() {
  const [w, setW] = useState(() => window.innerWidth)
  useEffect(() => {
    const onResize = () => setW(window.innerWidth)
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])
  return w
}
```

| Hook | Job |
|------|-----|
| `useState` / `useReducer` | Local state |
| `useEffect` | Sync with outside world |
| `useLayoutEffect` | DOM measure before paint |
| `useId` | Stable SSR-safe IDs |

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Hooks order error | Conditional / early return | Move hooks above conditions |
| Stale closure | Missing dep | Add dep or functional setState |
| Infinite setState loop | Effect writes its dep | Restructure deps |
| Invalid hook call | Called outside component | Only in components/custom hooks |

- **Mistake:** **ESLint `exhaustive-deps`**
- **Mistake:** **`useEffect` is not `componentDidMount` only**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Class components you won’t touch**
- **Con / skip when:** **Data fetching sprawl**

## Comparison
- vs [[react-query]]: **Data fetching sprawl** — prefer [[react-query]] over many raw effects.


### Use cases
- Apply react hooks in feature code where the Key Concepts match
