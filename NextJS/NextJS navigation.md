[[ISR (Incremental Static Regeneration)]] [[React/React data management]] [[javascript/user triggered event]]

# Next.js navigation

> Client-side routing in the App/Pages router — when to use `Link`, `router`, or a real new tab.

## Mental model

Next.js intercepts in-app navigation to avoid full page reloads. **App Router** uses `next/navigation` (`useRouter`, `redirect`, `Link`). **Pages Router** uses `next/router`. Opening a new browser tab/window is **not** SPA navigation — use `<a target="_blank">` or `window.open`, not `router.push`.

```
Same tab in-app  → <Link href="..."> or router.push('/path')
New tab          → <a href="..." target="_blank" rel="noopener noreferrer">
Full reload      → window.location.href = '...'  (rare)
```

## Standard config / commands

### App Router

```tsx
'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export function Nav() {
  const router = useRouter();
  return (
    <>
      <Link href="/dashboard">Dashboard</Link>
      <button onClick={() => router.push('/settings')}>Settings</button>
      <a href="/docs" target="_blank" rel="noopener noreferrer">Docs (new tab)</a>
    </>
  );
}
```

### Server redirect

```ts
import { redirect } from 'next/navigation';

export default async function Page() {
  const session = await getSession();
  if (!session) redirect('/login');
}
```

### Pages Router (legacy)

```tsx
import { useRouter } from 'next/router';
const router = useRouter();
router.push('/about');
// router.push(url, '_blank') — NOT supported; use <a target="_blank">
```

### Prefetch control

```tsx
<Link href="/heavy" prefetch={false}>Lazy route</Link>
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `router.push` doesn't open tab | API design | Use `<a target="_blank">` |
| State lost on navigate | Full remount | Lift state to URL/searchParams or store |
| Back button weird | Shallow routing misuse | App Router: use `router.replace` intentionally |
| 404 on client nav | Missing route file | Check `app/` segment or `pages/` file |
| Scroll jumps | Default scroll restore | `scroll={false}` on Link if needed |

## Gotchas

> [!WARNING]
> **`router.push` after async** — component may unmount; check mounted or use transition API.
>
> **External URLs in `Link`** — must use plain `<a>`.
>
> **Middleware redirect loops** — login ↔ home; test cookie/session in middleware.

## When NOT to use

- Don't `router.push` for file downloads — use `<a download>` or signed URL.
- Don't client-nav to logout that must clear httpOnly cookies — use server route/form POST.

## Related

[[ISR (Incremental Static Regeneration)]] [[React/React data management]] [[Security/CORS (Cross Origin Request Sharing)]]
