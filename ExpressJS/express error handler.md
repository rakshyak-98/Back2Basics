[[ExpressJS]] [[NodeJS]] [[Node.js security flaws in architecture]] [[Express middleware]]

# Express Error Handler

> One-line: four-argument middleware `(err, req, res, next)` must be registered **last** — centralize status codes, hide stacks in prod, never leak internals.

## Mental model

Express distinguishes error-handling middleware by **arity (4 params)**. Calling `next(err)` or throwing inside async route (with wrapper) skips normal middleware and jumps to error handler.

```
Request → parsers → routes → 404 factory → GLOBAL ERROR HANDLER (4 args)
                                    ↑
                              next(err) lands here
```

Without async wrapper, rejected Promises in `async (req,res)` ** bypass** error handler unless you use Express 5 or explicit `try/catch`.

---

## Standard config / commands

### Production-safe stack

```javascript
import express from 'express';

const app = express();

// 1. Pre-route middleware
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// 2. Routes
app.use('/api/v1/hotels', hotelRouter);
app.use('/api/v1/auth', authRouter);

// 3. 404 — routes that don't exist
app.all('*', (req, res, next) => {
  const err = new Error(`Can't find ${req.originalUrl} on this server`);
  err.statusCode = 404;
  next(err);
});

// 4. Global error handler — MUST be last
app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || err.statusCode >= 500 ? 'error' : 'fail';

  if (process.env.NODE_ENV === 'development') {
    return res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
      stack: err.stack,
      error: err,
    });
  }

  // Operational vs programming errors
  if (err.isOperational) {
    return res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
    });
  }

  // Unknown/programming error — log, generic response
  console.error('ERROR', err);
  return res.status(500).json({
    status: 'error',
    message: 'Something went wrong',
  });
});

app.listen(3000);
```

### Async errors (Express 4)

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

Express 5: native async error propagation — verify your version.

### Custom AppError class

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

// usage: throw new AppError('Invalid email', 400);
```

### Unhandled rejections (last resort)

```javascript
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION', err);
  // graceful shutdown — don't leave corrupt state
  server.close(() => process.exit(1));
});
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stack trace in prod JSON | `NODE_ENV` | Gate stack on `development` only |
| 404 returns HTML not JSON | Error handler after static middleware order | Move API routes + 404 before static; separate routers |
| Async route hangs, no log | Missing `catch(next)` | Wrap async handlers |
| `headers already sent` | Double `res.send` in error path | `if (res.headersSent) return next(err)` |
| Validation errors inconsistent | Ad-hoc status codes | Centralize in error class + handler |
| Error handler never runs | Only 3-arg middleware registered | Must be `(err, req, res, next)` |

---

## Gotchas

> [!WARNING]
> **Order matters** — error handler after all `app.use` routes; 404 handler before error handler.

> [!WARNING]
> **`next()` with no err after headers sent** — Express 4 default behavior changed; check docs for your version.

> [!WARNING]
> **Logging PII in error middleware** — scrub bodies/passwords before `console.error`.

> [!WARNING]
> **Same handler for 404 and 500** — fine if statusCode distinguishes; don't leak path existence on auth-sensitive routes (optional generic 404).

---

## When NOT to use

- **Per-route try/catch everywhere** — duplicates logic; use wrapper + global handler.
- **Sending `err.stack` to clients in any environment** — security finding every time.

---

## Related

[[Express middleware]] [[Node.js security flaws in architecture]] [[Error handeling]] [[node error]]
