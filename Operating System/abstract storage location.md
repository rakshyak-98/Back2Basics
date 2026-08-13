[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[file descriptors]] [[logical partitions]]

# Abstract storage location

> An abstract storage location is any addressable place where bytes live — file, block device, memory-mapped region, or cloud object — without naming the physical medium underneath.

Operating systems and applications rarely talk to spinning platters or NAND cells directly. They talk to **abstract locations**: paths, volume identifiers, logical block addresses, or handles returned by the kernel. The abstraction hides geometry, vendor firmware, and RAID layout while still exposing read, write, seek, and durability semantics.

## Why abstraction matters

| Layer | What the caller sees | What is hidden |
|-------|----------------------|----------------|
| Application | `open("/var/log/app.log")` | inode, extents, SSD wear leveling |
| Database | tablespace file or raw device | partition table, LVM striping |
| Container | bind-mounted path in a namespace | host filesystem, copy-on-write graph driver |
| Cloud VM | EBS volume or persistent disk | hypervisor storage backend |

Abstraction lets the same program run on a laptop SSD, a SAN LUN, or a network file system. It also centralizes policy: permissions, quotas, encryption, and caching apply at the abstract boundary ([[file descriptors]], [[Buffer cache]]).

## How locations are named

**Path names** resolve through a virtual file system layer to an inode and backing store. **Block devices** (`/dev/nvme0n1p2`) expose fixed-size sectors; user space often still uses a filesystem on top. **Memory-mapped files** map an abstract file range into the process address space — the same cached pages may back both `read()` and a direct load instruction.

Persistent storage notes tie the idea to concrete boot and layout topics: [[MBR]], [[logical partitions]], [[Persistent Block Storage]].

## Durability is not automatic

Writing to an abstract location usually lands in a cache first ([[Buffer cache]], page cache). The bytes are visible to readers on the same machine, but survive power loss only after the kernel and device flush dirty data — see [[fsync]] and [[Persistent Block Storage]].

## Sources

- Linux kernel documentation: [Page Cache](https://docs.kernel.org/mm/page_cache.html)
- Tanenbaum & Bos, *Modern Operating Systems* — file system and I/O abstraction layers
- Wikipedia: [Computer data storage](https://en.wikipedia.org/wiki/Computer_data_storage)
