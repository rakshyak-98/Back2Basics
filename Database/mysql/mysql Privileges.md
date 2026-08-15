[[mysql user]] [[mysql]] [[ACL (postgreSQL)]] [[psql privileges]]

# mysql Privileges

> MySQL privilege model — global, database, table, column, and routine grants checked on each statement so accounts only do what you allow.

## Interview Relevance
Interviewers probe least-privilege design, `GRANT` levels, and MySQL 8 roles versus “give the app root.” Expect a concrete grant example and how privileges differ from PostgreSQL’s role/ACL model ([[ACL (postgreSQL)]]).

## Sources
- [MySQL Privileges Provided](https://dev.mysql.com/doc/refman/en/privileges-provided.html) — overview
- [MySQL GRANT](https://dev.mysql.com/doc/refman/en/grant.html) — deep-dive
- [MySQL Roles](https://dev.mysql.com/doc/refman/en/roles.html) — deep-dive

## Key Concepts
- **Privilege scopes:** Global (`*.*`), database (`db.*`), table, column, and routine — grant the narrowest scope that still works.
- **Roles (8.0+):** Named privilege bundles assigned to users; activate with `SET ROLE` / default roles.
- **Dynamic privileges:** Fine-grained admin rights (e.g. `CONNECTION_ADMIN`) separate from the old “superuser dump.”
- **Host part matters:** `'app'@'10.%'` is a different account from `'app'@'%'`.

## Technical Details
```sql
GRANT SELECT ON myapp.* TO 'readonly'@'%';
GRANT INSERT, UPDATE ON myapp.orders TO 'writer'@'%';
GRANT EXECUTE ON PROCEDURE myapp.report TO 'report'@'%';

CREATE ROLE app_read, app_write;
GRANT SELECT ON myapp.* TO app_read;
GRANT app_read TO 'human'@'%';
SET DEFAULT ROLE ALL TO 'human'@'%';
```

Inspect with `SHOW GRANTS FOR 'user'@'host'`. After grant changes in older workflows, `FLUSH PRIVILEGES` reloads grant tables when not using `CREATE USER`/`GRANT` paths that auto-reload.

## Real-World Applications
Read-only reporting users get `SELECT` only; the API user gets DML on app schemas; humans inherit roles rather than one-off grants copied per person.

## Pros/Cons or Trade-offs
- **Pro:** Granular scopes and roles reduce blast radius when credentials leak.
- **Con:** Too many overlapping grants become hard to audit; prefer role composition over long personal grant lists.
- **Trade-off:** Column-level grants are precise but fragile when schemas change often.

## Comparison
vs [[ACL (postgreSQL)]] / [[psql privileges]]: MySQL keys accounts as `user`@`host` with privilege tables; PostgreSQL uses roles, schemas, and catalog ACLs (`relacl`), plus optional row-level security.

## Mistakes to Avoid
- Granting `ALL PRIVILEGES ON *.*` to application users.
- Forgetting the host part and wondering why login from another subnet fails.
- Assuming `FLUSH PRIVILEGES` is always required after modern `GRANT` (it is not always).
