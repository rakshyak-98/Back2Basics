[[mysql]] [[SQL error]] [[mysql query]]

# MySQL Error

> MySQL server error numbers and messages—duplicate key `1062`, deadlock `1213`, lock wait timeout `1205`—mapped to fixes and retry policies.

## Common errors

| Code | Message pattern | Action |
|------|-----------------|--------|
| 1062 | Duplicate entry | Upsert or return 409 |
| 1213 | Deadlock found | Retry transaction |
| 1205 | Lock wait timeout | Shorter txs; index tuning |
| 1040 | Too many connections | [[connection pooling]] |
| 1146 | Table doesn't exist | Migration drift |

## SQLSTATE

MySQL also returns SQLSTATE for portable handling—check driver docs for mapping.

```sql
SHOW WARNINGS;
SHOW ERRORS;
```

## Sources

- MySQL Reference Manual — [Error Message Reference](https://dev.mysql.com/doc/mysql-errors/en/server-error-reference.html)
- MySQL Reference Manual — [Client Error Codes](https://dev.mysql.com/doc/mysql-errors/en/client-error-reference.html)
