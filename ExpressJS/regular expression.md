[[ExpressJS]] [[NodeJS]] [[express error handler]] [[express query handler]] [[Nginx]]

# Express route regular expressions

> Express path patterns are not full JavaScript RegExp — anchoring, capture groups, and `*` semantics differ from string routes; misread routes cause 404s, open redirects, and ReDoS.

---

## Two routing modes

Express compiles string routes via `path-to-regexp`. RegExp routes are raw patterns you own entirely.

```txt
String route '/users/:id'     → one segment for :id
RegExp route /^\/users\/(\d+)$/ → full path match (query excluded)
```

1. **String routes** — `:param`, optional `?`, inline `(regex)` per parameter, `*` splat (Express 4.x).
2. **RegExp routes** — `app.get(/^\/foo\/bar$/, ...)` — entire pattern must match `req.path`.

---

## Named parameters with inline regex

```js
app.get('/users/:id(\\d+)', (req, res) => {
  res.json({ id: req.params.id });
});

app.get('/posts/:slug([a-z0-9-]+)', handler);
```

### Optional segments

```js
app.get('/files/:dir/:file?', (req, res) => {
  // /files/a → file undefined
  // /files/a/b.txt → file = 'b.txt'
});
```

### Route order

```js
app.get('/api/v1/users', listUsers);
app.get('/api/v1/users/:id(\\d+)', getUser);
// Static paths BEFORE parametric routes
```

### Router mount

```js
const router = express.Router();
router.get('/:id(\\d+)', getOne);
app.use('/items', router); // matches /items/123
```

### ReDoS-safe patterns

```js
// BAD: unbounded capture
app.get('/search/:q(.+)', handler);

// GOOD: bounded charset
app.get('/search/:q([^/]{1,100})', handler);
```

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Route never matches | Missing `^` `$` on RegExp route | Add anchors; log `req.path` |
| Wrong handler runs | `/:id` registered before `/new` | Static paths first |
| `:id` eats too much | Greedy `.+` in custom regex | Use `[^/]+` or `(\\d+)` |
| 404 on valid URL | Doubled mount prefix | `/api` + `/users` → `/api/users` |
| `%2F` in param breaks | Decoded slash splits segments | Use query string instead |
| Performance spike | Catastrophic backtracking | Simplify; cap length |

---

## Critical gotchas

- Inline `(regex)` needs double backslashes in JS strings: `'/:id(\\d+)'`.
- String route `/[abc]/` is literal `[abc]`, not a character class — use RegExp or `:param(regex)`.
- `strict routing` affects `/foo` vs `/foo/` — inconsistent redirects duplicate cache entries.
- Default matching is case-sensitive — macOS case-insensitive FS can hide `/User` vs `/user` bugs.
- `app.use('/path', fn)` matches prefix — runs for `/path/anything` unless designed carefully.

Validation belongs in middleware ([[express query handler]]), not in routing regex.

---

## Related

[[express error handler]] · [[express query handler]] · [[NodeJS]] · [[Nginx]]
