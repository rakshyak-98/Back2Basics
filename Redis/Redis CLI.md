[[Redis CLI]] [[INDEX]]

# Redis CLI

> redis-cli — connect, INFO, memory, slowlog, and keyspace scans.

---

## redis-cli

### Connect & auth

From [[Redis CLI]].

```bash
redis-cli -h 127.0.0.1 -p 6379
redis-cli -u redis://default:PASSWORD@127.0.0.1:6379/0
redis-cli --tls --cert ./client.crt --key ./client.key --cacert ./ca.crt
PING
SELECT 2                         # avoid in cluster
DBSIZE
```

### INFO — first stop on-call

From [[Redis CLI]].

```bash
redis-cli INFO server
redis-cli INFO memory
redis-cli INFO stats
redis-cli INFO persistence
redis-cli INFO replication
redis-cli INFO keyspace
```

### MEMORY / SLOWLOG / latency

From [[Redis CLI]].

```bash
redis-cli MEMORY STATS
redis-cli MEMORY DOCTOR
redis-cli MEMORY USAGE mykey
redis-cli --bigkeys
redis-cli SLOWLOG GET 20
redis-cli --latency
redis-cli LATENCY DOCTOR
```

### Persistence

From [[Redis CLI]].

```bash
redis-cli LASTSAVE
redis-cli BGSAVE
redis-cli CONFIG GET appendonly
redis-cli CONFIG GET appendfsync
```
