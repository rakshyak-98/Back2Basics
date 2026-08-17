[[Database design]] [[mysql index]] [[covering index]] [[OLTP]] [[OLAP]] [[GIN]] [[mysql partitioning]] [[ACID]]

# Data access patterns

> The read and write paths your application actually runs—indexes, query shapes, and caching should follow these patterns, not the ER diagram alone.





## Interview Relevance
Strong schema design answers start from access patterns: cardinality, QPS, consistency needs, and which index or partition serves each path. Interviewers look for keyset pagination, covering indexes, and N+1 awareness—not only 3NF drawings.

## Sources
- [Use The Index, Luke!](https://use-the-index-luke.com/) — deep-dive
- [PostgreSQL Documentation — Indexes](https://www.postgresql.org/docs/current/indexes.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview

## Key Concepts
- **Hot paths first:** document SQL/ORM, cardinality, consistency, peak QPS per feature → structure follows load, not only entities.
- **Pattern → structure:** lookup, filter+sort, pagination, full-text, time-series each imply different indexes/partitions.
- **Anti-patterns:** `SELECT *`, cross-column OR, N+1 → defeat indexes and amplify round trips.

## Technical Details
For each feature, capture:

- SQL or ORM equivalent
- Expected cardinality (1 row vs millions)
- Consistency needs ([[ACID]] vs stale OK)
- Peak queries per second

| Pattern | Structure |
|---------|-----------|
| Lookup by id | Primary key or unique index |
| Filter + sort | Composite index matching `WHERE` then `ORDER BY` |
| Pagination | Keyset (`WHERE id > ?`) beats `OFFSET` at scale |
| Full-text | PostgreSQL [[GIN]] / `tsvector`; MySQL `FULLTEXT` |
| Time-series | Partition by time ([[mysql partitioning]]) |

Anti-patterns:

- `SELECT *` on wide rows — prevents index-only scans
- OR conditions across columns — often defeats one index; use `UNION ALL` of two indexed queries
- N+1 ORM queries — batch with `IN (...)` or joins

*What breaks first when access patterns change but indexes do not?* Full table scans and lock contention on the primary.

## Real-World Applications
Designing an orders list for [[OLTP]]: index `(user_id, created_at)` and keyset-paginate instead of `OFFSET 100000`. Analytics ([[OLAP]]) may need a replica or warehouse rather than new indexes on the primary alone.

## Pros/Cons or Trade-offs
- **Pro:** Indexes and partitions match real load; fewer production surprises when traffic grows.
- **Con:** Over-indexing every imagined query wastes write I/O and buffer pool; patterns must be revisited as product changes.

## Comparison
vs [[Database design]]: design is the modeling process; access patterns are the workload inputs that should drive that design. vs [[covering index]]: a covering index is one structure chosen because a pattern selects a fixed column set.

## Mistakes to Avoid
- Drawing ER diagrams before listing queries and write rates.
- Using `OFFSET` pagination on large tables.
- Leaving indexes unchanged after a new filter/sort lands in production.
- Optimizing for rare admin reports on the primary at the expense of hot [[OLTP]] paths.
