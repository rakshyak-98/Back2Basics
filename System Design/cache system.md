[[Redis]] [[System design]] [[Distributed computing]] [[database sharding]] [[Eventual consistency]] [[DNS]] [[backpressure]]

# Cache system

> A cache stores copies of data closer to readers — process memory, Redis, CDN edge — to cut latency and shield the origin from repeated work.

```txt
        Cache system ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Cache-aside + invalidation, stampede protection, HTTP cache safety for person…

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* — caching — deep-dive
- [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) — HTTP Caching — deep-dive
- Redis docs — eviction policies — deep-dive

## Key Concepts
- **Layers:** browser/CDN, in-process, distributed ([[Redis]]), query/object caches.
- **Eventually consistent:** by nature ([[Eventual consistency]]).
- **Cache-aside:** miss → origin → populate; write → delete/invalidate.
- **Stampede:** singleflight/lock + TTL jitter.

## Technical Details
```txt
Read:  App → L1 → L2 (Redis) → Database
Write: App → Database → invalidate → entries expire
```

| Layer | Examples | Typical TTL | Invalidation |
|-------|----------|-------------|--------------|
| Browser/CDN | Cache-Control, ETag | s–days | Purge API |
| In-process | Caffeine, sync.Map | seconds | Bus or short TTL |
| Distributed | Redis | minutes | Delete / pubsub |
| ORM 2nd-level | Risky | — | Write-through/bust |

```python
def get_user(user_id):
    key = f"user:{user_id}"
    cached = redis.get(key)
    if cached: return json.loads(cached)
    user = db.query(user_id)
    redis.setex(key, 300, json.dumps(user))
    return user
```

- Stampede: `SET lock NX EX` → rebuild → set data → del lock.
- HTTP: never `public` authenticated JSON without reviewing `Vary`.
- DNS cache TTLs bite during cutovers.

- Watch hit rate, evictions, p99, fragmentation.
- Oversized values saturate network first.

| Mistake | Consequence |
|---------|-------------|
| Cache as source of truth | Loss on eviction |
| No invalidation | Stale until TTL |
| Cache null forever | Amplifies load — short negative TTL |
| Local-only L1 multi-instance | Skew across pods |
| Long DNS TTL pre-migration | Clients hit old IPs |

## Mistakes to Avoid
- **Mistake:** TTL-only invalidation for user-visible correctness
- **Mistake:** Marking private responses `public`
- **Mistake:** No circuit breaker on miss path when origin is sick

## Pros/Cons or Trade-offs
- **Pro:** Latency and origin protection.
- **Con:** Consistency bugs; stampede; memory cost.
- **Trade-off:** short TTL (fresher) vs hit rate.

## Comparison
- vs DB replicas: replicas are durable copies; caches are disposable accelerators.
- vs [[backpressure]]: cache misses under origin slowdown need shedding/singleflight.


### Use cases
- API response caching, session stores, CDN static assets, and protecting shard…
