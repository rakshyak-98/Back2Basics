[[React]] [[Hooks/react useEffect]] [[useRef]] [[Optimizing performance]]

# react hooks

> Functions that let function components hold state and side effects — call them at the top level, same order every render.

---

## How it works

```txt
useState  → UI state
useEffect → after paint side effects
useRef    → mutable box, no re-render
useMemo / useCallback → stable values/fns
useContext → read provider
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Rules of Hooks** | Top-level, same order | “Enables React to match state to calls.” |
| **Custom hook** | `useX` composing hooks | “Share logic without HOCs.” |
| **Deps** | When effects/memos refresh | “Declare everything you read — or justify.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Hooks order error | Conditional / early return | Move hooks above conditions |
| Stale closure | Missing dep | Add dep or functional setState |
| Infinite setState loop | Effect writes its dep | Restructure deps |
| Invalid hook call | Called outside component | Only in components/custom hooks |

---


## Gotchas

> [!WARNING]
> **ESLint `exhaustive-deps`** — silencing it without a reason usually creates bugs.

> [!WARNING]
> **`useEffect` is not `componentDidMount` only** — think “synchronize with a system,” not lifecycle cargo cult.

---


## When not to use

- **Class components you won’t touch** — don’t rewrite just to use hooks.
- **Data fetching sprawl** — prefer [[react-query]] over many raw effects.

---


## Related

[[Hooks/react useEffect]] [[useRef]] [[Optimizing performance]] [[React Pattern/Higher order Component (HOCs)]]

## Sources

- [Wikipedia — react hooks](https://en.wikipedia.org/wiki/react_hooks)
