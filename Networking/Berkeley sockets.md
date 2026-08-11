[[POSIX Socket]] [[TCP]] [[UDP]] [[webSocket]]

# Berkeley sockets

> BSD-origin API (`socket`, `bind`, `listen`, `connect`, `send`, `recv`) — the POSIX façade for Internet and Unix domain communication.

---

## Mental model

**Berkeley sockets** are the **C ABI** most languages wrap:

```txt
socket(domain, type, protocol)
   │
   ├─ AF_INET/AF_INET6 + SOCK_STREAM → TCP
   ├─ AF_INET + SOCK_DGRAM           → UDP
   └─ AF_UNIX + SOCK_STREAM           → local IPC
```

File-descriptor shaped — fits `select`/`poll`/`epoll` ([[file descriptors]]). Kernel holds connection state; userspace sees fd + syscalls.

Also see [[POSIX Socket]] for portable behavior details and [[BSD Socket]] if present as sibling note.

---

## Standard config / commands

### Minimal TCP server (C pattern)

```c
int fd = socket(AF_INET, SOCK_STREAM, 0);
bind(fd, ...);
listen(fd, SOMAXCONN);
int c = accept(fd, ...);
read(c, buf, n);
```

### Debug live sockets

```bash
ss -tlnp                    # listening TCP
ss -tan state established
strace -e trace=network -p PID
```

### Socket options (production)

```c
int yes = 1;
setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);
setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &yes, sizeof yes);
```

```bash
# Linux: inspect via ss
ss -tin 'sport = :8080'
```

**Why `SO_REUSEADDR`:** faster restart after crash/TIME-WAIT; **TCP_NODELAY:** disable Nagle for latency-sensitive RPC.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep PORT` | `SO_REUSEADDR`; kill stale holder; change port |
| Hang on connect | `ss -tan`; firewall | Security group; SYN dropped → timeout |
| `ECONNRESET` | Peer closed; TLS mismatch | App logs; tcpdump |
| Accept queue overflow | `ss -lnt` Send-Q vs `somaxconn` | Raise `net.core.somaxconn`; tune backlog |

---

## Gotchas

> [!WARNING]
> **Partial reads/writes** — `read`/`write` may return less than requested; loop or use `sendmsg`.

> [!WARNING]
> **Blocking vs non-blocking** changes error shape (`EAGAIN`) — see [[non-blocking]].

> [!WARNING]
> **FD leaks** — every `accept` needs `close` on all paths.

---

## When NOT to use

For same-host IPC only, **Unix domain sockets** avoid IP stack overhead. For HTTP/gRPC, use libraries — don't hand-roll protocol on bare sockets unless necessary.

---

## Related

[[POSIX Socket]] [[TCP]] [[UDP]] [[Berkeley sockets]] [[Inter Process Communication]] [[file descriptors]]
