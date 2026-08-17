[[Database]] [[OLAP]] [[ACID]] [[MVCC]] [[mysql]] [[SQL/postgres]] [[connection pooling]] [[SQL normalization]] [[Alter table]] [[database migration]] [[mysql index]] [[covering index]]

# OLTP

> Online Transaction Processing — many short, concurrent reads and writes on a live system where latency and correctness under contention matter more than scan throughput.

```txt
        OLTP ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how you keep p99 low under contention, when to pool connecti…

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 (OLTP vs OLAP storage) — deep-dive
- [Wikipedia — Online transaction processing](https://en.wikipedia.org/wiki/Online_transaction_processing) — overview
- [PostgreSQL Documentation — Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html) — overview
- [MySQL Reference Manual — Optimization](https://dev.mysql.com/doc/refman/en/optimization.html) — overview

## Key Concepts
- **Point / small-range access:** `WHERE id = ?` and tight indexes ([[mysql index]], [[covering index]]).
- **High concurrency:** many sessions; locks and [[MVCC]] matter.
- **Strict [[ACID]]:** money and inventory paths need durable commits and clear isolation.
- **Normalized schema:** [[SQL normalization]] reduces write anomalies on live data.
- **Connection discipline:** [[connection pooling]] so workers do not each hold a dedicated database sessi…


- **Core:** OLTP systems serve interactive user and API traffic: small transactions, high…

## Technical Details
- Workload signature:

```txt
User click ──► API ──► single-row UPDATE + INSERT audit
                         (milliseconds, indexed, transactional)
```

| Dimension | OLTP | OLAP |
|-----------|------|------|
| Query size | Few rows | Millions of rows |
| Schema | Normalized ([[SQL normalization]]) | Often denormalized star/snowflake |
| Hardware pattern | Fast SSD, many connections | Columnar storage, batch loads |
| Latency goal | Milliseconds p99 | Minutes/hours for batch OK |

- Design pressures:

- **Connection limits:** — pool; one request thread ≠ one permanent database session.
- **Hot rows:** — serial writes to one row bottleneck; queue, shard key, or redesign.
- **Migrations:** — online [[Alter table]] and [[database migration]] tooling to avoid long loc…
- **Analytics bleed:** — route heavy aggregates off the primary (replica or warehouse).

```sql
-- Classic OLTP shape: indexed primary-key update in a transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = $1 AND balance >= 100;
INSERT INTO ledger(account_id, amount) VALUES ($1, -100);
COMMIT;
```

## Mistakes to Avoid
- **Mistake:** Running year-long `GROUP BY` reports on the primary during peak …
- **Mistake:** Opening one database connection per application thread without a…
- **Mistake:** Spreading read-modify-write across multiple autocommit statement…
- **Mistake:** Blocking migrations that lock hot tables through the busiest hour

## Pros/Cons or Trade-offs
- **Pro:** Low latency for user paths; strong correctness when durability and isolation are set correctly.
- **Con:** Poor fit for wide historical scans; schema changes need careful online strategies.
- **Trade-off:** Strong isolation / sync commit vs throughput under write storms.

## Comparison
- vs [[OLAP]]: interactive writes vs analytical scans


### Use cases
- Checkout, session stores, inventory reservation, and payment capture on Postg…
