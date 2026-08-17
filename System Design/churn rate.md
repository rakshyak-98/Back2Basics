[[System design]] [[CMS]] [[Authentication web application]]

# Churn rate

> Churn rate — (attrition) measures how many customers stop paying or actively leave in a time window, expressed as a percentage of the starting cohort. It

```txt
        Churn rate ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Define churn formula, cohort vs blunt rate, and product/ops levers that move …

## Sources
- [Wikipedia — churn rate](https://en.wikipedia.org/wiki/churn_rate) — overview

## Key Concepts
- **Attrition metric:** customers lost over a period ÷ base.
- **Cohorts beat blunt rates:** when signup mix shifts, overall churn lies.
- **Product + ops levers:** onboarding, reliability, pricing, support.
- **Leading indicators:** engagement drops before cancel.

## Technical Details
### How it works

- **Churn rate:** (attrition) measures **how many customers stop paying or activ…
- It is the inverse lens of retention: high churn destroys unit economics and l…

```txt
Starting subscribers (period)     10,000
Cancellations + involuntary churn    800
Net churn rate = 800 / 10,000 = 8% (monthly)

Revenue churn may differ if downgrades count separately
```

| Metric | Formula (monthly) | Notes |
|--------|-------------------|-------|
| **Customer churn** | `(lost customers / start customers) × 100` | SaaS standard |
| **Revenue churn** | `(MRR lost / start MRR) × 100` | Includes downgrade |
| **Net revenue churn** | Includes expansion | Can be negative (good) |
| **Logo vs dollar** | Enterprise vs SMB mix | One whale ≠ many logos |

- Distinguish **voluntary** (cancel button) versus **involuntary** (failed paym…

### Configuration and commands

### SQL — monthly customer churn (sketch)

```sql
WITH start_cohort AS (
  SELECT user_id FROM subscriptions
  WHERE status = 'active' AND date_trunc('month', started_at) < '2026-07-01'
    AND (ended_at IS NULL OR ended_at >= '2026-07-01')
),
churned AS (
  SELECT user_id FROM subscriptions
  WHERE ended_at >= '2026-07-01' AND ended_at < '2026-08-01'
)
SELECT COUNT(DISTINCT c.user_id)::float / NULLIF(COUNT(DISTINCT s.user_id), 0) AS churn_rate
FROM start_cohort s
LEFT JOIN churned c ON s.user_id = c.user_id;
```

### Event-driven tracking (product analytics)

```txt
Events: subscription_started, subscription_cancelled, payment_failed
Properties: plan_id, reason_code, tenure_days
Cohort by signup month — compare churn curves, not single headline %
```

### Involuntary churn playbook

```txt
payment_failed → retry dunning (Day 1, 3, 7)
→ email + in-app banner
→ grace period read-only
→ cancel + data retention policy ([[CMS]] export window)
```

### Capacity planning link

```txt
If monthly churn 5% and signups flat → MAU declines → scale down async workers
Conversely: viral growth + low churn → [[database sharding]] ahead of inflection
```

### Dashboard minimum

```txt
Gross churn % (monthly)
Net revenue churn %
Churn by plan / channel / tenure bucket
Reactivation rate (win-back campaigns)
```

## Mistakes to Avoid
> [!WARNING]
> **Annual plans** — monthly churn math needs **cohort normalization** or misleading 0% months.

> [!WARNING]
> **Free tier not in denominator** — mixing free + paid dilutes signal.

> [!WARNING]
> **Pause ≠ cancel** — define policy; pauses hide churn time bomb.

> [!WARNING]
> **Delayed cancellation** — user churns emotionally at click; ends at period — match metric to finance.

> [!WARNING]
> **Seasonal events** — compare YoY not MoM for retail streaming.

---

| Symptom | Check | Fix |
|---------|-------|-----|
| Churn spike post deploy | Release correlation | Rollback; feature flag |
| Involuntary churn up | Payment gateway errors | Update cards; retry rules |
| Enterprise logos leave | Support tickets | CSM review; SLA breach |
| Metric disagrees finance | Definition drift | Align cancel date vs end-of-period |
| "Churn" from duplicate accounts | Bad dedupe | One user = one subscriber ID |
| Low churn but revenue down | Downgrades not counted | Track revenue churn separately |

---

## Pros/Cons or Trade-offs
- **Pre-PMF startup** — sample too small; focus qualitative exit interviews.
- **Single metric for eng SLOs**
- **Blame eng for all churn**

---


- **Pro:** Forces focus on retention economics.
- **Con:** Bad definitions make false victories.
- **Trade-off:** logo churn vs revenue churn.

## Comparison
- vs growth/acquisition metrics: opposite side of the funnel.
- vs [[Throughput]]: system capacity ≠ customer retention.


### Use cases
- SaaS growth reviews, subscription businesses, and marketplace retention work.
