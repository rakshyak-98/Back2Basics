[[mongoose/mongoose]] [[mongodb schema]] [[mongoose/mongoose methods]] [[MongoDB query validation]]

# mongoose schema

> A Mongoose schema declares paths, types, indexes, and options — the contract for a model.





## Interview Relevance
Mongoose schema interviews cover types, required/index, and mismatch with flexible MongoDB documents.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
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

## Technical Details
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

## Pros/Cons or Trade-offs
- **Schemaless event blobs** — Mixed carefully or native driver.
- **One-off import** — skip elaborate schemas.

## Mistakes to Avoid
> [!WARNING]
> **`unique: true` is an index** — not a validator; racey without the index built.

> [!WARNING]
> **Changing schema ≠ migrating data** — old docs stay until you rewrite.

| Symptom | Check | Fix |
|---------|-------|-----|
| CastError | wrong type | Fix input or SchemaType |
| unique not enforced | index missing | `syncIndexes()` |
| Mixed type chaos | `Schema.Types.Mixed` | Narrow types |
| Huge nested docs | unbounded arrays | Cap / bucket |
