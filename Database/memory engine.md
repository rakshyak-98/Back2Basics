[[mysql engine]] [[MySQL Engines]] [[MySQL storage]] [[ACID]]

# memory engine

> MySQL `MEMORY` (formerly `HEAP`) storage engine—tables live entirely in RAM with table-level locking and no crash durability.

## Interview Relevance

MEMORY engine questions check whether you know it is non-durable and table-locked—valid for scratch/cache tables, never for production durable state. Contrast with InnoDB ([[mysql engine]]).

## Sources

- [MySQL Reference Manual — MEMORY Storage Engine](https://dev.mysql.com/doc/refman/en/memory-storage-engine.html) — deep-dive

## Key Concepts

- **RAM-only tables:** data lost on server restart.
- **Fixed-length rows:** variable types become fixed width internally.
- **Indexes:** `HASH` or `BTREE`.
- **Table-level locks:** poor concurrent write scaling.

## Technical Details

Characteristics:

- Fixed-length rows only (variable types become fixed width internally)
- Data lost on server restart
- `HASH` or `BTREE` indexes
- Table-level locks — poor concurrent write scaling

Valid uses:

- Session scratch tables, temporary caches inside MySQL, read-only lookup tables rebuilt on startup

Not for production state: any data that must survive restart belongs in InnoDB ([[mysql engine]]) or an external store.

```sql
CREATE TABLE session_scratch (
  id INT PRIMARY KEY,
  payload CHAR(255)
) ENGINE=MEMORY;
```

## Real-World Applications

Ephemeral lookup tables rebuilt at startup, or per-session scratch space inside stored procedures. Example: a nightly job loads a small code list into MEMORY for fast joins, then discards it—knowing restart clears it is acceptable.

## Pros/Cons or Trade-offs

- **Pro:** Very fast reads for small working sets; simple for disposable data.
- **Con:** No durability; table locks; memory pressure can affect the whole server.

## Comparison

vs InnoDB ([[mysql engine]]): InnoDB gives row locks, [[ACID]], and crash recovery; MEMORY trades all of that for RAM speed. vs external Redis: Redis is purpose-built for ephemeral shared cache with richer ops tooling than MySQL MEMORY tables.

## Mistakes to Avoid

- Storing user or financial state in MEMORY and discovering it vanished after restart.
- Expecting row-level concurrency under write load.
- Oversizing MEMORY tables until mysqld is OOM-killed.
