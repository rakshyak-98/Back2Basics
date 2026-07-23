[[ExpressJS]] [[NodeJS]] [[express error handler]] [[express query handler]]

# Express route regular expressions

> Express path patterns are **not** full JavaScript RegExp — anchoring, capture groups, and `*` semantics differ; misread routes cause 404s, open redirects, and ReDoS.

## Mental model

Express compiles route strings into an internal matcher (via `path-to-regexp`). A route like `/users/:id` is **anchored** to the full path segment unless you opt into regex or wildcards.

```
Request: GET /api/users/42/settings

Route '/users/:id'     → matches /users/42 only (one segment for :id)
Route '/users/:id(*)'  → :id captures rest including slashes (legacy)
Route /^\/users\/(\d+)$/ → full RegExp route — YOU own anchors ^ $
```

Two modes:
1. **String routes** — `:param`, optional `?`, custom `(regex)` per param, `*` splat (Express 4.x).
2. **RegExp routes** — `app.get(/^\/foo\/bar$/, ...)` — entire pattern must match path (query string excluded).

## Standard config / commands

### Named parameters with inline regex

```js
// Only digits — non-matching paths fall through to next route / 404
app.get('/users/:id(\\d+)', (req, res) => {
  res.json({ id: req.params.id });
});

// Slug: lowercase alphanumeric + hyphen
app.get('/posts/:slug([a-z0-9-]+)', handler);
```

### Optional segments

```js
app.get('/files/:dir/:file?', (req, res) => {
  // /files/a → file undefined
  // /files/a/b.txt → file = 'b.txt'
});
```

### Multiple handlers on same prefix

```js
app.get('/api/v1/users', listUsers);
app.get('/api/v1/users/:id(\\d+)', getUser);
// Order matters — static paths BEFORE parametric routes
```

### Full RegExp route

```js
app.get(/^\/legacy\/report-\d{4}-\d{2}$/, (req, res) => {
  // req.path available; no named captures unless you parse
});
```

### Router mount + relative paths

```js
const router = express.Router();
router.get('/:id(\\d+)', getOne);
app.use('/items', router); // matches /items/123
```

### Escaping literal dots

```js
// BAD: '/file.json' — dot may be treated specially in some matchers
// GOOD: explicit or RegExp
app.get('/file\\.json', serveManifest);
```

### ReDoS-safe patterns

```js
// BAD: nested quantifiers on user input path
app.get('/search/:q(.+)', handler); // if q is echoed in heavy regex elsewhere

// GOOD: bounded, simple param regex
app.get('/search/:q([^/]{1,100})', handler);
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Route never matches | Missing anchors on RegExp route; typo in param regex | Add `^...$`; test with `req.path` logging |
| Wrong handler runs | Route order — `/:id` before `/new` | Register static paths first |
| `:id` eats too much | Greedy `.+` in custom regex | Restrict charset: `[^/]+` or `(\\d+)` |
| 404 on valid URL | Router mount path doubled | Mount at `/api` + route `/users` → `/api/users` |
| `%2F` in param breaks | Decoded slash splits segments | Avoid slashes in params; use query string |
| Express 5 vs 4 splat change | `*` / `(*)` syntax migration | Check Express version docs for wildcard routes |
| Performance spike on some URLs | Catastrophic backtracking in regex | Simplify pattern; cap length; use string routes |
| `req.params` empty on RegExp route | Used anonymous groups incorrectly | Use named string routes or parse `req.path` |

## Gotchas

> [!WARNING]
> **Inline `(regex)` must be parenthesized and escaped for backslashes** — in JS strings: `'/:id(\\d+)'` (double backslash).

> [!WARNING]
> **String route ≠ JS RegExp** — `/[abc]/` as a string route is literal characters `[abc]`, not a character class. Use RegExp object or `:param(regex)`.

> [!WARNING]
> **Trailing slash** — `strict routing` setting affects `/foo` vs `/foo/`; inconsistent redirects cause duplicate cache entries.

> [!WARNING]
> **Case sensitivity** — default is case-sensitive; macOS dev on case-ins insensitive FS can hide `/User` vs `/user` bugs.

> [!WARNING]
> **`app.use('/path', fn)` matches prefix** — middleware runs for `/path`, `/path/`, `/path/anything` unless you end with `$` in RegExp or design routes carefully.

## When NOT to use

- **Complex URL parsing** — use a dedicated router (e.g. explicit path parser) instead of nested regex.
- **Validation as routing** — route should identify resource; validate body/query in middleware ([[express query handler]]).
- **Open-ended user-defined regex** — never compile user input into RegExp routes (ReDoS + bypass).

## Related

[[ExpressJS]] [[express error handler]] [[express query handler]] [[NodeJS]] [[Nginx]]
