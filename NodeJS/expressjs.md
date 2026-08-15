[[NodeJS]] [[Express middleware]] [[HTTP module]] [[node error]]

# expressjs

> Minimal HTTP framework on Node’s `http` — routers and middleware; concurrency is still the single-threaded event loop.

## Interview Relevance

Interviewers use **expressjs** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Middleware**, **app.set**, **Router**.

## Sources

- [Express — API reference](https://expressjs.com/en/4x/api.html) — deep-dive
- [Wikipedia — expressjs](https://en.wikipedia.org/wiki/expressjs) — overview

## Key Concepts

- **Middleware:** `(req,res,next)` layer — Auth, parse, log — then route.
- **app.set:** Framework settings — `trust proxy`, view engine, etc.
- **Router:** Mountable mini-app — Split features by path prefix.

## Technical Details

```txt
req → middleware… → route → res.send
         next()
```

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

## Real-World Applications

In production APIs and tooling, **expressjs** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **CPU-heavy work blocks all requests** — offload to [[worker]] / [[child process]]; **Empty `{}` body** — no body, unmatched type, or parse error can look like empty object depending on setup.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Minimal HTTP framework on Node’s `http` — routers and middleware; concurrency is…).
- **Con / when not:** **Ultra-low-level HTTP** — raw `http` / Fastify if you need different perf model.
- **Con / when not:** **Non-HTTP services** — gRPC/queues aren’t Express’s job.

## Comparison

vs [[Express middleware]]: know when each applies — do not treat them as interchangeable. vs [[HTTP module]]: Express adds routing/middleware; `http` is the primitive Server/IncomingMessage/ServerResponse. vs [[node error]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **CPU-heavy work blocks all requests** — offload to [[worker]] / [[child process]].
- **Empty `{}` body** — no body, unmatched type, or parse error can look like empty object depending on setup.
- **`req.body` undefined:** check Missing parser / wrong CT; fix: `express.json()`; check Content-Type
- **Hang forever:** check Forgot `res`/`next`; fix: Always end or `next(err)`
- **Wrong client IP:** check Behind proxy; fix: `trust proxy`
- **404 on mounted router:** check Path double-prefix; fix: Mount path + router paths
