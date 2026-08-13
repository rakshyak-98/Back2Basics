[[Networking]] [[BSD Socket]] [[TCP]] [[UDP]] [[address port]]

# POSIX Socket

> POSIX sockets are the portable `socket()`/`bind()`/`connect()` API — a socket is a file descriptor you `read`/`write`/`close`.

---

## How it works

```txt
Server: socket → bind → listen → accept → recv/send → close
Client: socket → (optional bind) → connect → send/recv → close
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Socket** | Communication endpoint (fd) | “Looks like a file to the process.” |
| **bind** | Attach local IP:port | “Server identity; clients usually skip it.” |
| **listen / accept** | Queue + take connections | “TCP server path.” |
| **connect** | Dial peer | “Client; OS may ephemeral-bind first.” |
| **AF_INET / AF_UNIX** | IPv4 vs local IPC | “Unix domain skips the network stack.” |
| **Non-blocking** | Return `EAGAIN` instead of wait | “Needed with `epoll`/`poll`.” |

### Core calls (map)

| Call | Role |
|------|------|
| `socket` | Create |
| `bind` / `listen` / `accept` | Server |
| `connect` | Client |
| `send`/`recv` or `read`/`write` | TCP stream |
| `sendto`/`recvfrom` | UDP datagram |
| `setsockopt` | Tunables (`SO_REUSEADDR`, timeouts, …) |

---


## Configuration and commands

```c
int fd = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in addr = {
  .sin_family = AF_INET,
  .sin_port = htons(8080),
  .sin_addr.s_addr = htonl(INADDR_ANY), // 0.0.0.0
};
bind(fd, (struct sockaddr *)&addr, sizeof addr);
listen(fd, 128);
int cfd = accept(fd, NULL, NULL);
```

```bash
# See binds / peers
ss -tlnp
ss -tnp
```

| Knob | Why it matters |
|------|----------------|
| `SO_REUSEADDR` | Rebind after TIME_WAIT |
| `SO_RCVTIMEO` / `SNDTIMEO` | Bound stuck `recv`/`send` |
| `O_NONBLOCK` | Event-loop friendly |
| `IPV6_V6ONLY` | Dual-stack vs IPv6-only behavior |
| Backlog (`listen`) | Syn flood / accept lag ⇒ drops |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep :port` | Kill old process; `SO_REUSEADDR`; other port |
| `EAGAIN` / `EWOULDBLOCK` | Non-blocking + empty/full buffer | Wait on `epoll`; retry; handle partial I/O |
| Partial `send`/`recv` | Byte count &lt; requested | Loop until done (TCP is a stream) |
| `SIGPIPE` / `EPIPE` | Write after peer close | `MSG_NOSIGNAL` or ignore SIGPIPE |
| Client works, server unreachable from LAN | Bound `127.0.0.1` | Bind `0.0.0.0` / correct interface |

---


## Gotchas

> [!WARNING]
> **TCP has no message boundaries** — one `send` ≠ one `recv`; frame in the app.

> [!WARNING]
> **bind is optional for clients** — omit it unless you need a fixed source port/IP.

> [!WARNING]
> **POSIX ≈ portable BSD sockets** — Linux extras (`epoll`, `SO_REUSEPORT`) are beyond strict POSIX; check man pages per OS.

---


## When not to use

- **Raw sockets for application protocols** — prefer HTTP/gRPC libraries unless you own the wire format.
- **Blocking sockets in a single-thread server** — one slow client stalls everyone.
- **AF_INET for same-host IPC when AF_UNIX fits** — Unix sockets are simpler and skip NAT/firewall noise.

---


## Related

[[Networking]] [[BSD Socket]] [[TCP]] [[UDP]] [[address port]] [[localhost]]

## Sources

- [Wikipedia — POSIX Socket](https://en.wikipedia.org/wiki/POSIX_Socket)
