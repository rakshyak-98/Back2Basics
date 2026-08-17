[[react hooks]] [[React State management]] [[React Architecture]]

# Hydration

> Client React attaches listeners to server-rendered HTML — mismatch between server and client markup breaks the page.

```txt
        Hydration ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want the SSR → hydrate story and classic mismatch causes (`Date.…

## Sources
- [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) — deep-dive
- [Hydrating HTML](https://react.dev/reference/react-dom/client/hydrateRoot#hydrating-server-rendered-html) — overview

## Key Concepts
- **Same tree:** server HTML must match client’s first render.
- **Browser-only values:** gate with `useEffect` or client components.
- **suppressHydrationWarning:** rare escape hatch for known text diffs (e.g. timestamps).


- **Core:** Hydration reuses server HTML and binds React event system

## Technical Details
```tsx
// Bad: server time ≠ client time
<span>{new Date().toLocaleString()}</span>
// Better: render placeholder, fill after mount
const [now, setNow] = useState<string | null>(null)
useEffect(() => setNow(new Date().toLocaleString()), [])
```

## Mistakes to Avoid
- **Mistake:** Reading `window` / `localStorage` during render on the server pa…
- **Mistake:** Random IDs without `useId`

## Pros/Cons or Trade-offs
- **Pro:** Fast first paint from SSR HTML.
- **Con:** Strict matching rules; mismatches are costly to debug.

## Comparison
- vs CSR-only: no hydration step; slower first contentful paint for content-heavy pages.


### Use cases
- Next.js app shows a hydration warning because a theme class from `localStorag…
