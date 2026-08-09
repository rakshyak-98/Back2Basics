[[postgres]] [[psql user]] [[psql essential]]

# psql user acl

> Postgres ACL strings show who can connect/create/temp on a database — decode `{role=privs/grantor}`.

---

## Index

- [[#Mental model]]
- [[#Interview map (words you can say)]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `\l` / `datacl` prints compact grants; empty role before `=` means `PUBLIC`; letters are privileges; `/grantor` is who granted them.

```txt
drm_streaming | {=Tc/drm_tester,drm_tester=CTc/drm_tester}
                 │                │
                 PUBLIC: T+c      drm_tester: C+T+c
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **PUBLIC** | Everyone (`=` with no name) | “Default CONNECT often comes from PUBLIC.” |
| **c** | CONNECT | “Can open a session to this DB.” |
| **C** | CREATE | “Can create schemas in the DB.” |
| **T** | TEMP | “Can create temporary tables.” |
| **Grantor** | After `/` | “Who granted; revoke needs matching grant.” |

---

## Standard config / commands

```sql
-- See ACLs
\l+
SELECT datname, datacl FROM pg_database WHERE datname = 'drm_streaming';

-- Lock down: strip PUBLIC
REVOKE CONNECT ON DATABASE drm_streaming FROM PUBLIC;
REVOKE TEMPORARY ON DATABASE drm_streaming FROM PUBLIC;
-- or
REVOKE ALL PRIVILEGES ON DATABASE drm_streaming FROM PUBLIC;

GRANT CONNECT ON DATABASE drm_streaming TO app_role;
```

| Knob | Why it matters |
|------|----------------|
| PUBLIC CONNECT | Any login role can reach the DB name |
| Schema USAGE | DB CONNECT alone ≠ table access |
| Default privileges | New objects may still grant to PUBLIC |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied to database | `datacl` / `\l` | GRANT CONNECT; fix `pg_hba.conf` |
| Anyone can connect | `=c/` in ACL | REVOKE CONNECT FROM PUBLIC |
| Can connect, can’t read tables | Schema/table grants | GRANT USAGE ON SCHEMA + table privs |
| Temp tables fail | Missing `T` | GRANT TEMP ON DATABASE … |

---

## Gotchas

> [!WARNING]
> **`pg_hba.conf` is separate** — ACL says “allowed if authenticated”; HBA decides *how* you authenticate (host/user/db).

> [!WARNING]
> **CONNECT ≠ data access** — still need schema USAGE + table privileges.

---

## When NOT to use

- **App-level multi-tenant row filters** — ACL is coarse (DB/schema/table), not row-level alone (use RLS).
- **Replacing secrets rotation** — ACL doesn’t rotate passwords.

---

## Related

[[psql user]] [[psql essential]] [[psql table]] [[postgres]]
