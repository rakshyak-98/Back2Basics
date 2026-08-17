[[Security/KMS]] [[NodeJS/node-convict]] [[Deployment/vercel deployment]] [[AWS/IAM]]

# Doppler

> Doppler — stores secrets in projects × configs (dev/staging/prod). The CLI or SDK injects values at runtime — nothing sensitive lives in the repo.

```txt
        Doppler ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Doppler (secrets) reviews cover syncing secrets to runtimes without baking…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** Doppler stores secrets in **projects** × **configs** (development/staging/pro…

```
Developer / CI
      │
      ▼
 doppler run ──► inject env vars ──► your app process
      │
- **Note:** └── secrets live in Doppler cloud (RBAC, audit log, rotation)
```

| Concept | Meaning |
|---------|---------|
| **Project** | One app or service boundary |
| **Config** | Environment slice (`dev`, `staging`, `prod`) |
| **Secret** | Key/value; can reference other secrets |
| **Service token** | CI/CD read-only access (no interactive login) |

- **Note:** Replaces checked-in `.env` files and ad-hoc `export` in shell history.

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> `doppler secrets download > .env` recreates the problem you moved away from — prefer `doppler run` or the SDK so secrets never touch disk.

- **Mistake:** **Precedence:** shell exports override Doppler unless you use `-…
- **Mistake:** **Monorepos:** each service directory needs its own `doppler set…
- **Mistake:** **Rotation:** updating a secret in the dashboard does **not** ho…

| Symptom | Check | Fix |
|---------|-------|-----|
| `Doppler Error: you must run doppler setup` | `doppler configure get project` | `doppler setup` in repo root |
| App sees old secret after rotation | Process still running with old env | Restart process; `doppler run` picks up latest |
| CI fails auth | Token scope / expiry | Regenerate service token; store in CI secret store |
| Wrong env vars in prod | Config mismatch | Verify `doppler configure get config`; use separate tokens per env |
| `doppler run` works locally, not in Docker | Token not passed to container | Mount `DOPPLER_TOKEN` or use Doppler sidecar/K8s operator |

## Pros/Cons or Trade-offs
- Static, non-sensitive configuration (feature flags, public URLs)
- Air-gapped or strict data-residency without Doppler region support
- One-off local scripts where `.env.local` (gitignored) is simpler and the team…
