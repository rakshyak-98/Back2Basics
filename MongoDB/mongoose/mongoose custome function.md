[[mongoose/mongoose]] [[mongoose/mongoose methods]] [[mongoose middleware]] [[mongoose/mongoose schema]]

# mongoose custome function

> Custom validators, getters/setters, and schema helpers — teach Mongoose your domain checks.

```txt
        mongoose custome f ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Custom functions on schemas check reuse versus keeping domain logic testable …

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
```txt
set(value) → validate(fn) → save
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **validate** | Sync/async check | “Return false or throw.” |
| **get/set** | Transform on read/write | “Normalize email toLowerCase.” |
| **Custom SchemaType** | Reuse a type | “Shared Money type.” |
| **pre hook** | Middleware | “See mongoose middleware.” |

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Updates ≠ save path** — many validators/setters don’t run unless configured.

> [!WARNING]
> **Heavy async validators** — external HTTP in validate = flaky saves.

| Symptom | Check | Fix |
|---------|-------|-----|
| Update skips validation | `findOneAndUpdate` | `{ runValidators: true }` |
| Async validator ignored | not returning promise | return Promise / async fn |
| Setter not applied | update operators | setters need `update` pipelines / save path |
| Vague ValidationError | no message | Add message strings |

## Pros/Cons or Trade-offs
- **Cross-document rules** — transactions/services.
- **One-time data cleanup** — migration scripts.
