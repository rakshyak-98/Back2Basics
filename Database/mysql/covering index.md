[[mysql index]] [[mysql query]] [[Data access patterns]]

# covering index

> An index that contains all columns needed by a query—InnoDB can satisfy the query from the index leaf pages alone (`Using index` in EXPLAIN) without touching the clustered table.

```txt
        covering index ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Covering indexes are a classic optimization interview topic: explain `Using i…

## Sources
- [MySQL Reference Manual — EXPLAIN Extra Information](https://dev.mysql.com/doc/refman/en/explain-output.html) — deep-dive
- [Use The Index, Luke! — Covering Indexes](https://use-the-index-luke.com/sql/indexing-covering-indexes) — deep-dive

## Key Concepts
- **Index-only scan:** all selected/filtered columns live in the secondary index → no clustered look…
- **EXPLAIN signal:** `Using index` in Extra.
- **Width cost:** every extra column slows writes and grows the index

## Technical Details
```sql
-- Query: SELECT status, created_at FROM orders WHERE user_id = 42;
CREATE INDEX idx_orders_user_cover ON orders (user_id, status, created_at);
```

- Fewer random I/O lookups to clustered index
- Smaller read footprint for reporting queries

- InnoDB secondary indexes already include the primary key

## Mistakes to Avoid
- **Mistake:** Adding every column “just in case”
- **Mistake:** Forgetting the query changed (`SELECT *`) and the index no longe…
- **Mistake:** Creating duplicate overlapping indexes that waste buffer pool

## Pros/Cons or Trade-offs
- **Pro:** Large read latency wins when the working set fits in the buffer pool as index pages.
- **Con:** Wider indexes cost storage and slow INSERT/UPDATE/DELETE; stale covering indexes hurt when SELECT lists grow.

## Comparison
- vs ordinary [[mysql index]]: a normal secondary index may still need table lo…


### Use cases
- High-QPS status dashboards that filter by `user_id` and only need a few colum…
