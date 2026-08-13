[[React]] [[react hooks]] [[Hooks/react useEffect]]

# React interview

> Common interview fetch/effect pitfalls — abort races, handle errors, keep effects sync.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Interviewers want a fetch keyed by `id` that aborts on change/unmount, surfaces errors, and never leaves a hanging promise in `useEffect`.

```txt
id change → abort old fetch → fetch new → setData | setError
unmount → abort
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **AbortController** | Cancel in-flight fetch | “Cleanup aborts so stale responses don’t win.” |
| **No async effect** | Effect body stays sync | “Call async inside; return cleanup only.” |
| **Race** | Old response after new id | “Abort or ignore when signal aborted.” |

## Standard config / commands

```tsx
function TestComponent({ id }: { id: string }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const c = new AbortController()
    ;(async () => {
      try {
        const res = await fetch(`/api/data/${id}`, { signal: c.signal })
        if (!res.ok) throw new Error('Failed to fetch')
        setData(await res.json())
        setError(null)
      } catch (e: any) {
        if (e.name !== 'AbortError') setError(e.message)
      }
    })()
    return () => c.abort()
  }, [id])

  if (error) return <div>Error: {error}</div>
  if (!data) return <div>Loading...</div>
  return <div>{JSON.stringify(data)}</div>
}
```

| Knob | Why it matters |
|------|----------------|
| `signal` | Ties fetch to effect lifetime |
| `res.ok` check | HTTP 4xx/5xx aren’t thrown by `fetch` |
| Fallback `onError` on `<img>` | Swap broken src without crashing |

```tsx
<img src={url} onError={(e) => { e.currentTarget.src = fallback }} />
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong data after fast id change | No abort | AbortController in cleanup |
| Unhandled rejection | Async effect returned | IIFE + try/catch inside effect |
| Blank forever on 404 | Only network catch | Throw when `!res.ok` |
| Broken image | Missing `onError` | Set fallback src |

---

## Gotchas

> [!WARNING]
> **Don’t make the effect callback `async`** — React ignores the returned Promise; cleanup must be a sync function.

> [!WARNING]
> **Strict Mode double-mount** — cleanup must abort; effects should be idempotent.

---

## When NOT to use

- **Production data layer** — prefer [[react-query]] / [[Redux/Redux createApi]] over hand-rolled fetch in every interview-style component.

---

## Related

[[Hooks/react useEffect]] [[react hooks]] [[react-query]] [[react error]]
