[[Next JS]] [[NextJS Config]] [[Next js Build]] [[ISR (Incremental Static Regeneration)]] [[vercel deployment]]

# NextJS Deployment

> Deploying Next.js means serving the production build — static HTML where possible, plus a Node (or platform) server for SSR, API routes, and ISR.





## Interview Relevance
Interviewers ask how you deploy Next.js to see if you know it is not a plain Create React App static `index.html`, when static export is enough, and what `standalone` and ISR need on self-hosted platforms.

## Sources
- [Next.js Docs — Deploying](https://nextjs.org/docs/app/getting-started/deploying) — overview
- [Next.js Docs — Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports) — deep-dive
- [Next.js Docs — Self-Hosting](https://nextjs.org/docs/app/guides/self-hosting) — deep-dive

## Core Definition
A production deploy runs `next build`, then either hosts static files (`output: 'export'`), runs `next start` / standalone `server.js`, or uses a platform adapter (for example Vercel) that understands SSR and cache revalidation.

## Recall Cues
- Why do interviewers care about how you deploy Next.js to see if you know it is not a plain Create React App static `index.html`, when static export is enough, and what `standalone` and ISR need on self-hosted platforms?
- What mistake is **Deploying like CRA and expecting SSR/ISR to work on a static bucket**?
- What mistake is **Forgetting to copy `public` and `.next/static` next to standalone `server.js`**?
- What mistake is **Running multiple instances with ISR and a local-only cache — users see split-brain content**?

## Technical Details
Typical `next build` log meaning:

```txt
✓ Collecting page data
```

Runs data functions / fetch for routes that need it.

```txt
✓ Generating static pages (5/5)
```

Writes static HTML (+ JSON for hydration) for prerendered routes.

```txt
✓ Collecting build traces
```

Records which files each route needs — used by `standalone` and platforms to slim the deploy.

```txt
✓ Finalizing page optimization
```

Tree-shaking, minification, chunking of JS/CSS.

```bash
npm run build
npm run start                    # Node server
# or with standalone:
node .next/standalone/server.js  # after copying public + .next/static
```

| Mode | Host needs | Loses |
|------|------------|-------|
| Static export | Any CDN / object storage | SSR, ISR, many dynamic APIs |
| `next start` | Node process | Extra packaging work |
| Standalone | Node + copied static dirs | Still need shared cache for multi-instance ISR |
| Platform (Vercel, etc.) | Platform adapter | Vendor-specific ops model |

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank or 404 assets | `basePath` / missing `.next/static` | Align [[NextJS Config]]; copy static into standalone |
| ISR never updates | Host / export mode | Need Node runtime; not static export |
| Multi-pod stale pages | Per-instance filesystem cache | Shared `cacheHandler` (Redis, etc.) |
| Works in `next dev` only | Build-time environment | Provide CI environment; run [[Next js Build]] locally |

## Mistakes to Avoid
- Deploying like CRA and expecting SSR/ISR to work on a static bucket.
- Forgetting to copy `public` and `.next/static` next to standalone `server.js`.
- Running multiple instances with ISR and a local-only cache — users see split-brain content.

## Comparison
- vs [[React]] SPA deploy: SPA is static assets only; Next.js often needs a server process.
- vs [[ISR (Incremental Static Regeneration)]]: ISR is a caching mode that only works when the deploy supports revalidation.

## Real-World Applications
Marketing sites often use static export or CDN-backed static pages; SaaS apps run Node/standalone behind a load balancer; content sites use ISR on Vercel or self-hosted Node with a persistent cache disk.

**Example:** Docker sets `HOSTNAME=0.0.0.0`, `output: 'standalone'`, copies `public/` and `.next/static/`, and health-checks `/`.

## Pros/Cons or Trade-offs
- **Pro:** Same codebase can be mostly static at the edge with selective server routes.
- **Con:** Feature set dictates hosting — static hosts cannot run ISR or Server Actions.
- **Con:** Self-hosting ISR across replicas needs shared cache design.
