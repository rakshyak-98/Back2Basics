<!-- note-strategy: operational -->
[[ExpressJS]] [[NodeJS]] [[Express middleware]]

# express concepts

> Express concepts — minimal HTTP framework: app, router, middleware chain `(req,res,next)`, and error middleware.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Request flows through middleware until a handler sends a response. `next(err)` jumps to error handlers. Order of `app.use` matters.

```txt
req → mw1 → mw2 → route handler → res
              ↘ next(err) → err mw
```

| Piece | Job |
|-------|-----|
| `app` | Top-level |
| `Router` | Mountable routes |
| Middleware | Cross-cutting |

---

## Standard config / commands

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
| Middleware order | Auth before handler |
| `Router({ mergeParams })` | Nested params |
| Trust proxy | Correct IPs behind LB |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hangs | Never `res`/`next` | Always end or next |
| Body empty | Missing json parser | `express.json()` |
| 404 all | Mount path | Check `app.use('/api', router)` |
| Error HTML | No err middleware | 4-arg handler |

---

## Gotchas

> [!WARNING]
> **Async errors** — must `next(err)` or wrap; Express 4 doesn’t catch async auto.

> [!WARNING]
> **`app.use(path)` vs `app.get`** — method matching.

---

## When NOT to use

- **Extreme throughput raw TCP** — specialized servers.
- **Full batteries framework** — Nest/Fastify may fit better.

---

## Related

[[Express middleware]] [[express query handler]] [[express build]]
