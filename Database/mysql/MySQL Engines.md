[[mysql engine]] [[MySQL storage]] [[memory engine]]

# MySQL Engines

> Overview of MySQL storage engines—InnoDB for transactional data, specialized engines for caches and archives; `ENGINE=` clause selects per table.

```txt
        MySQL Engines ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** A comparison-style question: name engines, transaction/locking support, and w…

## Sources
- [MySQL Reference Manual — Storage Engines](https://dev.mysql.com/doc/refman/en/storage-engines.html) — deep-dive
- [MySQL Reference Manual — InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — overview

## Key Concepts
- **Per-table engine:** `ENGINE=` and `SHOW ENGINES` availability.
- **Transactions and locking differ by engine.:** 
- **Production default:** InnoDB unless you have a documented exception.

## Technical Details
| Engine | Transactions | Row locking | Typical use |
|--------|--------------|-------------|-------------|
| InnoDB | Yes | Yes | Default OLTP |
| MEMORY | No | Table lock | Temp caches |
| CSV | No | Table lock | Export/import |
| ARCHIVE | No | Row insert only | Compressed logs |

```sql
SHOW ENGINES;
SELECT engine, support FROM information_schema.ENGINES;
```

- Production tables should use **InnoDB** unless you have a documented exceptio…

## Mistakes to Avoid
- **Mistake:** Shipping CSV/MEMORY engines for durable user data
- **Mistake:** Ignoring `SHOW ENGINES` on managed MySQL where some engines are …
- **Mistake:** Assuming “row insert only” ARCHIVE behaves like InnoDB for updat…

## Pros/Cons or Trade-offs
- **Pro:** Flexibility for niche table roles (scratch, archive, CSV exchange).
- **Con:** Mixed engines mean mixed durability and locking semantics—easy to reason wrong under failure.

## Comparison
- vs [[mysql engine]]: overview vs InnoDB-focused leaf. vs [[memory engine]]: M…


### Use cases
- Auditing a legacy schema for non-InnoDB tables before an HA upgrade
