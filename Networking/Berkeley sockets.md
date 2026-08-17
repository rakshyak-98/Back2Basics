[[POSIX Socket]] [[BSD Socket]] [[TCP]] [[UDP]] [[webSocket]] [[Inter Process Communication]] [[file descriptors]]

# Berkeley sockets

> BSD-origin API (`socket`, `bind`, `listen`, `connect`, `send`, `recv`) — the POSIX façade for Internet and Unix domain communication.





## Interview Relevance
Interviewers expect you to walk a TCP server path (`socket` → `bind` → `listen` → `accept`) and know that languages wrap this C ABI — not invent a different kernel model.

## Sources
- [Wikipedia — Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets) — overview
- [IEEE Std 1003.1 — sockets](https://pubs.opengroup.org/onlinepubs/9699919799/functions/socket.html) — deep-dive
- [man 7 socket (Linux)](https://man7.org/linux/man-pages/man7/socket.7.html) — deep-dive

## Key Concepts
- **C ABI most languages wrap:** domain + type + protocol → kernel holds connection state; userspace sees an fd + syscalls.
- **Fd-shaped I/O:** fits `select` / `poll` / `epoll` — see [[file descriptors]].
- **Stream vs datagram:** `SOCK_STREAM` → [[TCP]]; `SOCK_DGRAM` → [[UDP]]; `AF_UNIX` → local IPC.
- **Socket options:** `SO_REUSEADDR`, `TCP_NODELAY`, timeouts → production tunables via `setsockopt`.

## Technical Details
```txt
socket(domain, type, protocol)
   │
   ├─ AF_INET/AF_INET6 + SOCK_STREAM → TCP
   ├─ AF_INET + SOCK_DGRAM           → UDP
   └─ AF_UNIX + SOCK_STREAM           → local IPC
```

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

**Why `SO_REUSEADDR`:** faster restart after crash/TIME-WAIT. **`TCP_NODELAY`:** disable Nagle for latency-sensitive RPC.

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep PORT` | `SO_REUSEADDR`; kill stale holder; change port |
| Hang on connect | `ss -tan`; firewall | Security group; SYN dropped → timeout |
| `ECONNRESET` | Peer closed; TLS mismatch | App logs; tcpdump |
| Accept queue overflow | `ss -lnt` Send-Q vs `somaxconn` | Raise `net.core.somaxconn`; tune backlog |

## Real-World Applications
Go `net`, Python `socket`, Node `net`, and JVM NIO all sit on Berkeley sockets underneath.

**Example:** After a crash-restart, bind fails with `EADDRINUSE` during TIME-WAIT — enable `SO_REUSEADDR` (and understand what it does *not* do for multi-process bind).

## Pros/Cons or Trade-offs
- **Pro:** Universal, fd-compatible, maps cleanly to event loops.
- **Con:** Partial reads/writes and stream framing are the app’s job on [[TCP]].
- **Con:** Blocking sockets in a single-thread server stall everyone on one slow client.

## Comparison
- vs [[POSIX Socket]]: portable behavior and knobs; Berkeley naming emphasizes the historical C API.
- vs [[BSD Socket]]: sibling naming of the same lineage — use [[BSD Socket]] when distinguishing API vs BSD-the-OS.
- vs [[webSocket]]: WebSocket is an application protocol over TCP (HTTP Upgrade), not a replacement for the socket API.
- Same-host only: prefer `AF_UNIX` over IP to skip stack/NAT/firewall noise — see [[Inter Process Communication]].

## Mistakes to Avoid
- Assuming `read`/`write` return the full buffer — loop or use `sendmsg`; see [[non-blocking]] for `EAGAIN`.
- Leaking fds — every `accept` needs `close` on all paths.
- Hand-rolling HTTP/gRPC on bare sockets when a library already owns framing and TLS.
