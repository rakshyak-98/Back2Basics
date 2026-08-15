[[React]] [[react hooks]] [[Hooks/react useEffect]] [[Typescript with react]]

# useRef

> Holds a mutable box that survives renders without re-rendering — DOM nodes or “remember this value.”

## Interview Relevance

Interviewers want Rules of Hooks, dependency arrays, and when a custom hook beats an HOC — not a list of hook names.

## Sources

- [Wikipedia — useRef](https://en.wikipedia.org/wiki/useRef) — overview

## Key Concepts

- **ref:** Mutable box React keeps across renders — “I store the DOM node without causing a re-render.”
- **`.current`:** The actual value — “Focus via `inputRef.current.focus()`.”
- **forwardRef:** Pass a parent ref into a child — “Wrapper must forwardRef or the ref never reaches the input.”

## Technical Details

```txt
render → same ref object
           └─ .current  ← mutate freely (DOM | timer id | previous value)
```

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

## Real-World Applications

Apply useRef in feature code where the Key Concepts match; verify with the Mistakes table.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Value drives UI** — use `useState` / `useReducer`.
- **Con / skip when:** **Derived from props** — compute during render; don’t mirror into a reference unless you need “previous.”

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| `ref.current` is null | Called before mount / wrong element | Use in `useEffect` or event handler |
| Parent ref never hits input | Child is a function component | Wrap with `forwardRef` |
| UI stale after mutating ref | Expected re-render | Use `useState` for UI-driving values |
| Stale closure with ref | Read `.current` inside effect | Prefer reading `.current` at call time |

- **Ref ≠ state** — mutating `.current` never re-renders. Use state when the screen must update.
- **forwardRef types** — generics often collapse to `unknown`; augment or type the returned component explicitly.
