[[MongoDB]] [[mongosh query]] [[mongosh user management]] [[mongodb shell]]

# mongosh

> `mongosh` is the modern MongoDB shell — connect, explore, run scripts against clusters.





## Interview Relevance
mongosh interviews check interactive ops — useful queries, rs/status helpers, and not running dangerous commands blindly.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
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

## Technical Details
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

## Pros/Cons or Trade-offs
- **Application runtime** — use the official driver.
- **Complex application logic** — keep business code out of shell scripts.

## Mistakes to Avoid
> [!WARNING]
> **Paste passwords in shell history** — use config/env / prompting.

> [!WARNING]
> **Running on primary by habit** — heavy analytics can hurt writes.

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failed | URI / authSource | Fix user DB and roles |
| TLS errors | CA / allowInvalid | Fix certs; don’t disable in prod |
| Command unknown | old mongosh | Upgrade |
| Slow shell queries | no index / huge result | Limit + index |
