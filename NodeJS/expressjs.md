[[NodeJS]] [[Express middleware]] [[HTTP module]] [[node error]]

# expressjs

> Minimal HTTP framework on Node’s `http` — routers and middleware; concurrency is still the single-threaded event loop.

```txt
        expressjs ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **expressjs** to check whether you can explain the mechanism…

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

## Mistakes to Avoid
- **Mistake:** **CPU-heavy work blocks all requests**
- **Mistake:** **Empty `{}` body**
- **Mistake:** **`req.body` undefined:** check Missing parser / wrong CT
- **Mistake:** **Hang forever:** check Forgot `res`/`next`
- **Mistake:** **Wrong client IP:** check Behind proxy; fix: `trust proxy`
- **Mistake:** **404 on mounted router:** check Path double-prefix

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Minimal HTTP framework on Node’s `http` — routers and middleware; concurrency is…).
- **Con / when not:** **Ultra-low-level HTTP**
- **Con / when not:** **Non-HTTP services** — gRPC/queues aren’t Express’s job.

## Comparison
- vs [[Express middleware]]: know when each applies


### Use cases
- In production APIs and tooling, **expressjs** shows up whenever teams ship No…
