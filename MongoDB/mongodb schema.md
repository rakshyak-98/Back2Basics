<!-- note-strategy: operational -->
[[MongoDB]] [[mongodb migration]] [[MongoDB query validation]]

# mongodb schema

> MongoDB documents are flexible by default — add fields freely; use JSON Schema validation when you need guardrails.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Collections don’t force one shape; application + optional validators decide required fields and types.

```txt
App writes docs → (optional $jsonSchema) → BSON on disk
Design for: queries you run, not SQL tables
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Flexible schema** | Fields can vary per doc | “Evolve without ALTER TABLE.” |
| **Validator** | Server-side JSON Schema | “Reject bad inserts at write time.” |
| **Embedded vs ref** | Nest vs point | “Embed for read-together; ref for many.” |
| **Polymorphism** | Type field + variants | “One collection, several shapes.” |

---

## Standard config / commands

```js
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email'],
      properties: {
        email: { bsonType: 'string' },
        age: { bsonType: 'int', minimum: 0 },
      },
    },
  },
  validationAction: 'error', // or 'warn'
})
```

| Knob | Why it matters |
|------|----------------|
| `validationAction` | `warn` for migrate-in; `error` in prod |
| `validationLevel` | `moderate` skips invalid existing docs on update |
| Indexes | Schema ≠ speed — still index query fields |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Insert Document failed validation | `db.getCollectionInfos` | Fix doc or relax schema |
| Mixed types on field | app bugs / no validator | Normalize + validate |
| Slow “schema” evolution | huge backfill | [[mongodb migration]] in batches |
| App assumes field always present | sparse docs | Default in app or `$ifNull` |

---

## Gotchas

> [!WARNING]
> **Schema-less ≠ design-free** — bad embedding still kills performance.

> [!WARNING]
> **Validators don’t rewrite old docs** — migrate existing data explicitly.

---

## When NOT to use

- **Strict relational invariants across many entities** — use SQL.
- **Heavy multi-document joins as the default access** — rethink model.

## Related

[[MongoDB query validation]] [[mongodb migration]] [[mongodb denormalization]] [[mognodb indexing]]
