<!-- note-strategy: operational -->
[[React Pattern]] [[React Pattern/Provider pattern]] [[React Pattern/Compound Components 1]]

# Compound Components

> Build a feature UI from named parts that share one context — state in the parent, markup flexible for the caller.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Export a provider root plus parts (`Header`, `Body`, `Footer`) that call `useX()`. Callers compose parts; you don’t drill ten props.

```txt
ClassManagement (Provider + state)
  ├─ ClassHeader  → useClass()
  ├─ ClassBody    → useClass()
  └─ ClassFooter  → useClass()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Compound** | Parts share implicit state | “Like `<select>` + `<option>`.” |
| **Provider vs router** | State ≠ navigation | “Don’t put `router.push` in the cart provider.” |
| **useClass hook** | Typed context consumer | “Throw if missing provider.” |

## Standard config / commands

```tsx
const ClassCtx = createContext<null | ClassValue>(null)
export function useClass() {
  const v = useContext(ClassCtx)
  if (!v) throw new Error('useClass outside ClassManagement')
  return v
}

export function ClassManagement({ children }: { children: React.ReactNode }) {
  const [students, setStudents] = useState<{ id: number; name: string }[]>([])
  const value = {
    students,
    addStudent: (s: { id: number; name: string }) => setStudents((p) => [...p, s]),
    removeStudent: (id: number) => setStudents((p) => p.filter((s) => s.id !== id)),
  }
  return <ClassCtx.Provider value={value}>{children}</ClassCtx.Provider>
}

// Checkout: keep routing outside the provider
function ProceedToCheckout() {
  const { proceed } = useCart()
  const router = useRouter()
  return <button onClick={() => { proceed(); router.push('/checkout') }}>Checkout</button>
}
```

| Knob | Why it matters |
|------|----------------|
| Hook guard | Fail fast outside tree |
| Thin provider | State/actions only — no routing |
| Part components | Optional; callers can use hook directly |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hook throws | Missing provider | Wrap with `ClassManagement` |
| Provider hard to reuse | Router inside provider | Move navigation to leaf |
| Extra re-renders | New object every render | `useMemo` value or split contexts |
| Parts unused API | Over-compounded | Flatten to props |

---

## Gotchas

> [!WARNING]
> **Cart/provider + routing mixed** — breaks testability and reuse; navigate in a child.

> [!WARNING]
> **Duplicated ClassHeader/Body samples in old notes** — one definition each.

---

## When NOT to use

- **Simple prop tree (2–3 levels)** — pass props.
- **Global application state** — Redux/Zustand, not a feature compound.

---

## Related

[[React Pattern/Compound Components 1]] [[React Pattern/Provider pattern]] [[React Pattern/Composite pattern]] [[React Pattern/Component Presentational Pattern]]
