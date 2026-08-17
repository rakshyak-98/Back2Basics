[[psql essential]] [[SQL/postgres]] [[Alter table]] [[GIN]] [[psql functions]]

# psql table

> Create and inspect PostgreSQL tables — types, constraints, indexes (including [[GIN]]), partitions, and `\d` introspection.

```txt
        psql table ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Schema design in Postgres: `TIMESTAMPTZ`, `JSONB`+GIN, identity/serial keys, …

## Sources
- [CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html) — deep-dive
- [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html) — deep-dive

## Key Concepts
- **Rich types:** `JSONB`, arrays, ranges, UUID, `TIMESTAMPTZ`.
- **Constraints:** PK, FK, CHECK, UNIQUE — enforced strongly.
- **Indexes:** B-tree default; GIN for JSONB/full-text.
- **Declarative partitioning:** Parent + partitions for ranges/lists/hash.

## Technical Details
```sql
CREATE TABLE orders (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  metadata    JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_user ON orders (user_id);
CREATE INDEX idx_orders_meta ON orders USING GIN (metadata);

\d+ orders
SELECT * FROM pg_indexes WHERE tablename = 'orders';

CREATE TABLE orders_2024 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

- Large rewrites: see [[Alter table]] patterns and `pg_repack` / rewrite-aware …

## Mistakes to Avoid
- **Mistake:** Using `TIMESTAMP` without time zone for absolute instants
- **Mistake:** Partitioning without aligning PK/unique constraints to the parti…
- **Mistake:** Skipping `\d` / catalogs and guessing column types in incidents

## Pros/Cons or Trade-offs
- **Pro:** Expressive types reduce external document stores for moderate needs.
- **Con:** JSONB without constraints becomes a junk drawer; GIN indexes cost writes.
- **Trade-off:** `BIGSERIAL` vs `GENERATED … AS IDENTITY` / UUIDs.

## Comparison
- vs [[mysql table]]: InnoDB clusters on PK


### Use cases
- SaaS OLTP schemas with JSONB metadata for optional attributes and GIN for con…
