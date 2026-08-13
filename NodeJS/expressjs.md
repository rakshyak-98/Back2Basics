[[NodeJS]] [[Express middleware]] [[HTTP module]]

# expressjs

> Minimal HTTP framework on Node’s `http` — routers and middleware; concurrency is still the single-threaded event loop.

---

## How it works

```txt
req → middleware… → route → res.send
         next()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Middleware** | `(req,res,next)` layer | “Auth, parse, log — then route.” |
| **app.set** | Framework settings | “`trust proxy`, view engine, etc.” |
| **Router** | Mountable mini-app | “Split features by path prefix.” |


## Configuration and commands

```js
import express from 'express'
const app = express()
app.set('trust proxy', 1)
app.use(express.json({ limit: '1mb' }))
app.get('/health', (_req, res) => res.send('ok'))
app.listen(3000)
```

| Knob | Why it matters |
|------|----------------|
| `trust proxy` | Correct client IP behind LB |
| `express.json` | Parses body when Content-Type matches |
| Error middleware `(err,req,res,next)` | Must be 4-arg, last |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `req.body` undefined | Missing parser / wrong CT | `express.json()`; check Content-Type |
| Hang forever | Forgot `res`/`next` | Always end or `next(err)` |
| Wrong client IP | Behind proxy | `trust proxy` |
| 404 on mounted router | Path double-prefix | Mount path + router paths |

---


## Gotchas

> [!WARNING]
> **CPU-heavy work blocks all requests** — offload to [[worker]] / [[child process]].

> [!WARNING]
> **Empty `{}` body** — no body, unmatched type, or parse error can look like empty object depending on setup.

---


## When not to use

- **Ultra-low-level HTTP** — raw `http` / Fastify if you need different perf model.
- **Non-HTTP services** — gRPC/queues aren’t Express’s job.

---


## Related

[[Express middleware]] [[HTTP module]] [[node error]]

## Sources

- [Wikipedia — expressjs](https://en.wikipedia.org/wiki/expressjs)
