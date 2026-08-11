[[MongoDB]] [[mongosh]] [[MongoDB query validation]]

# mongodb shell

> The legacy `mongo` shell runs JS against the server — prefer [[mongosh]] on modern installs; same admin patterns.

---

## Mental model

**Say it in one breath:** Connect, pick a DB, run helpers (`find`, `createCollection`) or raw `runCommand`.

```txt
mongo/mongosh → db.<coll>.<method> | db.runCommand({…})
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`db`** | Current database handle | “`use mydb` switches context.” |
| **`runCommand`** | Raw command API | “Everything is a command underneath.” |
| **Session / txn** | Multi-doc ACID | “Needs replica set.” |
| **Validator** | Schema on collection | “Set at create or collMod.” |

---

## Standard config / commands

```js
db.createCollection('users', {
  validator: { $jsonSchema: {
    bsonType: 'object',
    required: ['name', 'email'],
    properties: {
      name: { bsonType: 'string' },
      email: { bsonType: 'string', pattern: '^.+@.+$' },
    },
  }},
})

const session = db.getMongo().startSession()
session.startTransaction()
// … ops on session.getDatabase('test')
session.commitTransaction()
session.endSession()
```

| Knob | Why it matters |
|------|----------------|
| Replica set | Transactions require it |
| `listSessions` | Debug stuck txns |
| Prefer mongosh | Better UX; mongo shell deprecated |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Txn not supported | Standalone node | Use replica set |
| Auth failed | User/roles | [[mongosh user management]] |
| Command not found | Wrong shell/version | Upgrade mongosh |
| Validation errors | Schema vs doc | Fix doc or collMod |

---

## Gotchas

> [!WARNING]
> **`mongo` vs `mongosh`** — scripts can differ; target mongosh.

> [!WARNING]
> **Long interactive txns** — hold locks/resources; keep them short.

---

## When NOT to use

- **application data path** — use a driver, not the shell.
- **CI automation** — prefer mongosh non-interactive + scripts.

## Related

[[mongosh]] [[mongosh query]] [[MongoDB query validation]]
