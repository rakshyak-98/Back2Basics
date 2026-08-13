<!-- note-strategy: operational -->
[[React]] [[React Pattern/Higher order Component (HOCs)]] [[react-query]]

# Data Fetching HOC component

> Wrap a presentational list with fetch/loading/error — HOC owns the request; child gets `data`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `withDataFetching(Comp, url)` returns a component that fetches, then renders `Comp` with `data` — or loading/error UI.

```txt
HOC mounts → fetch(url) → loading | error | <Wrapped data={…} />
unmount → ignore / abort
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **HOC** | Function → enhanced component | “Compose behavior without editing child.” |
| **Mounted flag / abort** | Stop setState after unmount | “Cleanup prevents warnings/races.” |
| **Injected props** | `data`, `error`, `refetch` | “Child stays presentational.” |

## Standard config / commands

```tsx
function withDataFetching<P>(Wrapped: React.ComponentType<P & { data: unknown }>, url: string) {
  return function WithData(props: P) {
    const [data, setData] = useState(null)
    const [error, setError] = useState<Error | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
      const c = new AbortController()
      setLoading(true)
      fetch(url, { signal: c.signal })
        .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json() })
        .then(setData)
        .catch((e) => { if (e.name !== 'AbortError') setError(e) })
        .finally(() => setLoading(false))
      return () => c.abort()
    }, [url])

    if (loading) return <div>Loading...</div>
    if (error) return <div>Error: {error.message}</div>
    return <Wrapped {...props} data={data} />
  }
}

export default withDataFetching(UserList, '/api/users')
```

| Knob | Why it matters |
|------|----------------|
| `url` dep | Refetch when endpoint changes |
| Abort cleanup | Race-safe |
| Loading/Error slots | Swap UI without touching child |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrapper hell / prop collisions | Nested HOCs | Prefer hooks / [[react-query]] |
| Stale data on nav | No abort | AbortController |
| `JSON.stringify` in deps | Unstable objects | Stabilize config or use hook |
| Child ignores loading | Assumes data always set | Keep gate in HOC |

---

## Gotchas

> [!WARNING]
> **HOCs obscure the tree in DevTools** — name the inner function (`WithDataFetching`).

> [!WARNING]
> **Static config HOCs don’t get props-driven URLs cleanly** — hooks usually win.

---

## When NOT to use

- **New code** — custom hook or [[react-query]] instead of fetch HOCs.
- **authentication/logging cross-cuts** — still OK for true cross-cutting; not for every GET.

---

## Related

[[React Pattern/Higher order Component (HOCs)]] [[React Pattern/data fetching component]] [[react-query]] [[Hooks/react useEffect]]
