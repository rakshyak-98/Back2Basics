[[SQL/postgres]] [[mysql index]] [[Data access patterns]]

# GIN

> PostgreSQL Generalized Inverted Index—stores (key → row pointers) entries for composite values like arrays, `jsonb`, and full-text `tsvector` documents.

```txt
        GIN ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** GIN comes up when discussing PostgreSQL full-text search, `jsonb` containment…

## Sources
- [PostgreSQL Documentation — GIN Indexes](https://www.postgresql.org/docs/current/gin.html) — deep-dive
- [PostgreSQL Documentation — Full Text Search](https://www.postgresql.org/docs/current/textsearch.html) — deep-dive

## Key Concepts
- **Inverted index:** maps component keys (tokens, jsonb keys/values, array elements) to row pointe…
- **Composite values:** arrays, `jsonb`, `tsvector` — not a simple B-tree equality column alone.
- **Build vs lookup:** GIN favors faster lookups at the cost of larger indexes and slower builds tha…

## Technical Details
- When GIN fits:

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

- GIN indexes can be large

## Mistakes to Avoid
- **Mistake:** Indexing entire unbounded `jsonb` documents when only two paths …
- **Mistake:** Expecting GIN to speed equality lookups that a B-tree already ha…
- **Mistake:** Ignoring index bloat after heavy update workloads

## Pros/Cons or Trade-offs
- **Pro:** Excellent for containment and full-text inside PostgreSQL—fewer moving parts than an external search cluster for medium scale.
- **Con:** Large indexes, slower updates/builds; over-indexing entire `jsonb` documents wastes space.

## Comparison
- vs GiST: GiST is often better for geometry and lossy/smaller indexes


### Use cases
- Product search on `tsvector` columns and API filters on `jsonb` attributes
