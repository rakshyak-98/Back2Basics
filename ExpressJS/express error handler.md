[[express concepts]] [[Express middleware]] [[expressjs]] [[Node.js security flaws in architecture]] [[node error]] [[Error handeling]]

# Express Error Handler

> Express routes failures to four-argument middleware `(err, req, res, next)` — `next(err)` or a wrapped async throw skips normal handlers and lands there.

```txt
        Express Error Hand ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you know arity-based error middleware, Express 4 v…

## Sources
- [Express — Error handling](https://expressjs.com/en/guide/error-handling.html) — deep-dive
- [Express — Migrating to Express 5 (rejected promises)](https://expressjs.com/en/guide/migrating-5.html) — overview
- [Node.js — Errors](https://nodejs.org/api/errors.html) — overview

## Key Concepts
- **Arity:** `(err, req, res, next)`
- **Operational vs programmer errors:** expected 4xx (`isOperational`) vs unexpected 500
- **Async gap (Express 4):** rejected promises bypass the error handler unless you `catch(next)` or wrap h…
- **Express 5:** rejected promises from middleware/handlers forward to the error handler autom…
- **Headers already sent:** if a handler already wrote the body, defer to the default handler via `next(e…


- **Core:** Error-handling middleware is identified by four parameters. Anything that cal…

## Technical Details
```txt
Request → parsers → routes → 404 factory → GLOBAL ERROR HANDLER (4 args)
                                    ↑
                              next(err) lands here
```

```javascript
import express from 'express';

const app = express();

app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

app.use('/api/v1/hotels', hotelRouter);
app.use('/api/v1/auth', authRouter);

app.all('*', (req, res, next) => {
  const err = new Error(`Can't find ${req.originalUrl} on this server`);
  err.statusCode = 404;
  next(err);
});

app.use((err, req, res, next) => {
  if (res.headersSent) return next(err);

  err.statusCode = err.statusCode || 500;
  err.status = err.status || (err.statusCode >= 500 ? 'error' : 'fail');

  if (process.env.NODE_ENV === 'development') {
    return res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
      stack: err.stack,
      error: err,
    });
  }

  if (err.isOperational) {
    return res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
    });
  }

  console.error('ERROR', err);
  return res.status(500).json({
    status: 'error',
    message: 'Something went wrong',
  });
});

app.listen(3000);
```

- **Async wrapper (Express 4):** 

```javascript
const catchAsync = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/user/:id', catchAsync(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) {
    const err = new Error('User not found');
    err.statusCode = 404;
    err.isOperational = true;
    throw err;
  }
  res.json(user);
}));
```

```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}
```

```javascript
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION', err);
  server.close(() => process.exit(1));
});
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Stack in production JSON | `NODE_ENV` not set | Gate `stack` on development only |
| 404 returns HTML | Static middleware before API 404 | Separate routers; 404 before static |
| Async route hangs, no log | Missing `catch(next)` on Express 4 | Wrap async handlers |
| `headers already sent` | Double `res.send` in error path | `if (res.headersSent) return next(err)` |
| Error handler never runs | Only 3-arg middleware registered | Must be `(err, req, res, next)` |

## Mistakes to Avoid
- **Mistake:** Sending `err.stack` to clients in any non-development environment
- **Mistake:** Logging request bodies that may contain passwords or tokens
- **Mistake:** Registering the error handler before routes
- **Mistake:** Relying on Express 4 async handlers without `catch(next)`
- **Mistake:** Calling `res.json` again after headers were already sent

## Pros/Cons or Trade-offs
- **Pro:** One place to shape status codes, logging, and client payloads.
- **Con:** Express 4 async gaps are easy to miss until production hangs.
- **Con:** Over-sharing error objects in development habits often ship to production if `NODE_ENV` is wrong.

## Comparison
- vs default Express handler: default may send HTML; custom keeps API clients on JSON.
- vs [[node error]] / process-level handlers: those catch escapes outside the request pipeline
- vs GraphQL ([[graphql-yoga]]): GraphQL often returns HTTP 200 with errors in the body


### Use cases
- JSON APIs that need stable error envelopes, hotel/booking backends with opera…

- **Example:** A mobile client shows “Something went wrong” for a missing room
