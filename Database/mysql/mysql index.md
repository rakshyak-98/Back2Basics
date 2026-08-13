[[mysql query]] [[covering index]] [[mysql table]] [[Data access patterns]]

# mysql index

> B-tree secondary structures in InnoDB that map indexed column values to primary keys—right indexes turn table scans into range seeks; wrong indexes slow writes.

## Create

```sql
CREATE INDEX idx_orders_user_status ON orders (user_id, status);
```

## Composite index order

Leftmost prefix rule: index `(user_id, status)` serves `WHERE user_id = ?` and `WHERE user_id = ? AND status = ?`, not `WHERE status = ?` alone.

## EXPLAIN access types (best → worst)

`const` / `eq_ref` / `ref` / `range` / `index` / **`ALL`**

## Costs

Each index duplicates data, slows inserts/updates, and consumes buffer pool. Drop unused indexes found via Performance Schema.

## Sources

- MySQL Reference Manual — [Optimization and Indexes](https://dev.mysql.com/doc/refman/en/optimization-indexes.html)
- Use The Index, Luke! — [MySQL chapter](https://use-the-index-luke.com/sql/anatomy)
