[[mongoose]] [[mongoose schema]] [[mongoose methods]] [[MongoDB]] [[Data access patterns]]

# Mongoose middleware

> Pre/post hooks on document and query lifecycle — powerful cross-cutting layer that hides bugs when misused — **Mongoose docs + production scars**.

---

## Mental model

**Middleware** runs between Mongoose API call and MongoDB operation. Hooks attach to **`save`**, **`validate`**, **`remove`**, and **`find*` query methods** — not all methods trigger all hook types.

```txt
new User({...}).save()
  → pre('validate') → validate → post('validate')
  → pre('save')     → Mongo insert/update → post('save')

User.findOneAndUpdate(...)
  → pre('findOneAndUpdate')  ← query middleware (different context!)
  → Mongo update
  → post('findOneAndUpdate')
```

| Hook type | `this` refers to | Typical use |
|-----------|------------------|-------------|
| **Document** (`save`, `init`) | Document instance | hash password, timestamps, denormalize |
| **Query** (`find`, `update*`) | Query object | soft-delete filter, tenant scoping |
| **Aggregate** | Aggregation | rare — read path transforms |

**Order matters:** global → schema → pre before op → post after op. Multiple pres on same hook run in registration order.

---

## Standard config / commands

### Document middleware (save path)

```javascript
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.post('save', function (doc, next) {
  auditLog('user.created', doc._id);
  next();
});
```

### Query middleware (soft delete)

```javascript
userSchema.pre(/^find/, function (next) {
  this.where({ deletedAt: null });
  next();
});

userSchema.pre('findOneAndUpdate', async function (next) {
  const update = this.getUpdate();
  if (update.$set?.password) {
    update.$set.password = await bcrypt.hash(update.$set.password, 12);
  }
  next();
});
```

### Async styles (Mongoose 5+)

```javascript
// Preferred: async function — errors thrown propagate
schema.pre('save', async function () {
  await doWork(this);
});

// Legacy: next(err) — still works; easy to forget next() → hung request
schema.pre('save', function (next) {
  doWork(this).then(() => next()).catch(next);
});
```

### Disable middleware (debug)

```javascript
await doc.save({ validateBeforeSave: false }); // skips validate hooks only partially — read docs
User.find().bypassMiddleware(); // if plugin supports — prefer explicit flag on schema
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Request hangs forever | Missing `next()` in sync pre | Add `next()` or switch to async/await |
| Password not hashed on update | Used `updateOne` not `save` | Query middleware on `findOneAndUpdate` or hash in service layer |
| Infinite loop | post('save') calls `doc.save()` | Remove recursive save; use `updateOne` or flag |
| Hook didn't run | Wrong op (`insertMany` skips some) | Use supported hook or explicit service function |
| Tests flaky | Parallel saves; shared doc state | Isolate fixtures; `sinon` stub hooks |
| Data differs prod vs script | Script uses collection API directly | Scripts bypass Mongoose — duplicate logic or use models |
| `this` is wrong in arrow fn | Arrow doesn't bind document `this` | Use `function () {}` in document hooks |

```javascript
// Debug: log hook registration
console.log(userSchema._pres.get('save'));
```

---

## Gotchas

> [!WARNING]
> **`findOneAndUpdate` bypasses `save` middleware** — most common prod bug. Password/hash hooks on `pre('save')` silently skipped.

> [!WARNING]
> **`next()` called twice** — Express-style double callback; unpredictable state.

> [!WARNING]
> **Hidden business logic** — middleware spreads rules across files; new dev uses raw driver → security hole.

> [!WARNING]
> **`insertMany`** — no full document middleware chain; bulk import paths need explicit validation.

> [!WARNING]
> **Performance** — N+1 in `post('find')` loading relations for list endpoints — moved work to hot path.

> [!WARNING]
> **Transactions** — hook side effects (email, SQS) outside transaction commit → orphan messages on rollback.

---

## When NOT to use

- **Authorization / tenancy** — enforce at API/gateway layer; query middleware is defense-in-depth only.
- **Cross-collection invariants** — use transaction + explicit domain service, not cascading hooks.
- **Heavy I/O in pre hooks** — blocks request; queue async job in post-commit hook or outbox pattern.

---

## Related

[[mongoose]] [[mongoose schema]] [[mongoose methods]] [[Mongoose plugin]] [[Data access patterns]] [[ACID]]
