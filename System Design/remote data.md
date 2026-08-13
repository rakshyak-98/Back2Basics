[[System Design]] [[Data fetching Frontend]] [[cache system]] [[ETAG or IF MATCH]]

# remote data

> Remote data — state that lives on another machine; every read/write is a network call with failure, lag, and versioning.

---

## How it works

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


## Configuration and commands

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


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Spinner forever | No timeout | Client + gateway timeouts |
| Flicker stale→fresh | Cache policy | SWR; keep previous data |
| Conflict writes | No version | ETag / If-Match |
| Partial page empty | Waterfall fail | Error boundaries per section |
| Wrong tenant data | Cache key | Include tenant in key |

---


## Gotchas

> [!WARNING]
> **Assuming LAN latency in product UX** — design for 200–500ms+.

> [!WARNING]
> **Caching personalized data at CDN** — leak risk; vary on auth.

> [!WARNING]
> **Silent empty arrays** — distinguish “none” vs “failed.”

---


## When not to use

- **Fully local apps** — embedded DB.
- **Secrets in client-visible remote configs** — server-only.
- **Huge binary blobs in JSON APIs** — object storage URLs.

---


## Related

[[Data fetching Frontend]] [[cache system]] [[ETAG or IF MATCH]] [[Real-time Subscription]]

## Sources

- [Wikipedia — remote data](https://en.wikipedia.org/wiki/remote_data)
