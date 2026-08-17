[[MongoDB]] [[mongoose/mongoose]] [[query/mongodb lookup query]] [[mongodb denormalization]]

# MongoDB data populate

> Populate (Mongoose) replaces ObjectId refs with documents — convenience join at the app layer.

```txt
        MongoDB data popul ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Populate questions cover reference hydration costs versus embedding

## Sources
- [MongoDB Manual](https://www.mongodb.com/docs/manual/) — deep-dive
- [MongoDB Docs home](https://www.mongodb.com/docs/) — overview

## Key Concepts
```txt
- **Note:** Post { author: ObjectId } ──populate──► Post { author: UserDoc }
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **ref** | Path points at another model | “`ref: 'User'` on the schema.” |
| **populate** | Hydrate refs | “Extra query unless you aggregate.” |
| **select** | Limit fields | “Don’t pull whole user.” |
| **vs `$lookup`** | Aggregation join | “Prefer `$lookup` for heavy reports.” |

## Technical Details
```js
const post = await Post.findById(id).populate('author', 'name email')
await Post.find().populate({ path: 'comments', populate: { path: 'user' } })
```

| Knob | Why it matters |
|------|----------------|
| Field select | Payload size |
| Lean | Faster plain objects |
| Match/options | Filter populated set |

## Mistakes to Avoid
> [!WARNING]
> **Populate is not free** — lists with nested populate can explode query count.

> [!WARNING]
> **Missing refs become null** — orphan ids fail quietly.

| Symptom | Check | Fix |
|---------|-------|-----|
| null after populate | Bad id / wrong ref | Fix ObjectId; check model name |
| N+1 slowness | Many populates | `$lookup` or batch |
| Huge payloads | No select | Project fields |
| Circular populate | A↔B depth | Cap depth; redesign |

## Pros/Cons or Trade-offs
- **Analytics joins** — aggregation `$lookup`.
- **Data always read together** — embed instead of reference.
