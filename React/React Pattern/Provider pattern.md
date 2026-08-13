[[React Pattern]] [[React code smells]] [[Optimizing performance]]

# Provider pattern

> Put shared state in React context — consumers subscribe without prop drilling; split state vs actions to limit re-renders.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Provider holds value; `useContext` reads it. If the value object is new every render, every consumer re-renders — split contexts or memoize.

```txt
<AuthProvider>  value={{ user, login }}
   └─ useAuth() in deep child (no prop chain)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Provider** | Context root | “Injects dependencies down the tree.” |
| **Split context** | State vs stable actions | “Actions context rarely changes.” |
| **vs Redux** | Built-in, local | “Context for theme/auth; Redux for complex client state.” |

## Standard config / commands

```tsx
const AuthStateContext = createContext<User | null>(null)
const AuthActionsContext = createContext<{ login: () => void; logout: () => void } | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const login = useCallback(() => { /* … */ setUser(/* … */) }, [])
  const logout = useCallback(() => setUser(null), [])
  const actions = useMemo(() => ({ login, logout }), [login, logout])
  return (
    <AuthStateContext.Provider value={user}>
      <AuthActionsContext.Provider value={actions}>{children}</AuthActionsContext.Provider>
    </AuthStateContext.Provider>
  )
}
```

| Knob | Why it matters |
|------|----------------|
| Separate state/actions | Button-only consumers skip user updates |
| `useMemo` value | Stable reference when contents unchanged |
| Default null + hook assert | Fail fast outside provider |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Whole tree re-renders | Inline `{…}` value | Memoize or split context |
| null context crash | Used outside provider | Guard in `useX` hook |
| Stale actions | Missing `useCallback` | Stabilize action fns |
| Prop drilling returns | Forgot provider high enough | Lift provider to layout |

---

## Gotchas

> [!WARNING]
> **Context is not a silver bullet** — high-frequency state (mouse coords) will thrash consumers; use refs or external stores.

> [!WARNING]
> **Default value traps** — a working default hides missing providers in tests.

---

## When NOT to use

- **Pass 1–2 levels** — props are clearer.
- **Server cache** — [[react-query]] / RTK Query.

---

## Related

[[React code smells]] [[Optimizing performance]] [[Render props]] [[Redux]]
