[[mongoose middleware]] [[mongodb model]] [[MongoDB]] [[Design pattern/Static Members]]

# Mongoose plugin

> Mongoose plugin — a plugin is a function (schema, options) => void registered on a schema before mongoose.model(). Global plugins apply to every schema. Plugins compose

```txt
        Mongoose plugin ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Plugin questions cover reusable schema plugins and avoiding global side effec…

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
- **Note:** A plugin is a function `(schema, options) => void` registered on a schema bef…

```
plugin(schema) → adds paths / hooks / statics
schema.plugin(plugin, opts) → per-schema
mongoose.plugin(plugin)       → global (all schemas)
```

## Technical Details
### Write a plugin

```js
function timestampsPlugin(schema) {
  schema.add({ deletedAt: { type: Date, default: null } });
  schema.methods.softDelete = function () {
    this.deletedAt = new Date();
    return this.save();
  };
  schema.pre(/^find/, function () {
    this.where({ deletedAt: null });
  });
}
```

### Apply before compiling model

```js
const userSchema = new mongoose.Schema({ name: String });
userSchema.plugin(timestampsPlugin);
// MUST register plugins before:
const User = mongoose.model('User', userSchema);
```

### Global plugin

```js
mongoose.plugin(require('mongoose-sequence')); // example: auto-increment
```

### Popular patterns

| Plugin style | Adds |
|--------------|------|
| Soft delete | `deletedAt`, default query filter |
| Pagination | `.paginate(filter, opts)` static |
| Unique validator | async uniqueness check |
| Audit | `createdBy`, `updatedBy` hooks |

## Mistakes to Avoid
> [!WARNING]
> **Plugin order matters** — pre-hooks run in registration order; conflicting plugins need explicit ordering.
>
> **Global plugins in tests** — leak across test files; call `mongoose.deleteModel()` / isolate connections.
>
> **Over-plugining** — magic behavior hides in hooks; hard to debug "who filtered this query?".

| Symptom | Check | Fix |
|---------|-------|-----|
| Plugin hook never runs | Order of `plugin()` vs `model()` | Register plugin before `mongoose.model()` |
| Global plugin breaks one schema | `schema.plugin` override | Disable per-schema or guard with option flag |
| Duplicate index from plugin | `schema.indexes()` | Merge indexes; one plugin owns index |
| Method not on document | Applied to wrong schema | Confirm `schema.plugin` on correct schema |

## Pros/Cons or Trade-offs
- Don't plugin one-off business logic
- Don't global-plugin heavy side effects (external API calls) without opt-in pe…
