[[MongoDB]] [[mongodb schema]] [[mongodb shell]] [[mongodb migration]]

# MongoDB query validation

> Collection validators reject bad writes — JSON Schema (or operators) enforced by the server.





## Interview Relevance
Validation interviews check schema validators, validationLevel/action, and migration of invalid docs.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
```txt
write → validator ($jsonSchema) → accept | reject
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`$jsonSchema`** | Draft-ish schema for BSON | “required, bsonType, pattern…” |
| **`validationAction`** | error vs warn | “warn while backfilling.” |
| **`validationLevel`** | strict vs moderate | “moderate skips already-invalid docs.” |
| **collMod** | Change validator later | “Evolve without recreate.” |

## Technical Details
```js
db.runCommand({
  collMod: 'users',
  validator: { $jsonSchema: {
    bsonType: 'object',
    required: ['email'],
    properties: { email: { bsonType: 'string' } },
  }},
  validationLevel: 'moderate',
  validationAction: 'error',
})
```

| Knob | Why it matters |
|------|----------------|
| moderate | Lets old bad docs update other fields |
| warn | Observe without blocking |
| App + server validation | Defense in depth |

## Pros/Cons or Trade-offs
- **Highly polymorphic events** — validate in the producer instead.
- **One-off scratch collections** — skip until shape stabilizes.

## Mistakes to Avoid
> [!WARNING]
> **Validators don’t migrate history** — old docs stay wrong until you rewrite them.

> [!WARNING]
> **Complex `$jsonSchema`** — hard to read; keep rules minimal and clear.

| Symptom | Check | Fix |
|---------|-------|-----|
| Document failed validation | error details / schema | Fix payload or schema |
| Legacy writes blocked | strict + old docs | moderate + migrate |
| Validator too weak | only app checks | Add server schema |
| Silent bad data | action=warn | Flip to error after cleanup |
