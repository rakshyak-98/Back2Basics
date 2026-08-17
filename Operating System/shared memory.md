[[Operating System]] [[Inter Process Communication]] [[How to manipulate memory directly]] [[mutexes]] [[file descriptors]] [[IPC namespace]]

# Shared memory

> Shared memory maps the same physical pages into multiple processes — zero-copy IPC once mapped, requiring separate synchronization for concurrent access.

```txt
        Shared memory ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** IPC menu: when shm beats pipes, how you sync (mutex/atomics in the region), a…

## Sources
- Stevens, *Advanced Programming in the UNIX Environment* — deep-dive
- Linux `shm_overview(7)` manual page — deep-dive
- [Wikipedia — Shared memory](https://en.wikipedia.org/wiki/Shared_memory) — overview

## Key Concepts
- **Same page frames:** multiple address spaces, one physical backing.
- **APIs:** POSIX `shm_open`+`mmap`; System V `shmget`/`shmat`.
- **Sync separate:** [[mutexes]] or atomics in the shared region.
- **Namespace:** [[IPC namespace]] isolates SysV keys.

## Technical Details
```txt
Process A ──┐
            ├── same page frames → fast bulk data
Process B ──┘
```

- After mapping, loads/stores are ordinary.
- Contrast pipes (kernel copies each byte).
- See [[How to manipulate memory directly]] for `mmap` details

## Mistakes to Avoid
- **Mistake:** Mapping without a defined layout and sync protocol
- **Mistake:** Leaking SysV segments (`ipcs` leftovers)
- **Mistake:** Assuming stores are instantly visible without barriers/atomics o…

## Pros/Cons or Trade-offs
- **Pro:** Highest bandwidth IPC after setup.
- **Con:** Explicit sync; lifetime/cleanup hazards; security blast radius.
- **Trade-off:** shm speed vs pipe/socket simplicity.

## Comparison
- vs pipes/sockets: copy vs map.
- vs threads sharing heap: threads share by default; processes need shm.


### Use cases
- High-bandwidth telemetry, database buffer pools across processes, and game en…
