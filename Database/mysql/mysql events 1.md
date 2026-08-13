[[MySQL Events]] [[mysql Programmable SQL]]

# mysql events 1

> Supplemental examples for MySQL scheduled events—one-shot events, conditional execution, and privilege requirements alongside [[MySQL Events]].

## One-time event

```sql
CREATE EVENT archive_2024_q1
ON SCHEDULE AT '2025-01-01 00:00:00'
DO
  INSERT INTO archive.orders SELECT * FROM orders WHERE created_at < '2024-04-01';
```

## Permissions

Creating events requires `EVENT` privilege:

```sql
GRANT EVENT ON mydb.* TO 'scheduler'@'%';
```

## Definer security

`DEFINER` clause runs event as another user—review for privilege escalation.

## Sources

- MySQL Reference Manual — [CREATE EVENT](https://dev.mysql.com/doc/refman/en/create-event.html)
