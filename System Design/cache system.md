[[Redis]] [[System design]] [[Distributed computing]] [[database sharding]] [[Eventual consistency]] [[DNS]]

# Cache system

> A cache stores copies of data closer to readers — process memory, distributed memory, content delivery network edge — to reduce latency and protect the origin database or application programming interface from repeated work.

---

## Read path and write path

```txt
Read:  Application → L1 (in-process) → L2 (Redis) → Database
Write: Application → Database → invalidate or publish → cache entries expire
```

Caches are **eventually consistent** by definition. The design question is how stale data is allowed to be and how invalidation happens without melting the origin under load.

| Layer | Examples | Typical time-to-live | Invalidation |
|-------|----------|----------------------|--------------|
| Browser / content delivery network | `Cache-Control`, `ETag` | Seconds to days | Purge application programming interface |
| In-process | Caffeine, `sync.Map` | Seconds | Event bus or short time-to-live |
| Distributed | [[Redis]] | Minutes | Key delete, pub/sub channel |
| Query / object cache | Object-relational mapper second-level cache | Risky | Write-through or explicit bust |

**DNS resolver cache** is a special case — stale name records look like random connectivity failures after a cutover.

## Cache-aside (lazy loading)

The application checks the cache first; on miss, loads from origin and populates:

```python
def get_user(user_id):
    key = f"user:{user_id}"
    cached = redis.get(key)
    if cached:
        return json.loads(cached)
    user = db.query(user_id)
    redis.setex(key, 300, json.dumps(user))
    return user
```

On update, **delete** the key (or publish an invalidation message) — relying on time-to-live alone means users see wrong state until expiry.

## Stampede protection

When a hot key expires, every request may miss simultaneously and hammer the database (**cache stampede**):

```txt
On miss: one worker acquires lock → rebuilds → others wait or serve stale
Redis: SET lock:resource NX EX 30 → build → SET data → DEL lock
```

Add **jitter** to time-to-live values so keys do not all expire at the same second.

## HTTP caching cautions

```http
Cache-Control: public, max-age=3600, stale-while-revalidate=60
ETag: "abc123"
Vary: Accept-Encoding
```

Never mark authenticated JSON as `public` without reviewing `Vary: Authorization`. Personalized responses belong behind `private` or `no-store`.

## Sizing and monitoring

```txt
Working set (hot keys) × average value size × replica factor < memory budget
Watch: hit rate, evicted_keys, latency p99, memory fragmentation
```

Oversized values (megabyte blobs at high queries per second) saturate network before central processing unit.

## Common mistakes

| Mistake | Consequence |
|---------|-------------|
| Cache as source of truth | Data loss on eviction; no durability guarantee |
| No invalidation on write | Stale reads until time-to-live |
| Cache null forever | Attackers or bugs amplify database load — use short time-to-live for misses |
| Local cache in multi-instance fleet | Instance A invalidates; instance B still stale — use pub/sub or skip L1 |
| Long DNS time-to-live before migration | Clients hit old addresses for days |

*What breaks first when the origin slows?* An unprotected cache miss path — design singleflight and circuit breakers ([[backpressure]]).

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), chapter on caching.
- [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) — HTTP Caching.
- Redis documentation — eviction policies (`allkeys-lru`, `volatile-lru`), memory limits.
