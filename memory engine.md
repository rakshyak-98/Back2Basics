-> stores all data in RAM instead of on disk.
-> used for Temp/cache tables, session data, fast lookups.

> [!INFO] Edge cases
> - Limited by `max_heap_table_size`
> - No support for `TEXT`, `BLOB`, `AUTO_INCREMENT`
> - Data wiped on MySQL restart or crash