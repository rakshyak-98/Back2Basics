[[Operating System]] [[process]] [[shared memory]] [[file descriptors]] [[Thread]]

# Inter Process Communication

> IPC is how separate processes exchange data — pipes, sockets, shared memory, and messages — instead of sharing an address space.

---

## Mental model

**Say it in one breath:** Processes are isolated; pick an IPC primitive by need — stream bytes, messages, shared RAM, or RPCs over sockets.

```txt
Process A                     Process B
    │                             │
    ├──── pipe / FIFO ────────────┤  byte stream (local)
    ├──── UNIX socket ────────────┤  local, fd passing
    ├──── TCP/UDP socket ─────────┤  local or remote (ports)
    ├──── shared memory + sync ───┤  fastest bulk, manual sync
    └──── mq / dbus / … ──────────┘  structured messages
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Pipe** | One-way byte stream | “Shell `|` is an anonymous pipe.” |
| **FIFO** | Named pipe on the filesystem | “Unrelated processes meet at a path.” |
| **UNIX domain socket** | Local socket via path/`abstract` | “Faster than TCP localhost; can pass fds.” |
| **TCP port** | Host:port demux to a process | “Kernel delivers to the listening socket.” |
| **Shared memory** | Same physical pages mapped twice | “Fastest large transfers; you handle sync.” |
| **Synchronization** | Mutex/sem on shm or message order | “Shm without locks is a data race across processes.” |

### Approaches (pick by constraint)

| Need | Prefer |
|------|--------|
| Simple parent↔child bytes | Anonymous pipe |
| Unrelated local services | UNIX socket |
| Remote / language-agnostic | TCP/UDP (+ framing/RPC) |
| Huge bulk local data | [[shared memory]] + [[mutexes]]/[[semaphores]] |
| Desktop bus signals | [[D-Bus]] |

### Ports and the outside world

External clients don’t “enter the OS IPC layer” magically — they hit a **socket bound to a port**. The kernel demultiplexes by protocol/port to the listening process; that process may then talk to workers via local IPC.

```txt
Internet → NIC → kernel stack → :443 LISTEN socket → process
                                      │
                                      └─ optional worker IPC (shm/unix/pipe)
```

---

## Standard config / commands

```bash
# Who listens (network IPC edge)
ss -lptn
sudo lsof -iTCP -sTCP:LISTEN

# UNIX sockets
ss -xlp
ls -l /run/*.sock 2>/dev/null

# Pipes / fds between processes
lsof -p <pid> | grep -E 'FIFO|PIPE|unix|TCP'
ls -l /proc/<pid>/fd

# Shared memory segments (SysV)
ipcs -m
ipcrm -m <shmid>          # cleanup leftover

# POSIX shm typically under /dev/shm
ls -l /dev/shm
```

| Knob | Why it matters |
|------|----------------|
| Socket backlog / `somaxconn` | Connection drops under accept load |
| Framing on streams | TCP/pipes are bytes — you define messages |
| `SCM_RIGHTS` | Pass fds over UNIX sockets (privilege pattern) |
| Shm + lock placement | Wrong sync → heisenbugs across processes |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `connection refused` | `ss -lptn` port/process | Start service; fix bind address |
| Hang on `read` pipe | Peer dead? both ends open? | Ensure writer closes; handle `EOF` |
| Slow localhost RPC | Using TCP loopback | Prefer UNIX sockets for local |
| `ENOSPC` on `/dev/shm` | `df -h /dev/shm` | Size tmpfs; clean segments |
| Leftover SysV shm after crash | `ipcs -m` | `ipcrm`; use POSIX shm + unlink |
| Permission on socket file | Path mode/owner | dir `700`/`770`; correct user |

---

## Gotchas

> [!WARNING]
> **TCP is a byte stream** — without length prefixes/delimiters you will merge messages.

> [!WARNING]
> **Shared memory is not “free IPC”** — you still need memory ordering and locks; one bad writer corrupts everyone.

> [!WARNING]
> **Half-closed pipes** — if the reader vanishes, writer gets `SIGPIPE`/`EPIPE`.

> [!WARNING]
> **Port IPC ≠ only “IPC mechanisms” chapter** — sockets are the bridge to the network; local UNIX sockets are still IPC.

---

## When NOT to use

- **Don’t use multi-process + shm for simple apps** — threads in one process may be enough ([[Thread]]).
- **Don’t expose raw SysV shm to multi-tenant hosts** — easy to leak and hard to ACL; prefer supervised sockets.
- **Don’t invent a new RPC** when HTTP/gRPC on UNIX/TCP already fits ops and tooling.

---

## Related

[[process]] [[Thread]] [[shared memory]] [[file descriptors]] [[mutexes]] [[semaphores]] [[IPC namespace]] [[D-Bus]] [[ss]] [[lsof]] [[Blocking]] [[system call]]
