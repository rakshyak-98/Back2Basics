[[MongoDB]] [[mongodb connection]] [[mongodb model]]

# MongoDB errors

> Symptom → cause → fix for the errors that show up in prod logs and Compass — **MongoDB Manual** + Mongoose gotchas.

## Mental model

MongoDB errors fall into a few buckets: **wire/auth** (can't connect), **write concern / topology** (not primary, election), **schema/validation** (document shape), **index/constraints** (duplicate key), and **query/update syntax** (wrong operator shape). The message usually names the bucket; the fix is in the operator or topology state.

## Standard config / commands

### Inspect live state

```bash
mongosh --eval 'rs.status()'          # replica set health
mongosh --eval 'db.currentOp({ active: true })'
mongosh mydb --eval 'db.getCollectionNames()'
```

### Safe update shape (always object for modifiers)

```js
// WRONG — string instead of field map
db.users.updateOne({ _id: id }, { $set: "Documents missing" });

// RIGHT
db.users.updateOne({ _id: id }, { $set: { status: "active" } });
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Modifiers operate on fields but we found type string` | Update payload shape | `$set`, `$inc`, etc. need `{ field: value }`, not a bare string |
| `E11000 duplicate key error` | Index definition | Remove dup doc or fix unique index fields |
| `Document failed validation` | JSON Schema / `$jsonSchema` | Align insert with validator or relax rules in dev |
| `not primary and secondaryOk=false` | `rs.status()` | Route writes to primary; wait for election |
| `Executor error: Sort exceeded memory limit` | `explain("executionStats")` | Add index matching sort; or `{ allowDiskUse: true }` (aggregation) |
| `BSONObj size: ... is invalid. Size must be between 0 and 16793600` | Document size | Split doc, use GridFS for blobs — see [[GridFS]] |
| `MongoTimeoutError` | Network, pool, load | See [[mongodb connection]] triage table |

## Gotchas

> [!WARNING]
> **Mongoose `updateOne` without `$set`** — `{ name: "x" }` replaces entire doc in some paths; use `$set` explicitly for partial updates.
>
> **Case-sensitive field names** — `{ Email: 1 }` index ≠ `{ email: 1 }`; duplicates slip through.
>
> **Silent `undefined` strips** — Mongoose omits undefined keys; can look like "update didn't work".

## When NOT to use

- Don't blanket `catch` and retry without reading error code — duplicate key and validation errors won't heal on retry.
- Don't disable write concern globally to "fix" timeout errors.

## Related

[[mongodb connection]] [[mongodb model]] [[GridFS]] [[mongoose middleware]]
