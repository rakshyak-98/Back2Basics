[[Next JS]] [[ISR (Incremental Static Regeneration)]] [[React data management]] [[hydration]]

# Next.js navigation

> Next.js intercepts in-app navigations so the browser does not full-reload — App Router uses `next/navigation`; Pages Router uses `next/router`.

```txt
        Next.js navigation ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers check whether you know App Router versus Pages Router navigation…

## Sources
- [Next.js Docs — Linking and Navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating) — deep-dive
- [Next.js Docs — `useRouter` (App)](https://nextjs.org/docs/app/api-reference/functions/use-router) — overview
- [Next.js Docs — `next/link`](https://nextjs.org/docs/app/api-reference/components/link) — overview

## Key Concepts
- **App Router:** `next/link`, `useRouter` / `redirect` from `next/navigation` → works with Ser…
- **Pages Router:** `next/router` → different API; do not import it under `app/`.
- **`<Link>` prefetch:** warms the next route → turn off for heavy rarely visited pages.
- **New tab / download:** use `<a>` — `router.push` cannot open a tab.
- **Scroll and history:** default scroll restore; `replace` vs `push` changes back-button behavior.


- **Core:** Client-side navigation swaps route segments and fetches RSC/page payloads whi…

## Technical Details
```txt
Same tab in-app  → <Link href="..."> or router.push('/path')
New tab          → <a href="..." target="_blank" rel="noopener noreferrer">
Full reload      → window.location.href = '...'  (rare)
```

### App Router

```tsx
'use client'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function Nav() {
  const router = useRouter()
  return (
    <>
      <Link href="/dashboard">Dashboard</Link>
      <button onClick={() => router.push('/settings')}>Settings</button>
      <a href="/docs" target="_blank" rel="noopener noreferrer">
        Docs (new tab)
      </a>
    </>
  )
}
```

### Server redirect

```ts
import { redirect } from 'next/navigation'

export default async function Page() {
  const session = await getSession()
  if (!session) redirect('/login')
}
```

### Pages Router (legacy)

```tsx
import { useRouter } from 'next/router'
const router = useRouter()
router.push('/about')
// router.push(url, '_blank') — not supported; use <a target="_blank">
```

### Prefetch control

```tsx
<Link href="/heavy" prefetch={false}>
  Lazy route
</Link>
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `router.push` does not open a tab | API design | Use `<a target="_blank">` |
| State lost on navigate | Full remount | Lift state to URL/`searchParams` or a store |
| Odd back button | Accidental `replace` | Use `push` vs `replace` intentionally |
| 404 on client nav | Missing route file | Check `app/` segment or `pages/` file |
| Scroll jumps | Default scroll restore | `scroll={false}` on `Link` if needed |

## Mistakes to Avoid
- **Mistake:** Using `next/router` inside `app/`
- **Mistake:** Putting external URLs in `<Link>` — use `<a>` for other origins
- **Mistake:** Calling `router.push` after async work without checking the comp…
- **Mistake:** Client-navigating to logout that must clear httpOnly cookies

## Pros/Cons or Trade-offs
- **Pro:** Fast in-app transitions and shared layouts without full reloads.
- **Con:** Two router APIs (App vs Pages) confuse migrations.
- **Con:** Prefetch can waste bandwidth on low-traffic heavy routes.

## Comparison
- vs full page load: keeps client state and shared layout
- vs [[React data management]]: navigation often should encode filter/state in the URL so refresh a…


### Use cases
- Dashboards use `<Link>` for sidebar routes

- **Example:** Middleware that redirects unauthenticated users to `/login` must…
