[[React]] [[RSC (React Server Component boundaries)]] [[SSR]]

# hydration

> Browser JS “wakes up” server HTML — attach listeners and state so the page becomes interactive.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Server sends HTML fast; client React walks that DOM, builds its tree, and attaches events — markup must match or you get hydration errors.

```txt
SSR HTML ──► paint (fast, not interactive)
     │
     ▼ JS loads
React hydrate ──► same tree + listeners ──► interactive
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **SSR** | HTML built on the server | “User sees content before JS finishes.” |
| **Hydration** | Client attaches React to that HTML | “We don’t re-create DOM if markup matches.” |
| **Mismatch** | Server HTML ≠ client first render | “Clocks, `Math.random`, locale → classic bugs.” |

## Standard config / commands

```tsx
// Next App Router: Server Component HTML + Client Component islands
'use client'
export function Counter() {
  const [n, setN] = useState(0)
  return <button onClick={() => setN(n + 1)}>{n}</button>
}
```

| Knob | Why it matters |
|------|----------------|
| Match SSR/CSR output | Text, locale, time must be stable on first client render |
| Client islands | Only hydrate interactive parts — smaller JS |
| `suppressHydrationWarning` | Last resort for known date/locale diffs |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hydration failed / text mismatch | Server HTML vs first client render | Stabilize random/time; render dynamic bits after mount |
| Flash then correct | Client-only data on first paint | Fetch on server or defer to `useEffect` |
| Dead clicks until JS loads | Heavy bundle / late hydrate | Split client components; reduce JS |
| SEO empty | Client-only render | Prefer SSR/RSC for content |

---

## Gotchas

> [!WARNING]
> **Browser-only APIs in render** (`window`, `localStorage`) break SSR and hydration — gate behind `useEffect` or client components.

> [!WARNING]
> **Mismatch ≠ “just a warning”** — React may throw away server DOM and remount (worse TTI).

---

## When NOT to use

- **Pure SPA with no SEO/FCP need** — client render may be enough.
- **Fully static marketing page** — HTML-only; skip React hydrate cost.

---

## Related

[[RSC (React Server Component boundaries)]] [[SSR]] [[react error]]
