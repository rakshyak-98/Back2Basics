[[Architectures]] [[Database]] [[MVCC]] [[ACID]] [[Idempotent-key]] [[race condition]]

# OCC

> OCC (Optimistic Concurrency Control) lets transactions run, then checks for conflict at commit — retry if someone else wrote first.





## Interview Relevance
OCC interviews contrast validate-at-commit vs locking — retry storms under contention and when MVCC/locking fits better.

## Sources
- [Wikipedia — Optimistic concurrency control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) — overview
- [Kung & Robinson — On Optimistic Methods for Concurrency Control](https://dl.acm.org/doi/10.1145/319566.319567) — deep-dive

## Key Concepts
```txt
read version/etag → compute → commit if version unchanged else retry
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Optimistic** | Don’t lock early | “We detect conflict at commit, not at read.” |
| **Version / etag** | Token that changes on write | “Compare-and-swap on the version.” |
| **Retry** | Run the txn again | “Conflicts should be rare or OCC hurts.” |
| **vs pessimistic** | Lock first | “Hot rows prefer locks or queues.” |

Used in: HTTP `If-Match`, DynamoDB conditional writes, many ORMs’ `@Version`.

## Technical Details
```sql
-- version column pattern
UPDATE accounts SET balance = $1, version = version + 1
WHERE id = $2 AND version = $3;
-- 0 rows → conflict → reload and retry
```

```http
PUT /doc/1
If-Match: "etag-abc"
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Constant retries | hot key | Pessimistic lock / queue / shard |
| Lost update | no version check | Add version/etag CAS |
| Double charge | retry without idempotency | Idempotent keys |
| High latency | retry storms | Cap retries; backoff |

## Pros/Cons or Trade-offs
- **Trade-off:** Very hot rows — use locks, single-threaded owner, or atomic increment.
- **Trade-off:** Multi-row invariants without a txn story — need real transactions, not only etags.

## Mistakes to Avoid
- OCC needs rare conflicts — hot counters are a bad fit.
- Retry must be safe — pair with idempotency for side effects.
