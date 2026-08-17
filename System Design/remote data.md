[[System Design]] [[Data fetching Frontend]] [[cache system]] [[ETAG or IF MATCH]]

# remote data

> Remote data — state that lives on another machine; every read/write is a network call with failure, lag, and versioning.





## Interview Relevance
Every remote read is a distributed call: timeouts, caching, partial failure.

## Sources
- [Wikipedia — remote data](https://en.wikipedia.org/wiki/remote_data) — overview

## Key Concepts
- **State on another machine:** every access is a distributed call.
- **Partial failure:** timeouts, retries, stale caches.
- **Locality:** cache or colocate hot reads ([[cache system]]).
- **Contracts:** schemas and SLOs for the remote source.

## Technical Details
### How it works

```txt
UI local cache  ←get/put→  API  ←→  DB
     (stale ok?)     (timeouts)   (source of truth)
```

| Concern | Tactic |
|---------|--------|
| Latency | Cache, CDN, parallel fetch |
| Failure | Retry/backoff; degrade UX |
| Freshness | TTL, ETag, subscriptions |
| Auth | Tokens per request |

---


### Configuration and commands

```http
GET /items/1
If-None-Match: "v3"
→ 304 Not Modified
```

```ts
type Remote<T> =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: T; fetchedAt: number }
```

---

## Real-World Applications
Mobile/web clients, microservices fetching dependencies, and multi-region reads.

## Pros/Cons or Trade-offs
- **Fully local apps** — embedded DB.
- **Secrets in client-visible remote configs** — server-only.
- **Huge binary blobs in JSON APIs** — object storage URLs.

---


- **Pro:** Specialization and independent scale of data owners.
- **Con:** Latency and consistency complexity.
- **Trade-off:** chatty remote reads vs BFF aggregation.

## Comparison
- vs local memory: no shared heap; need protocols.
- vs [[Data fetching Frontend]]: UI-specific fetch/cache patterns for remote APIs.

## Mistakes to Avoid
> [!WARNING]
> **Assuming LAN latency in product UX** — design for 200–500ms+.

> [!WARNING]
> **Caching personalized data at CDN** — leak risk; vary on auth.

> [!WARNING]
> **Silent empty arrays** — distinguish “none” vs “failed.”

---

| Symptom | Check | Fix |
|---------|-------|-----|
| Spinner forever | No timeout | Client + gateway timeouts |
| Flicker stale→fresh | Cache policy | SWR; keep previous data |
| Conflict writes | No version | ETag / If-Match |
| Partial page empty | Waterfall fail | Error boundaries per section |
| Wrong tenant data | Cache key | Include tenant in key |

---
