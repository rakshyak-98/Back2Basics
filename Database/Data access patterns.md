[[Database design]] [[mysql index]] [[covering index]] [[OLTP]] [[OLAP]]

# Data access patterns

> The read and write paths your application actually runs—indexes, query shapes, and caching should follow these patterns, not the ER diagram alone.

## Document hot paths

For each feature, capture:

- SQL or ORM equivalent
- Expected cardinality (1 row vs millions)
- Consistency needs ([[ACID]] vs stale OK)
- Peak queries per second

## Pattern → structure mapping

| Pattern | Structure |
|---------|-----------|
| Lookup by id | Primary key or unique index |
| Filter + sort | Composite index matching `WHERE` then `ORDER BY` |
| Pagination | Keyset (`WHERE id > ?`) beats `OFFSET` at scale |
| Full-text | PostgreSQL [[GIN]] / `tsvector`; MySQL `FULLTEXT` |
| Time-series | Partition by time ([[mysql partitioning]]) |

## Anti-patterns

- `SELECT *` on wide rows — prevents index-only scans
- OR conditions across columns — often defeats one index; use `UNION ALL` of two indexed queries
- N+1 ORM queries — batch with `IN (...)` or joins

*What breaks first when access patterns change but indexes do not?* Full table scans and lock contention on the primary.

## Sources

- Use The Index, Luke! — [https://use-the-index-luke.com/](https://use-the-index-luke.com/)
- PostgreSQL Documentation — [Indexes](https://www.postgresql.org/docs/current/indexes.html)
- Kleppmann, *DDIA*, Ch. 3
