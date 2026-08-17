[[Database]] [[ACID]] [[SQL Configurations]] [[mysql]] [[SQL/postgres]] [[Database design]] [[SQL error]] [[SQL normalization]] [[Alter table]]

# SQL

> Declarative language for relational data — you describe the result or change set; the optimizer picks access paths and the engine enforces [[ACID]] rules inside transactions.

```txt
        SQL ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers test query shape (joins, indexes, CTEs), injection safety, and D…

## Sources
- ISO/IEC 9075 SQL standard — deep-dive
- [PostgreSQL Documentation — SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html) — deep-dive
- [OWASP — SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — overview
- [MySQL Reference Manual — SQL Statements](https://dev.mysql.com/doc/refman/en/sql-statements.html) — overview

## Key Concepts
- **DQL:** `SELECT` — query rows.
- **DML:** `INSERT`, `UPDATE`, `DELETE`, `MERGE` — change data.
- **DDL:** `CREATE`, `ALTER`, `DROP` — schema; see [[Alter table]].
- **DCL:** `GRANT`, `REVOKE` — privileges ([[mysql Privileges]], [[psql privileges]]).
- **TCL:** `BEGIN`, `COMMIT`, `ROLLBACK` — transaction boundaries.
- **Parameterization:** values travel separately from SQL text — mandatory against injection.


- **Core:** SQL is a set-oriented language: statements declare what rows to read or change

## Technical Details
| Family | Purpose |
|--------|---------|
| **DQL** | `SELECT` — query rows |
| **DML** | `INSERT`, `UPDATE`, `DELETE`, `MERGE` |
| **DDL** | `CREATE`, `ALTER`, `DROP` — [[Alter table]] |
| **DCL** | `GRANT`, `REVOKE` |
| **TCL** | `BEGIN`, `COMMIT`, `ROLLBACK` |

- Mental model:

```txt
SQL text ──► parser ──► rewriter ──► planner ──► executor ──► rows
```

- Parameterization:

```python
# Safe — bound parameter
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Unsafe — SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

- *When would you choose a CTE over a subquery?* Readability first; in PostgreS…

- Schema design ties to [[SQL normalization]] and [[Database design]].
- Failures surface as [[SQL error]] codes (SQLSTATE / vendor numbers).

## Mistakes to Avoid
- **Mistake:** Concatenating user input into SQL strings
- **Mistake:** Assuming `SELECT *` is fine on wide tables under load
- **Mistake:** Blind trust in CTEs without checking whether the planner materia…
- **Mistake:** Mixing DDL that locks tables into peak [[OLTP]] traffic without …

## Pros/Cons or Trade-offs
- **Pro:** Portable intent across engines; optimizer absorbs many physical choices.
- **Con:** Vendor dialects diverge; dynamic SQL built by string concat is a security hazard.
- **Trade-off:** Rich declarative SQL vs application-side loops that fight the optimizer.

## Comparison
- vs ORM query builders: ORMs still emit SQL


### Use cases
- API list endpoints use parameterized `SELECT` with keyset pagination
