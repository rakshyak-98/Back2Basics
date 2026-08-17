[[express concepts]] [[express query handler]] [[express error handler]] [[expressjs]] [[Nginx]]

# Express route regular expressions

> Express path patterns are not full JavaScript `RegExp` — anchoring, capture groups, and `*` semantics differ; misread routes cause 404s, open redirects, and ReDoS.

```txt
        Express route regu ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers test whether you understand `path-to-regexp` vs raw `RegExp` rou…

## Sources
- [Express — Routing](https://expressjs.com/en/guide/routing.html) — deep-dive
- [path-to-regexp](https://github.com/pillarjs/path-to-regexp) — deep-dive
- [OWASP — Regular expression Denial of Service](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS) — overview

## Key Concepts
- **String routes:** `'/users/:id'` — one path segment for `:id` unless you customize.
- **Inline parameter regex:** `'/:id(\\d+)'` — constrains a named param (double backslashes in JS strings).
- **RegExp routes:** `app.get(/^\/users\/(\d+)$/, ...)` — full path match; add `^` / `$`.
- **Order:** static paths before parametric ones (`/users/new` before `/users/:id`).
- **ReDoS:** unbounded `.+` in route patterns can burn CPU — bound length and charset.


- **Core:** String routes go through `path-to-regexp` (`:param`, optional segments, inlin…

## Technical Details
```txt
String route '/users/:id'     → one segment for :id
RegExp route /^\/users\/(\d+)$/ → full path match (query excluded)
```

```js
app.get('/users/:id(\\d+)', (req, res) => {
  res.json({ id: req.params.id });
});

app.get('/posts/:slug([a-z0-9-]+)', handler);

app.get('/files/:dir/:file?', (req, res) => {
  // /files/a → file undefined
  // /files/a/b.txt → file = 'b.txt'
});

app.get('/api/v1/users', listUsers);
app.get('/api/v1/users/:id(\\d+)', getUser);
// Static paths BEFORE parametric routes

const router = express.Router();
router.get('/:id(\\d+)', getOne);
app.use('/items', router); // matches /items/123
```

```js
// BAD: unbounded capture
app.get('/search/:q(.+)', handler);

// GOOD: bounded charset
app.get('/search/:q([^/]{1,100})', handler);
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Route never matches | Missing `^` `$` on RegExp route | Add anchors; log `req.path` |
| Wrong handler runs | `/:id` before `/new` | Static paths first |
| `:id` eats too much | Greedy `.+` | Use `[^/]+` or `(\\d+)` |
| 404 on valid URL | Doubled mount prefix | `/api` + `/users` → `/api/users` |
| `%2F` in param breaks | Decoded slash splits segments | Prefer query string |
| Performance spike | Catastrophic backtracking | Simplify; cap length |

- **Gotchas:** string route `/[abc]/` is literal `[abc]`, not a character class.
- `strict routing` changes `/foo` vs `/foo/`.
- Default matching is case-sensitive.
- `app.use('/path', fn)` is a prefix match.

## Mistakes to Avoid
- **Mistake:** Unbounded `.+` captures that invite ReDoS
- **Mistake:** Forgetting double backslashes in string route regex: `'/:id(\\d+…
- **Mistake:** Putting parametric routes ahead of static siblings
- **Mistake:** Treating routing regex as the only input validation
- **Mistake:** Assuming RegExp routes match query strings

## Pros/Cons or Trade-offs
- **Pro:** Inline regex keeps invalid IDs out of handlers early.
- **Con:** Complex patterns hide bugs; validation middleware is clearer for business rules.
- **Con:** Raw RegExp routes are powerful and easy to get wrong (anchors, ReDoS).

## Comparison
- vs [[express query handler]] validation: routing regex = shape of the path
- vs [[Nginx]] location regex: similar order and greediness pitfalls at the reverse-proxy layer.
- vs Express 5 / newer `path-to-regexp`: splat and optional syntax differ by major version


### Use cases
- ID-constrained REST resources, optional file-path segments, and API versionin…

- **Example:** Registering `GET /users/:id` before `GET /users/export` makes `e…
