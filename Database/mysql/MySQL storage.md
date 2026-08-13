[[mysql engine]] [[write-ahead logging]] [[mysql index]] [[Configuration]]

# MySQL storage

> How InnoDB lays out tablespaces, buffer pool pages, redo/undo logs, and doublewrite buffer on disk—the physical layer behind [[mysql transaction]] durability.

## Key components

```txt
Buffer pool (RAM) ──► dirty pages ──► .ibd tablespace files
        │
        └── redo log (#innodb_redo) ──► crash recovery
```

## Tablespaces

- **File-per-table** (`innodb_file_per_table=ON`) — each table gets `.ibd`
- **System tablespace** — data dictionary, undo (version dependent)

## Tuning

- `innodb_buffer_pool_size` — primary memory knob
- `innodb_redo_log_capacity` — write throughput vs checkpoint frequency
- `innodb_flush_log_at_trx_commit=1` for full durability

## Sources

- MySQL Reference Manual — [InnoDB Disk Layout](https://dev.mysql.com/doc/refman/en/innodb-disk-layout.html)
- MySQL Reference Manual — [InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/en/innodb-buffer-pool.html)
