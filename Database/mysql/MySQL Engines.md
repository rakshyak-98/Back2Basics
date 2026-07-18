`.idb` -> is the InnoDB data file used by MySQL to store individual table data and indexes when `innodb_file_per_table=ON` (default in MySQL 5.6+).
- binary format -> uses InnoDB internal data structure layout (pages, records, B-tree).
- Optimised for Performance, not for inspection.
- Designed for InnoDB engine internals, not for user access.

> [!WARNING]
> Don't try -> moving `.idb` without matching metadata (`.frm` or MySQL 8+ `data dictionary`) .
## CSV
```mysql
CREATE TABLE my_table()
ENGINE=CSV
```
- `/var/lib/mysql/your_db/your_table.ibd` location

```ini
[mysqld]
innodb_file_per_table = 1
```