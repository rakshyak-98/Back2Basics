[[Networking]] [[BSD Socket]] [[Berkeley sockets]] [[TCP]] [[UDP]] [[address port]] [[localhost]]

# POSIX Socket

> POSIX sockets are the portable `socket()`/`bind()`/`connect()` API — a socket is a file descriptor you `read`/`write`/`close`.

```txt
        POSIX Socket ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want the client/server call sequence, what `bind` does vs `conne…

## Sources
- [IEEE Std 1003.1 — `socket`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/socket.html) — deep-dive
- [IEEE Std 1003.1 — `bind` / `listen` / `accept`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/bind.html) — deep-dive
- [Wikipedia — Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets) — overview

## Key Concepts
- **Socket as fd:** create with `socket`, then `read`/`write`/`close` like a file → “looks like a…
- **`bind`:** attach local IP:port → server identity
- **`listen` / `accept`:** queue + take connections → TCP server path.
- **`connect`:** dial peer → client path; OS may ephemeral-bind first.
- **`AF_INET` / `AF_UNIX`:** IPv4 network vs local IPC → Unix domain skips the network stack.
- **Non-blocking:** return `EAGAIN` instead of wait → needed with `epoll`/`poll`.

### Core calls

| Call | Role |
|------|------|
| `socket` | Create |
| `bind` / `listen` / `accept` | Server |
| `connect` | Client |
| `send`/`recv` or `read`/`write` | TCP stream |
| `sendto`/`recvfrom` | UDP datagram |
| `setsockopt` | Tunables (`SO_REUSEADDR`, timeouts, …) |

## Technical Details
```txt
Server: socket → bind → listen → accept → recv/send → close
Client: socket → (optional bind) → connect → send/recv → close
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep :port` | Kill old process; `SO_REUSEADDR`; other port |
| `EAGAIN` / `EWOULDBLOCK` | Non-blocking + empty/full buffer | Wait on `epoll`; retry; handle partial I/O |
| Partial `send`/`recv` | Byte count &lt; requested | Loop until done (TCP is a stream) |
| `SIGPIPE` / `EPIPE` | Write after peer close | `MSG_NOSIGNAL` or ignore SIGPIPE |
| Client works, server unreachable from LAN | Bound `127.0.0.1` | Bind `0.0.0.0` / correct interface |

## Mistakes to Avoid
- **Mistake:** Treating one `send` as one `recv` on [[TCP]]
- **Mistake:** Requiring `bind` on every client
- **Mistake:** Binding `127.0.0.1` then expecting LAN reachability

## Pros/Cons or Trade-offs
- **Pro:** Portable across Unix-like systems; one mental model for stream and datagram.
- **Con:** Strict POSIX ≠ Linux extras (`epoll`, `SO_REUSEPORT`) — check man pages per OS.
- **Con:** Blocking sockets in a single-thread server: one slow client stalls everyone.

## Comparison
- vs [[BSD Socket]] / [[Berkeley sockets]]: POSIX ≈ portable Berkeley/BSD sockets
- vs `AF_UNIX` for same-host IPC: prefer Unix sockets when you do not need IP
- vs application libraries: prefer HTTP/gRPC stacks unless you own the wire format.


### Use cases
- POSIX sockets are the portable baseline for servers and clients

- **Example:** A service bound only to `127.0.0.1` passes local health checks b…
