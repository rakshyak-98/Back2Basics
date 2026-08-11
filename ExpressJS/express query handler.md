[[ExpressJS]] [[express concepts]] [[mongosh query]]

# express query handler

> Query handlers — read `req.query` / `req.params` / `req.body`, validate, call services, return status + JSON.

---

## Mental model

**Say it in one breath:** Handlers are adapters: parse input → validate → service → map errors to HTTP. Keep SQL/Mongo out of the handler when possible.

```txt
HTTP → handler → service → DB
         ↘ 400/401/404/500
```

---

## Standard config / commands

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

| Knob | Why it matters |
|------|----------------|
| Validation | Zod/Joi before service |
| Status codes | Clients branch correctly |
| Pagination query | `limit`/`cursor` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Query always strings | `req.query` types | Coerce/validate |
| Empty body | Parser missing | `express.json()` |
| Unhandled async | No try/next | Wrap async |
| 200 with error payload | Wrong status | Set codes |

---

## Gotchas

> [!WARNING]
> **Prototype pollution via query** — don’t merge blindly into objects.

> [!WARNING]
> **Array query params** — `?tag=a&tag=b` shapes vary.

---

## When NOT to use

- **GraphQL-only APIs** — different resolver model.
- **Raw static files** — `express.static`.

---

## Related

[[express concepts]] [[Express middleware]] [[Service Layer]]
