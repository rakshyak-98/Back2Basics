[[Networking]] [[POSIX Socket]] [[Berkeley sockets]] [[TCP]] [[UDP]] [[Inter Process Communication]] [[address port]]

# BSD Socket

> BSD sockets are the original Berkeley API for network (and Unix-domain) I/O — POSIX standardized the same shape.

```txt
        BSD Socket ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use “BSD sockets” to check whether you know the classic `socket`…

## Sources
- [Wikipedia — Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets) — overview
- [IEEE Std 1003.1 — `socket`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/socket.html) — deep-dive
- [man 2 socket (Linux)](https://man7.org/linux/man-pages/man2/socket.2.html) — deep-dive

## Key Concepts
- **BSD / Berkeley API:** `socket`, `bind`, `listen`, `connect`, `send`, `recv` → the programming model…
- **POSIX sockets:** portable standardization of that shape → same calls
- **Address family:** `AF_INET`, `AF_INET6`, `AF_UNIX` → which namespace the address lives in.
- **Socket type:** `SOCK_STREAM` / `SOCK_DGRAM` → TCP-like stream vs UDP-like datagram.
- **File descriptor:** sockets are fds → `poll` / `select` / `epoll` work on them like files.

### BSD the OS vs BSD the API

| Meaning | What people mean |
|---------|------------------|
| **API** | `socket`/`bind`/`connect` programming model (this note) |
| **OS family** | FreeBSD, OpenBSD, NetBSD, Darwin — systems descended from Berkeley Unix |

## Technical Details
```txt
Your code
   │  BSD / POSIX API
   ▼
socket fd ── AF_INET + SOCK_STREAM ──► TCP
         └── AF_INET + SOCK_DGRAM  ──► UDP
         └── AF_UNIX               ──► local IPC
```

```c
#include <sys/socket.h>
#include <netinet/in.h>

int s = socket(AF_INET, SOCK_STREAM, 0);  // TCP
int u = socket(AF_INET, SOCK_DGRAM, 0);   // UDP
```

```bash
# Who owns which sockets
ss -antp
lsof -i -P -n
```

| Knob | Why it matters |
|------|----------------|
| Family + type | Wrong combo ⇒ wrong protocol behavior |
| `SOCK_NONBLOCK` (Linux) | Create non-blocking in one step |
| Protocol arg `0` | Kernel picks default for type (usual) |

| Symptom | Check | Fix |
|---------|-------|-----|
| `EAFNOSUPPORT` | Family not compiled/enabled | Use `AF_INET`/`AF_INET6` available on host |
| `EPROTONOSUPPORT` | Type/protocol mismatch | Match `SOCK_STREAM`↔TCP, `SOCK_DGRAM`↔UDP |
| Works on Linux, fails on BSD | Linux-only option | Gate `epoll`/`SO_*` behind `#ifdef` |
| Can’t find peer via Unix socket | Path / permissions | Same FS path; check directory execute bits |

## Mistakes to Avoid
- **Mistake:** Treating “BSD sockets” in embedded docs as “you run FreeBSD”
- **Mistake:** Assuming the API alone sends packets
- **Mistake:** Teaching only mandatory client/server
- **Mistake:** Confusing OpenBSD/FreeBSD hardening docs with the `socket(2)` ma…

## Pros/Cons or Trade-offs
- **Pro:** One fd-shaped model for [[TCP]], [[UDP]], and local [[Inter Process Communication]].
- **Con:** API alone is not a stack — you still need transport, routing, and usually a higher-level library (TLS, HTTP).
- **Con:** Linux extras (`epoll`, some `SO_*`) are beyond strict portable BSD/POSIX; gate them per OS.

## Comparison
- vs [[POSIX Socket]]: POSIX is the portable standardization of the Berkeley shape
- vs [[Berkeley sockets]]: same API family
- vs raw application protocols in C: prefer mature libraries unless you must own the wire format.


### Use cases
- Every language runtime’s networking layer wraps this API

- **Example:** A microservice opens `AF_INET` + `SOCK_STREAM` for outbound HTTP…
