[[mysql table]] [[mysql json]] [[key Constraint]] [[mysql normalization]]

# mysql columns

> Column definitions—types, nullability, defaults, generated columns, and character sets—that determine storage size, index eligibility, and validation.

## Type selection

| Need | Type |
|------|------|
| Integer IDs | `BIGINT UNSIGNED` |
| Money | `DECIMAL(p,s)` — never `FLOAT` for currency |
| Timestamps | `TIMESTAMP` (session TZ) or `DATETIME` |
| Unicode text | `VARCHAR` with `utf8mb4` |
| Semi-structured | [[mysql json]] `JSON` |

## Defaults and auto-update

```sql
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

Prefer application-managed `updated_at` when triggers are undesirable.

## Generated columns

```sql
ALTER TABLE users ADD full_name VARCHAR(200)
  AS (CONCAT(first_name, ' ', last_name)) STORED;
```

## Sources

- MySQL Reference Manual — [Data Types](https://dev.mysql.com/doc/refman/en/data-types.html)
- MySQL Reference Manual — [CREATE TABLE Column Specifications](https://dev.mysql.com/doc/refman/en/create-table.html)
