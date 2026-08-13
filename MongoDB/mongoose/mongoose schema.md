[[mongoose/mongoose]] [[mongodb schema]] [[mongoose/mongoose methods]]

# mongoose schema

> A Mongoose schema declares paths, types, indexes, and options — the contract for a model.

---

## How it works

```txt
Schema({ email: String, … }) → Model → collection
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Path** | One field definition | “`email: { type: String }`.” |
| **required / enum** | Built-in validators | “Fail save early.” |
| **ref** | Point at another model | “For populate.” |
| **timestamps** | createdAt/updatedAt | “`{ timestamps: true }`.” |

---


## Configuration and commands

```js
const schema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, index: true },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
  profile: { bio: String },
}, { timestamps: true, strict: true })
```

| Knob | Why it matters |
|------|----------------|
| `strict: false` | Keep unknown keys |
| `select: false` | Hide secrets by default |
| Nested schemas | Subdocuments |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| CastError | wrong type | Fix input or SchemaType |
| unique not enforced | index missing | `syncIndexes()` |
| Mixed type chaos | `Schema.Types.Mixed` | Narrow types |
| Huge nested docs | unbounded arrays | Cap / bucket |

---


## Gotchas

> [!WARNING]
> **`unique: true` is an index** — not a validator; racey without the index built.

> [!WARNING]
> **Changing schema ≠ migrating data** — old docs stay until you rewrite.

---


## When not to use

- **Schemaless event blobs** — Mixed carefully or native driver.
- **One-off import** — skip elaborate schemas.


## Related

[[mongoose/mongoose]] [[mongoose/mongoose methods]] [[MongoDB query validation]]

## Sources

- [Wikipedia — mongoose schema](https://en.wikipedia.org/wiki/mongoose_schema)
