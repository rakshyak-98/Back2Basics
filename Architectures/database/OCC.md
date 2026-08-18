[[Architectures]] [[Database]] [[MVCC]] [[ACID]]

# OCC

> OCC (Optimistic Concurrency Control) lets transactions run, then checks for conflict at commit — retry if someone else wrote first.

## Mental model

**Say it in one breath:** Assume no conflict, do the work, validate at the end — if another txn touched the same data, abort and retry.

```txt
read version/etag → compute → commit if version unchanged else retry
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Optimistic** | Don’t lock early | “We detect conflict at commit, not at read.” |
| --- | --- | --- |
| **Version / etag** | Token that changes on write | “Compare-and-swap on the version.” |
| **Retry** | Run the txn again | “Conflicts should be rare or OCC hurts.” |
| **vs pessimistic** | Lock first | “Hot rows prefer locks or queues.” |

Used in: HTTP `If-Match`, DynamoDB conditional writes, many ORMs’ `@Version`.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Constant retries | hot key | Pessimistic lock / queue / shard |
| Lost update | no version check | Add version/etag CAS |
| Double charge | retry without idempotency | Idempotent keys |
| High latency | retry storms | Cap retries; backoff |

## Gotchas

> [!WARNING]
> **OCC needs rare conflicts** — hot counters are a bad fit.

> [!WARNING]
> **Retry must be safe** — pair with idempotency for side effects.

## When NOT to use

- **Very hot rows** — use locks, single-threaded owner, or atomic increment.
- **Multi-row invariants without a txn story** — need real transactions, not only etags.

## Related

[[MVCC]] [[ACID]] [[Idempotent-key]] [[race condition]]
