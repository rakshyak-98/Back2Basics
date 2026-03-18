## Express.js v5 — Full Feature Reference

> Latest version: **5.2.1** | Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.

---

### 1. Application Setup — `express()`

```js
import express from 'express'  // ESM (now clean in v5)
// const express = require('express') // CommonJS still works

const app = express()

// Global app settings
app.set('view engine', 'ejs')       // template engine
app.set('views', './views')          // views directory
app.set('trust proxy', 1)            // trust first proxy (for req.ip behind nginx)
app.set('case sensitive routing', false) // /Foo and /foo treated as same
app.set('strict routing', false)     // /foo and /foo/ treated as same

app.get('settingName')               // read a setting value

app.listen(3000, () => {
  console.log('Server running on port 3000')
})
```

---

### 2. Routing — `app.METHOD()`

```js
// Basic HTTP method routes
app.get('/path', handler)
app.post('/path', handler)
app.put('/path', handler)
app.patch('/path', handler)
app.delete('/path', handler)   // NOTE: app.del() removed in v5, use app.delete()
app.options('/path', handler)
app.head('/path', handler)

// Match ALL HTTP methods
app.all('/path', (req, res, next) => {
  // runs for GET, POST, PUT, DELETE, etc.
  next()
})

// Route parameters — captured in req.params
app.get('/users/:id', (req, res) => {
  // req.params.id → dynamic segment
})

// Optional parameter
app.get('/users/:id?', handler)

// Wildcard — matches anything after /files/
app.get('/files/*splat', handler)   // req.params.splat in v5

// Chained route handlers (multiple callbacks)
app.get('/path',
  middlewareFn,    // e.g. auth check
  handlerFn        // final handler
)
```

---

### 3. `app.route()` — Chained Route Definition

Groups all HTTP methods for a single path to avoid repetition.

```js
app.route('/users/:id')
  .all((req, res, next) => {
    // runs for every method on this route (e.g. auth check)
    next()
  })
  .get((req, res) => {
    // fetch user
  })
  .put((req, res) => {
    // update user
  })
  .delete((req, res) => {
    // delete user
  })
```

---

### 4. `express.Router()` — Modular Route Handling

The Router in Express.js is a mini Express application — it provides a way to create modular and mountable route handlers, allowing you to keep routes organized and manageable especially in large applications.

```js
// routes/users.js
import { Router } from 'express'
const router = Router({
  caseSensitive: false,  // inherit from app by default
  strict: false,         // trailing slash behavior
  mergeParams: false     // merge parent req.params into this router's
})

// Router-level middleware (only applies to this router)
router.use((req, res, next) => {
  // runs before every route in this file
  next()
})

router.get('/', handler)           // GET /users
router.post('/', handler)          // POST /users
router.get('/:id', handler)        // GET /users/:id
router.put('/:id', handler)
router.delete('/:id', handler)

// Mount on app
app.use('/users', router)

export default router
```

---

### 5. Middleware — `app.use()`

Middleware functions execute during the request-response cycle and have access to both the request object (`req`) and the response object (`res`). Express middleware includes application-level, router-level, and error handling functionality and can be built-in or from a third party.

```js
// Application-level middleware (runs for every request)
app.use((req, res, next) => {
  // modify req/res, log, auth check, etc.
  next()  // MUST call next() or the request will hang
})

// Path-scoped middleware (only runs for matching paths)
app.use('/api', (req, res, next) => {
  next()
})

// Chaining multiple middleware functions
app.use(middlewareA, middlewareB, middlewareC)

// Order matters — define middleware BEFORE routes that need it
app.use(express.json())  // ✅ parses JSON before routes run
app.get('/data', handler)
```

---

### 6. Async Middleware & Promise-Based Error Handling _(v5 — Key Change)_

Express 5 improves error handling in async middleware and routes by automatically passing rejected promises to the error-handling middleware, removing the need for `try/catch` blocks.

```js
// ❌ Express 4 — manual try/catch required
app.get('/data', async (req, res, next) => {
  try {
    const result = await fetchData()
    res.json(result)
  } catch (err) {
    next(err)   // had to manually forward errors
  }
})

// ✅ Express 5 — rejected promise auto-forwarded to error handler
app.get('/data', async (req, res) => {
  const result = await fetchData()  // if this throws, Express catches it
  res.json(result)
})

// Async middleware works the same way
app.use(async (req, res, next) => {
  req.user = await getUser(req.headers.authorization)
  next()
})
```

