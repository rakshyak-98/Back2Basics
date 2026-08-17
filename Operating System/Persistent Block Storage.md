[[Operating System]] [[abstract storage location]] [[disk IOPS]] [[Buffer cache]] [[fsync]] [[MBR]] [[Boot/UEFI]] [[logical partitions]]

# Persistent Block Storage

> Persistent block storage survives power-off — HDDs, SSDs, NVMe, SAN LUNs — exposed as numbered sectors or volumes under partitions and file systems.





## Interview Relevance
Expect durability questions: what `write` + [[fsync]] guarantee on a block device, how cloud volumes differ from local NVMe, and where [[disk IOPS]] / queue depth show up under load.

## Sources
- [Linux kernel docs — Block layer](https://docs.kernel.org/block/index.html) — deep-dive
- SNIA storage tutorials — overview
- [Wikipedia — Block (data storage)](https://en.wikipedia.org/wiki/Block_(data_storage)) — overview

## Key Concepts
- **Block interface:** fixed sectors (often 512 B or 4 KiB logical).
- **Stack:** path → VFS → filesystem → block layer → driver → device.
- **Cache vs media:** [[Buffer cache]] holds dirty/clean pages; media holds durable bits after flush.
- **Cloud volumes:** remote block devices with their own latency and durability SLAs.

## Technical Details
```txt
Application path → VFS → filesystem → block layer → driver → NVMe/SATA
Partition: [[MBR]] or GPT ([[Boot/UEFI]]) → [[logical partitions]]
```

Writes may sit in drive **write cache** until [[fsync]] and flush commands complete — critical for databases. [[disk IOPS]] and queue depth define throughput under load.

## Real-World Applications
Local NVMe for databases, EBS/Persistent Disk for VMs, SAN LUNs for shared enterprise storage. Backup pipelines snapshot volumes then copy off-box.

## Pros/Cons or Trade-offs
- **Pro:** Simple random R/W interface; OS and databases understand blocks universally.
- **Con:** Latency and durability depend on cache layers you do not always see.
- **Trade-off:** local NVMe latency vs cloud volume elasticity and replication.

## Comparison
- vs [[abstract storage location]]: abstract locations are logical names; block storage is the durable sector device underneath.
- vs object storage: blocks are mutable sectors; objects are usually whole-blob PUT/GET.

## Mistakes to Avoid
- Treating cloud volume “99.99% durable” as application-level backup.
- Ignoring drive write cache / controller battery when arguing fsync safety.
- Sizing only capacity (GB) and forgetting IOPS and latency SLOs.
