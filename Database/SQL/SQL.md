[[Database]] [[ACID]] [[SQL Configurations]] [[mysql]] [[SQL/postgres]] [[Database design]]

# SQL

> Declarative language for relational data—you specify the result set or change set; the optimizer chooses access paths and enforces [[ACID]] rules inside transactions.

## Core command families

| Family | Purpose |
|--------|---------|
| **DQL** | `SELECT` — query rows |
| **DML** | `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| **DDL** | `CREATE`, `ALTER`, `DROP` — [[Alter table]] |
| **DCL** | `GRANT`, `REVOKE` — [[mysql Privileges]] / [[psql privileges]] |
| **TCL** | `BEGIN`, `COMMIT`, `ROLLBACK` |

## Parameterization is mandatory

Never concatenate user input into SQL strings. Use bound parameters so values are sent separately from the query plan.

```python
# Safe
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Unsafe — SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## Mental model

```txt
SQL text ──► parser ──► rewriter ──► planner ──► executor ──► rows
```

*When would you choose a CTE over a subquery?* Readability and sometimes optimization fences (`MATERIALIZED` in PostgreSQL).

## Sources

- ISO/IEC 9075 SQL standard
- PostgreSQL Documentation — [SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html)
- OWASP — [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
