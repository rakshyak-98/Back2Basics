[[vercel cli]] [[vercel deployment]] [[Netlify/Netlify deployment]]

# Render CLI

> Terminal client for Render — authenticate to a workspace, then trigger deploys, stream logs, and inspect services already wired to Git or an image.





## Interview Relevance
Interviewers contrast Render’s “deploy an existing service” model with Vercel’s directory deploy, plus CI flags (`--wait`, `--confirm`, API keys).

## Sources
- [Render — CLI](https://render.com/docs/cli) — deep-dive
- [Render — Deploying](https://render.com/docs/deploys) — overview

## Key Concepts
- **Service-centric:** `srv-…` already knows repo/image; CLI triggers a deploy.
- **Workspace auth:** interactive login or `RENDER_API_KEY` for CI.
- **`--wait`:** block until deploy finishes; non-zero on failure.
- **Config path:** `$HOME/.render/cli.yaml` (overridable).

## Technical Details
```bash
render login
render workspace set
render services
render deploys create srv-abc123 --wait --confirm
render deploys create srv-abc123 --commit <sha> --wait --confirm
render deploys create srv-abc123 --clear-cache --wait --confirm
render deploys list srv-abc123
```

CI: set `RENDER_API_KEY`, pass service id, use `--confirm` and `-o json` as needed.

## Real-World Applications
Pipeline builds an image, then `render deploys create … --image … --wait` to roll a background worker.

**Example:** Interactive menus fail in CI — switch to API key + explicit service id + `--confirm`.

## Pros/Cons or Trade-offs
- **Pro:** Simple promote/restart story for long-running web/worker services.
- **Con:** Not a “push this folder” CDN workflow like pure static hosts.

## Comparison
- vs [[vercel cli]]: Vercel optimizes preview static/serverless apps; Render CLI operates blueprints/services.
- vs dashboard-only: CLI makes wait-on-deploy scripting reliable.

## Mistakes to Avoid
- Expecting `render` to create a brand-new app from a random folder without a service.
- Skipping `--wait` in CI and marking green before the deploy finishes.
- Committing API keys into the repository.
