[[Deployment/vercel deployment]] [[NextJS/ISR (Incremental Static Regeneration)]] [[Netlify/Netlify deployment]]

# Vercel CLI

> Link local project, preview deploy, and promote to production without leaving the terminal.

## Mental model

`vercel` CLI talks to Vercel platform: creates preview URL per deploy, production on `--prod`. Project linked via `.vercel/project.json` after `vercel link`. Builds run remotely (default) or locally (`vercel dev`). Env vars pulled from dashboard or `vercel env pull`.

```
local repo → vercel → remote build → *.vercel.app preview → --prod → custom domain
```

## Standard config / commands

### Install and auth

```bash
npm i -g vercel
vercel login
```

### Link and dev

```bash
vercel link              # associate or create project
vercel env pull .env.local
vercel dev               # local dev with Vercel routing/functions
```

### Deploy

```bash
vercel                   # preview deploy (interactive)
vercel --prod            # production
vercel --prod --yes      # CI non-interactive
```

### vercel.json (Next.js often optional)

```json
{
  "buildCommand": "next build",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

### Inspect

```bash
vercel ls
vercel inspect <url>
vercel logs <deployment-url>
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong project linked | `.vercel/project.json` | `vercel link` again |
| Env missing in build | Dashboard vs preview/prod | `vercel env pull`; scope vars |
| `vercel dev` ≠ prod | Edge vs Node runtime | Test preview deploy |
| Build OOM | Build logs | Increase memory tier; optimize build |
| Typo `varcel dev` | — | `vercel dev` |
| 404 on API routes | Output config | Don't `output: 'export'` if using API routes |

## Gotchas

> [!WARNING]
> **Preview URLs are public** — don't deploy secrets in client bundle assuming privacy.
>
> **Git integration vs CLI** — two deploy paths; know which owns production branch.
>
> **Monorepo** — set Root Directory in project settings.

## When NOT to use

- Don't use CLI prod deploy without CI checks — wire Git integration + required checks.
- Don't commit `.vercel` with tokens — only project ids; secrets stay in dashboard.

## Related

[[Deployment/vercel deployment]] [[NextJS/ISR (Incremental Static Regeneration)]] [[Netlify/Netlify deployment]]
