[[react hooks]] [[React State management]] [[React Architecture]]

# Render props

> Component takes a function as children/prop and calls it with state — share behavior before hooks were common.

```txt
        Render props ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers expect you to recognize render props in legacy code and explain …

## Sources
- [React Children (related)](https://react.dev/reference/react/Children) — overview
- [Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) — deep-dive

## Key Concepts
- **Pattern:** `<Mouse>{pos => <Cursor x={pos.x} />}</Mouse>`.
- **Era:** popular pre-hooks; still appears in libs.
- **Today:** prefer `useMouse()` custom hook unless composing with component trees.


- **Core:** A render prop is a function prop (often `children`) that receives values and …

## Technical Details
```tsx
function Mouse({ children }: { children: (p: { x: number; y: number }) => React.ReactNode }) {
  const [p, setP] = useState({ x: 0, y: 0 })
  useEffect(() => {
    const onMove = (e: MouseEvent) => setP({ x: e.clientX, y: e.clientY })
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])
  return children(p)
}
```

## Mistakes to Avoid
- **Mistake:** Nesting five render-prop providers until JSX is unreadable
- **Mistake:** Rewriting stable render-prop libraries “just because.”

## Pros/Cons or Trade-offs
- **Pro:** Flexible composition without HOCs wrapping display names.
- **Con:** Wrapper hell and harder static typing than hooks.

## Comparison
- vs [[React Pattern/Higher order Component (HOCs)]]: both share behavior


### Use cases
- Legacy React Router and early Formik APIs used render props
