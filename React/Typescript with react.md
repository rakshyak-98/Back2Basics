<!-- note-strategy: operational -->
[[React]] [[useRef]] [[react hooks]]

# Typescript with react

> Type React props, hooks, and refs so the compiler catches wrong shapes before runtime.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Components are functions of typed props; hooks take type arguments (`useRef<T>`, `useReducer<R>`); `forwardRef` often needs an explicit generic or a small type augment.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`FC` / props type** | Shape of props | “Prefer `function Comp(props: Props)` over `React.FC`.” |
| **`useRef<T>(null)`** | Ref may be null until mount | “Include `null` in the type.” |
| **`Reducer<S, A>`** | State + action types | “Built-in helper for `useReducer`.” |
| **forwardRef generics** | Ref + props params | “Default typings often erase props generics.” |

## Standard config / commands

```tsx
type Props = { label: string; onSave: (id: string) => void }

function Form({ label, onSave }: Props) { /* … */ }

const inputRef = useRef<HTMLInputElement>(null)

type State = { n: number }
type Action = { type: 'inc' } | { type: 'set'; n: number }
const [state, dispatch] = useReducer<React.Reducer<State, Action>>(reducer, { n: 0 })

const Input = React.forwardRef<HTMLInputElement, Props>(function Input(props, ref) {
  return <input ref={ref} {...props} />
})
```

| Knob | Why it matters |
|------|----------------|
| Props as type alias | Clear, no `children` surprises from old `FC` |
| `useRef<T>(null)` | Matches real lifecycle |
| Augment `forwardRef` | Restore generic props if lib types erase them |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Ref typed `never` / wrong | Initializer vs type arg | `useRef<T>(null)` when T excludes null incorrectly |
| forwardRef props become `unknown` | Lib typing | Explicit generics or `*.d.ts` augment |
| Event handler type errors | Wrong event type | `React.ChangeEvent<HTMLInputElement>` etc. |
| Children type fights you | `React.FC` defaults | Drop `FC`; type `children` explicitly |

---

## Gotchas

> [!WARNING]
> **`forwardRef` forgets generics** — returned component types often collapse; assert or augment.

> [!WARNING]
> **`useRef<T>(null)` overload** — if `T` does not include `null` but you pass `null`, you hit a special overload; prefer `useRef<T \| null>(null)`.

---

## When NOT to use

- **Throwaway prototypes** — JS is fine until the API stabilizes.
- **Over-modeling runtime CSS** — don’t type every style object if it slows delivery.

---

## Related

[[useRef]] [[react hooks]] [[Hooks/react useEffect]]
