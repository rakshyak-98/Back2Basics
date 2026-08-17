[[mysql engine]] [[MySQL Engines]] [[MySQL storage]] [[ACID]]

# memory engine

> MySQL `MEMORY` (formerly `HEAP`) storage engine—tables live entirely in RAM with table-level locking and no crash durability.

```txt
        memory engine ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** MEMORY engine questions check whether you know it is non-durable and table-lo…

## Sources
- [MySQL Reference Manual — MEMORY Storage Engine](https://dev.mysql.com/doc/refman/en/memory-storage-engine.html) — deep-dive

## Key Concepts
- **RAM-only tables:** data lost on server restart.
- **Fixed-length rows:** variable types become fixed width internally.
- **Indexes:** `HASH` or `BTREE`.
- **Table-level locks:** poor concurrent write scaling.

## Technical Details
- Characteristics:

- Fixed-length rows only (variable types become fixed width internally)
- Data lost on server restart
- `HASH` or `BTREE` indexes
- Table-level locks — poor concurrent write scaling

- Valid uses:

- Session scratch tables, temporary caches inside MySQL, read-only lookup table…

- Not for production state: any data that must survive restart belongs in InnoD…

```sql
CREATE TABLE session_scratch (
  id INT PRIMARY KEY,
  payload CHAR(255)
) ENGINE=MEMORY;
```

## Mistakes to Avoid
- **Mistake:** Storing user or financial state in MEMORY and discovering it van…
- **Mistake:** Expecting row-level concurrency under write load
- **Mistake:** Oversizing MEMORY tables until mysqld is OOM-killed

## Pros/Cons or Trade-offs
- **Pro:** Very fast reads for small working sets; simple for disposable data.
- **Con:** No durability; table locks; memory pressure can affect the whole server.

## Comparison
- vs InnoDB ([[mysql engine]]): InnoDB gives row locks, [[ACID]], and crash rec…


### Use cases
- Ephemeral lookup tables rebuilt at startup, or per-session scratch space insi…
