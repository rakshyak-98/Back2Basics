[[Database]] [[ACID]] [[database migration]] [[connection pooling]] [[SQL]] [[mysql lock]]

# Database mistakes

> Recurring production failures from treating the database as a dumb file store—autocommit races, missing indexes, untested backups, and schema drift.





## Interview Relevance
“What goes wrong in production?” questions map directly here. Naming the mistake, the symptom, and the fix direction shows operational judgment beyond textbook [[ACID]] definitions.

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7–9 — overview
- [Google SRE Book — Data Integrity](https://sre.google/sre-book/data-integrity/) — deep-dive

## Key Concepts
- **Autocommit races:** read-modify-write without a transaction → oversell and double spend.
- **Missing indexes:** especially on foreign keys → slow joins and cascading deletes.
- **Ops hygiene:** pooling, tested restores, migration-only DDL, UTC time — skip any and incidents follow.
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

ORM-specific traps:

- Lazy loading in loops (N+1)
- `@Transactional` on private methods (no-op in Spring without aspect weaving)
- Assuming `save()` is upsert — may INSERT duplicate

## Real-World Applications
Postmortems after inventory oversell, connection storms, or failed restores. Example: incident review finds three autocommit UPDATEs for stock decrement; fix wraps them in one transaction with `FOR UPDATE` ([[mysql lock]] patterns).

## Pros/Cons or Trade-offs
- **Pro:** A checklist prevents repeating industry-standard foot-guns.
- **Con:** Treating the list as complete — new product patterns invent new mistakes; keep measuring.

## Comparison
vs [[Database design]]: design aims to prevent many of these; this note catalogs failure modes when design or ops slip. vs [[ACID]]: knowing ACID is necessary but not sufficient if boundaries and indexes are wrong.

## Mistakes to Avoid
- Discovering backups do not restore during the outage itself.
- Fixing pool exhaustion by raising `max_connections` without fixing query hold time.
- Shipping ORM code that silently N+1 under production data volume.
- Hotfixing production schema outside the migration tool.
