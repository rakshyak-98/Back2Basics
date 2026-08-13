[[psql essential]] [[SQL/postgres]] [[Alter table]] [[GIN]]

# psql table

> Creating and inspecting tables in PostgreSQL—data types, constraints, partitions, and `\d` introspection from [[psql essential]].

## Create

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
```

## Inspect

```sql
\d+ orders
SELECT * FROM pg_indexes WHERE tablename = 'orders';
```

## Partitioning

```sql
CREATE TABLE orders_2024 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## Sources

- PostgreSQL Documentation — [CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- PostgreSQL Documentation — [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
