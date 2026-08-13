<!-- note-strategy: operational -->
[[React]] [[react routes]] [[hydration]]

# React feature implementations

> Detect “user arrived via path A → B” — pass router state, keep a short history, or cookie middleware.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Browsers don’t give you a full path sequence API. You either pass `location.state` on navigate, keep a rolling history in context, or record paths in middleware cookies.

```txt
Link state:  A --state{from}--> B
Context:     […paths].slice(-n) on each route change
Middleware:  cookie nav-history updated per request
```

### Interview map (words you can say)

| Tool | Plain meaning | Say in interview |
|------|---------------|------------------|
| **location.state** | Ephemeral nav payload | “Best for one hop intent.” |
| **useNavigationType** | PUSH / REPLACE / POP | “Back button ≠ fresh entry.” |
| **History context** | Last N pathnames | “Multi-step funnels.” |

## Standard config / commands

```tsx
// React Router — one hop
<Link to="/target" state={{ from: '/source-path' }}>Go</Link>
const { state } = useLocation()
if (state?.from === '/source-path') { /* … */ }

// Rolling history (Next pages router sketch)
useEffect(() => {
  const on = (url: string) => setHistory((h) => [...h.slice(-1), url])
  router.events.on('routeChangeComplete', on)
  return () => router.events.off('routeChangeComplete', on)
}, [router])
```

| Knob | Why it matters |
|------|----------------|
| `state` | Lost on full reload / external entry |
| Keep last 2–3 | Enough for “came from sequence” |
| Cookie middleware | Server can see sequence |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `state` always undefined | Hard refresh / typed URL | Don’t rely on state alone |
| Wrong “previous” | Updated after paint incorrectly | Store previous before overwrite |
| Sequence false positive | History too long / unordered | Explicit tuple check |
| App Router no `router.events` | Pages API assumption | Use pathname effect / instrumentation |

---

## Gotchas

> [!WARNING]
> **`document.referrer` is unreliable** — cross-origin and privacy truncate it.

> [!WARNING]
> **Analytics ≠ UX gating** — don’t block checkout on client history alone.

---

## When NOT to use

- **Authz / payments** — server session truth, not path folklore.
- **Simple “where did I come from?” back button** — `router.back()` / `POP`.

---

## Related

[[react routes]] [[React Architecture]] [[hydration]]
