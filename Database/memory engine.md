[[mysql/MySQL Engines]] [[mysql/mysql engine]] [[mysql]]

# MEMORY storage engine (MySQL)

> One-line: table data lives in RAM only — microsecond reads for temp/session data; gone on restart; strict type/size limits.

## Mental model

MySQL **MEMORY** (historically HEAP) stores rows in memory hash or fixed structure. No durable on-disk data file for table contents — **full loss on restart/crash**. Optimizer may still use MEMORY for internal temp tables.

```
DISK (InnoDB)     vs     MEMORY
persistent               ephemeral
MVCC, FK                 table-level lock (legacy)
TEXT/BLOB                limited types
```

Also distinguish **InnoDB buffer pool** (cached disk pages) — that's not the MEMORY engine.

## Standard config / commands

### Create MEMORY table

```sql
CREATE TABLE session_cache (
  session_id CHAR(64) PRIMARY KEY,
  payload JSON,
  expires_at DATETIME
) ENGINE=MEMORY;
```

### Size limits

```ini
# my.cnf
max_heap_table_size = 64M      # per table cap
tmp_table_size = 64M           # internal temp table threshold
```

```sql
SHOW VARIABLES LIKE 'max_heap_table_size';
SHOW VARIABLES LIKE 'tmp_table_size';
```

### When internal temp becomes MEMORY

```sql
EXPLAIN ANALYZE SELECT ... GROUP BY huge ...;
-- if result set fits limits → MEMORY temp; else disk temp (InnoDB/MyISAM)
```

### Prefer InnoDB for "cache" in modern apps

```sql
-- Redis/Memcached for session cache; InnoDB for durable cache with TTL job
CREATE TABLE cache (
  k VARCHAR(255) PRIMARY KEY,
  v MEDIUMBLOB,
  expires_at TIMESTAMP,
  INDEX (expires_at)
) ENGINE=InnoDB;
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Table empty after restart | Expected MEMORY behavior | Move to InnoDB/Redis; accept ephemeral |
| `table is full` | `max_heap_table_size` | Raise limit or shard; move to InnoDB |
| Can't use TEXT/BLOB column | ENGINE limitation | VARCHAR up to row limit or external store |
| No AUTO_INCREMENT (older) | Engine limits | Use InnoDB or app-generated ids |
| Lock contention | Table-level locks | Switch engine or reduce scope |
| OOM on server | Huge MEMORY table | Cap rows; use Redis with eviction |

## Gotchas

> [!WARNING]
> **Replication** — MEMORY tables on replica also volatile; not a durable replica of data.

> [!WARNING]
> **Fixed row format** — VARCHAR stored fixed width; can waste RAM.

> [!WARNING]
> **Default engine** — always specify `ENGINE=` explicitly in migrations.

## When NOT to use

- **Anything that must survive restart** — InnoDB or external cache.
- **Large datasets** — RAM-bound; use InnoDB + buffer pool instead.
- **Production session store at scale** — Redis/Memcached with TTL/eviction policies.

## Related

[[mysql/MySQL Engines]] [[mysql/mysql engine]] [[Redis/redis installation]] [[Database mistakes]]
