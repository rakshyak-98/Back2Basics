[[NodeJS]] [[Express middleware]] [[expressjs]] [[Error handeling]] [[Runtime Errors]]

# async utils

> Tiny wrappers so async route handlers don’t need try/catch — rejected promises become `next(err)`.

```txt
        async utils ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **async utils** to check whether you can explain the mechani…

## Sources
- [Express — Error handling](https://expressjs.com/en/guide/error-handling.html) — overview
- [Wikipedia — async utils](https://en.wikipedia.org/wiki/async_utils) — overview

## Key Concepts
- **asyncHandler:** Promise → `next(err)` — No try/catch on every route.
- **Express 5:** Native async errors — Older Express needs a wrapper.

## Technical Details
```txt
asyncHandler(fn) → Promise.resolve(fn(...)).catch(next)
```

```js
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next)

router.post('/api', asyncHandler(async (req, res) => {
  const data = schema.parse(req.body) // throws → next(err)
  const row = await create(data)
  res.status(201).json({ id: row.id })
}))
```

| Knob | Why it matters |
|------|----------------|
| `catch(next)` | Lands in 4-arg error middleware |
| Thin responses | Don’t leak full ORM objects |

## Mistakes to Avoid
- **Mistake:** **Wrapper typos** (`ers` vs `res`)
- **Mistake:** **UnhandledRejection:** check Raw async mw, no wrap
- **Mistake:** **Empty 500:** check No error middleware
- **Mistake:** **Validation as 500:** check Zod/Yup not mapped

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Tiny wrappers so async route handlers don’t need try/catch — rejected promises b…).
- **Con / when not:** **Sync middleware** — call `next()` yourself.
- **Con / when not:** **Non-Express** — use framework-native async error hooks.

## Comparison
- vs [[Express middleware]]: know when each applies


### Use cases
- In production APIs and tooling, **async utils** shows up whenever teams ship …
