[[React Pattern]] [[React Pattern/Compound Components]] [[React Pattern/Provider pattern]]

# Compound Components 1

> Parent owns shared state; children read it via context — Tabs/Cart without prop drilling.

## Mental model

**Say it in one breath:** Compound components are a mini API (`Tabs`, `Tabs.Tab`, `Tabs.Panel`) that share state through context so callers compose JSX freely.

```txt
<Tabs>                 ← state + Provider
  <Tabs.List>…</Tabs.List>
  <Tabs.Panel />       ← useContext
</Tabs>
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Compound** | Related components, one state | “Implicit coupling via context.” |
| --- | --- | --- |
| **Static children** | `Tabs.Tab = …` | “Discoverable API on the parent.” |
| **Index / value** | Which panel is active | “Controlled or uncontrolled.” |

## Standard config / commands

```tsx
const TabsCtx = createContext<{ active: number; setActive: (n: number) => void } | null>(null)

function Tabs({ children, defaultIndex = 0 }: { children: React.ReactNode; defaultIndex?: number }) {
  const [active, setActive] = useState(defaultIndex)
  return <TabsCtx.Provider value={{ active, setActive }}>{children}</TabsCtx.Provider>
}

Tabs.Tab = function Tab({ index, children }: { index: number; children: React.ReactNode }) {
  const ctx = useContext(TabsCtx)!
  return (
    <button type="button" onClick={() => ctx.setActive(index)} aria-selected={ctx.active === index}>
      {children}
    </button>
  )
}

Tabs.Panel = function Panel({ index, children }: { index: number; children: React.ReactNode }) {
  const ctx = useContext(TabsCtx)!
  return ctx.active === index ? <div>{children}</div> : null
}
```

| Knob | Why it matters |

| Context null check | Throw if used outside parent |
| --- | --- |
| Controlled `value`/`onChange` | Forms & URL sync |
| `index` vs `id` | Prefer stable ids in real UIs |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `useContext` null | Child outside provider | Nest under `<Tabs>` |
| All panels show/none | Index mismatch | Align Tab/Panel indices |
| Re-render storm | Huge context value | Split state/dispatch contexts |
| Can’t deep-link tab | Uncontrolled only | Controlled + search params |

## Gotchas

> [!WARNING]
> **Children must be under the provider** — cloning/mapping outside loses context.

> [!WARNING]
> **Duplicate of [[React Pattern/Compound Components]]** — same idea; keep one canonical Tabs example in reviews.

## When NOT to use

- **One-off layout** — plain props are clearer.
- **Unrelated siblings** — don’t force a compound API.

## Related

[[React Pattern/Compound Components]] [[React Pattern/Provider pattern]] [[React Pattern/Composite pattern]] [[React Pattern/Summary pattern]]
