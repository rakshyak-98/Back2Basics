<!-- note-strategy: operational -->
[[NodeJS]] [[expressjs]] [[node error]]

# Express middleware

> Functions `(req, res, next)` in a pipeline — log, auth, parse, then route; call `next()` or end the response.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Middleware runs in registration order. If it doesn’t send a response, it must `next()` or `next(err)`.

```txt
app.use(A) → app.use(B) → app.get('/') → error mw
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **next()** | Continue chain | “Forgot it = hung request.” |
| **Error middleware** | `(err,req,res,next)` | “Four args — must be last.” |
| **Router-level** | `router.use` | “Scope middleware to a mount.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Request hangs | No `next` / no `res` | Always continue or end |
| Error HTML dump | No error middleware | Add 4-arg handler |
| `body` empty | Parser after route | Reorder `express.json()` |
| Auth skipped | Middleware after route | `app.use(auth)` before protected routes |

---

## Gotchas

> [!WARNING]
> **Async middleware** — rejected promises don’t auto-`next(err)` on older Express; wrap or use Express 5.

> [!WARNING]
> **Sending twice** — `res.send` then `next()` → “Cannot set headers after they are sent.”

---

## When NOT to use

- **Business logic only used by one route** — put it in the route/handler module.
- **Heavy CPU** — don’t block the middleware chain; queue/worker.

---

## Related

[[expressjs]] [[node error]] [[Runtime Errors]]
