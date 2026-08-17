[[mysql index]] [[mysql query]] [[Data access patterns]]

# covering index

> An index that contains all columns needed by a query—InnoDB can satisfy the query from the index leaf pages alone (`Using index` in EXPLAIN) without touching the clustered table.





## Interview Relevance
Covering indexes are a classic optimization interview topic: explain `Using index`, leftmost prefixes, and the write/storage cost of wide indexes. Ties directly to [[Data access patterns]].

## Sources
- [MySQL Reference Manual — EXPLAIN Extra Information](https://dev.mysql.com/doc/refman/en/explain-output.html) — deep-dive
- [Use The Index, Luke! — Covering Indexes](https://use-the-index-luke.com/sql/indexing-covering-indexes) — deep-dive

## Key Concepts
- **Index-only scan:** all selected/filtered columns live in the secondary index → no clustered lookup.
- **EXPLAIN signal:** `Using index` in Extra.
- **Width cost:** every extra column slows writes and grows the index — include only what the query needs.

## Technical Details
```sql
-- Query: SELECT status, created_at FROM orders WHERE user_id = 42;
CREATE INDEX idx_orders_user_cover ON orders (user_id, status, created_at);
```

Benefits:

- Fewer random I/O lookups to clustered index
- Smaller read footprint for reporting queries

InnoDB secondary indexes already include the primary key; covering still requires including non-PK selected columns explicitly in the index definition (or selecting only PK + indexed cols).

## Real-World Applications
High-QPS status dashboards that filter by `user_id` and only need a few columns. Example: cover `(user_id, status, created_at)` so list endpoints stop hammering the clustered primary for wide order rows.

## Pros/Cons or Trade-offs
- **Pro:** Large read latency wins when the working set fits in the buffer pool as index pages.
- **Con:** Wider indexes cost storage and slow INSERT/UPDATE/DELETE; stale covering indexes hurt when SELECT lists grow.

## Comparison
vs ordinary [[mysql index]]: a normal secondary index may still need table lookups (`Using index condition` / row fetch); a covering index avoids that for a specific query shape. vs selecting `*`: covering is incompatible with wide SELECT lists.

## Mistakes to Avoid
- Adding every column “just in case” — write amplification without benefit.
- Forgetting the query changed (`SELECT *`) and the index no longer covers.
- Creating duplicate overlapping indexes that waste buffer pool.
