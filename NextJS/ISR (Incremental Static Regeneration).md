[[Next JS]] [[NextJS Deployment]] [[NextJS navigation]] [[vercel deployment]] [[vercel cli]]

# ISR (Incremental Static Regeneration)

> Incremental Static Regeneration regenerates static pages on a timer or on demand after deploy — users get a stale page immediately while a fresh one builds in the background.

```txt
        ISR (Incremental S ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use ISR to test whether you can explain stale-while-revalidate v…

## Sources
- [Next.js Docs — Incremental Static Regeneration](https://nextjs.org/docs/app/guides/incremental-static-regeneration) — deep-dive
- [Next.js Docs — `revalidatePath`](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) — overview
- [Next.js Blog — ISR](https://nextjs.org/blog/next-9-5#stable-incremental-static-regeneration) — overview

## Key Concepts
- **Time-based revalidate:** `revalidate: N` (Pages) or `export const revalidate = N` / `fetch(..., { next…
- **On-demand:** `revalidatePath` / `revalidateTag` (or Pages `res.revalidate`) → CMS webhooks…
- **Stale-while-revalidate:** first request after expiry still gets the old page → document editorial fresh…
- **Runtime requirement:** Node.js server (default) — not supported with static export.
- **Self-host multi-instance:** default filesystem cache is per process → use a shared `cacheHandler`.


- **Core:** ISR keeps CDN/filesystem-cached HTML for a route, then regenerates that page …

## Technical Details
```txt
Request → CDN/static (stale OK) → optional background regen → update cache
```

### Pages Router

```js
export async function getStaticProps() {
  const data = await fetchCMS()
  return {
    props: { data },
    revalidate: 60, // at most every 60s after stale
  }
}
```

### App Router

```ts
export const revalidate = 60

export default async function Page() {
  const data = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 },
  }).then((r) => r.json())
  return <div>{data.title}</div>
}
```

### On-demand revalidation

```ts
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'

export async function POST(req: Request) {
  const secret = req.headers.get('x-revalidate-secret')
  if (secret !== process.env.REVALIDATE_SECRET) {
    return new Response('Unauthorized', { status: 401 })
  }
  revalidatePath('/blog/[slug]')
  return Response.json({ revalidated: true })
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Content never updates | `revalidate` set? | Add interval or on-demand hook |
| Users see old data long | CDN TTL vs revalidate | Align edge cache; purge CDN |
| Build OK, production stale | Hosting ISR support | Need Node; not `output: 'export'` |
| 401 on revalidate | Secret mismatch | Match header and environment variable |
| Split views across pods | Local cache only | Shared `cacheHandler` |

## Mistakes to Avoid
- **Mistake:** Expecting ISR with `output: 'export'`
- **Mistake:** ISR-caching personalized pages (cart, account)
- **Mistake:** Promising “always fresh” without stating the stale window to edi…

## Pros/Cons or Trade-offs
- **Pro:** Near-static performance with post-deploy updates — no full rebuild for every edit.
- **Con:** Readers can see stale content until regeneration finishes.
- **Con:** Incorrect for per-user or real-time data; needs shared cache when scaled out.

## Comparison
- vs pure SSG: SSG needs a full rebuild (or redeploy) for content changes
- vs SSR: SSR is fresh every request but costs latency and origin load.
- vs [[NextJS Deployment]] static export: export has no server to revalidate.


### Use cases
- Marketing blogs and product catalogs regenerate from a CMS on a webhook while…

- **Example:** Editors publish in Contentful → webhook hits `/api/revalidate` →…
