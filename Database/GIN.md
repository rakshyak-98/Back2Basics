[[SQL/postgres]] [[mysql index]] [[Data access patterns]]

# GIN

> PostgreSQL Generalized Inverted Index—stores (key → row pointers) entries for composite values like arrays, `jsonb`, and full-text `tsvector` documents.

## When GIN fits

- `jsonb` containment queries (`@>`, `?`, `?&`)
- Full-text search (`@@` with `to_tsvector`)
- Array overlap (`&&`)

```sql
CREATE INDEX idx_docs_body ON documents USING GIN (to_tsvector('english', body));
SELECT * FROM documents WHERE to_tsvector('english', body) @@ to_tsquery('postgres & index');
```

## GIN versus GiST

| Index | Strength |
|-------|----------|
| **GIN** | Faster lookups; larger index; slower builds |
| **GiST** | Lossy but smaller; better for geometry |

## Maintenance

GIN indexes can be large; use `jsonb_path_ops` or targeted expressions instead of indexing entire documents when possible.

## Sources

- PostgreSQL Documentation — [GIN Indexes](https://www.postgresql.org/docs/current/gin.html)
- PostgreSQL Documentation — [Full Text Search](https://www.postgresql.org/docs/current/textsearch.html)
