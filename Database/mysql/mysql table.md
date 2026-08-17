[[mysql]] [[mysql columns]] [[key Constraint]] [[Alter table]] [[mysql index]] [[mysql query]]

# mysql table

> InnoDB tables store rows in clustered primary-key order — DDL defines columns, constraints, and indexes that shape every [[mysql query]] plan.

```txt
        mysql table ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Clustered primary key design (narrow, monotonic) and the cost of large `ALTER…

## Sources
- [CREATE TABLE](https://dev.mysql.com/doc/refman/en/create-table.html) — overview
- [Clustered and Secondary Indexes](https://dev.mysql.com/doc/refman/en/innodb-index-types.html) — deep-dive

## Key Concepts
- **Clustered index = table:** Secondary index leaves store primary key values.
- **Narrow monotonic PKs:** Prefer `BIGINT AUTO_INCREMENT` (or UUID strategies that avoid random hotspots…
- **Constraints:** PK, UNIQUE, FK, CHECK (version-dependent enforcement).
- **Charset:** Default `utf8mb4` for modern Unicode.

## Technical Details
```sql
CREATE TABLE orders (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id    BIGINT UNSIGNED NOT NULL,
  total      DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_orders_user (user_id),
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

- Large `ALTER` may rebuild the table

## Mistakes to Avoid
- **Mistake:** Wide, mutable primary keys that inflate every secondary index
- **Mistake:** `ALTER` on huge tables without an online strategy
- **Mistake:** Mixing charsets/collations across related columns

## Pros/Cons or Trade-offs
- **Pro:** Clustered storage makes PK lookups and PK-range scans fast.
- **Con:** Random UUIDs as PK can fragment pages and hurt insert throughput.
- **Trade-off:** Natural vs surrogate keys — correctness/clarity versus insert locality.

## Comparison
- vs heap-organized tables in other engines: InnoDB always clusters on PK (or h…


### Use cases
- Order/payment tables with surrogate BIGINT PKs, FKs to users, and secondary i…