---

### 7. Error Handling Middleware

```js
// Must have exactly 4 parameters — (err, req, res, next)
app.use((err, req, res, next) => {
  console.error(err.stack)

  // v5: throws an error if status code is invalid (e.g. res.status(99))
  res.status(err.status || 500).json({
    message: err.message || 'Internal Server Error'
  })
})

// 404 catch-all — place AFTER all routes
app.use((req, res) => {
  res.status(404).json({ message: 'Not found' })
})
```

---

### 8. Built-in Middleware

```js
// Parse incoming JSON bodies → populates req.body
app.use(express.json({
  limit: '10mb',     // max body size
  strict: true       // only accept arrays/objects
}))

// Parse URL-encoded form data → populates req.body
app.use(express.urlencoded({
  extended: false,   // v5 default changed to false (uses querystring)
  limit: '10mb'
}))

// Parse raw binary body → req.body as Buffer
app.use(express.raw({ type: 'application/octet-stream' }))

// Parse plain text body → req.body as string
app.use(express.text({ type: 'text/plain' }))

// Serve static files from a directory
app.use(express.static('public', {
  maxAge: '1d',        // cache-control header
  etag: true,          // enable ETag generation
  index: 'index.html', // default file
  dotfiles: 'ignore'   // ignore hidden files
}))
```

---

### 9. `app.param()` — Route Parameter Pre-Processing

Automatically runs whenever a specific named parameter appears in a route.

```js
// Fires whenever :userId appears in any route
app.param('userId', async (req, res, next, id) => {
  // validate / load resource and attach to req
  req.user = await User.findById(id)
  if (!req.user) return res.status(404).json({ message: 'User not found' })
  next()
})

// Now req.user is pre-loaded in all routes with :userId
app.get('/users/:userId', (req, res) => {
  res.json(req.user)
})

// NOTE: app.param(fn) — the callback form — was REMOVED in v5
```

---

### 10. Request Object — `req`

```js
req.params         // route parameters     → { id: '123' }
req.query          // query string         → { search: 'foo' }
req.body           // parsed request body  → requires body-parsing middleware
req.headers        // HTTP headers
req.method         // HTTP method          → 'GET', 'POST', etc.
req.url            // relative URL         → '/users?foo=bar'
req.originalUrl    // full original URL (unchanged by middleware)
req.path           // URL path only        → '/users'
req.baseUrl        // mount path of the router
req.hostname       // from Host header
req.ip             // client IP (respects trust proxy)
req.protocol       // 'http' or 'https'
req.secure         // true if HTTPS
req.subdomains     // ['api', 'v2'] from 'v2.api.example.com'
req.cookies        // parsed cookies (requires cookie-parser)
req.signedCookies  // verified signed cookies
req.fresh          // true if response is still "fresh" (ETag/Last-Modified)
req.stale          // opposite of req.fresh
req.xhr            // true if X-Requested-With: XMLHttpRequest
req.app            // reference to the Express app instance

// Content negotiation methods
req.accepts('html')                    // check Accept header
req.acceptsCharsets('utf-8')           // NOTE: pluralized in v5
req.acceptsEncodings('gzip')           // NOTE: pluralized in v5
req.acceptsLanguages('en', 'es')       // NOTE: pluralized in v5
req.is('application/json')             // check Content-Type

// Helpers
req.get('header-name')                 // get a specific request header
req.range(size)                        // parse Range header
```

---

### 11. Response Object — `res`

