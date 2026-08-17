[[NodeJS]] [[node error]] [[Express middleware]] [[async utils]] [[Runtime Errors]]

# Error handling

> How Node and Express turn thrown/rejected failures into logged, typed responses — custom `Error` subclasses, `next(err)`, and process-level guards.

```txt
        Error handling ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about error handling to see if you separate operational erro…

## Sources
- [Node.js — Errors](https://nodejs.org/api/errors.html) — deep-dive
- [Express — Error handling](https://expressjs.com/en/guide/error-handling.html) — overview

## Key Concepts
- **Operational vs programmer errors:** bad input / network = handle and continue
- **Custom Error subclass:** `name`, `code`, and optional `statusCode` for HTTP mapping.
- **Async propagation:** rejected promises in Express 4 need `next(err)` or an async wrapper
- **Process guards:** `uncaughtException` / `unhandledRejection` are last-resort

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

- Centralize mapping: validation → 400, auth → 401/403, not found → 404, unexpe…

## Mistakes to Avoid
- **Mistake:** **Swallowing rejections** with empty `catch`
- **Mistake:** **Trusting `uncaughtException` to continue**
- **Mistake:** **Leaking stack traces** to public API clients
- **Mistake:** **Forgetting 4-arg error middleware** in Express

## Pros/Cons or Trade-offs
- **Pro:** Typed errors + one middleware keep routes thin and responses consistent.
- **Con:** Over-catching at the process level hides bugs and leaves the process in an unknown state.

## Comparison
- vs [[node error]]: Node’s built-in error shapes and codes


### Use cases
- API services map domain failures to stable error codes for clients while pagi…
