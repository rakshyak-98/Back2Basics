[[Database]] [[ACID]] [[SQL Configurations]] [[mysql]] [[SQL/postgres]] [[Database design]] [[SQL error]] [[SQL normalization]] [[Alter table]]

# SQL

> Declarative language for relational data — you describe the result or change set; the optimizer picks access paths and the engine enforces [[ACID]] rules inside transactions.

## Interview Relevance

Interviewers test query shape (joins, indexes, CTEs), injection safety, and DDL vs DML awareness. Signal: you parameterize every user value, read plans, and know when a CTE is a readability tool versus an optimization fence.

## Sources

- ISO/IEC 9075 SQL standard — deep-dive
- [PostgreSQL Documentation — SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html) — deep-dive
- [OWASP — SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — overview
- [MySQL Reference Manual — SQL Statements](https://dev.mysql.com/doc/refman/en/sql-statements.html) — overview

## Core Definition

SQL is a set-oriented language: statements declare what rows to read or change; the parser, rewriter, planner, and executor turn that into physical operations under transaction control.

## Key Concepts

- **DQL:** `SELECT` — query rows.
- **DML:** `INSERT`, `UPDATE`, `DELETE`, `MERGE` — change data.
- **DDL:** `CREATE`, `ALTER`, `DROP` — schema; see [[Alter table]].
- **DCL:** `GRANT`, `REVOKE` — privileges ([[mysql Privileges]], [[psql privileges]]).
- **TCL:** `BEGIN`, `COMMIT`, `ROLLBACK` — transaction boundaries.
- **Parameterization:** values travel separately from SQL text — mandatory against injection.

## Technical Details

| Family | Purpose |
|--------|---------|
| **DQL** | `SELECT` — query rows |
| **DML** | `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| **DDL** | `CREATE`, `ALTER`, `DROP` — [[Alter table]] |
| **DCL** | `GRANT`, `REVOKE` |
| **TCL** | `BEGIN`, `COMMIT`, `ROLLBACK` |

Mental model:

```txt
SQL text ──► parser ──► rewriter ──► planner ──► executor ──► rows
```

Parameterization:

```python
# Safe — bound parameter
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Unsafe — SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

*When would you choose a CTE over a subquery?* Readability first; in PostgreSQL, `MATERIALIZED` / `NOT MATERIALIZED` can fence or allow inlining — measure with `EXPLAIN`.

Schema design ties to [[SQL normalization]] and [[Database design]]. Failures surface as [[SQL error]] codes (SQLSTATE / vendor numbers).

## Real-World Applications

API list endpoints use parameterized `SELECT` with keyset pagination; migrations use DDL in controlled windows; reporting uses read-only roles via DCL so analysts cannot mutate production tables.

## Pros/Cons or Trade-offs

- **Pro:** Portable intent across engines; optimizer absorbs many physical choices.
- **Con:** Vendor dialects diverge; dynamic SQL built by string concat is a security hazard.
- **Trade-off:** Rich declarative SQL vs application-side loops that fight the optimizer.

## Comparison

vs ORM query builders: ORMs still emit SQL — parameterization and N+1 still matter. vs [[OLAP]] engines: same language family, different storage (columnar) and cost models. vs stored procedures: logic moves into the database; harder to version and test than app code for many teams.

## Mistakes to Avoid

- Concatenating user input into SQL strings.
- Assuming `SELECT *` is fine on wide tables under load.
- Blind trust in CTEs without checking whether the planner materializes them.
- Mixing DDL that locks tables into peak [[OLTP]] traffic without online strategies.
