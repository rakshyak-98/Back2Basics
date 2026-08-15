[[vercel deployment]] [[render cli]] [[Netlify/Netlify deployment]]

# Vercel CLI

> Terminal client for Vercel — link a project, pull environment variables, preview-deploy, and promote to production.

## Interview Relevance

Interviewers want preview vs `--prod`, how linking works (`.vercel/`), and CI-friendly non-interactive deploys.

## Sources

- [Vercel CLI reference](https://vercel.com/docs/cli) — deep-dive
- [Vercel — Deploying](https://vercel.com/docs/deployments/overview) — overview

## Key Concepts

- **Preview deploy:** default `vercel` → unique URL per deployment.
- **Production:** `vercel --prod` → production aliases/domains.
- **Link:** `.vercel/project.json` associates the directory with a project.
- **Remote build:** platform builds unless you use local `vercel build` flows.

## Technical Details

```bash
npm i -g vercel
vercel login
vercel link
vercel env pull .env.local
vercel                 # preview
vercel --prod --yes    # CI / non-interactive production
vercel logs <url>
```

```json
{
  "buildCommand": "next build",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

## Real-World Applications

Open a PR preview URL from CLI during incidents when Git integration is slow; promote with `--prod` after checks pass.

**Example:** CI uses `vercel --prod --yes` with a token — never embed personal interactive login in pipelines.

## Pros/Cons or Trade-offs

- **Pro:** Fast previews; same platform as Git deploys.
- **Con:** Easy to ship to the wrong project if `link` is wrong.

## Comparison

- vs [[vercel deployment]]: CLI is the operator interface; deployment note covers CDN/serverless behavior.
- vs [[render cli]]: Vercel often “upload/build this directory”; Render CLI usually triggers an existing Git-wired service.

## Mistakes to Avoid

- Committing `.vercel` with the wrong org/project to a shared repo without care.
- Putting secrets in `NEXT_PUBLIC_*` via `env pull` mistakes.
- Using interactive prompts in CI without `--yes` / tokens.
