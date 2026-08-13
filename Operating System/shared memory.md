[[Operating System]] [[Inter Process Communication]] [[How to manipulate memory directly]] [[mutexes]] [[file descriptors]]

# Shared memory

> Shared memory maps the same physical pages into multiple processes — zero-copy IPC once mapped, requiring separate synchronization for concurrent access.

POSIX: `shm_open` + `mmap`. System V: `shmget`, `shmat`. After mapping, reads/writes are plain loads/stores — use [[mutexes]] or atomics in the shared region.

```txt
Process A ──┐
            ├── same page frames → fast bulk data
Process B ──┘
```

Contrast pipes (kernel copies each byte). [[IPC namespace]] isolates SysV keys between containers.

## Sources

- Stevens, *Advanced Programming in the UNIX Environment*
- Linux `shm_overview(7)` manual page
- Wikipedia: [Shared memory](https://en.wikipedia.org/wiki/Shared_memory)
