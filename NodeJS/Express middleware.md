[[NodeJS]] [[expressjs]] [[node error]] [[Runtime Errors]]

# Express middleware

> Functions `(req, res, next)` in a pipeline — log, auth, parse, then route; call `next()` or end the response.

## Interview Relevance

Interviewers use **Express middleware** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **next()**, **Error middleware**, **Router-level**.

## Sources

- [Express — Using middleware](https://expressjs.com/en/guide/using-middleware.html) — deep-dive
- [Wikipedia — Express middleware](https://en.wikipedia.org/wiki/Express_middleware) — overview

## Key Concepts

- **next():** Continue chain — Forgot it = hung request.
- **Error middleware:** `(err,req,res,next)` — Four args — must be last.
- **Router-level:** `router.use` — Scope middleware to a mount.

## Technical Details

```txt
app.use(A) → app.use(B) → app.get('/') → error mw
```

```js
app.use(express.json())
app.use((req, _res, next) => {
  console.log(req.method, req.url)
  next()
})

app.use((err, _req, res, _next) => {
  console.error(err)
  res.status(err.status || 500).json({ error: err.message })
})
```

| Knob | Why it matters |
|------|----------------|
| Order | Parser before routes that need `body` |
| Path-scoped `app.use('/api', …)` | Don’t run globally when unneeded |
| Async errors | Pass to `next(err)` (or wrappers) |

## Real-World Applications

In production APIs and tooling, **Express middleware** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Async middleware** — rejected promises don’t auto-`next(err)` on older Express; wrap or use Express 5; **Sending twice** — `res.send` then `next()` → “Cannot set headers after they are sent.”.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Functions `(req, res, next)` in a pipeline — log, auth, parse, then route; call …).
- **Con / when not:** **Business logic only used by one route** — put it in the route/handler module.
- **Con / when not:** **Heavy CPU** — don’t block the middleware chain; queue/worker.

## Comparison

vs [[expressjs]]: know when each applies — do not treat them as interchangeable. vs [[node error]]: know when each applies — do not treat them as interchangeable. vs [[Runtime Errors]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Async middleware** — rejected promises don’t auto-`next(err)` on older Express; wrap or use Express 5.
- **Sending twice** — `res.send` then `next()` → “Cannot set headers after they are sent.”
- **Request hangs:** check No `next` / no `res`; fix: Always continue or end
- **Error HTML dump:** check No error middleware; fix: Add 4-arg handler
- **`body` empty:** check Parser after route; fix: Reorder `express.json()`
- **Auth skipped:** check Middleware after route; fix: `app.use(auth)` before protected routes
