[[ExpressJS]] [[NodeJS]] [[Node.js security flaws in architecture]] [[Express middleware]] [[express concepts]]

# Express Error Handler

> Express routes errors to middleware with four parameters `(err, req, res, next)` — `next(err)` or a wrapped async throw skips normal middleware and lands there; order and async handling determine whether clients see consistent JSON or leaked stacks.

---

## How errors propagate

Express distinguishes error-handling middleware by **arity**: four parameters, not three.

```txt
Request → parsers → routes → 404 factory → GLOBAL ERROR HANDLER (4 args)
                                    ↑
                              next(err) lands here
```

Without an async wrapper, rejected promises in `async (req, res)` **bypass** the error handler in Express 4 unless you use `try/catch` or a `catchAsync` wrapper. Express 5 propagates async errors natively — verify your version.

---

## Production-safe stack

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

---

## Async errors (Express 4)

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
```

### Unhandled rejections (last resort)

```javascript
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION', err);
  server.close(() => process.exit(1));
});
```

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Stack trace in production JSON | `NODE_ENV` not set | Gate `stack` on `development` only |
| 404 returns HTML | Static middleware before API 404 | Separate routers; 404 before static |
| Async route hangs, no log | Missing `catch(next)` | Wrap async handlers |
| `headers already sent` | Double `res.send` in error path | `if (res.headersSent) return next(err)` |
| Error handler never runs | Only 3-arg middleware registered | Must be `(err, req, res, next)` |

---

## Security notes

- Never send `err.stack` to clients in any environment.
- Scrub bodies and passwords before `console.error` in error middleware.
- Error handler must be registered **after** all `app.use` routes; 404 handler immediately before it.

---

## Related

[[Express middleware]] · [[Node.js security flaws in architecture]] · [[Error handeling]] · [[node error]]
