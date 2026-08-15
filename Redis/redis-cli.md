[[redis installation]] [[connection pooling]] [[BASE]] [[Data access patterns]]

# redis-cli

> `redis-cli` is the interactive and scripted admin client — inspect memory, latency, persistence, and live traffic when Redis misbehaves under load.

## Interview Relevance

Interviewers watch whether you reach for `INFO`/`SLOWLOG`/`SCAN` instead of `KEYS *`, and whether you understand single-threaded command execution.

## Sources

- [Redis — redis-cli](https://redis.io/docs/latest/operate/oss_and_stack/management/cli/) — deep-dive
- [Redis — Memory optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/) — overview
- [Redis — Latency monitoring](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency-monitor/) — overview

## Key Concepts

- **One thread executes commands:** slow `KEYS *`, huge `SMEMBERS`, or Lua loops spike latency for everyone.
- **INFO first:** memory, persistence, replication, stats — on-call starting point.
- **Eviction vs OOM:** `maxmemory-policy` decides whether writes fail or keys disappear.
- **RDB vs AOF:** snapshots versus append log — durability windows differ.

## Technical Details

```
redis-cli ──► TCP/UNIX ──► Redis single-threaded event loop
                              │
                              ├── command processing (one at a time)
                              ├── memory (maxmemory + eviction)
                              ├── persistence fork (RDB/AOF)
                              └── slow clients block the world
```

### Connect & auth

```bash
redis-cli -h 127.0.0.1 -p 6379
redis-cli -u redis://default:PASSWORD@127.0.0.1:6379/0
redis-cli --tls --cert ./client.crt --key ./client.key --cacert ./ca.crt
PING
SELECT 2                         # avoid in cluster
DBSIZE
```

### INFO — first stop on-call

```bash
redis-cli INFO server
redis-cli INFO memory
redis-cli INFO stats
redis-cli INFO persistence
redis-cli INFO replication
redis-cli INFO keyspace
```

| Field | Meaning |
|-------|---------|
| `used_memory_rss` | OS view — can exceed `used_memory` with fragmentation |
| `mem_fragmentation_ratio` | >1.5 sustained → restart/replica rebuild may help |
| `maxmemory` | 0 = no limit until OOM killer |
| `evicted_keys` | rising = cache too small or TTL missing |

### MEMORY / SLOWLOG / latency

```bash
redis-cli MEMORY STATS
redis-cli MEMORY DOCTOR
redis-cli MEMORY USAGE mykey
redis-cli --bigkeys
redis-cli SLOWLOG GET 20
redis-cli --latency
redis-cli LATENCY DOCTOR
```

```ini
slowlog-log-slower-than 10000    # 10ms
slowlog-max-len 128
```

### Eviction policy

| Policy | Behavior |
|--------|----------|
| `noeviction` | Writes fail when full — queue/cache apps break |
| `allkeys-lru` | Evict any key LRU — pure cache |
| `volatile-lru` | Evict keys with TTL only |
| `allkeys-lfu` | Frequency — hot key retention (4.0+) |

### Persistence

```bash
redis-cli LASTSAVE
redis-cli BGSAVE
redis-cli CONFIG GET appendonly
redis-cli CONFIG GET appendfsync
```

| Mode | Durability | Recovery |
|------|------------|----------|
| RDB snapshots | Point-in-time; lose since last save | Fast restart |
| AOF | Append every write; `everysec` ≈ 1s window | Slower rewrite |
| Both | Common production | RDB baseline + AOF incremental |

### Safe iteration

```bash
redis-cli SCAN 0 MATCH user:* COUNT 100
redis-cli HGETALL user:1001
redis-cli TTL session:abc
# redis-cli MONITOR   # incident only — adds load
```

| Symptom | Check | Fix |
|---------|-------|-----|
| OOM / killed | `INFO memory`; host `dmesg` | Set `maxmemory` + policy; add RAM; delete big keys |
| Timeouts app-side | `LATENCY DOCTOR`; `SLOWLOG` | Remove KEYS; pipeline; split hot key |
| `OOM command not allowed` | `maxmemory-policy noeviction` | Change policy or raise limit |
| Spike every N minutes | `INFO persistence` rewrite/bgsave | Disable save during peak; disk tuning |
| Replica lag | `INFO replication` offset | Slow commands on master; network |
| Connections refused | `INFO stats` rejected | `maxclients`; file descriptors |
| Data "vanished" | Eviction + no TTL | TTL on cache keys; monitor `evicted_keys` |
| AOF corrupt on boot | Logs | `redis-check-aof --fix`; restore RDB backup |

## Real-World Applications

Incident triage when API latency climbs, capacity checks before a sale, and validating persistence after a crash.

**Example:** `SLOWLOG GET` shows monitoring still runs `KEYS *`; replace with `SCAN` and latency returns to baseline.

## Pros/Cons or Trade-offs

- **Pro:** Full visibility into a single Redis process without extra agents.
- **Con:** `MONITOR` and `KEYS` can worsen the incident.
- **Con:** More CPU cores do not speed one instance — shard or use cluster.

## Comparison

- vs application metrics alone: `redis-cli` shows server-side eviction, forks, and slow commands metrics miss.
- vs dedicated brokers: Redis lists/`BLPOP` are not a full message queue at scale.
- vs object storage: values >512MB hurt — wrong store.

## Mistakes to Avoid

- `KEYS *` in production — blocks the event loop.
- `FLUSHALL` / `FLUSHDB` without ACL denial — no undo.
- Taking BGSAVE on a huge primary during peak — prefer replica backups.
- Using `SELECT` with cluster (DB 0 only).
- Treating Redis as durable source of truth without AOF/RDB consciously enabled.
