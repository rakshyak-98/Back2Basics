[[Github runner]] [[Github cli]] [[DevOps/Jenkins]] [[Deployment/spinnaker]]

# GitHub Actions

> CI/CD workflows as YAML in the repository — events trigger jobs that run steps on runners.

```txt
        GitHub Actions ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want triggers (`push`/`pull_request`/`schedule`), jobs vs steps,…

## Sources
- [GitHub Docs — Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) — overview
- [GitHub Docs — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) — deep-dive

## Key Concepts
- **Workflow:** YAML under `.github/workflows/` → automation unit.
- **Job:** runs on one runner; jobs parallel by default → use `needs:` for order.
- **Step:** `run:` shell or `uses:` action → compose the job.
- **Contexts / expressions:** `${{ secrets.* }}`, `github`, `matrix` → inject configuration safely.
- **Permissions:** least-privilege `GITHUB_TOKEN` → limit write scope.

## Technical Details
```
Trigger → Workflow → Job(s) → Steps on a Runner
```

```yaml
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
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npm test
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Not triggering | `on:` filters | Match branch/paths; try `workflow_dispatch` |
| Empty secret | Scope / fork PR | Set at right level; forks lack secrets on `pull_request` |
| YAML invalid | Actions UI error | Fix indentation (spaces, not tabs) |

## Mistakes to Avoid
- **Mistake:** Using `pull_request_target` casually — easy RCE on the base repo
- **Mistake:** String-concatenating untrusted input into `run:` scripts
- **Mistake:** Pinning actions only to floating tags without knowing the trust …

## Pros/Cons or Trade-offs
- **Pro:** Co-located with code; huge action ecosystem.
- **Con:** Minutes/cost; supply-chain risk if actions are unpinned.

## Comparison
- vs [[DevOps/Jenkins]]: Actions is GitHub-native SaaS; Jenkins is self-hosted and more DIY.
- vs [[Github runner]]: Actions is the orchestration; runners are where jobs execute.


### Use cases
- PR checks, scheduled nightlies, and deploy pipelines that call cloud CLIs wit…

- **Example:** Cron at `30 5 * * 1,3`
