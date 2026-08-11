[[MongoDB]] [[mongoose/mongoose]] [[query/mongodb lookup query]]

# MongoDB data populate

> Populate (Mongoose) replaces ObjectId refs with documents — convenience join at the app layer.

---

## Mental model

**Say it in one breath:** Store refs as ids; `.populate('author')` runs follow-up queries (or a `$lookup`) and stitches results.

```txt
Post { author: ObjectId } ──populate──► Post { author: UserDoc }
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ref** | Path points at another model | “`ref: 'User'` on the schema.” |
| **populate** | Hydrate refs | “Extra query unless you aggregate.” |
| **select** | Limit fields | “Don’t pull whole user.” |
| **vs `$lookup`** | Aggregation join | “Prefer `$lookup` for heavy reports.” |

---

## Standard config / commands

```js
const post = await Post.findById(id).populate('author', 'name email')
await Post.find().populate({ path: 'comments', populate: { path: 'user' } })
```

| Knob | Why it matters |
|------|----------------|
| Field select | Payload size |
| Lean | Faster plain objects |
| Match/options | Filter populated set |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| null after populate | Bad id / wrong ref | Fix ObjectId; check model name |
| N+1 slowness | Many populates | `$lookup` or batch |
| Huge payloads | No select | Project fields |
| Circular populate | A↔B depth | Cap depth; redesign |

---

## Gotchas

> [!WARNING]
> **Populate is not free** — lists with nested populate can explode query count.

> [!WARNING]
> **Missing refs become null** — orphan ids fail quietly.

---

## When NOT to use

- **Analytics joins** — aggregation `$lookup`.
- **Data always read together** — embed instead of reference.

## Related

[[mongoose/mongoose]] [[query/mongodb lookup query]] [[mongodb denormalization]]
