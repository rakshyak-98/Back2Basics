[[React]] [[React Architecture]] [[React Application Architecture for Production]]

# Creating a stack from scratch

> Pick foundation + data + styling from constraints — risk, speed, or legacy — not fashion.

## Mental model

**Say it in one breath:** Stack choice is a constraint match: regulated enterprise wants boring/typed; prototype wants batteries included; legacy wants minimal churn.

```txt
Constraints → Foundation → Data layer → Styling
enterprise     React+TS      Apollo/RTK    styled / DS
prototype      Remix         Supabase+SWR  Ant Design
legacy         CRA/Vite      Redux         CSS Modules
```

### Interview map (words you can say)

| Scenario | Bias | Why |
| --- | --- | --- |
| **Financial / regulated** | React+TS, explicit data layer | Auditability, hiring pool, fewer magic frameworks |
| **Investor prototype** | Remix/Next + BaaS + SWR | Ship features; UI uniqueness secondary |
| **Legacy dashboard** | Keep Redux + CSS Modules | Change surface area small |

## Standard config / commands

| Stack | Foundation | Data | Style |

| Enterprise | React + TypeScript | Apollo or RTK Query | Design system / styled-components |
| --- | --- | --- | --- |
| Prototype | Remix (or Next) | Supabase + SWR | Ant Design |
| Legacy maintain | CRA → Vite migrate later | Redux | CSS Modules |

```txt
Decide:
1) SSR needed? → Next/Remix : Vite SPA
2) GraphQL org standard? → Apollo : REST + RTK Query/react-query
3) Design system exists? → use it : don’t invent one in week one
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Prototype stuck in Ant defaults | Product needs brand | Swap UI kit early or budget redesign |
| Enterprise rejected Remix | Risk/compliance | Stick to React+TS + known libs |
| Legacy can’t hire CRA experts | Tooling frozen | Vite migration plan; keep Redux |
| Two data libraries | Apollo + React Query | Pick one cache story |

## Gotchas

> [!WARNING]
> **“Comprehensive web app” ≠ maximal stack** — every library is an ops surface.

> [!WARNING]
> **CRA is maintenance mode** — new work should plan Vite/Next exit.

## When NOT to use

- **Copying a blog’s “perfect stack”** — ignore if constraints differ.
- **Rewriting legacy for fashion** — stabilize first.

## Related

[[React Architecture]] [[React Application Architecture for Production]] [[React project configuration]] [[React build]]
