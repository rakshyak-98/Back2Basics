[[React]] [[hydration]] [[react hooks]]

# react error (common failures)

> React runtime errors you’ll hit in prod — wrong hook counts, hydration mismatches, and security headers that break assets.

---

## Mental model

**Say it in one breath:** React demands stable hook order every render; SSR demands matching markup; browsers demand correct `Content-Type` (and often `nosniff`).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Rules of Hooks** | Same hooks, same order | “No hooks after conditional return.” |
| **Hydration mismatch** | Server HTML ≠ client | “Stabilize time/random on first paint.” |
| **nosniff** | Trust declared MIME | “Stops MIME-sniff XSS on uploaded files.” |

## Standard config / commands

```tsx
// ❌ early return before hooks
function Bad({ user }) {
  if (!user) return null
  const [x, setX] = useState(0) // shifts hook count
}

// ✅ hooks first
function Good({ user }) {
  const [x, setX] = useState(0)
  if (!user) return null
  return <div>{x}</div>
}
```

```http
X-Content-Type-Options: nosniff
Content-Type: application/javascript; charset=utf-8
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Rendered fewer/more hooks | Conditional hooks / early return | Call all hooks unconditionally |
| Minified `#310` / `#418` | Decode via React error decoder | Usually hydration or hook order |
| Script blocked / MIME | Response headers | Correct `Content-Type` + `nosniff` |
| Hydration failed | Server vs client text | Defer dynamic bits; match SSR |
| Invalid hook call | Duplicate React / call outside component | One React copy; only in function components/hooks |

---

## Gotchas

> [!WARNING]
> **Error codes in prod** — map `#NNN` at https://react.dev/errors/NNN (version-specific).

> [!WARNING]
> **`nosniff` + wrong MIME** — legitimate JS served as `text/plain` will refuse to run.

---

## When NOT to use

- **Swallowing errors in empty catch** — use an error boundary for UI failures.
- **Treating hydration warnings as noise** — they often mean remounts and lost SSR wins.

---

## Related

[[hydration]] [[Hooks/react useEffect]] [[RSC (React Server Component boundaries)]]
