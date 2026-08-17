[[MongoDB]] [[mongosh]] [[MongoDB query validation]] [[mongosh query]]

# mongodb shell

> The legacy `mongo` shell runs JS against the server — prefer [[mongosh]] on modern installs; same admin patterns.

```txt
        mongodb shell ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Shell literacy covers legacy mongo vs mongosh and administrative recipes.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
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

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **`mongo` vs `mongosh`** — scripts can differ; target mongosh.

> [!WARNING]
> **Long interactive txns** — hold locks/resources; keep them short.

| Symptom | Check | Fix |
|---------|-------|-----|
| Txn not supported | Standalone node | Use replica set |
| Auth failed | User/roles | [[mongosh user management]] |
| Command not found | Wrong shell/version | Upgrade mongosh |
| Validation errors | Schema vs doc | Fix doc or collMod |

## Pros/Cons or Trade-offs
- **application data path** — use a driver, not the shell.
- **CI automation** — prefer mongosh non-interactive + scripts.
