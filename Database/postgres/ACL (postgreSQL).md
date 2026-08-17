[[psql privileges]] [[psql user]] [[mysql Privileges]] [[SQL/postgres]]

# ACL (postgreSQL)

> PostgreSQL access control lists — privileges stored in the catalog on each object, evaluated per statement from role membership and `SET ROLE`.

```txt
        ACL (postgreSQL) ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Shows whether you understand role-based grants, reading `relacl`, and how row…

## Sources
- [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html) — overview
- [Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — deep-dive

## Key Concepts
- **ACL in catalogs:** e.g. `pg_class.relacl` lists grantee/grantor privilege bits.
- **Object types:** Tables, sequences, schemas, functions — each with its privilege set.
- **Role membership:** Privileges flow through `GRANT role TO role`.
- **RLS:** Row policies further filter visible/updatable rows — orthogonal to `GRANT`.

## Technical Details
```sql
SELECT relname, relacl FROM pg_class WHERE relname = 'orders';
```

| Object | Privileges |
|--------|------------|
| Table | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER |
| Sequence | USAGE, SELECT, UPDATE |
| Schema | USAGE, CREATE |
| Function | EXECUTE |

- Privilege letters in ACL strings include forms like `arwdDxt` for tables

## Mistakes to Avoid
- **Mistake:** Granting on tables but not `USAGE` on the schema or sequences
- **Mistake:** Assuming `GRANT SELECT` alone enforces multi-tenant isolation (n…
- **Mistake:** Auditing only `psql` `\dp` once and never after migrations creat…

## Pros/Cons or Trade-offs
- **Pro:** Fine-grained, schema-native security model.
- **Con:** Default privileges and sequence grants are easy to forget — apps fail on `nextval`.
- **Trade-off:** RLS power vs policy complexity and planning overhead.

## Comparison
- vs [[mysql Privileges]]: MySQL uses `user`@`host` privilege tables


### Use cases
- App roles get DML on `app` schema
