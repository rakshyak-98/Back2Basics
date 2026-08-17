[[Database design]] [[mysql index]] [[covering index]] [[OLTP]] [[OLAP]] [[GIN]] [[mysql partitioning]] [[ACID]]

# Data access patterns

> The read and write paths your application actually runs—indexes, query shapes, and caching should follow these patterns, not the ER diagram alone.

```txt
        Data access patter ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Strong schema design answers start from access patterns: cardinality, QPS, co…

## Sources
- [Use The Index, Luke!](https://use-the-index-luke.com/) — deep-dive
- [PostgreSQL Documentation — Indexes](https://www.postgresql.org/docs/current/indexes.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview

## Key Concepts
- **Hot paths first:** document SQL/ORM, cardinality, consistency, peak QPS per feature → structure …
- **Pattern → structure:** lookup, filter+sort, pagination, full-text, time-series each imply different …
- **Anti-patterns:** `SELECT *`, cross-column OR, N+1 → defeat indexes and amplify round trips.

## Technical Details
- For each feature, capture:

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

- Anti-patterns:

- `SELECT *` on wide rows — prevents index-only scans
- OR conditions across columns
- N+1 ORM queries — batch with `IN (...)` or joins

- *What breaks first when access patterns change but indexes do not?* Full tabl…

## Mistakes to Avoid
- **Mistake:** Drawing ER diagrams before listing queries and write rates
- **Mistake:** Using `OFFSET` pagination on large tables
- **Mistake:** Leaving indexes unchanged after a new filter/sort lands in produ…
- **Mistake:** Optimizing for rare admin reports on the primary at the expense …

## Pros/Cons or Trade-offs
- **Pro:** Indexes and partitions match real load; fewer production surprises when traffic grows.
- **Con:** Over-indexing every imagined query wastes write I/O and buffer pool; patterns must be revisited as product changes.

## Comparison
- vs [[Database design]]: design is the modeling process


### Use cases
- Designing an orders list for [[OLTP]]: index `(user_id, created_at)` and keys…
