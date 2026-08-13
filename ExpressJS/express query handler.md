[[ExpressJS]] [[express concepts]] [[mongosh query]] [[Express middleware]]

# express query handler

> Route handlers are adapters: read `req.query`, `req.params`, and `req.body`, validate input, call a service layer, and map outcomes to HTTP status codes and JSON — keep database logic out of the handler when possible.

---

## Handler as adapter

```txt
HTTP request → handler → service → database
                  ↘ 400 / 401 / 404 / 500
```

The handler's job is translation, not business logic. Validation (Zod, Joi) runs before the service call. Errors flow to [[express error handler]] via `next(err)`.

---

## Example

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
| Validation | Schema-check before service call |
| Status codes | Clients branch on 4xx vs 5xx |
| Pagination | `limit`, `cursor`, or `page` in `req.query` |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Query values always strings | `req.query` is untyped | Coerce and validate |
| Empty body | Parser missing | `express.json()` before routes |
| Unhandled async error | No `try/next` | Wrap async handlers |
| 200 with error payload | Wrong status code | Set explicit `res.status()` |

**Prototype pollution:** do not merge `req.query` blindly into objects. **Array query params** (`?tag=a&tag=b`) vary in shape depending on parser settings.

---

## When handlers are not the right layer

- **GraphQL APIs** — resolvers replace this pattern; see [[graphql-yoga]].
- **Static assets** — use `express.static` instead.

---

## Related

[[express concepts]] · [[Express middleware]] · [[Service Layer]]
