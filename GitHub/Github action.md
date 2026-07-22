[[Github runner]] [[Github cli]] [[DevOps/Jenkins]] [[Deployment/spinnaker]]

# GitHub Actions

> Event-driven CI/CD defined in YAML under `.github/workflows/` — jobs run on [[Github runner]] instances.

## Mental model

```
Trigger (push, PR, cron, dispatch)
  → Workflow (.yml)
    → Job(s) [parallel by default]
      → Steps (run shell or uses: action)
        → Runner environment
```

Secrets live in GitHub (`secrets.*`, `vars.*`); never commit them. Expressions `${{ }}` access context (`github`, `env`, `matrix`).

## Standard config / commands

### Minimal CI workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Secrets in steps

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh
```

### Scheduled cron (UTC)

```yaml
on:
  schedule:
    - cron: '30 5 * * 1,3'   # Mon/Wed 05:30 UTC
jobs:
  nightly:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ github.event.schedule }}"
```

### Disable CodeQL (repo setting path)

Settings → Code security → Code scanning → disable tool (prefer fixing findings over disabling in prod repos).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Workflow not triggering | `on:` branch/path filters | Match branch name; use `workflow_dispatch` to test |
| Secret empty in log | `secrets` scope (env vs repo) | Set secret at correct level; fork PRs don't get secrets |
| `ubuntu-latest` tool missing | Runner image changelog | Pin `actions/setup-*` or explicit apt install |
| YAML invalid | Actions tab error | Validate indentation; tabs break YAML |
| Cron didn't run | GitHub schedule delay | Cron is best-effort; can slip minutes on busy repos |
| Action pin drift | `@v4` vs SHA | Pin major tag or full SHA for supply-chain safety |

## Gotchas

> [!WARNING]
> **`pull_request` from forks** — secrets unavailable; use `pull_request_target` only with extreme care (RCE risk).
>
> **Cache poisoning across branches** — scope cache keys with `${{ github.ref }}`.
>
> **Reusable workflow inputs** — untrusted input in `run:` = injection; pass as env, not string concat in script.

## When NOT to use

- Don't run long-lived servers in Actions — use deploy targets (k8s, Lambda, VM).
- Don't replace proper secret manager (Vault, AWS SM) with hundreds of repo secrets for shared infra creds.

## Related

[[Github runner]] [[Github cli]] [[GIT/git hook]] [[DevOps/Jenkins]]
