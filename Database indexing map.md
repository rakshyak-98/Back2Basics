[[mognodb indexing]] [[Database]] [[SQL/postgres]] [[Data structure/Data structure]] [[ISAM]] [[GIN]]

# Database indexing map

> Database indexing notes — functional dependency and index types compared under pressure.

```txt
        Database indexing ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Database reviews almost always hit indexes: what they speed up, what they …

## Sources
- [PostgreSQL — Indexes](https://www.postgresql.org/docs/current/indexes.html) — deep-dive
- [Wikipedia — Database index](https://en.wikipedia.org/wiki/Database_index) — overview
- [Wikipedia — Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency) — overview

## Key Concepts
- **Functional dependency:** If two rows agree on X, they must agree on Y
- **Single-level vs multilevel indexes:** Deep trees (B+ tree) keep fanout high and height low.
- **B+ tree:** Default for range and equality in most RDBMSs.
- **Hash indexes:** Equality-friendly; weak for ranges (engine-dependent).
- **Bitmap:** Good for low-cardinality columns in analytics workloads.
- **Logical vs physical:** Logical design (which columns) vs structure on disk.
- **ISAM:** Classic indexed sequential access method


- **Core:** An index is a secondary structure that finds rows without scanning the whole …

## Technical Details
```txt
Query predicate
      │
      ▼
Index lookup (B+ / hash / bitmap / GIN…)
      │
      ▼
Heap / table row fetch (unless index-only scan)
```

- Rules of thumb:

- Index columns used in `WHERE` / `JOIN` / `ORDER BY` that matter for latency.
- Every index slows writes and uses disk — measure with `EXPLAIN`.
- Composite indexes: leftmost prefix matters in many engines.
- Specialized: [[GIN]] for full-text/JSONB arrays in Postgres.

- JS aside (type peeking, not DB indexing):

```js
Object.getPrototypeOf(value).constructor.name;
```

## Mistakes to Avoid
- **Mistake:** Indexing every column “just in case.”
- **Mistake:** Confusing functional dependency with correlation in statistics
- **Mistake:** Creating indexes that do not match query predicates (wrong order…
- **Mistake:** Ignoring write path and vacuum/maintenance cost

## Pros/Cons or Trade-offs
- **Pro:** Turns full scans into logarithmic lookups; enables uniqueness constraints.
- **Con:** Write amplification; wrong indexes unused; over-indexing kills ingest.

## Comparison
- vs full table scan: better when selectivity is high


### Use cases
- Slow `orders WHERE customer_id = ? AND created_at > ?` → composite index `(cu…
