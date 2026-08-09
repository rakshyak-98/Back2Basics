[[React Pattern]] [[React Pattern/Compound Components]] [[React Pattern/Provider pattern]]

# Composite pattern

> Treat a tree of UI parts as one unit — parent coordinates; children stay focused and reusable.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Composite = compose leaf widgets under a conductor that holds shared context. Same idea as compound components in React: recombine parts without rewriting wiring.

```txt
Conductor (context + orchestration)
  ├─ Leaf A (one job)
  ├─ Leaf B
  └─ Nested composite…
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Composite** | Tree of parts, uniform use | “Callers nest parts; parent orchestrates.” |
| **Decoupled leaf** | Child doesn’t know siblings | “Reuse Panel in another shell.” |
| **vs inheritance** | Composition wins in React | “No BaseWidget class hierarchy.” |

## Standard config / commands

```tsx
const ShellCtx = createContext<{ open: boolean; toggle: () => void } | null>(null)

export function Shell({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  const value = { open, toggle: () => setOpen((o) => !o) }
  return <ShellCtx.Provider value={value}><div className="shell">{children}</div></ShellCtx.Provider>
}

export function ShellToggle() {
  const ctx = useContext(ShellCtx)!
  return <button onClick={ctx.toggle}>{ctx.open ? 'Close' : 'Open'}</button>
}
```

| Knob | Why it matters |
|------|----------------|
| Context at conductor | Leaves stay prop-light |
| Public leaf exports | Recombine in other screens |
| Clear ownership | One place mutates shared state |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Leaf useless alone | Hard-coded parent | Depend only on context contract |
| God conductor | Too many concerns | Split composites |
| Prop drilling returns | Forgot context | Provider at composite root |

---

## Gotchas

> [!WARNING]
> **Composite ≠ fancy name for any folder of components** — needs a shared coordination surface.

> [!WARNING]
> **Overlap with compound components** — same React technique; composite is the OO/GoF framing.

---

## When NOT to use

- **Flat static pages** — composition without shared state is enough.
- **Global app store needs** — Redux/Zustand, not a local composite.

---

## Related

[[React Pattern/Compound Components]] [[React Pattern/Provider pattern]] [[React Pattern/React pattern categorisation]]
