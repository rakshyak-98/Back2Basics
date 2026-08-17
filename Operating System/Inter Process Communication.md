[[Operating System]] [[process]] [[shared memory]] [[file descriptors]] [[Thread]] [[IPC namespace]] [[mutexes]]

# Inter Process Communication

> Inter-process communication (IPC) lets separate address spaces exchange data and synchronize — pipes, sockets, shared memory, and message queues are the usual Unix toolkit.

```txt
        Inter Process Comm ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect a menu of IPC options with trade-offs (copy vs map, local vs network) …

## Sources
- Stevens, *Advanced Programming in the UNIX Environment* — IPC chapters — deep-dive
- Linux `pipe(7)`, `unix(7)`, `shm_overview(7)` manual pages — deep-dive
- [Wikipedia — Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication) — overview

## Key Concepts
- **Address-space isolation:** each [[process]] has private virtual memory; IPC bridges it.
- **Copy vs map:** pipes/sockets copy; [[shared memory]] maps for bandwidth.
- **Local sockets:** Unix domain sockets are fd-based and common for same-host services.
- **Namespace:** [[IPC namespace]] isolates SysV/POSIX mqueue identifiers in containers.

## Technical Details
| Mechanism | Copy behavior | Typical use |
|-----------|---------------|-------------|
| Pipe / socket | Kernel copies bytes | CLI tools, services |
| [[shared memory]] | Mapped into both | High bandwidth |
| Unix domain socket | Local, fd-based | DB clients on same host |
| Signals | Minimal metadata | Events, job control |

- Threads in one process ([[Thread]]) share memory by default

## Mistakes to Avoid
- **Mistake:** Using SysV shared memory without cleanup — leaked `ipcs` segments
- **Mistake:** Passing complex pointers through shared memory without a defined…
- **Mistake:** Choosing signals to carry payloads beyond a small event code

## Pros/Cons or Trade-offs
- **Pipes/sockets:** simple and safe; copy cost and kernel crossings.
- **Shared memory:** fast; needs explicit sync and careful lifetime.
- **Signals:** cheap wakeups; terrible for bulk data.

## Comparison
- vs [[Thread]] sharing: same address space — sync with locks, not IPC.
- vs network RPC: IPC on one host; RPC crosses machines (often still sockets underneath).


### Use cases
- Shell pipelines (`|`), PostgreSQL over Unix sockets, Redis/shm rings, and mic…
