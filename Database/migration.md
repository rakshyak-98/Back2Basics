[[database migration]] [[mysql data migrations]] [[Alter table]] [[Database]]

# migration

> Moving or transforming data and schema between states—includes versioned DDL ([[database migration]]) and one-off data backfills during deploys.





## Interview Relevance
“Migration” is overloaded—interviewers want you to split schema vs data migrations, describe batched backfills, and outline cross-system cutovers (dual-write/CDC), not just `mysqldump`.

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 4 — deep-dive
- Martin Fowler, "Evolutionary Database Design" — overview

## Key Concepts
- **Schema migration:** versioned DDL files (add column, index).
- **Data migration:** transform existing rows (split names, backfill flags).
- **Batched updates:** avoid long locks with `WHERE id BETWEEN …` chunks.
- **Cross-system:** dual-write or CDC—not a single dump during live traffic without a cutover plan.

## Technical Details
| Type | Scope | Example |
|------|-------|---------|
| **Schema migration** | DDL version files | Add `email_verified_at` column |
| **Data migration** | Transform existing rows | Split `full_name` into `first_name`, `last_name` |

Safe data migration pattern:

```sql
-- 1. Add nullable column
ALTER TABLE users ADD COLUMN first_name TEXT;

-- 2. Backfill in batches (avoid long locks)
UPDATE users SET first_name = split_part(name, ' ', 1)
WHERE id BETWEEN 1000 AND 1999;

-- 3. Enforce NOT NULL after backfill complete
ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

Cross-system migration: moving from MySQL to PostgreSQL or adding a read model requires dual-write or change-data-capture—not a single `pg_dump` during traffic without a cutover plan.

## Real-World Applications
Splitting a monolithic `name` column during a release train, or migrating a read model to a new store. Example: expand schema, backfill in 10k-row batches overnight, then flip reads and drop the old column next week.

## Pros/Cons or Trade-offs
- **Pro:** Evolutionary change without big-bang downtime when done in expand/contract steps.
- **Con:** Dual-write windows and long backfills add complexity and temporary inconsistency risk.

## Comparison
vs [[database migration]]: that note focuses on versioned schema tooling; this note covers both schema and data movement meanings. vs [[Alter table]]: ALTER is one DDL tool used inside a migration plan.

## Mistakes to Avoid
- Single huge `UPDATE` without batching — long locks and replication lag.
- Enforcing `NOT NULL` before backfill finishes.
- Cutover with only a dump/restore while writes continue on the old system.
