[[System design]] [[Authentication web application]] [[JWT authentication]] [[REST]]

# API design

> Contract between clients and backend — **resource-oriented URLs, predictable errors, auth**; hide implementation, not capability.

---

## Mental model

Good **API design** optimizes for **who** can call **what**, **how**, and **what they get back** — not for mirroring database tables. URLs express a **resource hierarchy**; HTTP methods express **intent**; status codes express **outcome**. Versioning and pagination are part of the contract from day one, not retrofits.

```txt
Client intent ──► HTTP method + resource path + auth context
                         │
                   Handler / domain logic
                         │
              Consistent response envelope + errors
```

| Principle | Good | Bad |
|-----------|------|-----|
| **Nouns in paths** | `GET /users/{id}` | `GET /getUserById` |
| **Hierarchy** | `/orgs/{id}/projects/{id}` | Flat opaque IDs only |
| **Idempotency** | `PUT` / `DELETE` idempotent | `POST` for everything |
| **Errors** | `{ "code", "message", "request_id" }` | Stack traces to client |

**Everyday user perspective:** hide shard keys, internal IDs, and retry semantics — expose stable product concepts ([[KISS]]).

---

## Standard config / commands

### URL hierarchy (example)

```txt
GET    /v1/domains/{domainId}/courses/{courseId}/lessons
POST   /v1/domains/{domainId}/courses
PATCH  /v1/domains/{domainId}/courses/{courseId}
DELETE /v1/domains/{domainId}/courses/{courseId}
```

Descending specificity: **domain → type → entity → action sub-resource**.

### HTTP method semantics

```txt
GET     Read (safe, cacheable)
POST    Create / non-idempotent action
PUT     Replace entire resource (idempotent)
PATCH   Partial update
DELETE  Remove (idempotent)
```

### Standard response envelope

```json
{
  "data": { "id": "crs_123", "title": "Intro" },
  "meta": { "request_id": "req_abc", "page": 1, "total": 42 }
}
```

### Error shape (RFC 7807 style)

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Course not found",
  "status": 404,
  "detail": "No course with id crs_999",
  "request_id": "req_abc"
}
```

### Auth checklist

```txt
Who: OAuth2 / JWT ([[JWT authentication]]) / API key per integration
What: RBAC or ABAC on resource + tenant
How: HTTPS only; scoped tokens (read vs write)
Need: Rate limits + idempotency-key header on POST payments
Return: 401 unauthenticated vs 403 forbidden — distinct
```

### Pagination (cursor preferred at scale)

```txt
GET /v1/items?limit=50&cursor=eyJpZCI6MTIzfQ
Response meta: { "next_cursor": "...", "has_more": true }
```

Offset pagination OK for admin UIs; degrades on large tables ([[database sharding]]).

### Versioning

```txt
/v1/... in path (explicit, cache-friendly)
Or Accept: application/vnd.example.v1+json
Never break v1 silently — add v2, deprecate with sunset header
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 429 storms | Client retry without backoff | Exponential backoff + jitter; raise limits if legit |
| Duplicate orders | POST retried | `Idempotency-Key` header + store |
| 404 vs empty list | Wrong path vs filter | `GET /items` → `[]` not 404 |
| N+1 from mobile | Chatty fine-grained API | Aggregate DTO endpoint |
| Breaking mobile old app | Field removed from v1 | Additive changes only; version bump |
| CORS errors browser | Preflight | Allow origin + methods; not API "bug" |
| Slow list endpoints | Missing index on sort column | DB index; cursor pagination |

---

## Gotchas

> [!WARNING]
> **Leaking internal IDs** — exposure enables enumeration; use opaque public IDs.

> [!WARNING]
> **200 with `{ "error": true }`** — breaks caches and clients; use proper status codes.

> [!WARNING]
> **Unbounded `GET /search?q=*`** — DOS vector; max limit, auth, timeout.

> [!WARNING]
> **Mirror DB in URL** — `/table_name_row_id` couples API to schema migrations.

> [!WARNING]
> **No request_id** — impossible to correlate logs across services.

---

## When NOT to use

- **gRPC internal east-west** — HTTP JSON for public/partner; gRPC for service mesh if already standard.
- **GraphQL for 3-field mobile screen** — complexity tax unless many client shapes.
- **Hypermedia HATEOAS everywhere** — rarely pays off for mobile/SPA teams.

---

## Related

[[System design]] [[Authentication web application]] [[JWT authentication]] [[KISS]] [[DRY]] [[backpressure]] [[cache system]]
