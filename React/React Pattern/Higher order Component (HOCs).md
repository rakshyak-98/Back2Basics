[[React Pattern]] [[Render props]] [[react hooks]]

# Higher order Component (HOCs)

> Function that takes a component and returns a wrapped one — share cross-cutting behavior (auth, logging) without copying it.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `withX(Comp) => EnhancedComp`. Props flow through the wrapper; today hooks usually replace HOCs for application code.

```txt
withAuth(Cart) → checks token → renders Cart or login wall
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **HOC** | Component factory | “Reuse behavior by wrapping.” |
| **Prop collision** | Wrapper and child share names | “Namespace injected props.” |
| **vs hooks** | Compose functions vs wrap trees | “Hooks compose cleaner in modern React.” |

## Standard config / commands

```tsx
function withAuth<P extends object>(Wrapped: React.ComponentType<P>) {
  return function WithAuth(props: P) {
    const token = localStorage.getItem('token')
    if (!token) return <p>Please log in</p>
    return <Wrapped {...props} />
  }
}

export default withAuth(Cart)
```

| Knob | Why it matters |
|------|----------------|
| Pass-through props | Spread `...props` to the wrapped component |
| `displayName` | `WithAuth(Cart)` helps DevTools |
| Static hoist | Copy statics if the child has them |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing props on child | Forgot spread | `{...props}` |
| ref doesn’t reach | Function wrapper | `forwardRef` through HOC |
| Double wrappers hell | Nested withX(withY(…)) | Prefer hooks/composition |
| Props overwritten | Same prop names | Prefix (`authUser`) |

---

## Gotchas

> [!WARNING]
> **HOCs hide the tree** — debugging wrapped stacks is harder than a `useAuth()` call.

> [!WARNING]
> **Don’t put hooks in the HOC factory body** — only inside the returned component.

---

## When NOT to use

- **New feature work** — custom hooks + providers first.
- **One-off UI** — just write the check inline or in a layout.

---

## Related

[[Render props]] [[react hooks]] [[React Pattern/Provider pattern]]
