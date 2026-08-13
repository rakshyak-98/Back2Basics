[[Operating System]] [[abstract storage location]] [[disk IOPS]] [[Buffer cache]] [[fsync]] [[MBR]]

# Persistent Block Storage

> Persistent block storage survives power-off — HDDs, SSDs, NVMe, SAN LUNs — exposed to the OS as numbered sectors or volumes layered with partition tables and file systems.

The block interface reads/writes fixed **sectors** (often 512 B or 4 KiB logical). File systems map paths to block ranges; the [[Buffer cache]] caches those blocks in RAM.

## Layout stack

```txt
Application path → VFS → filesystem → block layer → driver → NVMe/SATA
Partition: [[MBR]] or GPT ([[Boot/UEFI]]) → [[logical partitions]]
```

## Durability chain

Writes may sit in drive **write cache** until [[fsync]] and flush commands complete — critical for databases. [[disk IOPS]] and queue depth define throughput under load.

Cloud volumes (EBS, Persistent Disk) are remote block devices with their own latency and durability SLAs.

## Sources

- Linux kernel documentation: [Block layer](https://docs.kernel.org/block/index.html)
- SNIA storage tutorials
- Wikipedia: [Block (data storage)](https://en.wikipedia.org/wiki/Block_(data_storage))
