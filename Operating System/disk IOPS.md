[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[CPU IO Bound Task]] [[fsync]]

# disk IOPS

> IOPS counts how many read/write commands a storage device completes per second — bytes/sec and latency still matter for real workloads.

## Interview Relevance

Storage sizing: random 4K vs sequential MB/s, queue depth, and how [[fsync]] / page cache change observed IOPS.

## Sources

- Brendan Gregg — storage performance methodology — deep-dive
- [Wikipedia — IOPS](https://en.wikipedia.org/wiki/IOPS) — overview
- SNIA storage performance specifications — overview

## Key Concepts

- **IOPS vs throughput:** small random IO → IOPS; large sequential → MB/s.
- **Knobs:** block size, queue depth, media type, sync policy.
- **Cache effect:** [[Buffer cache]] merges/delays writes vs app `write()` count.
- **Sync tax:** [[fsync]] can collapse effective IOPS for databases.

## Technical Details

| Media | Random 4K IOPS (typical class) |
|-------|--------------------------------|
| HDD | tens to low hundreds |
| SATA SSD | tens of thousands |
| NVMe | hundreds of thousands+ |

```bash
iostat -xz 1
fio --name=test --rw=randread --bs=4k --iodepth=32 --numjobs=1
```

[[CPU IO Bound Task]] services waiting on disk show low CPU and high `await` in `iostat`.

## Real-World Applications

Database volume selection, fio capacity tests, and explaining why “plenty of GB free” still feels slow.

## Pros/Cons or Trade-offs

- **Higher queue depth:** more IOPS until latency explodes.
- **Larger blocks:** better MB/s; fewer IOPS for same bytes.
- **Trade-off:** sync durability vs peak IOPS.

## Comparison

- vs bandwidth: different bottleneck axes for the same [[Persistent Block Storage]] device.
- vs app ops/sec: not 1:1 because of caching and batching.

## Mistakes to Avoid

- Sizing from sequential MB/s for a random OLTP workload.
- Ignoring `await`/`svctm` while celebrating raw IOPS.
- Benchmarking with cache hits and calling it device IOPS.
