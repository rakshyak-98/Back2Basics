[[GridFS]] [[Database]] [[WAL (Write-Ahead Log)]] [[MMAP]] [[memory engine]]

# WiredTiger storage engine

> MongoDB's default storage engine since 4.2 — B-tree docs, MVCC, checkpointed durability, cache-bound performance — MongoDB manual + **Designing Data-Intensive Applications** (Kleppmann, log-structured ideas).

## Mental model

WiredTiger (WT) sits between MongoDB's query layer and disk:

```
mongod ──► WiredTiger API ──► cache (RAM) ──► on-disk tables + journal
                │                    │
                │                    └── dirty pages evicted async
                └── snapshots / txns (MVCC)
```

- **Documents** stored in B-trees (collections + indexes); no in-place overwrite for updates — new versions, old reclaimed by **eviction/compaction**.
- **Checkpoints** — consistent on-disk snapshot every `storage.wiredTiger.engineConfig.checkpoint=(wait, seconds)`; crash recovery = last checkpoint + journal replay ([[WAL (Write-Ahead Log)]] family).
- **Journal** — 100ms commit interval default (`journal.commitIntervalMs`); group commit like Postgres.
- **Cache** — single big WT cache (`cacheSizeGB`); **not** the filesystem page cache alone — working set must fit or I/O explodes.

```
Write path:  update in cache → journal record → ack (per write concern)
             checkpoint flushes dirty pages → .wt data files
Read path:   cache hit → fast | miss → disk + populate cache
```

## Standard config / commands

### mongod.conf essentials

```yaml
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
    commitIntervalMs: 100        # lower = safer, more IOPS; 100 default OK
  wiredTiger:
    engineConfig:
      cacheSizeGB: 4               # ~50% RAM on dedicated host; leave OS headroom
      journalCompressor: snappy    # or zstd (4.2+) for space
      directoryForIndexes: false   # true = separate volume for indexes
    collectionConfig:
      blockCompressor: snappy      # zstd for cold/archival if CPU cheap
    indexConfig:
      prefixCompression: true

operationProfiling:
  slowOpThresholdMs: 100
```

### Runtime inspection

```javascript
// Cache pressure — the #1 prod knob
db.serverStatus().wiredTiger.cache
// bytes currently in cache, tracked dirty bytes, pages evicted

// Checkpoint age
db.serverStatus().wiredTiger.transaction
// last checkpoint timestamp / time since

// Collection compression stats
db.serverStatus().wiredTiger.compression

// Slow ops
db.currentOp({ "microsecs_running": { $gte: 100000 }, "op": "query" })
```

```bash
# CLI
mongosh --eval 'db.serverStatus().wiredTiger.cache'
mongostat --rowcount 5   # flushes, faults, queue readers/writers
```

### Write concern vs durability

```javascript
// default { w: 1 } — journal sync per commitIntervalMs window
db.orders.insertOne(doc, { writeConcern: { w: "majority", j: true } })
// j:true — wait for journal fsync (single-node strong)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| High latency, disk idle | `serverStatus.wiredTiger.cache` — `pages evicted` spiking | Raise `cacheSizeGB`; reduce working set; add RAM |
| Disk 100%, cache OK | Checkpoint or compaction IO | Faster SSD; `checkpoint=(wait,60)` not 0; stagger jobs |
| Writes stall bursts | Journal on slow volume | Move journal/dbPath to NVMe; tune `commitIntervalMs` only if acceptable risk |
| RSS >> cacheSizeGB | Memory engine leak suspicion vs OS cache | Verify `cacheSizeGB`; check tcmalloc; restart after config fix |
| Replication lag | Oplog + primary cache pressure | Index the replica's hot paths; increase oplog; throttle writes |
| Data file huge, docs few | Update-heavy bloat | `compact` (maint window); resync; consider `collectionCompact` |
| After unclean shutdown | Recovery logs on startup | Let recover finish; restore if WT corruption after double fault |

## Gotchas

> [!WARNING]
> **`cacheSizeGB` too large on shared box** — WT steals from app/OS; OOM killer takes mongod. **Too small** — constant eviction, read latency cliffs.

> [!WARNING]
> **MMAPv1 nostalgia** — pre-4.2 engines differ; migration changed compression + lock granularity. Don't paste old tuning guides.

- **Checkpoint blocks** — `checkpoint=(wait,0)` disables throttling — I/O storms during peak.
- **Snappy vs zstd** — zstd saves disk, costs CPU; wrong on CPU-bound small instances.
- **Large documents + index** — docs >16MB rejected; padding fields bloat even with compression.
- **TTL / capped** — still WT btree maintenance; monitor delete rate vs eviction.
- **`repairDatabase`** — last resort; takes lock; restore from backup preferred.

## When NOT to use

- **WiredTiger is not optional** on supported MongoDB — engine choice is architectural for self-hosted legacy only.
- **Don't tune compression before cache** — eviction fixes beat compressor swaps.
- **In-memory analytics** — export to warehouse; `$lookup` across huge sharded collections isn't OLAP.

## Related

[[GridFS]] [[WAL (Write-Ahead Log)]] [[MMAP]] [[memory engine]] [[Database]] [[Data access patterns]]
