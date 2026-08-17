[[mysql query]] [[covering index]] [[mysql table]] [[Data access patterns]]

# mysql index

> B-tree secondary structures in InnoDB that map indexed column values to primary keys—right indexes turn table scans into range seeks; wrong indexes slow writes.

```txt
        mysql index ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Indexing is a staple: composite leftmost prefix, EXPLAIN access types, and wr…

## Sources
- [MySQL Reference Manual — Optimization and Indexes](https://dev.mysql.com/doc/refman/en/optimization-indexes.html) — deep-dive
- [Use The Index, Luke! — MySQL](https://use-the-index-luke.com/sql/anatomy) — deep-dive

## Key Concepts
- **Secondary → primary key:** InnoDB secondary indexes store PK for table lookup.
- **Leftmost prefix:** `(a,b)` serves `a` and `a,b`, not `b` alone.
- **EXPLAIN access types:** `const` / `eq_ref` / `ref` / `range` / `index` / **`ALL`**.
- **Cost:** duplicates data, slows writes, consumes buffer pool.

## Technical Details
```sql
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
```

- Composite index order: index `(user_id, status)` serves `WHERE user_id = ?` a…
- AND status = ?`, not `WHERE status = ?` alone.

- EXPLAIN access types (best → worst):

- `const` / `eq_ref` / `ref` / `range` / `index` / **`ALL`**

- Each index duplicates data, slows inserts/updates, and consumes buffer pool.
- Drop unused indexes found via Performance Schema.
- For index-only reads see [[covering index]].

## Mistakes to Avoid
- **Mistake:** Indexing columns in the wrong order for the `WHERE`/`ORDER BY` s…
- **Mistake:** Creating many overlapping indexes “for every filter.”
- **Mistake:** Ignoring `ALL` in EXPLAIN on a hot path until CPU burns

## Pros/Cons or Trade-offs
- **Pro:** Turns full scans into seeks; enables covering designs for hot reads.
- **Con:** Over-indexing destroys write throughput and wastes memory; wrong column order helps nobody.

## Comparison
- vs [[covering index]]: covering is a special case where the index satisfies t…


### Use cases
- Speeding an orders list filtered by user and status
