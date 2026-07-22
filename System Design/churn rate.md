[[System design]] [[CMS]] [[Authentication web application]]

# Churn rate

> Percent of customers/users lost in a period — **retention KPI**, drives infra downsizing and revenue models.

---

## Mental model

**Churn rate** (attrition) measures **how many customers stop paying or actively leave** in a time window, expressed as a **percentage of the starting cohort**. It is the inverse lens of retention: high churn destroys unit economics and leaves **orphaned data, idle seats, and over-provisioned capacity**.

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

Distinguish **voluntary** (cancel button) vs **involuntary** (failed payment) — fix paths differ.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Churn spike post deploy | Release correlation | Rollback; feature flag |
| Involuntary churn up | Payment gateway errors | Update cards; retry rules |
| Enterprise logos leave | Support tickets | CSM review; SLA breach |
| Metric disagrees finance | Definition drift | Align cancel date vs end-of-period |
| "Churn" from duplicate accounts | Bad dedupe | One user = one subscriber ID |
| Low churn but revenue down | Downgrades not counted | Track revenue churn separately |

---

## Gotchas

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

## When NOT to use

- **Pre-PMF startup** — sample too small; focus qualitative exit interviews.
- **Single metric for eng SLOs** — churn is business KPI, not p99 latency substitute.
- **Blame eng for all churn** — content, pricing, support dominate in media SaaS.

---

## Related

[[System design]] [[CMS]] [[Authentication web application]] [[Eventual consistency]] [[database sharding]]
