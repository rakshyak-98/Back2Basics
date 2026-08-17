[[React]] [[hydration]] [[react hooks]] [[Hooks/react useEffect]] [[RSC (React Server Component boundaries)]]

# react error (common failures)

> React runtime errors you’ll hit in prod — wrong hook counts, hydration mismatches, and security headers that break assets.

```txt
        react error (commo ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers use react error (common failures) to test whether you can apply …

## Sources
- [Wikipedia — react error](https://en.wikipedia.org/wiki/react_error) — overview

## Key Concepts
- **Rules of Hooks:** Same hooks, same order — “No hooks after conditional return.”
- **Hydration mismatch:** Server HTML ≠ client — “Stabilize time/random on first paint.”
- **nosniff:** Trust declared MIME — “Stops MIME-sniff XSS on uploaded files.”

## Technical Details
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

### Steps

1. …

### Verification

```bash
# …
```

### Rollback

1. …

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Rendered fewer/more hooks | Conditional hooks / early return | Call all hooks unconditionally |
| Minified `#310` / `#418` | Decode via React error decoder | Usually hydration or hook order |
| Script blocked / MIME | Response headers | Correct `Content-Type` + `nosniff` |
| Hydration failed | Server vs client text | Defer dynamic bits; match SSR |
| Invalid hook call | Duplicate React / call outside component | One React copy; only in function components/hooks |

- **Mistake:** **Error codes in prod**
- **Mistake:** **`nosniff` + wrong MIME**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Swallowing errors in empty catch**
- **Con / skip when:** **Treating hydration warnings as noise**

## Real-World Applications
- **Scenario:** Apply react error (common failures) in feature code where the Key Concepts ma…
