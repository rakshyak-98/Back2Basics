[[MongoDB]] [[mongoose middleware]] [[mongoose/Mongoose plugin]] [[Database/Data access patterns]]

# MongoDB model (Mongoose schema)

> Schema + indexes + hooks that define document shape, constraints, and query paths — **Mongoose docs** + DBA review habits.

## Mental model

A **model** is a compiled schema bound to a collection. The schema declares fields, types, defaults, validators, indexes, and middleware. MongoDB is schemaless at storage time; Mongoose enforces structure at the application layer unless you bypass it with `strict: false` or raw collection calls.

```
Schema (shape + rules) → Model (collection API) → MongoDB collection
         ↓
    indexes, hooks, virtuals
```

## Standard config / commands

### Schema with compound unique index

```js
const userSchema = new mongoose.Schema({
  tenantId: { type: String, required: true, index: true },
  email:    { type: String, required: true, lowercase: true, trim: true },
  role:     { type: String, enum: ['admin', 'member'], default: 'member' },
}, { timestamps: true });

// Compound unique — one email per tenant
userSchema.index({ tenantId: 1, email: 1 }, { unique: true });

module.exports = mongoose.model('User', userSchema);
```

### Index sync (dev / deploy)

```js
await User.createIndexes(); // idempotent; run after schema change
```

### Lean queries (read-heavy paths)

```js
const users = await User.find({ tenantId }).lean(); // plain objects, faster
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `E11000` on compound field | `db.users.getIndexes()` | Fix duplicate data; confirm index key order matches query |
| ValidationError on save | Schema path + `required` | Align payload; use `runValidators: true` on updates |
| Field missing after update | `strict` mode | Add field to schema or use `$set` with defined paths |
| Slow list queries | `explain()` | Add index on filter + sort fields |
| Stale subdocs | `.markModified('path')` | Required when Mixed/Array mutated in place |

## Gotchas

> [!WARNING]
> **Unique index created after dupes exist** — build fails or index stays partial; clean data first.
>
> **`field1` typo in index** — `{ filed1: 1 }` creates useless index; queries won't use it.
>
> **Hooks don't run on `updateMany`** — use middleware type `updateOne`/`findOneAndUpdate` or move logic to service layer.

## When NOT to use

- Don't mirror SQL normalized schemas 1:1 — embed when read together, reference when independent lifecycle.
- Don't skip indexes because "Mongo is fast" — unindexed collection scans hurt at scale.

## Related

[[mongoose middleware]] [[mongoose/Mongoose plugin]] [[mongodb connection]] [[GridFS]]
