[[Operating System]] [[Heap memory]] [[shared memory]] [[assembly language]] [[file descriptors]] [[opcode]]

# How to manipulate memory directly

> Direct memory manipulation means mapping bytes into your address space and touching them with pointers, atomics, or `mmap` — bypassing higher-level abstractions when you accept the safety cost.

## Interview Relevance

Systems interviews probe `mmap` vs `read`/`write`, shared-memory IPC, and why `/dev/mem` is almost never the right answer in production user space.

## Sources

- Kerrisk, *The Linux Programming Interface* — `mmap`, shared memory — deep-dive
- Linux `mmap(2)`, `mlock(2)` manual pages — deep-dive
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective* — deep-dive

## Key Concepts

- **Mapped memory:** file or anonymous pages appear as a byte array in the process.
- **Shared mappings:** [[shared memory]] for high-bandwidth IPC.
- **Pinning:** `mlock` prevents swap — latency vs memory pressure trade-off.
- **Capability boundary:** raw physical access is restricted; prefer fds and POSIX APIs.

## Technical Details

| Mechanism | Use |
|-----------|-----|
| `mmap()` | Map file or anonymous memory |
| `/dev/mem`, `/dev/kmem` | Raw physical (root, dangerous) |
| [[shared memory]] (`shm_open`, `mmap`) | IPC between processes |
| `mlock()` | Pin pages — avoid swap |

```c
void *p = mmap(NULL, len, PROT_READ|PROT_WRITE,
               MAP_SHARED, fd, offset);
/* read/write *p — page faults populate from file or zero fill */
munmap(p, len);
```

For instruction-level access patterns see [[assembly language]] and [[opcode]] encoding.

## Real-World Applications

Databases and message brokers mmap data files or use shared-memory rings. Language runtimes map JITed code (`PROT_EXEC` with care). High-performance packet paths use huge pages + pinned buffers.

## Pros/Cons or Trade-offs

- **Pro:** Zero-copy potential; simple random access vs stream I/O.
- **Con:** Easy to create use-after-unmap and TOCTOU bugs; security blast radius.
- **Trade-off:** `mlock` all hot data vs letting the kernel reclaim under pressure.

## Comparison

- vs [[Heap memory]]: heap is allocator-managed anonymous memory; mmap can be file-backed or explicit arenas.
- vs `read`/`write`: syscalls copy; mmap faults pages in and lets you touch them.

## Mistakes to Avoid

- Mapping `/dev/mem` “because it’s faster” on a modern multi-user host.
- Forgetting `MAP_SHARED` vs `MAP_PRIVATE` semantics when expecting IPC.
- Leaving execute permission on writable mappings without need (W^X violations).
