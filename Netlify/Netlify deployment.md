[[Deployment/vercel cli]] [[NextJS/ISR (Incremental Static Regeneration)]] [[Nginx/nginx SPA deployment]]

# Netlify deployment

> Git-connected or CLI deploy with `netlify.toml` — build command, publish dir, and Next.js plugin for SSR/ISR.

## Mental model

Netlify runs your **build command**, publishes **publish directory** to CDN, and optionally runs **serverless functions** at the edge. Next.js needs `@netlify/plugin-nextjs` for App Router features (not plain static export). Env vars live in Netlify UI per context (production/deploy-preview).

```
git push → Netlify build → plugin adapts Next → CDN + functions
```

## Standard config / commands

### netlify.toml (Next.js)

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"

[build.environment]
  NODE_VERSION = "20"
```

### CLI flow

```bash
npm i -g netlify-cli
netlify login
netlify init          # link site
netlify env:list
netlify deploy        # draft URL
netlify deploy --prod
```

### Redirects / headers (static)

```toml
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on dynamic routes | Plugin missing | Add `@netlify/plugin-nextjs` |
| Build works locally, fails CI | Node version | Pin `NODE_VERSION` in toml |
| Env var undefined | Context scope | Set for Production + Preview |
| Wrong publish dir | Empty site | Next: don't set publish to `out` unless static export |
| ISR not updating | Netlify cache | On-demand revalidation; check Next cache config |
| Function timeout | 10s default (tier) | Optimize API route or upgrade |

## Gotchas

> [!WARNING]
> **Confusing `publish = ".next"`** — plugin handles output; follow Netlify Next docs for your version.
>
> **Large function bundles** — tree-shake; externalize heavy deps.
>
> **Monorepo** — set **Base directory** in UI to app package.

## When NOT to use

- Don't use Netlify static hosting alone for heavy WebSocket/long-polling backends — dedicated server or specialized host.
- Don't commit `.env` — use Netlify env UI or secrets.

## Related

[[Deployment/vercel cli]] [[Deployment/vercel deployment]] [[NextJS/ISR (Incremental Static Regeneration)]]
