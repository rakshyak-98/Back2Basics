[[Operating System]] [[Persistent Block Storage]] [[Buffer cache]] [[file descriptors]] [[logical partitions]] [[MBR]] [[fsync]]

# Abstract storage location

> An abstract storage location is any addressable place where bytes live — file, block device, memory-mapped region, or cloud object — without naming the physical medium underneath.

## Interview Relevance

Interviewers want you to separate *what the app names* (path, volume, LBA, handle) from *what stores bits*, and to tie that to permissions, caching, and durability.

## Sources

- [Linux kernel docs — Page Cache](https://docs.kernel.org/mm/page_cache.html) — deep-dive
- Tanenbaum & Bos, *Modern Operating Systems* — file system and I/O layers — deep-dive
- [Wikipedia — Computer data storage](https://en.wikipedia.org/wiki/Computer_data_storage) — overview

## Key Concepts

- **Caller sees names/handles:** paths, volume IDs, LBAs, kernel handles ([[file descriptors]]).
- **Hidden:** geometry, wear leveling, RAID, hypervisor backends.
- **Policy at the boundary:** permissions, quotas, encryption, caching ([[Buffer cache]]).
- **Durability separate from visibility:** same-host readers may see bytes before they survive power loss.

## Technical Details

| Layer | What the caller sees | What is hidden |
|-------|----------------------|----------------|
| Application | `open("/var/log/app.log")` | inode, extents, SSD wear leveling |
| Database | tablespace file or raw device | partition table, LVM striping |
| Container | bind-mounted path in a namespace | host filesystem, copy-on-write graph driver |
| Cloud VM | EBS volume or persistent disk | hypervisor storage backend |

**Path names** resolve through VFS to an inode and backing store. **Block devices** expose sectors; filesystems usually sit on top. **Memory-mapped files** map a file range into the process — same cached pages may back both `read()` and loads.

Concrete layout: [[MBR]], [[logical partitions]], [[Persistent Block Storage]]. Durability: [[fsync]].

## Real-World Applications

The same binary runs on laptop SSD, SAN LUN, or NFS because it talks to abstract locations. Cloud volume attach/detach remaps the abstract device without rewriting the app.

## Pros/Cons or Trade-offs

- **Pro:** Portability and centralized policy.
- **Con:** Easy to forget which durability guarantees the backend actually provides.
- **Trade-off:** raw block devices (more control) vs filesystem paths (simpler ops).

## Comparison

- vs [[Persistent Block Storage]]: block storage is one durable backend; abstract location is the naming/handle layer above any medium.
- vs object storage keys: both are abstract; APIs and consistency models differ.

## Mistakes to Avoid

- Assuming a successful `write` to an abstract path is durable without flush semantics.
- Treating cloud volume identity as physical media identity for DR.
- Bypassing the abstraction with `/dev/mem`-style access when a file/block API exists.
