[[Database design]] [[OLTP]] [[OLAP]] [[connection pooling]] [[covering index]] [[BASE]]

# Data access patterns

> Data access patterns — schema follows access paths, not ER diagrams drawn once. Ask every feature:

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Data access patterns — I can explain the job, the config, and the top failure without jargon.


Schema follows **access paths**, not ER diagrams drawn once. Ask every feature:

1. **Who writes?** frequency, burstiness, idempotency
2. **Who reads?** latency SLO, staleness tolerance
3. **Key?** point lookup vs scan vs graph walk
4. **Shape?** row, document, time-series, blob

```
         ┌─────────────┐
Write ──►│  Primary    │──► CDC/outbox ──► search index / warehouse
         │  (OLTP)     │
         └──────┬──────┘
                │ read paths
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  Cache      Replica    Materialized view
 (eventual)  (lag OK)   (pre-aggregated)
```

**Pattern picks consistency boundary** — not the ORM.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Data access patterns** | This note’s core idea | “I explain Data access patterns in plain words.” |
| **idea** | What it is for | “One sentence, no jargon.” |
| **check** | How I verify | “I name the command or signal I look at.” |
| **fail** | How it breaks | “I name the top production failure.” |

---

## Standard config / commands

```bash
# version / help / dry-run when available
# keep env-specific values out of git
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow | EXPLAIN / slow log | Index or rewrite |
| Auth/connect fail | pg_hba / users | Fix grants and bind |
| Bad migration | backup + version | Roll forward carefully |

---

## Gotchas

> [!WARNING]
> Prefer words you can say aloud in an interview.

---

## When NOT to use

- Skip when a simpler existing approach already fits.

---

## Related

[[Database design]] [[OLTP]] [[OLAP]] [[connection pooling]] [[covering index]] [[BASE]]
