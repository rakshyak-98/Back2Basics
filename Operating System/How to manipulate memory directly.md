[[Operating System]] [[Heap memory]] [[shared memory]] [[assembly language]] [[file descriptors]] [[opcode]]

# How to manipulate memory directly

> Direct memory manipulation means mapping bytes into your address space and touching them with pointers, atomics, or `mmap` — bypassing higher-level abstractions when you accept the safety cost.

```txt
        How to manipulate  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Systems reviews probe `mmap` vs `read`/`write`, shared-memory IPC, and why…

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

- For instruction-level access patterns see [[assembly language]] and [[opcode]…

## Mistakes to Avoid
- **Mistake:** Mapping `/dev/mem` “because it’s faster” on a modern multi-user …
- **Mistake:** Forgetting `MAP_SHARED` vs `MAP_PRIVATE` semantics when expectin…
- **Mistake:** Leaving execute permission on writable mappings without need (W^…

## Pros/Cons or Trade-offs
- **Pro:** Zero-copy potential; simple random access vs stream I/O.
- **Con:** Easy to create use-after-unmap and TOCTOU bugs; security blast radius.
- **Trade-off:** `mlock` all hot data vs letting the kernel reclaim under pressure.

## Comparison
- vs [[Heap memory]]: heap is allocator-managed anonymous memory
- vs `read`/`write`: syscalls copy; mmap faults pages in and lets you touch them.


### Use cases
- Databases and message brokers mmap data files or use shared-memory rings
