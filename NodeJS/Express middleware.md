[[NodeJS]] [[expressjs]] [[node error]] [[Runtime Errors]]

# Express middleware

> Functions `(req, res, next)` in a pipeline — log, auth, parse, then route; call `next()` or end the response.

```txt
        Express middleware ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **Express middleware** to check whether you can explain the …

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

## Mistakes to Avoid
- **Mistake:** **Async middleware**
- **Sending twice**::** → “Cannot set headers after they are sent.”
- **Mistake:** **Request hangs:** check No `next` / no `res`
- **Mistake:** **Error HTML dump:** check No error middleware
- **Mistake:** **`body` empty:** check Parser after route
- **Mistake:** **Auth skipped:** check Middleware after route

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Functions `(req, res, next)` in a pipeline — log, auth, parse, then route; call …).
- **Con / when not:** **Business logic only used by one route**
- **Con / when not:** **Heavy CPU**

## Comparison
- vs [[expressjs]]: know when each applies


### Use cases
- In production APIs and tooling, **Express middleware** shows up whenever team…
