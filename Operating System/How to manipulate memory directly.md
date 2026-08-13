[[Operating System]] [[Heap memory]] [[shared memory]] [[assembly language]] [[file descriptors]]

# How to manipulate memory directly

> Direct memory manipulation means mapping bytes into your address space and touching them with pointers, atomics, or mmap — bypassing higher-level abstractions when you accept the safety cost.

## Common mechanisms (Linux)

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

## Safety and permissions

Modern kernels restrict raw hardware access. User space normally uses **file mappings** and **shared memory APIs**, not arbitrary physical addresses. Bugs become security vulnerabilities — use only with tests and capability boundaries.

For instruction-level access patterns see [[assembly language]] and [[opcode]] encoding.

## Sources

- Kerrisk, *The Linux Programming Interface* — `mmap`, shared memory
- Linux `mmap(2)`, `mlock(2)` manual pages
- Bryant & O’Hallaron, *Computer Systems: A Programmer’s Perspective*
