[[Jenkins]] [[spinnaker]] [[Docker compose]] [[Terraform workflow]] [[git merge]] [[Architectures/feature flag]] [[ecommerce-cicd-environments]]

# Release cycle

> Release cycle — the contract for when change ships, how much risk rides together, and what happens when production goes red.

## Interview Relevance
Staff interviews love deploy ≠ release, feature flags, rollback criteria, and expand/contract migrations. This is operational maturity, not semver trivia.

## Sources
- [Google SRE — Release Engineering](https://sre.google/sre-book/release-engineering/) — deep-dive
- [Wikipedia — Release management](https://en.wikipedia.org/wiki/Release_management) — overview

## Core Definition
A release cycle defines cadence (train vs continuous), exposure controls (flags/canaries), and failure playbooks (rollback vs forward fix) between engineering and customers.

## Key Concepts
- **Deploy ≠ release:** Code can sit in production at 0% flag until product turns it on.
- **Release train:** Fixed cadence — predictable ops load.
- **Feature flag:** Decouple deploy from exposure; kill switch without full rollback ([[Architectures/feature flag]]).
- **Rollback criteria:** Pre-agreed metrics that auto/manual revert.
- **Hotfix lane:** Bypass train for Sev-1 with mandatory backmerge.

## Technical Details
```txt
Feature branches ──► trunk/main (CI)
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   Feature flags    Release train    Hotfix lane
         │               │               │
         └───────────────┴───────────────► Production
```

| Mechanism | Purpose |
|-----------|---------|
| Release train | Batch risk on a calendar |
| Feature flag | Instant exposure control |
| Canary | Small % before full rollout |
| Change freeze | Protect peak business windows |

```txt
AUTO rollback if: error rate > 2× baseline; p99 SLO breach; payment success drop
DO NOT rollback if: forward-only migration already applied — forward fix + flag off
```

```shell
git tag -a v2026.07.22 -m "Release train 2026-W29"
kubectl rollout undo deployment/api -n prod
```

## Real-World Applications
Weekly train: Mon freeze → Tue tag → Wed canary → Thu full → Fri quiet. Bad checkout deploy: disable flag in minutes; only roll back artifact if flag cannot save you.

## Pros/Cons or Trade-offs
- **Pro:** Predictable risk; faster recovery; clearer ownership.
- **Con:** Process overhead; flag debt; trains that become cargo cult without metrics.

## Comparison
vs continuous deploy every commit: higher velocity, needs stronger automation and flags. vs huge quarterly releases: simpler calendar, larger blast radius. Tooling siblings: [[Jenkins]], [[spinnaker]], [[Terraform workflow]].

## Mistakes to Avoid
- Rolling back after irreversible schema migrations.
- Leaving hundreds of permanent feature flags.
- Friday deploys without on-call coverage.
- Treating semver as the release communication plan (use changelog + artifact digest).
