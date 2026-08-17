[[mongoose/mongoose]] [[mongoose/mongoose schema]] [[mongoose/mongoose custome function]]

# mongoose methods

> Instance methods and statics attach behavior to documents/models — keep query helpers next to the schema.





## Interview Relevance
Instance/static methods questions check where business logic belongs versus services.

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
```txt
doc.method() | Model.static() | Model.find().byEmail()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **methods** | Per-document API | “`user.checkPassword()`.” |
| **statics** | Per-model API | “`User.findByEmail()`.” |
| **query helper** | Chainable filter | “`.byTenant(id)`.” |
| **lean** | Skip hydrate | “Faster reads, no methods.” |

## Technical Details
```js
schema.methods.displayName = function () {
  return this.name || this.email
}
schema.statics.findByEmail = function (email) {
  return this.findOne({ email })
}
schema.query.byTenant = function (tenantId) {
  return this.where({ tenantId })
}
```

| Knob | Why it matters |
|------|----------------|
| Arrow functions | Break `this` binding — use `function` |
| lean() | Methods unavailable on plain objects |
| async methods | Always await |

## Pros/Cons or Trade-offs
- **Pure utilities** — plain functions may be clearer.
- **Cross-model workflows** — service layer, not one model’s statics.

## Mistakes to Avoid
> [!WARNING]
> **Business logic only in methods** — still enforce critical rules in services for non-Mongoose paths.

> [!WARNING]
> **Methods don’t exist after `lean()` or `toObject()` without virtuals config.**

| Symptom | Check | Fix |
|---------|-------|-----|
| `this` undefined | arrow fn on methods | Use classic function |
| method missing | lean query | Remove lean or plain helper |
| static not found | wrong model export | Export compiled model |
| Side effects in getters | hidden I/O | Move to explicit methods |
