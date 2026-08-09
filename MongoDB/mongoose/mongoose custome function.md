[[mongoose/mongoose]] [[mongoose/mongoose methods]] [[mongoose middleware]]

# mongoose custome function

> Custom validators, getters/setters, and schema helpers — teach Mongoose your domain checks.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Hook custom functions into path validators or setters so bad values never persist.

```txt
set(value) → validate(fn) → save
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **validate** | Sync/async check | “Return false or throw.” |
| **get/set** | Transform on read/write | “Normalize email toLowerCase.” |
| **Custom SchemaType** | Reuse a type | “Shared Money type.” |
| **pre hook** | Middleware | “See mongoose middleware.” |

---

## Standard config / commands

```js
email: {
  type: String,
  set: (v) => v?.trim().toLowerCase(),
  validate: {
    validator: (v) => /^[^\s@]+@[^\s@]+$/.test(v),
    message: 'Invalid email',
  },
}
```

| Knob | Why it matters |
|------|----------------|
| Async validators | Must `await` save |
| `message` | Clear API errors |
| runValidators on update | Off by default for updates |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Update skips validation | `findOneAndUpdate` | `{ runValidators: true }` |
| Async validator ignored | not returning promise | return Promise / async fn |
| Setter not applied | update operators | setters need `update` pipelines / save path |
| Vague ValidationError | no message | Add message strings |

---

## Gotchas

> [!WARNING]
> **Updates ≠ save path** — many validators/setters don’t run unless configured.

> [!WARNING]
> **Heavy async validators** — external HTTP in validate = flaky saves.

---

## When NOT to use

- **Cross-document rules** — transactions/services.
- **One-time data cleanup** — migration scripts.

## Related

[[mongoose/mongoose methods]] [[mongoose middleware]] [[mongoose/mongoose schema]]
