[[Database]] [[ACID]] [[database migration]] [[connection pooling]] [[SQL]] [[mysql lock]]

# Database mistakes

> Recurring production failures from treating the database as a dumb file store—autocommit races, missing indexes, untested backups, and schema drift.

```txt
        Database mistakes ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** “What goes wrong in production?” questions map directly here

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7–9 — overview
- [Google SRE Book — Data Integrity](https://sre.google/sre-book/data-integrity/) — deep-dive

## Key Concepts
- **Autocommit races:** read-modify-write without a transaction → oversell and double spend.
- **Missing indexes:** especially on foreign keys → slow joins and cascading deletes.
- **Ops hygiene:** pooling, tested restores, migration-only DDL, UTC time
- **Wrong abstraction:** using the database as a message queue → bloat and lock storms.

## Technical Details
| Mistake | Symptom | Fix direction |
|---------|---------|---------------|
| Read-modify-write without transaction | Oversold inventory, double spend | `BEGIN` … `FOR UPDATE` or optimistic versioning |
| No index on foreign keys | Slow joins and cascading deletes | Index child FK columns |
| `max_connections` without pool | Random timeouts under load | [[connection pooling]] |
| Backups never restored | Data loss discovered during incident | Monthly restore drill |
| Manual prod DDL | Environment drift | [[database migration]] only |
| Storing local time without time zone | DST bugs, wrong expiry | UTC + `timestamptz` |
| Using database as message queue | Table bloat, lock storms | Proper queue (SQS, Kafka) |

- ORM-specific traps:

- Lazy loading in loops (N+1)
- `@Transactional` on private methods (no-op in Spring without aspect weaving)
- Assuming `save()` is upsert — may INSERT duplicate

## Mistakes to Avoid
- **Mistake:** Discovering backups do not restore during the outage itself
- **Mistake:** Fixing pool exhaustion by raising `max_connections` without fixi…
- **Mistake:** Shipping ORM code that silently N+1 under production data volume
- **Mistake:** Hotfixing production schema outside the migration tool

## Pros/Cons or Trade-offs
- **Pro:** A checklist prevents repeating industry-standard foot-guns.
- **Con:** Treating the list as complete — new product patterns invent new mistakes; keep measuring.

## Comparison
- vs [[Database design]]: design aims to prevent many of these


### Use cases
- Postmortems after inventory oversell, connection storms, or failed restores. …
