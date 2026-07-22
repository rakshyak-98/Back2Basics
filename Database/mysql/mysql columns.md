[[mysql/mysql table]] [[Alter table]] [[mysql]]

# MySQL columns

> One-line: column DDL — types, nullability, defaults, order, and comments; full definition required on MODIFY; plan for online schema change.

## Mental model

Columns define **type**, **NULL/NOT NULL**, **DEFAULT**, **AUTO_INCREMENT**, **GENERATED**, charset/collation, and optional **COMMENT**. MySQL stores column order in metadata; reordering can **rebuild table**.

```
Logical table
├── id BIGINT PK AUTO_INCREMENT
├── email VARCHAR(255) NOT NULL
├── created_at DATETIME DEFAULT CURRENT_TIMESTAMP
└── metadata JSON
```

App migrations should match ORM models; production alters go through [[database migration]] with expand-contract for zero-downtime.

## Standard config / commands

### Add column

```sql
ALTER TABLE users
  ADD COLUMN phone VARCHAR(20) NULL COMMENT 'E.164' AFTER email;
```

### Modify (full definition required)

```sql
ALTER TABLE users
  MODIFY COLUMN email VARCHAR(320) NOT NULL COMMENT 'login email';
```

### Reorder

```sql
ALTER TABLE users
  MODIFY COLUMN status TINYINT NOT NULL DEFAULT 1 FIRST;

ALTER TABLE users
  MODIFY COLUMN avatar_url VARCHAR(512) NULL AFTER display_name;
```

### Drop / rename

```sql
ALTER TABLE users DROP COLUMN legacy_flag;
ALTER TABLE users RENAME COLUMN old_name TO new_name;  -- MySQL 8.0+
```

### Inspect

```sql
SHOW FULL COLUMNS FROM users;
DESCRIBE users;
SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users';
```

### Safe add with default (MySQL 8 instant)

```sql
ALTER TABLE big_table
  ADD COLUMN processed TINYINT NOT NULL DEFAULT 0,
  ALGORITHM=INSTANT;
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| MODIFY widens type fails | Data truncation | Clean bad rows first; staged migration |
| Implicit default NULL added | Missing NOT NULL on add | Explicit NULL/NOT NULL in ALTER |
| App breaks after rename | Deploy order | Expand-contract: add new → migrate → drop old |
| Long lock on reorder | Table rebuild | Skip cosmetic reorder; use online tool |
| JSON column slow | No generated index | STORED generated column + index on path |
| Charset garble | column vs table charset | `CONVERT TO CHARACTER SET utf8mb4` |

## Gotchas

> [!WARNING]
> **Partial MODIFY** — omitting `NOT NULL` can silently allow NULLs.

> [!WARNING]
> **AFTER/FIRST triggers rebuild** on many versions — not cosmetic on huge tables.

> [!WARNING]
> **Zero-date defaults** — deprecated; use NULL or explicit TIMESTAMP rules.

## When NOT to use

- **Frequent rename for naming taste** — costly; alias in ORM/view instead.
- **Storing large blobs in row** — object storage or separate table.

## Related

[[Alter table]] [[mysql table]] [[mysql index]] [[database migration]]
