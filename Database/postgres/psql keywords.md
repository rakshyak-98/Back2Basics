[[psql essential]] [[SQL]] [[SQL/postgres]]

# psql keywords

> Reserved and unreserved SQL keywords in PostgreSQL—identifiers that require quoting when used as table or column names.

## Quoting rules

```sql
SELECT "user".id FROM "user";  -- "user" is reserved
SELECT * FROM my_table;        -- lowercase unquoted folds to lowercase
```

## Check reserved status

```sql
SELECT word FROM pg_get_keywords() WHERE word = 'user';
```

## Style guidance

Avoid reserved words in schema design (`user` → `app_user`). If unavoidable, quote consistently in all SQL.

## Sources

- PostgreSQL Documentation — [SQL Key Words](https://www.postgresql.org/docs/current/sql-keywords-appendix.html)
- PostgreSQL Documentation — [Identifiers and Key Words](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
