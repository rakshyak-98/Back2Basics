[[vercel cli]] [[vercel deployment]] [[Netlify/Netlify deployment]]

# Render CLI

> Terminal client for Render — authenticate to a workspace, then trigger deploys, stream logs, and inspect services already wired to Git or an image.

```txt
        Render CLI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast Render’s “deploy an existing service” model with Vercel…

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

- CI: set `RENDER_API_KEY`, pass service id, use `--confirm` and `-o json` as n…

## Mistakes to Avoid
- **Mistake:** Expecting `render` to create a brand-new app from a random folde…
- **Mistake:** Skipping `--wait` in CI and marking green before the deploy fini…
- **Mistake:** Committing API keys into the repository

## Pros/Cons or Trade-offs
- **Pro:** Simple promote/restart story for long-running web/worker services.
- **Con:** Not a “push this folder” CDN workflow like pure static hosts.

## Comparison
- vs [[vercel cli]]: Vercel optimizes preview static/serverless apps
- vs dashboard-only: CLI makes wait-on-deploy scripting reliable.


### Use cases
- Pipeline builds an image, then `render deploys create … --image … --wait` to …

- **Example:** Interactive menus fail in CI
