[[Deployment/vercel cli]] [[Deployment/vercel deployment]] [[Netlify/Netlify deployment]]

# Render CLI

> Render CLI — local terminal → render CLI → Render API → service (build/deploy/logs/ssh)

---

## Mental model

`render` talks to your **active workspace**. Interactive mode (TTY) is menu-driven; scripts/CI use **API key + `--confirm` + `-o json`**. Deploys are **triggers against an existing service** (`srv-…`), not “upload this folder like `vercel`” — Git/image is already wired on the service.

```
local terminal → render CLI → Render API → service (build/deploy/logs/ssh)
CI: RENDER_API_KEY + service ID → deploys create --wait --confirm
```

configuration lives at `$HOME/.render/cli.yaml` (override with `RENDER_CLI_CONFIG_PATH`).

## Standard config / commands

### Install and auth

```bash
# Install / upgrade (Linux)
curl -fsSL https://raw.githubusercontent.com/render-oss/cli/refs/heads/main/bin/install.sh | sh

# Or pin a release binary (CI / reproducible)
curl -L https://github.com/render-oss/cli/releases/download/v1.1.0/cli_1.1.0_linux_amd64.zip -o render.zip
unzip render.zip
sudo mv cli_v1.1.0 /usr/local/bin/render

render login              # browser authorize → CLI token
render workspace set      # pick active workspace
```

CI / automation: set `RENDER_API_KEY` (API key wins over CLI token; does not expire like CLI tokens).

### Deploy

```bash
render services                              # list / pick service
render deploys create                        # interactive: pick service
render deploys create srv-abc123 --wait --confirm
render deploys create srv-abc123 --commit <sha> --wait --confirm
render deploys create srv-abc123 --image registry.io/app:tag --wait --confirm
render deploys create srv-abc123 --clear-cache --wait --confirm
render deploys list srv-abc123
render deploys cancel srv-abc123 dep-xyz789
```

`--wait` blocks and exits non-zero on failed deploy — use in CI. `--confirm` skips prompts.

### Inspect and operate

```bash
render services -o json --confirm
render logs -r srv-abc123 --tail
render ssh srv-abc123
render ssh srv-abc123 --ephemeral            # isolated shell; start cmd not run
render restart srv-abc123 --confirm
render psql pg-abc123
render psql pg-abc123 -c "SELECT NOW();" -o text
render blueprints validate                   # defaults to ./render.yaml
```

### Non-interactive / CI pattern

```bash
export RENDER_API_KEY=rnd_…
export RENDER_OUTPUT=json   # or pass -o json per command
export CI=true

render deploys create "$RENDER_SERVICE_ID" --wait --confirm -o json
```

Pin the CLI binary version in CI (GitHub releases) so upgrades don’t break pipelines.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong services listed | Active workspace | `render workspace set` / `render workspaces` |
| Auth fails in CI | `RENDER_API_KEY` set? | Create API key in dashboard; export before commands |
| CLI token expired | Idle / revoked token | `render login` again; revoke old tokens in Account Settings |
| Deploy “succeeded” but old code | Wrong service / commit | Pass `--commit <sha>`; confirm `srv-…` ID |
| Interactive hang in CI | TTY menus | Always `--confirm` + `-o json` (or `CI=true`) |
| Blueprint apply errors | YAML shape | `render blueprints validate ./render.yaml` |
| Can’t SSH / empty instance | Service not running | Check deploys; use `--ephemeral` for one-off shell |

## Gotchas

> [!WARNING]
> **CLI deploy does not disable auto-deploy** — Git pushes still deploy unless you turn auto-deploy off (dashboard or `services update`).
>
> **`RENDER_API_KEY` overrides CLI login** — local shells with the env var set will ignore `render login` tokens.
>
> **Ephemeral SSH ≠ production process** — `--ephemeral` skips the service start command; don’t debug “why isn’t my app listening” there.
>
> **Pin CLI version in CI** — the install script floats to latest; pin a `linux_amd64` release zip for reproducibility.

## When NOT to use

- Don’t trigger production deploys from a laptop as the only gate — prefer Git + required checks, or CI calling `deploys create --wait`.
- Don’t use the CLI as a substitute for IaC ownership of the whole stack — use Blueprints (`render.yaml`) for multi-service layout; CLI for day-2 operations.
- Don’t put API keys in the repository — secrets manager / CI secrets only.

## Related

[[Deployment/vercel cli]] [[Deployment/vercel deployment]] [[Netlify/Netlify deployment]] [[Terraform CLI]]
