[[NextJS/NextJS navigation]] [[Deployment/vercel cli]] [[css/tailwindcss]]

# ISR (Incremental Static Regeneration)

> Regenerate static pages on a timer or on-demand without full site rebuild — Next.js stale-while-revalidate for CDN-backed pages.

## Mental model

At build time, page is static HTML. After deploy, first request (or revalidate interval) can trigger **background regeneration**. Users get **stale** page immediately while fresh version builds — then CDN serves new static file. Distinct from SSR (every request) and pure SSG (rebuild all).

```
Request → CDN static (stale OK) → optional background regen → update CDN cache
```

## Standard config / commands

### Pages Router

```js
export async function getStaticProps() {
  const data = await fetchCMS();
  return {
    props: { data },
    revalidate: 60,   // regen at most every 60s on next request after stale
  };
}
```

### App Router

```ts
export const revalidate = 60;

export default async function Page() {
  const data = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 },
  }).then(r => r.json());
  return <div>{data.title}</div>;
}
```

### On-demand revalidation

```ts
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache';

export async function POST(req: Request) {
  const secret = req.headers.get('x-revalidate-secret');
  if (secret !== process.env.REVALIDATE_SECRET) return new Response('Unauthorized', { status: 401 });
  revalidatePath('/blog/[slug]');
  return Response.json({ revalidated: true });
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Content never updates | `revalidate` set? | Add interval or on-demand hook |
| Users see old data long | CDN TTL > revalidate | Align edge cache; purge CDN |
| Build OK, prod stale | Hosting ISR support | Vercel/Netlify plugin; not plain static export |
| 401 on revalidate | Secret mismatch | Match header + env |
| Thundering herd regen | Traffic spike on stale | Increase `revalidate`; use on-demand only |

## Gotchas

> [!WARNING]
> **`output: 'export'` disables ISR** — pure static export has no server to revalidate.
>
> **Stale content is a feature** — document SLA ("up to 60s old") for editors.
>
> **Personalized pages** — don't ISR user-specific data; use SSR or client fetch.

## When NOT to use

- Don't ISR real-time dashboards (stock tickers, live scores) — use SSR/WebSocket.
- Don't ISR pages that must be legally exact at every view (some pricing) without short revalidate + purge.

## Related

[[NextJS/NextJS navigation]] [[Deployment/vercel cli]] [[Netlify/Netlify deployment]] [[Deployment/vercel deployment]]
