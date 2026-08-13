[[database migration]] [[mysql data migrations]] [[Alter table]] [[Database]]

# migration

> Moving or transforming data and schema between states—includes versioned DDL ([[database migration]]) and one-off data backfills during deploys.

## Two meanings in practice

| Type | Scope | Example |
|------|-------|---------|
| **Schema migration** | DDL version files | Add `email_verified_at` column |
| **Data migration** | Transform existing rows | Split `full_name` into `first_name`, `last_name` |

## Safe data migration pattern

```sql
-- 1. Add nullable column
ALTER TABLE users ADD COLUMN first_name TEXT;

-- 2. Backfill in batches (avoid long locks)
UPDATE users SET first_name = split_part(name, ' ', 1)
WHERE id BETWEEN 1000 AND 1999;

-- 3. Enforce NOT NULL after backfill complete
ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

## Cross-system migration

Moving from MySQL to PostgreSQL or adding a read model requires dual-write or change-data-capture—not a single `pg_dump` during traffic without a cutover plan.

## Sources

- Kleppmann, *DDIA*, Ch. 4
- Martin Fowler, "Evolutionary Database Design"
