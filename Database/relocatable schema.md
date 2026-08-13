<!-- note-strategy: operational -->
[[Database]] [[Database design]] [[SQL normalization]]

# relocatable schema

> Schema objects you can move or rename without rewriting app SQL — names and search paths stay portable.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Don’t hardcode `db.schema.table` (or absolute paths) in application code; resolve objects via configuration, search_path, or a stable logical name so dumps/moves don’t break callers.

```txt
App ──► logical name / search_path ──► physical schema
              ▲
         env / config (not baked into queries)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Relocatable** | Objects move without app rewrite | “We bind schema via config, not string literals.” |
| **search_path** | Postgres name resolution order | “Omit schema; set path per role/tenant.” |
| **Qualified name** | `schema.table` hard-wired | “Moves and renames force a code sweep.” |
| **Logical vs physical** | App name vs storage location | “Migrations change physical; logical stays.” |

---

## Standard config / commands

```sql
-- Postgres: resolve unqualified names
SET search_path TO app, public;
SELECT * FROM users;  -- app.users if present
```

```js
// App: schema from env, not hardcoded
const schema = process.env.DB_SCHEMA || 'public'
await db.query(`SELECT * FROM ${schema}.users WHERE id = $1`, [id])
// Prefer ORM/schema config over string concat when possible
```

| Knob | Why it matters |
|------|----------------|
| `search_path` / default schema | Lets dumps land under a new schema without rewriting SQL |
| Connection `database` / catalog | Relocate across DBs only if apps don’t embed catalog names |
| Migrations | Own DDL; apps only own DML against stable names |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Relation does not exist | `show search_path` / current schema | Qualify or set path; fix deploy env |
| Works in prod, fails in staging | Hardcoded schema in SQL | Drive schema from config |
| Restore into new schema breaks app | Dump has `SET search_path` / qualified names | Strip quals or rewrite dump; set path on role |
| Cross-DB copy fails FKs | Objects reference old catalog | Relocate within one DB first; fix FKs |

---

## Gotchas

> [!WARNING]
> **Not the same as relocatable machine code** — that linker concept is unrelated; here it means portable *database* naming.

> [!WARNING]
> **Extensions and `public`** — some objects always land in `public`; moving them needs explicit `ALTER … SET SCHEMA`.

---

## When NOT to use

- **Single fixed schema forever** — hardcoding `public.` is fine for a tiny internal tool.
- **You need strong tenant isolation** — separate DBs/roles beat one shared relocatable schema.

---

## Related

[[Database design]] [[SQL normalization]] [[psql table]] [[ACL (postgreSQL)]] [[migration]]
