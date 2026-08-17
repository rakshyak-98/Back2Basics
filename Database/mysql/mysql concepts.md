[[mysql]] [[mysql engine]] [[mysql transaction]] [[SQL]] [[MySQL storage]]

# mysql concepts

> Core MySQL ideas—schema as database, storage engines, replication topology, and binary log—that frame every operational decision.

```txt
        mysql concepts ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Concept questions check MySQL vocabulary: database≡schema, binlog vs redo log…

## Sources
- [MySQL Reference Manual — Replication](https://dev.mysql.com/doc/refman/en/replication.html) — deep-dive
- [MySQL Reference Manual — Binary Log](https://dev.mysql.com/doc/refman/en/binary-log.html) — deep-dive

## Key Concepts
- **Schema = database:** `CREATE DATABASE` namespaces tables
- **Binary log (binlog):** logical change stream for replicas and CDC.
- **Redo log:** InnoDB physical crash recovery ([[MySQL storage]]).
- **Replication roles:** primary read/write → async replicas; lag is normal.

## Technical Details
- `CREATE DATABASE app` creates a namespace for tables.
- Unlike PostgreSQL, there is no separate "schema" layer inside a database (exc…

- Logical replication ingredients:

- **Binary log (binlog):** — logical change stream for replicas and CDC
- **Redo log:** — InnoDB physical crash recovery ([[MySQL storage]])

```txt
Primary (read/write) ──► Replica(s) (async read)
```

- Replicas can lag—do not assume read-your-writes on replica without routing lo…

## Mistakes to Avoid
- **Mistake:** Reading from a replica immediately after a write and assuming th…
- **Mistake:** Conflating binlog (replication/CDC) with InnoDB redo (crash reco…
- **Mistake:** Expecting PostgreSQL `search_path` schema patterns to map 1:1 on…

## Pros/Cons or Trade-offs
- **Pro:** Simple mental model; binlog enables replicas and many CDC tools.
- **Con:** Async replicas are not strongly consistent; confusing binlog with redo leads to wrong recovery expectations.

## Comparison
- vs PostgreSQL: PostgreSQL separates database and schema objects more clearly


### Use cases
- Designing read scaling with replicas and CDC into warehouses. Example: route …
