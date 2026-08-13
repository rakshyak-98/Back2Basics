[[mysql user]] [[mysql]] [[ACL (postgreSQL)]]

# mysql Privileges

> MySQL privilege model—global, database, table, column, routine, and dynamic privileges (`ROLES` in 8.0)—granted with `GRANT` and checked on each statement.

## Grant levels

```sql
GRANT SELECT ON myapp.* TO 'readonly'@'%';
GRANT INSERT, UPDATE ON myapp.orders TO 'writer'@'%';
GRANT EXECUTE ON PROCEDURE myapp.report TO 'report'@'%';
```

## Roles (8.0+)

```sql
CREATE ROLE app_read, app_write;
GRANT SELECT ON myapp.* TO app_read;
GRANT app_read TO 'human'@'%';
SET DEFAULT ROLE ALL TO 'human'@'%';
```

## Compare PostgreSQL

See [[ACL (postgreSQL)]] for `GRANT` on tables, sequences, schemas.

## Sources

- MySQL Reference Manual — [Privileges Provided](https://dev.mysql.com/doc/refman/en/privileges-provided.html)
- MySQL Reference Manual — [GRANT](https://dev.mysql.com/doc/refman/en/grant.html)
