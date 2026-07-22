[[Buffer cache]] [[fsync]] [[Persistent Block Storage]] [[Linux]]

# Disk IOPS

> Input/output operations per second — counts discrete read/write ops, not bytes; the limit that crushes random-workload databases before bandwidth caps.

---

## Mental model

**IOPS** = completed I/O operations per second (reads + writes, often reported separately). Distinct from **throughput** (MB/s):

```txt
Large sequential read  →  few ops, high MB/s
Random 4 KiB read      →  many ops, IOPS-bound (latency × queue depth)
```

Rough ceiling (order of magnitude):
| Media | Random 4K IOPS (single device) |
|-------|-------------------------------|
| HDD | 100–200 |
| SATA SSD | 10k–90k |
| NVMe | 100k–1M+ |
| EBS gp3 | provisioned IOPS (3k–16k+ per volume) |

Queue depth (`nr_requests`, app concurrency) multiplies effective IOPS until device or CPU saturates.

**Service impact:** Postgres/MySQL with fsync-heavy commits, etcd, and metrics backends hit **IOPS and latency** before raw bandwidth.

---

## Standard config / commands

### Host-level IOPS and latency

```bash
iostat -dx 1
# r/s w/s await util — util near 100% → saturated

# Per-process I/O
pidstat -d 1 -p PID
```

### Cloud dashboards

| Provider | Metrics |
|----------|---------|
| AWS RDS/EBS | `ReadIOPS`, `WriteIOPS`, `VolumeQueueLength` |
| Azure | Disk IOPS consumed % |
| GCP | `disk/read_ops_count`, `write_ops_count` |

### DB-specific

```bash
pidof postgres mysqld
pidstat -d 1 -p $(pidof postgres)
```

**Why `await` matters:** high IOPS with rising `await` means queueing — users see tail latency, not average throughput.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| DB slow commits | `iostat await`; fsync rate | Faster disk; group commit; reduce fsync frequency (risk tradeoff) |
| EBS throttling | Cloud `VolumeQueueLength`, burst balance | Provision IOPS; gp3 IOPS/throughput knobs |
| High IOPS, low useful work | Small random reads | [[Buffer cache]] hit ratio; index tuning; larger page cache |
| SSD wear / latency creep | SMART, `nvme smart-log` | Replace drive; spread writes |

---

## Gotchas

> [!WARNING]
> **Benchmark IOPS ≠ sustained prod IOPS** — burst buckets on cloud volumes lie in short tests.

> [!WARNING]
> **Splitting one workload across many small volumes** doesn't bypass per-instance limits on shared hardware.

> [!WARNING]
> **IOPS without block size** is ambiguous — always note IO size (4K vs 128K).

---

## When NOT to use

Don't size purely on IOPS if workload is **sequential streaming** (video, bulk ETL) — size on **throughput** (MB/s) instead.

---

## Related

[[Buffer cache]] [[fsync]] [[Persistent Block Storage]] [[system bus]] [[Linux]]
