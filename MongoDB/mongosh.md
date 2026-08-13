<!-- note-strategy: operational -->
[[MongoDB]] [[mongosh query]] [[mongosh user management]] [[mongodb shell]]

# mongosh

> `mongosh` is the modern MongoDB shell — connect, explore, run scripts against clusters.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** REPL + scripting host that speaks the driver protocol; prefer it over legacy `mongo`.

```txt
mongosh "mongodb://…" → use db → helpers / scripts
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **URI** | Connection string | “Includes auth, DB, options.” |
| **`use`** | Switch database | “Context for `db`.” |
| **`.mjs` scripts** | Automate admin | “Non-interactive CI.” |
| **config** | Snippets / history | “Editor integration.” |

---

## Standard config / commands

```bash
mongosh "mongodb://user:pass@localhost:27017/app?authSource=admin"
mongosh --file migrate.js
```

```js
show dbs
use app
db.stats()
db.users.find().limit(5)
```

| Knob | Why it matters |
|------|----------------|
| `authSource` | Where the user lives |
| `--quiet` | Clean script output |
| Read preference | Secondary reads for heavy ad-hoc |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failed | URI / authSource | Fix user DB and roles |
| TLS errors | CA / allowInvalid | Fix certs; don’t disable in prod |
| Command unknown | old mongosh | Upgrade |
| Slow shell queries | no index / huge result | Limit + index |

---

## Gotchas

> [!WARNING]
> **Paste passwords in shell history** — use config/env / prompting.

> [!WARNING]
> **Running on primary by habit** — heavy analytics can hurt writes.

---

## When NOT to use

- **Application runtime** — use the official driver.
- **Complex application logic** — keep business code out of shell scripts.

## Related

[[mongosh query]] [[mongosh user management]] [[mongodb shell]]
