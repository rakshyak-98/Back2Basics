[[expressjs]] [[Express middleware]] [[express error handler]] [[express query handler]] [[express build]]

# express concepts

> Express is a minimal HTTP framework: an `app`, mountable `Router`s, and a middleware chain where each `(req, res, next)` either responds or calls `next`.

## Interview Relevance

Interviewers use Express to test middleware order, error propagation, and whether you know when a thin framework is enough versus Fastify, Nest, or raw `http`.

## Sources

- [Express — Guide: Using middleware](https://expressjs.com/en/guide/using-middleware.html) — deep-dive
- [Express — Guide: Routing](https://expressjs.com/en/guide/routing.html) — overview
- [Express — API reference](https://expressjs.com/en/4x/api.html) — deep-dive

## Core Definition

Express wraps Node’s HTTP server with ordered middleware and routers. A request walks the stack until a handler sends a response or `next(err)` jumps to four-argument error middleware.

## Key Concepts

- **`app`:** top-level application — owns global middleware and route mounts.
- **`Router`:** mountable route groups (`app.use('/api', router)`) — keeps domains separate.
- **Middleware:** `(req, res, next)` — parsers, authentication, logging; order is part of the contract.
- **Error middleware:** four arguments `(err, req, res, next)` — see [[express error handler]].
- **`trust proxy`:** correct client IP and scheme behind a load balancer.

## Technical Details

```txt
req → middleware₁ → middleware₂ → route handler → res
              ↘ next(err) → error middleware (4 args)
```

| Piece | Role |
|-------|------|
| `app` | Top-level application; global middleware and routes |
| `Router` | Mountable groups (`app.use('/api', router)`) |
| Middleware | Cross-cutting: parsing, authentication, logging |
| Error middleware | Four-argument `(err, req, res, next)` |

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
| Middleware order | Authentication and parsers before route logic |
| `Router({ mergeParams: true })` | Nested routers inherit parent `:params` |
| `trust proxy` | Correct IP/protocol behind a load balancer |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Request hangs | Handler never calls `res` or `next` | Always end the response or call `next` |
| `req.body` empty | Missing JSON parser | `app.use(express.json())` before routes |
| 404 on every route | Wrong mount path | Check `app.use('/api', router)` prefix |
| Error returns HTML | No error middleware | Add four-argument handler last |

**Async handlers (Express 4):** rejected promises are not caught automatically — wrap with `try/catch` and `next(err)`, or use Express 5.

## Real-World Applications

REST and JSON APIs, BFF layers, and small services that need a large middleware ecosystem (Helmet, CORS, body parsers).

**Example:** An API behind a load balancer logs every client as the LB IP — set `app.set('trust proxy', 1)` so rate limits and audit logs see the real client.

## Pros/Cons or Trade-offs

- **Pro:** Minimal and familiar — huge middleware ecosystem, easy to hire for.
- **Con:** You own structure, validation, and documentation — Nest/Fastify reduce boilerplate.
- **Con:** Extreme throughput or raw WebSocket fanout may fit [[uWebSocket]] better.

## Comparison

- vs [[express query handler]]: concepts = framework model; query handler = adapter pattern for routes.
- vs Fastify / Nest: more batteries and stricter structure; Express stays unopinionated.
- vs [[Socket IO]] / [[uWebSocket]]: realtime transports — Express is request/response HTTP first.

## Mistakes to Avoid

- Registering the error handler before routes — it never runs for later errors.
- Forgetting `express.json()` and debugging empty bodies.
- Leaving async Express 4 handlers without `next(err)` so the request hangs.
- Mounting routers with a doubled prefix (`/api` + `/api/users`).
