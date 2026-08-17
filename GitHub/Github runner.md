[[Github action]] [[Github cli]] [[Docker/Docker compose]] [[DevOps/Jenkins]]

# GitHub Actions runner

> Machine that executes workflow jobs — ephemeral GitHub-hosted VMs or your own self-hosted agent.

```txt
        GitHub Actions run ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast hosted vs self-hosted (security, VPC access, ops burden…

## Sources
- [GitHub Docs — About runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners) — overview
- [GitHub Docs — Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) — deep-dive

## Key Concepts
- **Hosted runner:** clean VM per job → zero ops, no private network.
- **Self-hosted:** agent on your hardware/VPC → private deps/GPUs; you patch and secure it.
- **Labels / `runs-on`:** match jobs to capable runners.
- **Concurrency groups:** serialize deploys → avoid two prod rolls at once.

## Technical Details
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
  deploy:
    runs-on: [self-hosted, linux, prod]
    needs: build
concurrency:
  group: deploy-prod
  cancel-in-progress: false
```

| Type | Strength | Cost |
|------|----------|------|
| Hosted | Clean slate | No VPC; shared limits |
| Self-hosted | Private network | Patching + isolation duty |

## Mistakes to Avoid
- **Mistake:** Shared sticky self-hosted runners across untrusted repos
- **Mistake:** Running self-hosted on a laptop (sleep, IP churn, theft risk)
- **Mistake:** Ignoring disk growth from caches/artifacts on persistent runners

## Pros/Cons or Trade-offs
- **Pro (hosted):** no capacity planning for CI VMs.
- **Con (self-hosted):** fork PRs can be dangerous if workflows are too privile…

## Comparison
- vs [[Github action]]: runner is the executor; Actions is the workflow definition.
- vs Jenkins agents: same idea (build agents), different control plane.


### Use cases
- Build on hosted runners

- **Example:** Jobs queue forever
