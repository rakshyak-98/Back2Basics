[[mysql]] [[mysql index]] [[show query]] [[SQL]] [[covering index]]

# mysql query

> Running [[SQL]] on MySQL — read `EXPLAIN` plans, bind parameters, and shape predicates so the optimizer can use indexes instead of full scans.

```txt
        mysql query ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Almost every backend interview: interpret `EXPLAIN`, avoid functions on index…

## Sources
- [EXPLAIN Output](https://dev.mysql.com/doc/refman/en/explain-output.html) — deep-dive
- [Optimization](https://dev.mysql.com/doc/refman/en/optimization.html) — overview

## Key Concepts
- **Optimizer chooses access path:** Your job is selective predicates + useful indexes ([[mysql index]]).
- **Parameterized queries:** Values separate from SQL text — injection-safe and plan-friendly.
- **Bad smells in plans:** `type: ALL` on large tables; heavy `Using filesort` / `Using temporary`.
- **Covering indexes:** Select only needed columns ([[covering index]]).

## Technical Details
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42 AND status = 'open';

PREPARE stmt FROM 'SELECT id FROM users WHERE email = ?';
SET @email = 'a@b.com';
EXECUTE stmt USING @email;
```

- Hot-path checklist:

- Filter columns indexed and selective
- Avoid `WHERE YEAR(created_at)=2024` on an indexed timestamp — use a range
- Prefer driver bind APIs over string building

## Mistakes to Avoid
- **Mistake:** SQL injection via string concatenation
- **Mistake:** Selecting `*` on wide rows when a covering index would suffice
- **Mistake:** Shipping queries never inspected under production-like data volu…

## Pros/Cons or Trade-offs
- **Pro:** Declarative SQL lets the optimizer adapt as statistics change.
- **Con:** Subtle predicate changes can silently disable indexes.
- **Trade-off:** Hinting / forcing indexes vs fixing schema and statistics.

## Comparison
- vs ORM-generated SQL: ORMs are fine until N+1 or non-sargable predicates appe…


### Use cases
- Latency regressions traced with [[show query]] + `EXPLAIN ANALYZE`, then fixe…
