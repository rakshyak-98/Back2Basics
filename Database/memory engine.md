[[mysql engine]] [[MySQL Engines]] [[MySQL storage]]

# memory engine

> MySQL `MEMORY` (formerly `HEAP`) storage engine—tables live entirely in RAM with table-level locking and no crash durability.

## Characteristics

- Fixed-length rows only (variable types become fixed width internally)
- Data lost on server restart
- `HASH` or `BTREE` indexes
- Table-level locks — poor concurrent write scaling

## Valid uses

- Session scratch tables, temporary caches inside MySQL, read-only lookup tables rebuilt on startup

## Not for production state

Any data that must survive restart belongs in InnoDB ([[mysql engine]]) or an external store.

## Sources

- MySQL Reference Manual — [MEMORY Storage Engine](https://dev.mysql.com/doc/refman/en/memory-storage-engine.html)
