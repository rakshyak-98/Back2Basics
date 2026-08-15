[[NodeJS]] [[Express middleware]] [[expressjs]] [[Error handeling]] [[Runtime Errors]]

# async utils

> Tiny wrappers so async route handlers don’t need try/catch — rejected promises become `next(err)`.

## Interview Relevance

Interviewers use **async utils** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **asyncHandler**, **Express 5**.

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

## Real-World Applications

In production APIs and tooling, **async utils** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Wrapper typos** (`ers` vs `res`) — silent bugs; keep the helper tiny and tested; **UnhandledRejection:** check Raw async mw, no wrap; fix: Use `asyncHandler` / Express 5.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Tiny wrappers so async route handlers don’t need try/catch — rejected promises b…).
- **Con / when not:** **Sync middleware** — call `next()` yourself.
- **Con / when not:** **Non-Express** — use framework-native async error hooks.

## Comparison

vs [[Express middleware]]: know when each applies — do not treat them as interchangeable. vs [[expressjs]]: know when each applies — do not treat them as interchangeable. vs [[Error handeling]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Wrapper typos** (`ers` vs `res`) — silent bugs; keep the helper tiny and tested.
- **UnhandledRejection:** check Raw async mw, no wrap; fix: Use `asyncHandler` / Express 5
- **Empty 500:** check No error middleware; fix: Add `(err,req,res,next)` last
- **Validation as 500:** check Zod/Yup not mapped; fix: Map to 400 in error mw
