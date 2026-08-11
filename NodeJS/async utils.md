[[NodeJS]] [[Express middleware]] [[expressjs]]

# async utils

> Tiny wrappers so async route handlers don’t need try/catch — rejected promises become `next(err)`.

---

## Mental model

**Say it in one breath:** Wrap `(req,res,next) => Promise…` so `.catch(next)` runs; Express error middleware owns the response.

```txt
asyncHandler(fn) → Promise.resolve(fn(...)).catch(next)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **asyncHandler** | Promise → `next(err)` | “No try/catch on every route.” |
| **Express 5** | Native async errors | “Older Express needs a wrapper.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| UnhandledRejection | Raw async mw, no wrap | Use `asyncHandler` / Express 5 |
| Empty 500 | No error middleware | Add `(err,req,res,next)` last |
| Validation as 500 | Zod/Yup not mapped | Map to 400 in error mw |

---

## Gotchas

> [!WARNING]
> **Wrapper typos** (`ers` vs `res`) — silent bugs; keep the helper tiny and tested.

---

## When NOT to use

- **Sync middleware** — call `next()` yourself.
- **Non-Express** — use framework-native async error hooks.

---

## Related

[[Express middleware]] [[expressjs]] [[Error handeling]] [[Runtime Errors]]
