[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[CPU IO Bound Task]] [[fsync]]

# disk IOPS

> IOPS (I/O operations per second) counts how many read/write commands a storage device completes per second — throughput in bytes and latency in milliseconds both matter for real workloads.

**IOPS** rises with smaller random IO on SSDs/NVMe; large sequential transfers measure **MB/s** instead. Controllers, queue depth, and block size all change the number.

## Rough reference (order of magnitude, not guarantees)

| Media | Random 4K IOPS (typical class) |
|-------|--------------------------------|
| HDD | tens to low hundreds |
| SATA SSD | tens of thousands |
| NVMe | hundreds of thousands+ |

## OS stack effects

The [[Buffer cache]] merges and delays writes — measured IOPS at the disk may be lower than application `write()` calls. [[fsync]] forces flush and can collapse IOPS under sync-heavy databases.

```bash
iostat -xz 1
fio --name=test --rw=randread --bs=4k --iodepth=32 --numjobs=1
```

[[CPU IO Bound Task]] services waiting on disk show low CPU and high `await` in `iostat`.

## Sources

- Brendan Gregg — storage performance methodology
- Wikipedia: [IOPS](https://en.wikipedia.org/wiki/IOPS)
- SNIA storage performance specifications
