[[express concepts]] [[Express middleware]] [[express error handler]] [[Service Layer]] [[graphql-yoga]]

# express query handler

> Route handlers are adapters: read `req.query`, `req.params`, and `req.body`, validate, call a service, and map outcomes to HTTP status and JSON.

```txt
        express query hand ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers look for thin controllers, input validation, correct status code…

## Sources
- [Express — Request](https://expressjs.com/en/4x/api.html#req) — deep-dive
- [Express — Response](https://expressjs.com/en/4x/api.html#res) — overview
- [OWASP — Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) — overview

## Key Concepts
- **Adapter role:** HTTP in, domain call out
- **`req.query` / `req.params`:** always strings (or arrays of strings) until you coerce and validate.
- **Status discipline:** 4xx for client mistakes, 5xx for server failures
- **Pagination:** `limit`, `cursor`, or `page` live in query strings — validate bounds.
- **Pollution risk:** do not blindly merge query objects into models (prototype pollution / unexpec…


- **Core:** A query (or route) handler translates HTTP into application calls. Validation…

## Technical Details
```txt
HTTP request → handler → service → database
                  ↘ 400 / 401 / 404 / 500
```

```js
app.get('/users/:id', async (req, res, next) => {
  try {
    const id = String(req.params.id)
    const user = await users.get(id)
    if (!user) return res.status(404).json({ error: 'not found' })
    res.json(user)
  } catch (e) {
    next(e)
  }
})
```

| Concern | Practice |
|---------|----------|
| Validation | Schema-check (Zod, Joi) before the service call |
| Status codes | Explicit `res.status()` — never default 200 on failure |
| Pagination | Bound `limit`; prefer cursors for large sets |
| Body | `express.json()` mounted before routes that read `req.body` |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Query values always strings | Untyped `req.query` | Coerce and validate |
| Empty body | Parser missing | `express.json()` before routes |
| Unhandled async error | No `try` / `next` | Wrap async handlers (Express 4) |
| 200 with error payload | Wrong status | Set explicit `res.status()` |

- Array query params (`?tag=a&tag=b`) become arrays or last-wins depending on p…

## Mistakes to Avoid
- **Mistake:** Putting SQL or ORM calls directly in every route without a servi…
- **Mistake:** Trusting `req.query` types without coercion
- **Mistake:** Returning 200 with `{ error: ..
- **Mistake:** Merging query objects into Mongoose/update payloads without allo…

## Pros/Cons or Trade-offs
- **Pro:** Clear HTTP boundary — easy to test with mocked services.
- **Con:** Fat handlers become untestable; push rules into the service or domain.
- **Con:** REST status-per-error differs from GraphQL’s “200 + errors” pattern ([[graphql-yoga]]).

## Comparison
- vs [[express concepts]]: concepts = middleware model; this note = how a single route should look.
- vs GraphQL resolvers: resolvers replace REST handlers
- vs static assets: use `express.static` — not a query handler.


### Use cases
- CRUD REST APIs, admin list endpoints with filters, and BFF routes that aggreg…

- **Example:** `GET /orders?limit=999999` melts the database
