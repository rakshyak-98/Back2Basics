[[Operating System]] [[process]] [[shared memory]] [[file descriptors]] [[Thread]] [[IPC namespace]]

# Inter Process Communication

> Inter-process communication (IPC) lets separate address spaces exchange data and synchronize — pipes, sockets, shared memory, and message queues are the usual Unix toolkit.

Each [[process]] has private virtual memory. **IPC** bridges isolation:

| Mechanism | Copy behavior | Typical use |
|-----------|---------------|-------------|
| Pipe / socket | Kernel copies bytes | CLI tools, services |
| [[shared memory]] | Mapped into both | High bandwidth |
| Unix domain socket | Local, fd-based | DB clients on same host |
| Signals | Minimal metadata | Events, job control |

## Namespaces

[[IPC namespace]] isolates System V IPC identifiers and POSIX mqueue names — containers see their own IPC universe.

Threads in one process ([[Thread]]) share memory by default — use [[mutexes]] instead of IPC.

## Sources

- Stevens, *Advanced Programming in the UNIX Environment* — IPC chapters
- Linux `pipe(7)`, `unix(7)`, `shm_overview(7)` manual pages
- Wikipedia: [Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication)
