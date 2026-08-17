[[react hooks]] [[React State management]] [[React Architecture]]

# Hydration

> Client React attaches listeners to server-rendered HTML — mismatch between server and client markup breaks the page.





## Interview Relevance
Interviewers want the SSR → hydrate story and classic mismatch causes (`Date.now()`, `window`, locale).

## Sources
- [hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot) — deep-dive
- [Hydrating HTML](https://react.dev/reference/react-dom/client/hydrateRoot#hydrating-server-rendered-html) — overview

## Core Definition
Hydration reuses server HTML and binds React event system; server and first client render must produce the same tree.

## Key Concepts
- **Same tree:** server HTML must match client’s first render.
- **Browser-only values:** gate with `useEffect` or client components.
- **suppressHydrationWarning:** rare escape hatch for known text diffs (e.g. timestamps).

## Technical Details
```tsx
// Bad: server time ≠ client time
<span>{new Date().toLocaleString()}</span>
// Better: render placeholder, fill after mount
const [now, setNow] = useState<string | null>(null)
useEffect(() => setNow(new Date().toLocaleString()), [])
```

## Real-World Applications
Next.js app shows a hydration warning because a theme class from `localStorage` differs from server default — fix with client-only theme gate.

## Pros/Cons or Trade-offs
- **Pro:** Fast first paint from SSR HTML.
- **Con:** Strict matching rules; mismatches are costly to debug.

## Comparison
- vs CSR-only: no hydration step; slower first contentful paint for content-heavy pages.

## Mistakes to Avoid
- Reading `window` / `localStorage` during render on the server path.
- Random IDs without `useId`.
