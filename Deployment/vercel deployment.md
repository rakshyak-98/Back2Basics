[[nginx SPA deployment]] [[React]] [[CORS (Cross Origin Request Sharing)]] [[Deployment]]

# Vercel deployment

> **Git-push serverless hosting** for Next.js/static SPAs — edge CDN, serverless functions, env vars per environment. **Vercel docs** + classic SPA refresh 404 and env mismatch debug.

## Mental model

Vercel builds from Git (or CLI `vercel deploy`) → **static assets** on global CDN + **serverless functions** (`/api/*`, Next.js routes). Routing is **filesystem-based** (Next) or **`vercel.json` rewrites** (CRA/Vite SPA). No long-lived server — cold starts and regional execution matter for APIs.

```
Git push ──► build ──► static (CDN) + lambdas (region)
                           │
User refresh /deep link ──► must rewrite to index or SSR route
```

## Standard config / commands

### SPA fallback (Vite/CRA — fix refresh 404)

`vercel.json` at repo root:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

Next.js App Router: file-based routing — **no catch-all rewrite** unless custom static export.

### Next.js (recommended path)

- Framework preset auto-detected; `next build` output.
- **Server Components / API routes** run as serverless — watch **10s/60s timeout** (plan-dependent) and **body size limits**.

### Environment variables

| Scope | Use |
|-------|-----|
| Production / Preview / Development | Separate secrets per branch deploy |
| `NEXT_PUBLIC_*` | Exposed to browser — never secrets |
| Server-only | DB URLs, API keys in non-public vars |

```bash
vercel env pull .env.local
vercel --prod
vercel logs <deployment-url>
```

### Custom domain + HTTPS

- Project → Domains → add apex + `www`.
- DNS: CNAME to `cname.vercel-dns.com` or A to Vercel anycast (dashboard shows exact records).
- TLS automatic via Let's Encrypt.

### Monorepo

```json
{
  "buildCommand": "cd apps/web && npm run build",
  "outputDirectory": "apps/web/dist",
  "installCommand": "npm ci"
}
```
Or set **Root Directory** in project settings.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Refresh on `/dashboard` → 404 | Missing SPA rewrite | Add `vercel.json` rewrites to `/index.html` |
| Works locally, env undefined in prod | Var not set for Production | Dashboard env; rebuild after add |
| API 500 only on Vercel | Function timeout; edge vs node runtime | Increase timeout; `export const runtime = 'nodejs'` |
| CORS from browser to `/api` on same domain | Usually same-origin — if split domain | Configure API CORS or proxy ([[CORS (Cross Origin Request Sharing)]]) |
| Stale assets after deploy | CDN cache; service worker | Cache bust filenames; update SW |
| Build OOM | Large deps | Reduce bundle; `NODE_OPTIONS=--max-old-space-size` |
| Preview URL works, prod domain not | DNS not verified | Fix CNAME; wait propagation |

```bash
vercel inspect <url> --logs
curl -I https://your-app.vercel.app/deep/route
```

## Gotchas

> [!WARNING]
> **Catch-all rewrite breaks real static files** if ordered wrong — Vercel serves existing files first; rewrite applies to non-matches (usually OK).

> [!WARNING]
> **`NEXT_PUBLIC_` leaks secrets** — anything prefixed is in client bundle.

> [!WARNING]
> **Serverless cold start** — first request slow; not for long WebSocket sessions without dedicated solution.

> [!WARNING]
> **Regional functions + global DB** — latency; co-locate or use edge-compatible data (Planetscale/Vercel Postgres region hints).

## When NOT to use

- **Long-running workers / queues** — use Railway/Fly/ECS/K8s ([[Deployment]]).
- **Stateful TCP services** — Vercel is HTTP-centric.
- **Full control of nginx tuning** — compare [[nginx SPA deployment]] on own VM.

## Related

[[nginx SPA deployment]] · [[React]] · [[CORS (Cross Origin Request Sharing)]] · [[Deployment]] · [[Release cycle]]
