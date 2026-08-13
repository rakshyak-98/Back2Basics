[[Database]] [[ACID]] [[database migration]] [[connection pooling]] [[SQL]]

# Database mistakes

> Recurring production failures from treating the database as a dumb file store—autocommit races, missing indexes, untested backups, and schema drift.

## Classic failures

| Mistake | Symptom | Fix direction |
|---------|---------|---------------|
| Read-modify-write without transaction | Oversold inventory, double spend | `BEGIN` … `FOR UPDATE` or optimistic versioning |
| No index on foreign keys | Slow joins and cascading deletes | Index child FK columns |
| `max_connections` without pool | Random timeouts under load | [[connection pooling]] |
| Backups never restored | Data loss discovered during incident | Monthly restore drill |
| Manual prod DDL | Environment drift | [[database migration]] only |
| Storing local time without time zone | DST bugs, wrong expiry | UTC + `timestamptz` |
| Using database as message queue | Table bloat, lock storms | Proper queue (SQS, Kafka) |

## ORM-specific traps

- Lazy loading in loops (N+1)
- `@Transactional` on private methods (no-op in Spring without aspect weaving)
- Assuming `save()` is upsert — may INSERT duplicate

## Sources

- Kleppmann, *DDIA*, Ch. 7–9
- Google SRE Book — [Data Integrity](https://sre.google/sre-book/data-integrity/)
