[[Database]] [[OLAP]] [[ACID]] [[mysql]] [[SQL/postgres]] [[connection pooling]]

# OLTP

> Online Transaction Processing—many short, concurrent read/write operations on a live system where latency and correctness under contention matter more than scan throughput.

## Workload signature

- Point lookups and small range queries (`WHERE id = ?`)
- Frequent inserts/updates tied to user actions
- Strict [[ACID]] expectations on the primary
- Index-friendly access paths ([[mysql index]], [[covering index]])

```txt
User click ──► API ──► single-row UPDATE + INSERT audit
                         (milliseconds, indexed, transactional)
```

## Contrast with [[OLAP]]

| Dimension | OLTP | OLAP |
|-----------|------|------|
| Query size | Few rows | Millions of rows |
| Schema | Normalized ([[SQL normalization]]) | Often denormalized star/snowflake |
| Hardware pattern | Fast SSD, many connections | Columnar storage, batch loads |

Running heavy aggregates on the OLTP primary competes for buffer pool and I/O—route analytics to replicas or a warehouse.

## Design pressures

- **Connection limits** — use [[connection pooling]]; one thread per request does not mean one database session per thread at all times
- **Hot rows** — serial writes to the same row become a bottleneck; shard or queue
- **Migrations** — online [[Alter table]] and [[database migration]] tooling to avoid long locks

## Sources

- Kleppmann, *DDIA*, Ch. 3 (OLTP vs OLAP storage)
- Wikipedia — [Online transaction processing](https://en.wikipedia.org/wiki/Online_transaction_processing)
