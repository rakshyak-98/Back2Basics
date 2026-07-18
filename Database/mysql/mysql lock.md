`LOCK TABLES` -> manually locks entire tables to control concurrency.

```txt
LOCK TABLES table_name [READ | WRITE];
```

**Read lock**
- others can read
- others cannot write
- you also cannot write to the table
- used for consistent reads

**Write lock**
- others cannot read or write
- you can read & write
- Ensures exclusive write access

## Row locking

```sql
SELECT TRANSACTION;

SELECT * FROM INVENTORY
WHERE room_type_id = 101 AND date = "2026-04-25"
FOR UPDATE;

UPDATE inventory
SET available = available - 1
WHERE room_type_id = 101 AND date = "2026-04-25";

COMMIT:
```
- Other transactions trying `FOR UPDATE` wait.

### Shared lock

```sql
STAET TRANSACTION;

SELECT * FROM inventory
WHERE room_type_id = 101
FOR SHARE;

COMMIT:
```
- allow reads
- blocks writes