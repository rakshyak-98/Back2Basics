[[Jenkins]] [[spinnaker]] [[Docker compose]] [[Terraform workflow]] [[git merge]]

# Release cycle

> How staff teams ship safely — release trains, feature flags, rollback criteria — **operational maturity, not semver trivia**.

---

## Mental model

A **release cycle** is the contract between engineering and customers for **when** change arrives, **how much** risk is bundled, and **what happens** when it fails.

```txt
Feature branches ──► trunk/main (continuous integration)
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   Feature flags    Release train    Hotfix lane
   (dark launch)    (weekly cut)     (bypass train)
         │               │               │
         └───────────────┴───────────────► Production
```

| Mechanism | Purpose |
|-----------|---------|
| **Release train** | Fixed cadence (e.g. Tue deploy) — predictable ops load |
| **Feature flag** | Decouple deploy from exposure — kill switch without rollback |
| **Rollback** | Revert artifact or flip flag — time-bound decision |
| **Change advisory** | High-risk windows blocked (Black Friday, fiscal close) |

**Deploy ≠ release:** code can sit in prod behind a flag at 0% until product turns it on.

---

## Standard config / commands

### Release train checklist (weekly)

```txt
Mon:  code freeze for next train (P0 fixes only)
Tue:  cut release branch OR tag main SHA
      run full regression + migration dry-run on staging
Wed:  canary / 5% prod → metrics 24h
Thu:  100% prod if SLO green
Fri:  no prod deploys (on-call preservation) — team policy
```

### Feature flag hygiene

```txt
Naming:   team_feature_action (billing_invoice_pdf_export)
Owner:    team + expiry date in flag description
Defaults: off in prod until explicit enable
Cleanup:  flag removed within 2 sprints after 100% rollout
Tools:    LaunchDarkly, Unleash, Flipt, or homegrown + DB
```

```javascript
if (flags.isEnabled('checkout_apple_pay', { userId })) {
  showApplePay();
}
```

### Rollback criteria (define before deploy)

```txt
AUTO rollback if (any):
  - Error rate > 2× baseline for 5 min
  - p99 latency > SLO breach 10 min
  - Payment success rate drops > 0.5%
  - Health check failing > 50% instances

MANUAL rollback discussion if:
  - Minor UI regression non-revenue
  - Single-tenant report wrong (isolate tenant)

DO NOT rollback if:
  - Data migration already forward-only — forward fix + flag off instead
```

### Hotfix lane

```txt
1. Branch from prod tag (not main if main diverged)
2. Minimal fix + test
3. Deploy hotfix artifact
4. Cherry-pick to main same day
5. Postmortem if train was bypassed
```

### Version tagging

```shell
git tag -a v2026.07.22 -m "Release train 2026-W29"
git push origin v2026.07.22
# CI builds immutable artifact from tag SHA
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Bad deploy, metrics red | Rollback criteria met? | Revert deployment / previous artifact ([[spinnaker]], Argo, k8s rollout undo) |
| Bad deploy, metrics OK | Feature flag? | Disable flag first — faster than rollback |
| Rollback fails | DB migration irreversible | Forward fix; restore from backup only if data corrupt |
| Train delayed | Missing QA sign-off | Split train — ship low-risk packages only |
| Flag stuck on | Flag service outage | Default-off in code; cache TTL short |
| Divergent prod/main | Hotfixes not cherry-picked | Mandatory backmerge PR before next train |

```shell
kubectl rollout undo deployment/api -n prod
# or
git revert <commit> && redeploy
```

---

## Gotchas

> [!WARNING]
> **"Rollback" after schema migration** — down migrations often untested; design expand/contract migrations.

> [!WARNING]
> **Flag debt** — 200 flags, nobody knows defaults; accidental exposure.

> [!WARNING]
> **Friday deploy culture** — wins until it doesn't; align with on-call coverage.

> [!WARNING]
> ** semver as communication only** — v2.3.1 doesn't tell ops what's inside; use changelog + artifact digest.

> [!WARNING]
> **Skipping staging** — train exists to batch risk, not eliminate staging.

---

## When NOT to use

- **Early startup (<10 engineers)** — continuous deploy + flags may beat heavy train process.
- **Regulated freeze windows** — train still runs internally; prod promote waits.
- **Feature flags for every bugfix** — overhead; simple fixes go straight out with monitoring.

---

## Related

[[Jenkins]] [[spinnaker]] [[Terraform workflow]] [[git merge]] [[Docker compose]]
