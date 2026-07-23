[[Github cli]] [[DevOps/Jenkins]] [[Docker/Docker compose]]

# GitHub Actions runner

> Machine that executes workflow jobs — GitHub-hosted VM or your own hardware with the runner agent.

## Mental model

A **workflow** triggers on events; **jobs** run on a **runner** (isolated VM or your server). The runner pulls job steps, checks out code, runs actions/commands, uploads artifacts/logs. GitHub-hosted runners are ephemeral; self-hosted runners are persistent and inherit your network/VPC access.

```
Event → Workflow → Job(s) → Runner agent → Steps (checkout, build, deploy)
```

| Type | Pros | Cons |
|------|------|------|
| GitHub-hosted | Zero ops, clean slate | Shared pool, egress limits, no VPC |
| Self-hosted | Private deps, GPUs, faster cache | You patch, secure, scale |

## Standard config / commands

### Workflow runner selection

```yaml
jobs:
  build:
    runs-on: ubuntu-latest          # GitHub-hosted
  deploy:
    runs-on: [self-hosted, linux, prod]
    needs: build
```

### Register self-hosted runner (Linux)

```bash
# From repo Settings → Actions → Runners → New self-hosted runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.xxx.tar.gz -L https://github.com/actions/runner/releases/download/v2.xxx/actions-runner-linux-x64-2.xxx.tar.gz
tar xzf ./actions-runner-linux-x64-2.xxx.tar.gz
./config.sh --url https://github.com/org/repo --token <TOKEN>
sudo ./svc.sh install
sudo ./svc.sh start
```

### Concurrency (avoid double deploy)

```yaml
concurrency:
  group: deploy-prod
  cancel-in-progress: false
```

### Labels

- `runs-on: [self-hosted, gpu]` — match runner labels at registration time.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Job queued forever | Runners offline in Settings | Start runner service; check `./run.sh` logs |
| Self-hosted wrong user/env | Service account | Install runner as dedicated user; fix PATH |
| Out of disk on hosted runner | Large artifacts/cache | Trim cache; use `actions/upload-artifact` retention |
| Can't reach internal API | Network | Self-hosted in VPC; or OIDC + private endpoint |
| Duplicate deploys | Missing `concurrency` | Add concurrency group |
| Runner not picking job | Label mismatch | Align `runs-on` labels with runner registration |

## Gotchas

> [!WARNING]
> **Self-hosted = arbitrary code execution** — fork PRs can run untrusted workflows unless you restrict `pull_request_target` / approvals.
>
> **Shared self-hosted runner** — one compromised job reads others' secrets; use ephemeral runners or one runner per repo.
>
> **GitHub-hosted `ubuntu-latest` drift** — image updates break apt packages; pin tool versions in workflow.

## When NOT to use

- Don't run self-hosted runners on a laptop — sleep, IP changes, security nightmare.
- Don't use larger hosted runners for lint-only jobs — cost adds up fast.

## Related

[[Github action]] [[Github cli]] [[DevOps/Jenkins]] [[Docker/Docker compose]]
