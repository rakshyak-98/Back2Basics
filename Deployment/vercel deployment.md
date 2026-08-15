[[vercel cli]] [[Netlify/Netlify deployment]] [[CORS (Cross Origin Request Sharing)]] [[NextJS/ISR (Incremental Static Regeneration)]]

# Vercel deployment

> Git or CLI builds land on a global CDN for static assets plus serverless functions for APIs/SSR — no long-lived Node server by default.

## Interview Relevance

Interviewers ask SPA refresh 404s (rewrites), preview vs production env vars, cold starts/timeouts, and what must never be `NEXT_PUBLIC_`.

## Sources

- [Vercel — Project configuration](https://vercel.com/docs/project-configuration) — deep-dive
- [Vercel — Environment variables](https://vercel.com/docs/projects/environment-variables) — overview

## Key Concepts

- **Static + functions:** HTML/JS/CSS on CDN; `/api` and SSR as serverless.
- **Filesystem routing (Next.js):** prefer framework conventions over catch-all hacks.
- **SPA fallback:** Vite/CRA need rewrite to `index.html` for deep links.
- **Env scopes:** Production / Preview / Development separated.

## Technical Details

```
Git push ──► build ──► static (CDN) + lambdas (region)
```

SPA `vercel.json`:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

| Scope | Use |
|-------|-----|
| `NEXT_PUBLIC_*` | Browser-visible — never secrets |
| Server-only | DB URLs, private API keys |
| Preview vs Production | Different backends/secrets per stage |

Custom domains: dashboard DNS instructions; TLS via platform certificates.

## Real-World Applications

Next.js app: framework preset auto-detected; protect server routes; watch plan timeouts (often tens of seconds) for slow backends.

**Example:** Vite app refresh on `/settings` 404s — add SPA rewrite, or switch to Next-style routing.

## Pros/Cons or Trade-offs

- **Pro:** Excellent DX for frontends and preview URLs.
- **Con:** Long-running/websocket workloads need a different host model.

## Comparison

- vs [[Netlify/Netlify deployment]]: similar Jamstack shape; different function/CDN knobs.
- vs always-on VM/K8s: Vercel is request-scoped compute for the dynamic parts.

## Mistakes to Avoid

- Catch-all rewrites on Next.js app router “just in case.”
- Secrets in `NEXT_PUBLIC_*`.
- Assuming function timeouts match a home-server Node process.
