[notes webpage](https://sql.holt.courses/lessons/data/nodejs-and-postgresql)

pg has two ways to connect to a database: a client and a pool.

```sql
\du; -- view current roles
\l; -- list database
\c <db name> ; -- use the database
```

```sql
\dt -- view database
\d <table name>; -- view the columns
```
## Constraints
```mysql
CREATE UNIQUE INDEX unique_fsd_not_null
ON hkAppNotification(floorNumber, shiftName, department)
WHERE floorNumber IS NOT NULL AND shiftName IS NOT NULL AND department IS NOT NULL;

```

