[[System design]] [[Authentication web application]] [[REST]] [[backpressure]] [[cache system]] [[Token bucket]] [[database sharding]] [[KISS]]

# API design

> An application programming interface is the contract between clients and your backend: stable resources, predictable errors, and explicit authentication — hide implementation details, not product capability.

```txt
        API design ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers watch for resource modeling, idempotency on retries, pagination …

## Sources
- [RFC 7231](https://www.rfc-editor.org/rfc/rfc7231) — HTTP/1.1 semantics and methods — deep-dive
- [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807) — Problem Details for HTTP APIs — deep-dive
- Leonard Richardson & Mike Amundsen, *RESTful Web APIs* (O'Reilly, 2013) — deep-dive
- Microsoft REST API Guidelines — overview

## Key Concepts
- **Nouns in URLs, verbs in methods:** REST-style contracts clients can infer.
- **Consistent errors:** proper HTTP status + Problem Details; always a request id.
- **Idempotency:** clients retry; `Idempotency-Key` prevents duplicate side effects.
- **Pagination:** offset is simple; cursors scale ([[database sharding]] makes skips worse).

## Technical Details
| HTTP method | Typical intent | Safe? | Idempotent? |
|-------------|----------------|-------|-------------|
| `GET` | Read | Yes | Yes |
| `POST` | Create or non-idempotent action | No | No |
| `PUT` | Replace entire resource | No | Yes |
| `PATCH` | Partial update | No | Often |
| `DELETE` | Remove | No | Yes |

- **Good:** `GET /v1/organizations/{orgId}/projects/{projectId}` **Poor:** `GET…

```json
{
  "data": { "id": "proj_123", "name": "Alpha" },
  "meta": { "request_id": "req_abc", "page": 1, "total": 42 }
}
```

- RFC 7807 error body example: `type`, `title`, `status`, `detail`, `instance`.

| Concern | Practice |
|---------|----------|
| Transport | TLS only; no credentials in query strings |
| Identity | OAuth 2.0, JWT, or scoped API keys |
| Authorization | RBAC/ABAC on resource and tenant |
| Distinction | `401` = not authenticated; `403` = authenticated but not allowed |

- Cursor pagination: `GET /v1/items?limit=50&cursor=...` with `next_cursor` / `…
- Version in path (`/v1`) or content negotiation.
- Rate limits: [[Token bucket]].
- Cache headers for safe `GET`s — see [[cache system]].
- Apply [[backpressure]] at the gateway (max page size, timeouts).

| Smell | Why it hurts |
|-------|--------------|
| Internal DB ids in URLs | Couples clients; enables enumeration |
| Mirror tables in paths | Breaks on normalize/shard |
| Unbounded search | Denial-of-service vector |
| Stack traces in errors | Information disclosure |
| Missing correlation ids | Incidents become guesswork |

## Mistakes to Avoid
- **Mistake:** Returning `200` with `{ "error": true }`
- **Mistake:** Creating resources with bare `POST` and no idempotency key
- **Mistake:** Removing fields from a live version without a deprecation window

## Pros/Cons or Trade-offs
- **REST fine-grained:** simple caches; can be chatty on mobile.
- **Composite/expand reads:** fewer round trips; harder caching and authz.
- **GraphQL:** flexible client shapes; needs schema governance ([[KISS]]

## Comparison
- vs RPC/gRPC: different contract style; same need for idempotency and errors.
- vs [[Authentication web application]]: auth is the identity layer the API boundary enforces.


### Use cases
- Public SaaS APIs, mobile backends, and internal microservice contracts that m…
