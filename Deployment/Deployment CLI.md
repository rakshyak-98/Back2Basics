[[Vercel CLI]] [[Render CLI]] [[INDEX]]

# Deployment CLI

> Deployment platform CLIs — Vercel and Render.

---

## Vercel

From [[Vercel CLI]].

```bash
npm i -g vercel
vercel login
vercel link
vercel env pull .env.local
vercel                 # preview
vercel --prod --yes    # CI / non-interactive production
vercel logs <url>
```


## Render

From [[Render CLI]].

```bash
render login
render workspace set
render services
render deploys create srv-abc123 --wait --confirm
render deploys create srv-abc123 --commit <sha> --wait --confirm
render deploys create srv-abc123 --clear-cache --wait --confirm
render deploys list srv-abc123
```
