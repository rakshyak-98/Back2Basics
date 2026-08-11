[[MongoDB]] [[mongoose/mongoose schema]] [[mongodb connection]]

# mongoose

> Mongoose is the Node ODM for MongoDB — schemas, models, and connection pooling on top of the driver.

---

## Mental model

**Say it in one breath:** Define a schema → compile a model → `connect` once → CRUD through the model (validation + middleware included).

```txt
URI → mongoose.connect → Model(schema) → find/save
                              ↓
                         virtuals / hooks (app-level)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ODM** | Objects ↔ documents | “Schema lives in the app.” |
| **Model** | Collection constructor | “`mongoose.model('User', schema)`.” |
| **Virtual** | Computed field not stored | “MongoDB doesn’t store it.” |
| **Middleware** | pre/post hooks | “hash password pre('save').” |

---

## Standard config / commands

```js
await mongoose.connect(process.env.MONGO_URI, { maxPoolSize: 10 })
const userSchema = new mongoose.Schema({ email: { type: String, required: true } })
userSchema.virtual('domain').get(function () {
  return this.email.split('@')[1]
})
const User = mongoose.model('User', userSchema)
```

| Knob | Why it matters |
|------|----------------|
| Pool size | Too big thunders Mongo |
| `strict` | Drop unknown paths vs keep |
| `bufferCommands` | Behavior before connected |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| buffering timed out | connect never succeeded | Fix URI/network; await connect |
| ValidationError | schema vs payload | Align types/required |
| Duplicate key | unique index | Catch 11000; clean data |
| Virtual missing in JSON | not in `toJSON` | `schema.set('toJSON', { virtuals: true })` |

---

## Gotchas

> [!WARNING]
> **Virtuals aren’t in Mongo** — can’t query/filter them server-side.

> [!WARNING]
> **Multiple connections/models** — accidental `model` recompile in serverless hot reload.

---

## When NOT to use

- **Simple scripts** — native driver is enough.
- **Heavy aggregations only** — driver + aggregate may be clearer.

## Related

[[mongoose/mongoose schema]] [[mongoose/mongoose methods]] [[mongodb connection]]
