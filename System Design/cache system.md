[[Redis]] [[Distributed computing]] [[System design]] [[database sharding]]

# Cache system

> Fast read path in front of slow/expensive source — **TTL, invalidation, and stampede control** define correctness.

---

## Mental model

A **cache** stores **copies** of data closer to readers (memory, edge, CDN) to cut latency and load on origin (DB, API). Caches are **eventually consistent** by definition — the hard part is **when to expire** and **how to invalidate** without thundering herds.

```txt
Read:  App ──► L1 (in-process) ──► L2 (Redis) ──► DB
Write: App ──► DB ──► invalidate/publish ──► cache entries drop
```

| Layer | Typical | TTL | Invalidation |
|-------|---------|-----|--------------|
| **Browser/CDN** | HTTP `Cache-Control` | seconds–days | Purge API |
| **App local** | Caffeine, sync.Map | seconds | Event / TTL |
| **Distributed** | [[Redis]] | minutes | Key delete, pub/sub |
| **Query cache** | ORM / materialized view | tricky | Write-through or bust |

**DNS cache** is a special case — stale resolver data looks like "random" connectivity failures.

---

## Standard config / commands

### Redis cache-aside (read-through pattern)

```python
def get_user(user_id):
    key = f"user:{user_id}"
    cached = redis.get(key)
    if cached:
        return json.loads(cached)
    user = db.query(user_id)
    redis.setex(key, 300, json.dumps(user))  # TTL 5 min
    return user
```

### Invalidation on write

```python
def update_user(user_id, data):
    db.update(user_id, data)
    redis.delete(f"user:{user_id}")
    # Or: redis.publish("invalidate", f"user:{user_id}")
```

### HTTP CDN cache (static + API cautiously)

```http
Cache-Control: public, max-age=3600, stale-while-revalidate=60
ETag: "abc123"
Vary: Accept-Encoding
```

Never `Cache-Control: public` on personalized JSON without `Vary: Authorization` review.

### DNS resolver cache (Linux systemd)

```bash
resolvectl status
resolvectl statistics
resolvectl flush-caches    # after DNS cutover — ops playbook
dig +trace example.com
```

### Stampede protection (singleflight)

```txt
On cache miss: one worker rebuilds; others wait on lock/mutex key
Redis: SET lock:resource NX EX 30 → build → SET data → DEL lock
```

### Cache sizing heuristic

```txt
Working set hot keys × average value size × replica factor < Redis memory
Monitor: hit rate, evicted_keys, latency p99
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Stale data after update | TTL only, no invalidation | Delete key on write; shorter TTL |
| Redis OOM | `INFO memory`; evictions | Raise maxmemory; LRU policy; smaller values |
| Thundering herd on expiry | Spike on DB at T+0 | Jitter TTL; singleflight rebuild |
| "Random" DNS failures | `resolvectl statistics` | Flush cache; fix authoritative NS |
| CDN serves old API | Wrong Cache-Control | private/no-store on auth responses |
| Cache hit rate 0 | Key churn / wrong prefix | Namespace keys; log miss reason |
| Inconsistent replicas | Read from replica lag | Read-your-writes: primary or version check |

---

## Gotchas

> [!WARNING]
> **Cache null results** — cache "user not found" with short TTL or attackers/bugs hammer DB.

> [!WARNING]
> **Serializing huge objects** — 1 MB × 10k QPS = Redis network death; store IDs + field subset.

> [!WARNING]
> **TTL as only invalidation** — users see wrong state for TTL window after edits.

> [!WARNING]
> **Local cache in multi-instance** — instance A invalidates, B still stale — use Redis pub/sub or skip L1.

> [!WARNING]
> **DNS TTL 86400 during migration** — plan lower TTL days before cutover.

---

## When NOT to use

- **Strong consistency required** — read from primary or use linearizable store; no silent cache.
- **Write-heavy counters** — aggregate in DB/Redis INCR, not read-modify-write cache loop.
- **Secrets** — don't cache API keys in CDN edge.

---

## Related

[[Redis]] [[System design]] [[Distributed computing]] [[database sharding]] [[Eventual consistency]] [[DNS]]
