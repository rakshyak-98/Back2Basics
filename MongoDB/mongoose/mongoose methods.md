[[mongoose/mongoose]] [[mongoose/mongoose schema]] [[mongoose/mongoose custome function]]

# mongoose methods

> Instance methods and statics attach behavior to documents/models — keep query helpers next to the schema.

---

## Mental model

**Say it in one breath:** `methods` run on a document (`this`); `statics` run on the model; `query` helpers chain on find.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `this` undefined | arrow fn on methods | Use classic function |
| method missing | lean query | Remove lean or plain helper |
| static not found | wrong model export | Export compiled model |
| Side effects in getters | hidden I/O | Move to explicit methods |

---

## Gotchas

> [!WARNING]
> **Business logic only in methods** — still enforce critical rules in services for non-Mongoose paths.

> [!WARNING]
> **Methods don’t exist after `lean()` or `toObject()` without virtuals config.**

---

## When NOT to use

- **Pure utilities** — plain functions may be clearer.
- **Cross-model workflows** — service layer, not one model’s statics.

## Related

[[mongoose/mongoose schema]] [[mongoose/mongoose custome function]] [[mongoose/mongoose]]
