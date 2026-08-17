[[mysql]] [[mysql engine]] [[mysql transaction]] [[SQL]] [[MySQL storage]]

# mysql concepts

> Core MySQL ideas—schema as database, storage engines, replication topology, and binary log—that frame every operational decision.





## Interview Relevance
Concept questions check MySQL vocabulary: database≡schema, binlog vs redo log, primary/replica lag. Foundation for replication and CDC discussions.

## Sources
- [MySQL Reference Manual — Replication](https://dev.mysql.com/doc/refman/en/replication.html) — deep-dive
- [MySQL Reference Manual — Binary Log](https://dev.mysql.com/doc/refman/en/binary-log.html) — deep-dive

## Key Concepts
- **Schema = database:** `CREATE DATABASE` namespaces tables; no separate PostgreSQL-style schema layer (name synonym only).
- **Binary log (binlog):** logical change stream for replicas and CDC.
- **Redo log:** InnoDB physical crash recovery ([[MySQL storage]]).
- **Replication roles:** primary read/write → async replicas; lag is normal.

## Technical Details
`CREATE DATABASE app` creates a namespace for tables. Unlike PostgreSQL, there is no separate "schema" layer inside a database (except naming synonym).

Logical replication ingredients:

- **Binary log (binlog)** — logical change stream for replicas and CDC
- **Redo log** — InnoDB physical crash recovery ([[MySQL storage]])

```txt
Primary (read/write) ──► Replica(s) (async read)
```

Replicas can lag—do not assume read-your-writes on replica without routing logic.

## Real-World Applications
Designing read scaling with replicas and CDC into warehouses. Example: route user profile reads that need read-your-writes to the primary; send analytics queries to a replica and accept lag.

## Pros/Cons or Trade-offs
- **Pro:** Simple mental model; binlog enables replicas and many CDC tools.
- **Con:** Async replicas are not strongly consistent; confusing binlog with redo leads to wrong recovery expectations.

## Comparison
vs PostgreSQL: PostgreSQL separates database and schema objects more clearly; MySQL treats database/schema as synonyms. vs [[mysql engine]]: engines implement storage; these concepts sit above engine choice (though redo is InnoDB-specific).

## Mistakes to Avoid
- Reading from a replica immediately after a write and assuming the row is visible.
- Conflating binlog (replication/CDC) with InnoDB redo (crash recovery).
- Expecting PostgreSQL `search_path` schema patterns to map 1:1 onto MySQL.
