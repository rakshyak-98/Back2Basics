[[React Pattern]] [[React Pattern/Summary pattern]] [[React design patterns]]

# React pattern categorisation

> Map UI jobs to patterns — composition, hooks, compounds, providers — so a large codebase stays consistent.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Pick the pattern from the job: reuse UI → composition; reuse behavior → hooks/HOC/render props; shared subtree state → compound/provider; outside DOM → portal.

```txt
Job → Pattern → Example
UI atoms → Composition → Button, Grid
Cross-cut → HOC / hook → withAuth, useAuth
Flexible UI + logic → Render props / hooks
Linked parts → Compound → Tabs, Form.Field
App-wide deps → Provider → Theme, Auth
```

### Interview map (words you can say)

| Pattern | Plain meaning | Say in interview |
|---------|---------------|------------------|
| **Composition** | Nest small components | “Prefer over inheritance.” |
| **HOC** | Wrap to inject behavior | “Easy wrapper hell — prefer hooks.” |
| **Render props** | Logic calls `children(fn)` | “Mostly replaced by hooks.” |
| **Compound** | Parts share context | “Declarative `<Tabs>` API.” |
| **Provider** | Inject deps down tree | “Theme, auth, query client.” |
| **Portal** | Render elsewhere in DOM | “Modals, toasts, tooltips.” |
| **Container/Presentational** | Logic vs UI split | “Or just a hook + dumb UI.” |

## Standard config / commands

| Pattern | Example components |
|---------|-------------------|
| Composition | `Button`, `Card`, `Grid` |
| HOC | `withAuth`, `withErrorBoundary` |
| Render props | `DataFetcher` (legacy) |
| Compound | `Modal`, `Dropdown`, `Tabs` |
| Hooks | `useFetch`, `useModal` |
| Provider | `AuthProvider`, `ThemeProvider` |
| Factory | `WidgetFactory` (dynamic config) |
| Portal | `Tooltip`, `Snackbar` |
| Container/Presentational | `UserController` + `UserCard` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrapper hell | Stacked HOCs | Convert to hooks |
| Prop drilling 8 levels | No provider/compound | Context or compound API |
| Inconsistent patterns per feature | No team map | Document “pattern per job” |
| Untestable UI | Logic in presentational | Extract hook/container |

---

## Gotchas

> [!WARNING]
> **Don’t assign SOLID labels as cargo cult** — pattern follows the reuse problem.

> [!WARNING]
> **HOCs + render props still appear in interviews** — know them; ship hooks.

---

## When NOT to use

- **Greenfield tiny app** — composition + hooks cover 90%.
- **Forcing a factory** — only when config truly drives component choice.

---

## Related

[[React Pattern/Summary pattern]] [[React Pattern/Higher order Component (HOCs)]] [[Render props]] [[React Pattern/Provider pattern]] [[React Pattern/Compound Components]]
