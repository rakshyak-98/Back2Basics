[[mongoose middleware]] [[mongodb model]] [[MongoDB]]

# Mongoose plugin

> Reusable schema functions that add paths, indexes, methods, or hooks without copy-paste — [Mongoose plugins docs](https://mongoosejs.com/docs/plugins.html).

## Mental model

A plugin is a function `(schema, options) => void` registered on a schema before `mongoose.model()`. Global plugins apply to every schema. Plugins compose: one adds soft-delete, another adds pagination, another adds audit fields.

```
plugin(schema) → adds paths / hooks / statics
schema.plugin(plugin, opts) → per-schema
mongoose.plugin(plugin)       → global (all schemas)
```

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Plugin hook never runs | Order of `plugin()` vs `model()` | Register plugin before `mongoose.model()` |
| Global plugin breaks one schema | `schema.plugin` override | Disable per-schema or guard with option flag |
| Duplicate index from plugin | `schema.indexes()` | Merge indexes; one plugin owns index |
| Method not on document | Applied to wrong schema | Confirm `schema.plugin` on correct schema |

## Gotchas

> [!WARNING]
> **Plugin order matters** — pre-hooks run in registration order; conflicting plugins need explicit ordering.
>
> **Global plugins in tests** — leak across test files; call `mongoose.deleteModel()` / isolate connections.
>
> **Over-plugining** — magic behavior hides in hooks; hard to debug "who filtered this query?".

## When NOT to use

- Don't plugin one-off business logic — plain schema methods or service layer is clearer.
- Don't global-plugin heavy side effects (external API calls) without opt-in per schema.

## Related

[[mongoose middleware]] [[mongodb model]] [[Design pattern/Static Members]]
