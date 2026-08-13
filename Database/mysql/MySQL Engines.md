[[mysql engine]] [[MySQL storage]] [[memory engine]]

# MySQL Engines

> Overview of MySQL storage engines—InnoDB for transactional data, specialized engines for caches and archives; `ENGINE=` clause selects per table.

## Comparison

| Engine | Transactions | Row locking | Typical use |
|--------|--------------|-------------|-------------|
| InnoDB | Yes | Yes | Default OLTP |
| MEMORY | No | Table lock | Temp caches |
| CSV | No | Table lock | Export/import |
| ARCHIVE | No | Row insert only | Compressed logs |

## Check availability

```sql
SHOW ENGINES;
SELECT engine, support FROM information_schema.ENGINES;
```

Production tables should use **InnoDB** unless you have a documented exception.

## Sources

- MySQL Reference Manual — [Storage Engines](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html)
