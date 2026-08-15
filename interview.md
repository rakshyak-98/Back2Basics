[[mognodb indexing]] [[Database]] [[SQL/postgres]] [[Data structure/Data structure]] [[ISAM]] [[GIN]]

# interview

> Interview indexing notes — functional dependency and the index types you’ll be asked to compare under pressure.

## Interview Relevance
Database interviews almost always hit indexes: what they speed up, what they cost on writes, and how functional dependency relates to keys/normalization. Be ready to sketch B+ trees vs hash vs bitmap.

## Sources
- [PostgreSQL — Indexes](https://www.postgresql.org/docs/current/indexes.html) — deep-dive
- [Wikipedia — Database index](https://en.wikipedia.org/wiki/Database_index) — overview
- [Wikipedia — Functional dependency](https://en.wikipedia.org/wiki/Functional_dependency) — overview

## Core Definition
An index is a secondary structure that finds rows without scanning the whole table. A **functional dependency** `X → Y` means attribute set X determines Y — the foundation of keys and normalization.

## Key Concepts
- **Functional dependency:** If two rows agree on X, they must agree on Y; primary keys determine all attributes.
- **Single-level vs multilevel indexes:** Deep trees (B+ tree) keep fanout high and height low.
- **B+ tree:** Default for range and equality in most RDBMSs.
- **Hash indexes:** Equality-friendly; weak for ranges (engine-dependent).
- **Bitmap:** Good for low-cardinality columns in analytics workloads.
- **Logical vs physical:** Logical design (which columns) vs structure on disk.
- **ISAM:** Classic indexed sequential access method; ancestor ideas to modern trees ([[ISAM]]).

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

Rules of thumb:
- Index columns used in `WHERE` / `JOIN` / `ORDER BY` that matter for latency.
- Every index slows writes and uses disk — measure with `EXPLAIN`.
- Composite indexes: leftmost prefix matters in many engines.
- Specialized: [[GIN]] for full-text/JSONB arrays in Postgres.

JS aside (type peeking, not DB indexing):

```js
Object.getPrototypeOf(value).constructor.name;
```

## Real-World Applications
Slow `orders WHERE customer_id = ? AND created_at > ?` → composite index `(customer_id, created_at)`. Interview follow-up: why `(created_at, customer_id)` may not serve the same filter as well.

## Pros/Cons or Trade-offs
- **Pro:** Turns full scans into logarithmic lookups; enables uniqueness constraints.
- **Con:** Write amplification; wrong indexes unused; over-indexing kills ingest.

## Comparison
vs full table scan: better when selectivity is high. vs covering/index-only scans: include needed columns to skip heap fetch. Related vault: [[mognodb indexing]], [[SQL/postgres]], [[Data structure/Data structure]].

## Mistakes to Avoid
- Indexing every column “just in case.”
- Confusing functional dependency with correlation in statistics.
- Creating indexes that do not match query predicates (wrong order/direction).
- Ignoring write path and vacuum/maintenance cost.
