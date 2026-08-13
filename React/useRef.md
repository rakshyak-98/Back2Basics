[[React]] [[react hooks]]

# useRef

> Holds a mutable box that survives renders without re-rendering — DOM nodes or “remember this value.”

---

## How it works

```txt
render → same ref object
           └─ .current  ← mutate freely (DOM | timer id | previous value)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ref** | Mutable box React keeps across renders | “I store the DOM node without causing a re-render.” |
| **`.current`** | The actual value | “Focus via `inputRef.current.focus()`.” |
| **forwardRef** | Pass a parent ref into a child | “Wrapper must forwardRef or the ref never reaches the input.” |


## Configuration and commands

```tsx
const inputRef = useRef<HTMLInputElement>(null)
const countRef = useRef(0) // mutable counter, no re-render

useEffect(() => {
  inputRef.current?.focus()
}, [])

// Forward to child
const Input = React.forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
))
```

| Knob | Why it matters |
|------|----------------|
| `useRef(null)` + DOM | After mount, `.current` is the element |
| Mutable non-UI value | Timers, previous props, AbortController |
| `forwardRef` | Required when wrapping native elements |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `ref.current` is null | Called before mount / wrong element | Use in `useEffect` or event handler |
| Parent ref never hits input | Child is a function component | Wrap with `forwardRef` |
| UI stale after mutating ref | Expected re-render | Use `useState` for UI-driving values |
| Stale closure with ref | Read `.current` inside effect | Prefer reading `.current` at call time |

---


## Gotchas

> [!WARNING]
> **Ref ≠ state** — mutating `.current` never re-renders. Use state when the screen must update.

> [!WARNING]
> **forwardRef types** — generics often collapse to `unknown`; augment or type the returned component explicitly.

---


## When not to use

- **Value drives UI** — use `useState` / `useReducer`.
- **Derived from props** — compute during render; don’t mirror into a reference unless you need “previous.”

---


## Related

[[react hooks]] [[Hooks/react useEffect]] [[Typescript with react]]

## Sources

- [Wikipedia — useRef](https://en.wikipedia.org/wiki/useRef)
