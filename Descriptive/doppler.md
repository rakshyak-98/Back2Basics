[[Security/KMS]] [[NodeJS/node-convict]] [[Deployment/vercel deployment]] [[AWS/IAM]]

# Doppler

> Centralized secrets manager — sync API keys and env vars to dev/stage/prod without `.env` in git — **Doppler docs + production secret-rotation practice**.

## Mental model

Doppler stores secrets in **projects** × **configs** (dev/staging/prod). The CLI or SDK injects values at runtime — nothing sensitive lives in the repo.

```
Developer / CI
      │
      ▼
 doppler run ──► inject env vars ──► your app process
      │
      └── secrets live in Doppler cloud (RBAC, audit log, rotation)
```

| Concept | Meaning |
|---------|---------|
| **Project** | One app or service boundary |
| **Config** | Environment slice (`dev`, `staging`, `prod`) |
| **Secret** | Key/value; can reference other secrets |
| **Service token** | CI/CD read-only access (no interactive login) |

Replaces checked-in `.env` files and ad-hoc `export` in shell history.

## Standard config / commands

### Install + login (Ubuntu)

```bash
# https://docs.doppler.com/docs/install-cli
curl -Ls --tlsv1.2 --proto "=https" --retry 3 \
  https://cli.doppler.com/install.sh | sudo sh

doppler login
doppler setup   # pick project + config for this directory
```

### Daily workflow

```bash
# Run app with injected secrets (preferred over doppler secrets download)
doppler run -- node server.js
doppler run -- npm start

# Inspect without printing to disk
doppler secrets
doppler secrets get DATABASE_URL --plain

# List configs in a project
doppler configs --project my-api
```

### CI (service token — no interactive login)

```bash
export DOPPLER_TOKEN="dp.st.prod.xxxx"   # scoped read token
doppler run -- npm test
```

### Reset local binding

```bash
doppler configure unset project
doppler configure unset config
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Doppler Error: you must run doppler setup` | `doppler configure get project` | `doppler setup` in repo root |
| App sees old secret after rotation | Process still running with old env | Restart process; `doppler run` picks up latest |
| CI fails auth | Token scope / expiry | Regenerate service token; store in CI secret store |
| Wrong env vars in prod | Config mismatch | Verify `doppler configure get config`; use separate tokens per env |
| `doppler run` works locally, not in Docker | Token not passed to container | Mount `DOPPLER_TOKEN` or use Doppler sidecar/K8s operator |

## Gotchas

> [!WARNING]
> `doppler secrets download > .env` recreates the problem you moved away from — prefer `doppler run` or the SDK so secrets never touch disk.

- **Precedence:** shell exports override Doppler unless you use `--preserve-env=false`.
- **Monorepos:** each service directory needs its own `doppler setup` or explicit `--project` / `--config` flags.
- **Rotation:** updating a secret in the dashboard does **not** hot-reload running pods — roll the deployment.

## When NOT to use

- Static, non-sensitive config (feature flags, public URLs) — use normal config files or [[NodeJS/node-convict]].
- Air-gapped or strict data-residency without Doppler region support — use [[Security/KMS]] or Vault on-prem.
- One-off local scripts where `.env.local` (gitignored) is simpler and the team agrees.

## Related

[[Security/KMS]] [[NodeJS/node-convict]] [[AWS/IAM]] [[Deployment/vercel deployment]]
