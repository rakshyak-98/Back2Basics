[[Database]] [[OLAP]] [[ACID]] [[MVCC]] [[mysql]] [[SQL/postgres]] [[connection pooling]] [[SQL normalization]] [[Alter table]] [[database migration]] [[mysql index]] [[covering index]]

# OLTP

> Online Transaction Processing — many short, concurrent reads and writes on a live system where latency and correctness under contention matter more than scan throughput.





## Interview Relevance
Interviewers ask how you keep p99 low under contention, when to pool connections, and why analytics on the primary hurts checkout. Signal: indexed point access, [[ACID]] on the primary, and clear boundaries with [[OLAP]].

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 (OLTP vs OLAP storage) — deep-dive
- [Wikipedia — Online transaction processing](https://en.wikipedia.org/wiki/Online_transaction_processing) — overview
- [PostgreSQL Documentation — Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html) — overview
- [MySQL Reference Manual — Optimization](https://dev.mysql.com/doc/refman/en/optimization.html) — overview

## Core Definition
OLTP systems serve interactive user and API traffic: small transactions, high concurrency, strict durability and isolation on the primary — optimized for point lookups and short range scans, not warehouse-scale aggregates.

## Key Concepts
- **Point / small-range access:** `WHERE id = ?` and tight indexes ([[mysql index]], [[covering index]]).
- **High concurrency:** many sessions; locks and [[MVCC]] matter.
- **Strict [[ACID]]:** money and inventory paths need durable commits and clear isolation.
- **Normalized schema:** [[SQL normalization]] reduces write anomalies on live data.
- **Connection discipline:** [[connection pooling]] so workers do not each hold a dedicated database session forever.

## Technical Details
Workload signature:

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

Design pressures:

- **Connection limits** — pool; one request thread ≠ one permanent database session.
- **Hot rows** — serial writes to one row bottleneck; queue, shard key, or redesign.
- **Migrations** — online [[Alter table]] and [[database migration]] tooling to avoid long locks.
- **Analytics bleed** — route heavy aggregates off the primary (replica or warehouse).

```sql
-- Classic OLTP shape: indexed primary-key update in a transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = $1 AND balance >= 100;
INSERT INTO ledger(account_id, amount) VALUES ($1, -100);
COMMIT;
```

## Real-World Applications
Checkout, session stores, inventory reservation, and payment capture on PostgreSQL or MySQL. Example: debit and credit in one transaction so a crash cannot leave money in limbo; reports run on a lagged replica or warehouse.

## Pros/Cons or Trade-offs
- **Pro:** Low latency for user paths; strong correctness when durability and isolation are set correctly.
- **Con:** Poor fit for wide historical scans; schema changes need careful online strategies.
- **Trade-off:** Strong isolation / sync commit vs throughput under write storms.

## Comparison
vs [[OLAP]]: interactive writes vs analytical scans — do not share buffer pool fate carelessly. vs [[connection pooling]]: pooling is an OLTP scaling tool, not optional décor. vs [[Vector database]]: specialized ANN beside OLTP, not a replacement for orders and users.

## Mistakes to Avoid
- Running year-long `GROUP BY` reports on the primary during peak traffic.
- Opening one database connection per application thread without a pool.
- Spreading read-modify-write across multiple autocommit statements (lost updates).
- Blocking migrations that lock hot tables through the busiest hour.
