[[SQL/postgres]] [[mysql index]] [[Data access patterns]]

# GIN

> PostgreSQL Generalized Inverted Index—stores (key → row pointers) entries for composite values like arrays, `jsonb`, and full-text `tsvector` documents.

## Interview Relevance

GIN comes up when discussing PostgreSQL full-text search, `jsonb` containment, and GiST vs GIN tradeoffs. Interviewers want when to index expressions/`jsonb_path_ops` instead of whole documents.

## Sources

- [PostgreSQL Documentation — GIN Indexes](https://www.postgresql.org/docs/current/gin.html) — deep-dive
- [PostgreSQL Documentation — Full Text Search](https://www.postgresql.org/docs/current/textsearch.html) — deep-dive

## Key Concepts

- **Inverted index:** maps component keys (tokens, jsonb keys/values, array elements) to row pointers → fast containment and full-text matches.
- **Composite values:** arrays, `jsonb`, `tsvector` — not a simple B-tree equality column alone.
- **Build vs lookup:** GIN favors faster lookups at the cost of larger indexes and slower builds than some alternatives.

## Technical Details

When GIN fits:

- `jsonb` containment queries (`@>`, `?`, `?&`)
- Full-text search (`@@` with `to_tsvector`)
- Array overlap (`&&`)

```sql
CREATE INDEX idx_docs_body ON documents USING GIN (to_tsvector('english', body));
SELECT * FROM documents WHERE to_tsvector('english', body) @@ to_tsquery('postgres & index');
```

| Index | Strength |
|-------|----------|
| **GIN** | Faster lookups; larger index; slower builds |
| **GiST** | Lossy but smaller; better for geometry |

GIN indexes can be large; use `jsonb_path_ops` or targeted expressions instead of indexing entire documents when possible.

## Real-World Applications

Product search on `tsvector` columns and API filters on `jsonb` attributes. Example: index `to_tsvector('english', body)` so support search stays sub-second without shipping Elasticsearch for a modest corpus.

## Pros/Cons or Trade-offs

- **Pro:** Excellent for containment and full-text inside PostgreSQL—fewer moving parts than an external search cluster for medium scale.
- **Con:** Large indexes, slower updates/builds; over-indexing entire `jsonb` documents wastes space.

## Comparison

vs GiST: GiST is often better for geometry and lossy/smaller indexes; GIN wins many `jsonb`/FTS lookup workloads. vs MySQL [[mysql index]] / `FULLTEXT`: similar problem space, different index types and operators.

## Mistakes to Avoid

- Indexing entire unbounded `jsonb` documents when only two paths are queried.
- Expecting GIN to speed equality lookups that a B-tree already handles.
- Ignoring index bloat after heavy update workloads — monitor size and vacuum/reindex policy.
