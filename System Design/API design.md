[[System design]] [[Authentication web application]] [[REST]] [[backpressure]] [[cache system]]

# API design

> An application programming interface is the contract between clients and your backend: stable resources, predictable errors, and explicit authentication — hide implementation details, not product capability.

---

## Resources, methods, and intent

Representational State Transfer (REST) style application programming interfaces express **nouns in URLs** and **verbs in HTTP methods**. Clients should infer behavior from the contract, not from tribal knowledge.

| HTTP method | Typical intent | Safe? | Idempotent? |
|-------------|----------------|-------|-------------|
| `GET` | Read | Yes | Yes |
| `POST` | Create or non-idempotent action | No | No |
| `PUT` | Replace entire resource | No | Yes |
| `PATCH` | Partial update | No | Often |
| `DELETE` | Remove | No | Yes |

**Good:** `GET /v1/organizations/{orgId}/projects/{projectId}`  
**Poor:** `GET /getProjectById?id=7` — action verbs in paths age poorly and confuse caches.

Descending specificity helps clients and operators: domain → collection → entity → sub-resource (for example `/invoices/{id}/line-items`).

## Response shape and errors

Use a consistent envelope so clients can parse successes and failures uniformly:

```json
{
  "data": { "id": "proj_123", "name": "Alpha" },
  "meta": { "request_id": "req_abc", "page": 1, "total": 42 }
}
```

Errors should use proper HTTP status codes, not `200` with `{ "error": true }`. [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807) (*Problem Details for HTTP APIs*) defines a standard error body:

```json
{
  "type": "https://api.example.com/errors/not-found",
  "title": "Project not found",
  "status": 404,
  "detail": "No project with id proj_999",
  "instance": "/v1/projects/proj_999"
}
```

Always return a **request identifier** in headers or body so support can correlate logs across services.

## Authentication and authorization

See [[Authentication web application]] for patterns. At the application programming interface boundary:

| Concern | Practice |
|---------|----------|
| Transport | Transport Layer Security only; no credentials in query strings |
| Identity | OAuth 2.0, JSON Web Tokens, or scoped API keys per integration |
| Authorization | Role-based or attribute-based checks on the resource and tenant |
| Distinction | `401 Unauthorized` = not authenticated; `403 Forbidden` = authenticated but not allowed |

Rate limiting and [[Token bucket]] policies belong in the contract documentation, not as surprises in production.

## Pagination and versioning

**Offset pagination** (`?page=3&limit=50`) is simple for administrator interfaces but degrades on large tables — the database must skip many rows ([[database sharding]] makes this worse).

**Cursor pagination** scales better:

```http
GET /v1/items?limit=50&cursor=eyJpZCI6MTIzfQ
```

Response metadata: `{ "next_cursor": "...", "has_more": true }`.

Version in the path (`/v1/...`) or via content negotiation (`Accept: application/vnd.example.v1+json`). Never remove fields from a supported version without a deprecation window and sunset headers.

## Idempotency and retries

Clients **will** retry on timeouts. For `POST` operations that create side effects (payments, orders), accept an `Idempotency-Key` header and store the first successful response keyed by that value.

Without idempotency, a retry after a slow success creates duplicates — one of the most expensive application programming interface bugs to unwind.

## Performance and aggregation

Mobile and single-page applications suffer from chatty fine-grained endpoints. When a screen needs ten entities, offer a **composite read** or expand parameters (`?include=owner,permissions`) rather than forcing ten round trips.

Apply [[backpressure]] at the gateway: maximum page size, query timeouts, and rejection under overload instead of unbounded work per request.

## Caching semantics

`GET` responses may be cacheable when they are safe and when cache headers are explicit:

```http
Cache-Control: private, max-age=60
ETag: "a1b2c3"
```

Never mark personalized JSON as `public` without reviewing `Vary` headers. See [[cache system]] for invalidation strategy — the application programming interface layer should document what is safe to cache at the edge.

## Design smells

| Smell | Why it hurts |
|-------|--------------|
| Internal database identifiers in URLs | Couples clients to schema; enables enumeration |
| Mirror tables in paths (`/users_table`) | Breaks when you normalize or shard |
| Unbounded search (`GET /search?q=*`) | Denial-of-service vector |
| Stack traces in error bodies | Information disclosure |
| Missing correlation identifiers | Incidents become guesswork |

*When would you choose GraphQL over REST?* When many client shapes need different field sets and you can invest in schema governance — not for a three-field mobile screen ([[KISS]]).

## Sources

- [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231) — HTTP/1.1 semantics and methods.
- [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807) — Problem Details for HTTP APIs.
- Leonard Richardson & Mike Amundsen, *RESTful Web APIs* (O'Reilly, 2013).
- Microsoft REST API Guidelines — naming, versioning, long-running operations.
