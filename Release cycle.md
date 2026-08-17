[[Jenkins]] [[spinnaker]] [[Docker compose]] [[Terraform workflow]] [[git merge]] [[Architectures/feature flag]] [[ecommerce-cicd-environments]]

# Release cycle

> Release cycle — the contract for when change ships, how much risk rides together, and what happens when production goes red.

```txt
        Release cycle ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Staff reviews love deploy ≠ release, feature flags, rollback criteria, and…

## Sources
- [Google SRE — Release Engineering](https://sre.google/sre-book/release-engineering/) — deep-dive
- [Wikipedia — Release management](https://en.wikipedia.org/wiki/Release_management) — overview

## Key Concepts
- **Deploy ≠ release:** Code can sit in production at 0% flag until product turns it on.
- **Release train:** Fixed cadence — predictable ops load.
- **Feature flag:** Decouple deploy from exposure
- **Rollback criteria:** Pre-agreed metrics that auto/manual revert.
- **Hotfix lane:** Bypass train for Sev-1 with mandatory backmerge.


- **Core:** A release cycle defines cadence (train vs continuous), exposure controls (fla…

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

## Mistakes to Avoid
- **Mistake:** Rolling back after irreversible schema migrations
- **Mistake:** Leaving hundreds of permanent feature flags
- **Mistake:** Friday deploys without on-call coverage
- **Mistake:** Treating semver as the release communication plan (use changelog…

## Pros/Cons or Trade-offs
- **Pro:** Predictable risk; faster recovery; clearer ownership.
- **Con:** Process overhead; flag debt; trains that become cargo cult without metrics.

## Comparison
- vs continuous deploy every commit: higher velocity, needs stronger automation…


### Use cases
- Weekly train: Mon freeze → Tue tag → Wed canary → Thu full → Fri quiet. Bad c…