```js
// Send responses
res.send('Hello')                      // string / Buffer / object
res.json({ key: 'value' })             // JSON (sets Content-Type automatically)
res.jsonp({ key: 'value' })            // JSONP response
res.sendFile('/absolute/path/to/file') // stream a file
res.download('/path/to/file', 'name.pdf') // force download
res.end()                              // end without data

// Status codes
// v5: throws error for invalid codes (e.g. res.status(99) → error)
res.status(404).json({ message: 'Not found' })
res.sendStatus(200)                    // sends status + its text body

// Redirects
res.redirect('/new-path')              // 302 by default
res.redirect(301, '/permanent-path')

// Headers
res.set('X-Custom-Header', 'value')    // set a response header
res.get('Content-Type')                // read a response header
res.type('json')                       // set Content-Type shorthand
res.append('Link', '<http://...>')     // append to header

// Cookies
res.cookie('name', 'value', {
  maxAge: 900000,
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
})
res.clearCookie('name')

// Template rendering
res.render('viewName', {
  title: 'Page Title',
  data: []              // locals passed to template
})

// Locals (data available to templates for this response)
res.locals.user = req.user

// Misc
res.vary('Accept')                     // add Vary header
res.format({                           // content negotiation
  'text/html': () => res.send('<h1>HTML</h1>'),
  'application/json': () => res.json({ msg: 'JSON' }),
  default: () => res.status(406).send('Not Acceptable')
})
res.attachment('filename.pdf')         // set Content-Disposition
res.links({ next: 'http://...' })      // set Link header
res.location('/new-path')             // set Location header only (no redirect)
```

---

### 12. Template Engines — `app.engine()`

```js
import { engine } from 'express-handlebars'

// Register a custom or third-party engine
app.engine('handlebars', engine())
app.set('view engine', 'handlebars')
app.set('views', './views')

// Render with res.render()
app.get('/', (req, res) => {
  res.render('home', {
    title: 'Home',
    layout: 'main'   // engine-specific options
  })
})
```

---

### 13. Routing Security — ReDoS Fix _(v5 — Key Change)_

To avoid Regular Expression Denial of Service (ReDoS) attacks, Express 5 no longer supports sub-expressions in regular expressions, for example `/:foo(\\d+)`.

```js
// ❌ Express 4 — inline regex in route params (REMOVED in v5)
app.get('/:id(\\d+)', handler)

// ✅ Express 5 — validate in middleware instead
app.get('/:id', (req, res, next) => {
  if (!/^\d+$/.test(req.params.id)) return res.status(400).send('Invalid ID')
  next()
}, handler)
```

---

### 14. `app.router` — Base Router Reference _(Returned in v5)_

The `app.router` object, which was removed in Express.js 4, has returned in Express.js 5. However, it's now just a reference to the base Express router — you no longer need to explicitly load it like in Express 3; it's automatically available when you start using routing.

```js
// Access the app's base router directly
console.log(app.router)   // reference to root Router instance

// Useful for dynamically inspecting or attaching to the base router
app.router.stack           // array of registered layers/middleware
```

---

### 15. Sub-Applications — `app.use()` with mounted apps

```js
const adminApp = express()  // standalone mini-app

adminApp.get('/dashboard', handler)
adminApp.get('/users', handler)

// Mount admin app at a prefix
app.use('/admin', adminApp)
// → /admin/dashboard, /admin/users
```

---

### Summary Table

| Feature                     | Purpose                                              |
| --------------------------- | ---------------------------------------------------- |
| `express()` + `app.set()`   | App creation & configuration                         |
| `app.METHOD()`              | HTTP route definitions (GET, POST, PUT, DELETE…)     |
| `app.route()`               | Chained multi-method route on same path              |
| `express.Router()`          | Modular, mountable route files                       |
| `app.use()`                 | Middleware registration (global or path-scoped)      |
| Async middleware (v5)       | Auto-catches rejected promises — no try/catch needed |
| Error middleware (4 params) | Centralized error handling                           |
| `express.json()`            | Parse JSON request bodies                            |
| `express.urlencoded()`      | Parse form data bodies                               |
| `express.raw()`             | Parse binary bodies as Buffer                        |
| `express.text()`            | Parse plain-text bodies                              |
| `express.static()`          | Serve static files                                   |
| `app.param()`               | Pre-process named route parameters                   |
| `req` object                | Full access to request data                          |
| `res` object                | Full control over response                           |
| Template engines            | Server-side rendering via `res.render()`             |
| ReDoS-safe routing (v5)     | Sub-expression regex removed for security            |
| `app.router` (v5)           | Direct reference to base router instance             |
| Sub-applications            | Mount Express apps as middleware                     |