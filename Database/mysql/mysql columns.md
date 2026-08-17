[[mysql table]] [[mysql json]] [[key Constraint]] [[mysql normalization]]

# mysql columns

> Column definitions—types, nullability, defaults, generated columns, and character sets—that determine storage size, index eligibility, and validation.

```txt
        mysql columns ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Type-choice questions (money as `DECIMAL`, `utf8mb4`, timestamp pitfalls) sep…

## Sources
- [MySQL Reference Manual — Data Types](https://dev.mysql.com/doc/refman/en/data-types.html) — deep-dive
- [MySQL Reference Manual — CREATE TABLE Column Specifications](https://dev.mysql.com/doc/refman/en/create-table.html) — overview

## Key Concepts
- **Type selects storage and semantics:** integers, decimals, temporal, text, JSON.
- **Nullability and defaults:** control required fields and auto timestamps.
- **Character set:** `utf8mb4` for full Unicode (emoji).
- **Generated columns:** derived values, optionally indexed (STORED/VIRTUAL).

## Technical Details
| Need | Type |
|------|------|
| Integer IDs | `BIGINT UNSIGNED` |
| Money | `DECIMAL(p,s)` — never `FLOAT` for currency |
| Timestamps | `TIMESTAMP` (session TZ) or `DATETIME` |
| Unicode text | `VARCHAR` with `utf8mb4` |
| Semi-structured | [[mysql json]] `JSON` |

- Defaults and auto-update:

```sql
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

- Prefer application-managed `updated_at` when triggers are undesirable.

- Generated columns:

```sql
ALTER TABLE users ADD full_name VARCHAR(200)
  AS (CONCAT(first_name, ' ', last_name)) STORED;
```

## Mistakes to Avoid
- **Mistake:** Storing money in `FLOAT`/`DOUBLE`
- **Mistake:** Using `utf8` (3-byte) instead of `utf8mb4` and breaking emoji
- **Mistake:** Relying on client local time instead of explicit UTC strategy fo…

## Pros/Cons or Trade-offs
- **Pro:** Right types prevent subtle bugs (float money, truncated emoji) and enable indexes.
- **Con:** Wrong temporal type/`TIMESTAMP` session TZ surprises; overly wide `VARCHAR` wastes InnoDB row estimates.

## Comparison
- vs [[key Constraint]]: columns define shape


### Use cases
- Defining an orders table with money, status, and audit timestamps
