[[NodeJS]] [[node error]] [[Express middleware]] [[async utils]] [[Runtime Errors]]

# Error handling

> How Node and Express turn thrown/rejected failures into logged, typed responses — custom `Error` subclasses, `next(err)`, and process-level guards.

## Interview Relevance

Interviewers ask about error handling to see if you separate operational errors from programmer bugs, propagate async failures correctly, and avoid crashing the whole process on expected request failures.

## Sources

- [Node.js — Errors](https://nodejs.org/api/errors.html) — deep-dive
- [Express — Error handling](https://expressjs.com/en/guide/error-handling.html) — overview

## Key Concepts

- **Operational vs programmer errors:** bad input / network = handle and continue; invariant bugs = fail fast and restart.
- **Custom Error subclass:** `name`, `code`, and optional `statusCode` for HTTP mapping.
- **Async propagation:** rejected promises in Express 4 need `next(err)` or an async wrapper; Express 5 catches async route errors.
- **Process guards:** `uncaughtException` / `unhandledRejection` are last-resort — log and exit for unknown state.

## Technical Details

```js
class AppError extends Error {
  constructor(message, { code = 'APP_ERROR', statusCode = 500 } = {}) {
    super(message)
    this.name = 'AppError'
    this.code = code
    this.statusCode = statusCode
  }
}

// Express error middleware (4 args) — must be registered last
app.use((err, req, res, next) => {
  const status = err.statusCode || 500
  res.status(status).json({ error: err.code || 'INTERNAL', message: err.message })
})

// Async route without Express 5:
const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next)
```

Centralize mapping: validation → 400, auth → 401/403, not found → 404, unexpected → 500 without leaking stacks to clients.

## Real-World Applications

API services map domain failures to stable error codes for clients while paging on unexpected 500s. Example: a payments service throws `AppError('card declined', { code: 'CARD_DECLINED', statusCode: 402 })` and lets error middleware format the JSON body.

## Pros/Cons or Trade-offs

- **Pro:** Typed errors + one middleware keep routes thin and responses consistent.
- **Con:** Over-catching at the process level hides bugs and leaves the process in an unknown state.

## Comparison

vs [[node error]]: Node’s built-in error shapes and codes. vs [[async utils]]: wrappers that forward promise rejections to `next`. vs [[Runtime Errors]]: symptoms and crash classes at runtime.

## Mistakes to Avoid

- **Swallowing rejections** with empty `catch` — request hangs or returns success incorrectly.
- **Trusting `uncaughtException` to continue** — memory/locks may already be corrupt; exit and let the supervisor restart.
- **Leaking stack traces** to public API clients.
- **Forgetting 4-arg error middleware** in Express — errors never become responses.
