[[mysql index]] [[mysql query]] [[Data access patterns]]

# covering index

> An index that contains all columns needed by a query—InnoDB can satisfy the query from the index leaf pages alone (`Using index` in EXPLAIN) without touching the clustered table.

## Example

```sql
-- Query: SELECT status, created_at FROM orders WHERE user_id = 42;
CREATE INDEX idx_orders_user_cover ON orders (user_id, status, created_at);
```

## Benefits

- Fewer random I/O lookups to clustered index
- Smaller read footprint for reporting queries

## Tradeoff

Wider indexes — more storage and slower writes. Include only columns actually selected.

## Sources

- MySQL Reference Manual — [EXPLAIN Extra Information](https://dev.mysql.com/doc/refman/en/explain-output.html)
- Use The Index, Luke! — [Covering Index](https://use-the-index-luke.com/sql/indexing-covering-indexes)
