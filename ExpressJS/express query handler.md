[[express concepts]] [[Express middleware]] [[express error handler]] [[Service Layer]] [[graphql-yoga]]

# express query handler

> Route handlers are adapters: read `req.query`, `req.params`, and `req.body`, validate, call a service, and map outcomes to HTTP status and JSON.





## Interview Relevance
Interviewers look for thin controllers, input validation, correct status codes, and safe handling of stringly-typed query parameters — not business logic stuffed in the route.

## Sources
- [Express — Request](https://expressjs.com/en/4x/api.html#req) — deep-dive
- [Express — Response](https://expressjs.com/en/4x/api.html#res) — overview
- [OWASP — Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) — overview

## Core Definition
A query (or route) handler translates HTTP into application calls. Validation and coercion happen before the [[Service Layer]]; failures become 4xx responses or `next(err)` for [[express error handler]].

## Key Concepts
- **Adapter role:** HTTP in, domain call out — keep database logic out of the handler when possible.
- **`req.query` / `req.params`:** always strings (or arrays of strings) until you coerce and validate.
- **Status discipline:** 4xx for client mistakes, 5xx for server failures — clients branch on status, not only message text.
- **Pagination:** `limit`, `cursor`, or `page` live in query strings — validate bounds.
- **Pollution risk:** do not blindly merge query objects into models (prototype pollution / unexpected arrays).

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

Array query params (`?tag=a&tag=b`) become arrays or last-wins depending on parser settings — see also [[Express HPP]].

## Real-World Applications
CRUD REST APIs, admin list endpoints with filters, and BFF routes that aggregate services.

**Example:** `GET /orders?limit=999999` melts the database — validate `limit` to a max (for example 100) in the handler before calling the service.

## Pros/Cons or Trade-offs
- **Pro:** Clear HTTP boundary — easy to test with mocked services.
- **Con:** Fat handlers become untestable; push rules into the service or domain.
- **Con:** REST status-per-error differs from GraphQL’s “200 + errors” pattern ([[graphql-yoga]]).

## Comparison
- vs [[express concepts]]: concepts = middleware model; this note = how a single route should look.
- vs GraphQL resolvers: resolvers replace REST handlers; context and DataLoader matter more than status codes.
- vs static assets: use `express.static` — not a query handler.

## Mistakes to Avoid
- Putting SQL or ORM calls directly in every route without a service boundary.
- Trusting `req.query` types without coercion.
- Returning 200 with `{ error: ... }` so clients cannot branch on HTTP status.
- Merging query objects into Mongoose/update payloads without allowlists.
