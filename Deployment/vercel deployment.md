[[vercel cli]] [[Netlify/Netlify deployment]] [[CORS (Cross Origin Request Sharing)]] [[NextJS/ISR (Incremental Static Regeneration)]]

# Vercel deployment

> Git or CLI builds land on a global CDN for static assets plus serverless functions for APIs/SSR — no long-lived Node server by default.

```txt
        Vercel deployment ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask SPA refresh 404s (rewrites), preview vs production env vars,…

## Sources
- [Vercel — Project configuration](https://vercel.com/docs/project-configuration) — deep-dive
- [Vercel — Environment variables](https://vercel.com/docs/projects/environment-variables) — overview

## Technical Details
```
Git push ──► build ──► static (CDN) + lambdas (region)
```

- SPA `vercel.json`:

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

- Custom domains: dashboard DNS instructions; TLS via platform certificates.

## Mistakes to Avoid
- **Mistake:** Catch-all rewrites on Next.js app router “just in case.”
- **Mistake:** Secrets in `NEXT_PUBLIC_*`
- **Mistake:** Assuming function timeouts match a home-server Node process

## Pros/Cons or Trade-offs
- **Pro:** Excellent DX for frontends and preview URLs.
- **Con:** Long-running/websocket workloads need a different host model.

## Comparison
- vs [[Netlify/Netlify deployment]]: similar Jamstack shape; different function/CDN knobs.
- vs always-on VM/K8s: Vercel is request-scoped compute for the dynamic parts.


### Use cases
- Next.js app: framework preset auto-detected

- **Example:** Vite app refresh on `/settings` 404s
