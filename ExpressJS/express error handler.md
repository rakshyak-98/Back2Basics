
```js
import express from 'express';
const app = express();

// 1. Pre-Route Middleware (Parsers, CORS)
app.use(express.json({ limit: '10kb' }));

// 2. Your Routes
app.use('/api/v1/hotels', hotelRouter);
app.use('/api/v1/auth', authRouter);

// 3. 404 Handler (For routes that don't exist)
app.all('*', (req, res, next) => {
  const err = new Error(`Can't find ${req.originalUrl} on this server!`);
  err.statusCode = 404;
  next(err); // Passing an argument to next() always triggers the error handler
});

// 4. THE GLOBAL ERROR HANDLER (Must be last)
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    status: 'error',
    message: err.message || 'Internal Server Error',
    // stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
  });
});

app.listen(3000);
```