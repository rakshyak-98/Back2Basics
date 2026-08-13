[[ExpressJS]] [[NodeJS]] [[Express middleware]] [[express error handler]] [[express query handler]]

# express concepts

> Express is a minimal HTTP framework: an `app`, mountable `Router`s, and a middleware chain where each function receives `(req, res, next)` until a handler sends a response or `next(err)` reaches an error handler.

---

## Request flow

A request enters middleware in registration order. Each middleware may modify `req`/`res`, end the response, call `next()` to continue, or call `next(err)` to skip to error handlers.

```txt
req → middleware₁ → middleware₂ → route handler → res
              ↘ next(err) → error middleware (4 args)
```

| Piece | Role |
|-------|------|
| `app` | Top-level application; owns global middleware and routes |
| `Router` | Mountable route groups (`app.use('/api', router)`) |
| Middleware | Cross-cutting logic: parsing, authentication, logging |
| Error middleware | Four-argument `(err, req, res, next)` — see [[express error handler]] |

**Order matters:** authentication before handlers; body parsers before routes that read `req.body`; error handler last.

---

## Minimal application

```js
import express from 'express'
const app = express()
app.use(express.json())
app.get('/health', (_req, res) => res.send('ok'))
app.use((err, _req, res, _next) => {
  console.error(err)
  res.status(500).json({ error: 'internal' })
})
app.listen(3000)
```

| Knob | Why it matters |
|------|----------------|
| Middleware order | Auth and parsers must run before route logic |
| `Router({ mergeParams: true })` | Nested routers inherit parent `:params` |
| `trust proxy` | Correct client IP and protocol behind a load balancer |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Request hangs | Handler never calls `res` or `next` | Always end the response or call `next` |
| `req.body` is empty | Missing JSON parser | `app.use(express.json())` |
| 404 on every route | Wrong mount path | Check `app.use('/api', router)` prefix |
| Error returns HTML | No error middleware registered | Add a four-argument error handler |

**Async handlers (Express 4):** rejected promises are not caught automatically — wrap with `try/catch` and `next(err)`, or use Express 5.

---

## When Express is a poor fit

- **Raw TCP or extreme throughput** — specialized servers ([[uWebSocket]], native `ws`).
- **Full batteries-included framework** — NestJS or Fastify may reduce boilerplate.

---

## Related

[[Express middleware]] · [[express query handler]] · [[express build]] · [[express error handler]]
