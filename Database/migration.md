[[database migration]] [[mysql data migrations]] [[Alter table]] [[Database]]

# migration

> Moving or transforming data and schema between states—includes versioned DDL ([[database migration]]) and one-off data backfills during deploys.

```txt
        migration ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** “Migration” is overloaded—interviewers want you to split schema vs data migra…

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 4 — deep-dive
- Martin Fowler, "Evolutionary Database Design" — overview

## Key Concepts
- **Schema migration:** versioned DDL files (add column, index).
- **Data migration:** transform existing rows (split names, backfill flags).
- **Batched updates:** avoid long locks with `WHERE id BETWEEN …` chunks.
- **Cross-system:** dual-write or CDC—not a single dump during live traffic without a cutover pla…

## Technical Details
| Type | Scope | Example |
|------|-------|---------|
| **Schema migration** | DDL version files | Add `email_verified_at` column |
| **Data migration** | Transform existing rows | Split `full_name` into `first_name`, `last_name` |

- Safe data migration pattern:

```sql
-- 1. Add nullable column
ALTER TABLE users ADD COLUMN first_name TEXT;

-- 2. Backfill in batches (avoid long locks)
UPDATE users SET first_name = split_part(name, ' ', 1)
WHERE id BETWEEN 1000 AND 1999;

-- 3. Enforce NOT NULL after backfill complete
ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

- Cross-system migration: moving from MySQL to PostgreSQL or adding a read mode…

## Mistakes to Avoid
- **Mistake:** Single huge `UPDATE` without batching
- **Mistake:** Enforcing `NOT NULL` before backfill finishes
- **Mistake:** Cutover with only a dump/restore while writes continue on the ol…

## Pros/Cons or Trade-offs
- **Pro:** Evolutionary change without big-bang downtime when done in expand/contract steps.
- **Con:** Dual-write windows and long backfills add complexity and temporary inconsistency risk.

## Comparison
- vs [[database migration]]: that note focuses on versioned schema tooling


### Use cases
- Splitting a monolithic `name` column during a release train, or migrating a r…
