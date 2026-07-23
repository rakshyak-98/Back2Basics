[[redis installation]] [[connection pooling]] [[BASE]]

# redis-cli

> Interactive + scripted Redis admin — inspect memory, latency, persistence, and live traffic under incident load.

## Mental model

```
redis-cli ──► TCP/UNIX ──► Redis single-threaded event loop
                              │
                              ├── command processing (one at a time)
                              ├── memory (maxmemory + eviction)
                              ├── persistence fork (RDB/AOF)
                              └── slow clients block the world
```

**One thread executes commands** — slow `KEYS *`, huge `SMEMBERS`, or Lua loops = latency spike for everyone. Prefer `SCAN`, `MEMORY DOCTOR`, `SLOWLOG`.

## Standard config / commands

### Connect & auth

```bash
redis-cli -h 127.0.0.1 -p 6379
redis-cli -u redis://default:PASSWORD@127.0.0.1:6379/0   # ACL user default
redis-cli --tls --cert ./client.crt --key ./client.key --cacert ./ca.crt

AUTH default yourpassword        # legacy; prefer ACL + -u URL
PING                             # PONG
SELECT 2                         # switch DB (avoid in cluster)
DBSIZE
```

### INFO — first stop on-call

```bash
redis-cli INFO server          # version, uptime, tcp_port
redis-cli INFO memory          # used_memory_human, maxmemory, mem_fragmentation_ratio
redis-cli INFO stats           # instantaneous_ops_per_sec, rejected_connections
redis-cli INFO persistence     # rdb_last_save_time, aof_enabled, aof_last_rewrite_time_sec
redis-cli INFO replication     # role, connected_slaves, master_link_status
redis-cli INFO keyspace          # keys per DB
redis-cli INFO all | less
```

**Memory fields to watch:**

| Field | Meaning |
|-------|---------|
| `used_memory_rss` | OS view — can exceed `used_memory` with fragmentation |
| `mem_fragmentation_ratio` | >1.5 sustained → restart/replica rebuild may help |
| `maxmemory` | 0 = no limit until OOM killer |
| `evicted_keys` | rising = cache too small or TTL missing |

### MEMORY subcommands (4.0+)

```bash
redis-cli MEMORY STATS
redis-cli MEMORY DOCTOR          # human-readable triage hints
redis-cli MEMORY USAGE mykey
redis-cli --bigkeys              # sample heavy keys — run off-peak
redis-cli --memkeys              # 7.0+ memory per key sampling
```

### SLOWLOG

```bash
redis-cli SLOWLOG GET 20
redis-cli SLOWLOG LEN
redis-cli CONFIG GET slowlog-log-slower-than   # microseconds; 10000 = 10ms
redis-cli CONFIG GET slowlog-max-len
```

Configure in `redis.conf`:

```ini
slowlog-log-slower-than 10000    # 10ms
slowlog-max-len 128
```

### Eviction policy

```bash
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET maxmemory-policy
```

| Policy | Behavior |
|--------|----------|
| `noeviction` | Writes fail when full — **queue/cache apps break** |
| `allkeys-lru` | Evict any key LRU — pure cache |
| `volatile-lru` | Evict keys with TTL only |
| `allkeys-lfu` | Frequency — hot key retention (4.0+) |

```ini
maxmemory 2gb
maxmemory-policy allkeys-lfu
```

### Persistence — RDB vs AOF

```bash
redis-cli INFO persistence
redis-cli LASTSAVE                 # unix time of last RDB
redis-cli BGSAVE                   # fork snapshot — watch latency spike
redis-cli CONFIG GET save            # RDB rules: 900 1 300 10 …
redis-cli CONFIG GET appendonly
redis-cli CONFIG GET appendfsync     # always | everysec | no
```

| Mode | Durability | Recovery |
|------|------------|----------|
| RDB snapshots | Point-in-time; lose since last save | Fast restart |
| AOF | Append every write; `everysec` ≈ 1s window | Slower rewrite |
| Both | Common prod | RDB baseline + AOF incremental |

```ini
appendonly yes
appendfsync everysec               # balance; always = slow, no = risky
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

### Latency diagnosis

```bash
redis-cli --latency                 # live sampling
redis-cli --latency-history
redis-cli LATENCY DOCTOR            # 6.2+ structured report
redis-cli LATENCY LATEST
```

Causes: slow commands, AOF rewrite fork, huge key expiry batch, disk IO on persistence, **KEYS *** from monitoring tool.

### Safe iteration (not KEYS *)

```bash
redis-cli SCAN 0 MATCH user:* COUNT 100
redis-cli HGETALL user:1001
redis-cli TTL session:abc
```

### Live monitor (incident only — adds load)

```bash
redis-cli MONITOR    # every command — disable in prod unless brief
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OOM / killed | `INFO memory`; host `dmesg` | Set `maxmemory` + policy; add RAM; delete big keys |
| Timeouts app-side | `LATENCY DOCTOR`; `SLOWLOG` | Remove KEYS; pipeline; split hot key |
| `OOM command not allowed` | `maxmemory-policy noeviction` | Change policy or raise limit |
| Spike every N minutes | `INFO persistence` rewrite/bgsave | Disable save during peak; disk tuning; diskless replica |
| Replica lag | `INFO replication` offset | Slow commands on master; network; `repl-diskless-sync` |
| Connections refused | `INFO stats` rejected | `maxclients`; file descriptors; connection storm |
| Data "vanished" | Eviction + no TTL | TTL on cache keys; monitor `evicted_keys` |
| AOF corrupt on boot | Logs | `redis-check-aof --fix`; restore RDB backup |

## Gotchas

> [!WARNING]
> **`KEYS *` in prod** — blocks event loop. Use `SCAN` or `--bigkeys` sampling.

> [!WARNING]
> **`FLUSHALL` / `FLUSHDB`** — no undo. Alias commands in prod ACL deny list.

- **Single-thread** — more CPU cores ≠ faster one instance; shard or use cluster.
- **Fork latency** — BGSAVE/AOF rewrite on huge RAM → copy-on-write spike; prefer replica for backups.
- **Hot key** — one `INCR` key = single-thread bottleneck; local aggregate or sharded counter.
- **`SELECT` + cluster** — cluster only DB 0; client library may hide this.
- **MONITOR in incident** — can make incident worse; use briefly.

## When NOT to use

- **Primary source of truth without persistence** — enable AOF/RDB or accept loss.
- **Redis as message queue at scale** — use dedicated broker; `BLPOP` patterns hit limits.
- **Large object store** — >512MB values hurt; use object storage.

## Related

[[redis installation]] [[connection pooling]] [[BASE]] [[Data access patterns]]
