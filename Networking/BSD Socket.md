[[Networking]] [[POSIX Socket]] [[TCP]] [[UDP]] [[Inter Process Communication]]

# BSD Socket

> BSD sockets are the original Berkeley API for network (and Unix-domain) I/O — POSIX standardized the same shape.

## Mental model

**Say it in one breath:** Everything is `socket()` + address family + type (stream/datagram); TCP/UDP (or Unix) do the real transport underneath.

```txt
Your code
   │  BSD / POSIX API
   ▼
socket fd ── AF_INET + SOCK_STREAM ──► TCP
         └── AF_INET + SOCK_DGRAM  ──► UDP
         └── AF_UNIX               ──► local IPC
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **BSD sockets** | Berkeley socket API | “The model Linux/macOS still expose.” |
| --- | --- | --- |
| **POSIX sockets** | Portable standardization of that API | “Same calls; fewer OS-specific extras.” |
| **Address family** | `AF_INET`, `AF_INET6`, `AF_UNIX` | “Which namespace the address lives in.” |
| **Socket type** | `SOCK_STREAM` / `SOCK_DGRAM` | “TCP-like vs UDP-like.” |
| **fd** | File descriptor | “`poll`/`select`/`epoll` work on sockets.” |

### BSD the OS vs BSD the API

| Meaning | What people mean |

| **API** | `socket`/`bind`/`connect` programming model (this note) |
| --- | --- |
| **OS family** | FreeBSD, OpenBSD, NetBSD, Darwin — systems descended from Berkeley Unix |

## Standard config / commands

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

| Family + type | Wrong combo ⇒ wrong protocol behavior |
| --- | --- |
| `SOCK_NONBLOCK` (Linux) | Create non-blocking in one step |
| Protocol arg `0` | Kernel picks default for type (usual) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `EAFNOSUPPORT` | Family not compiled/enabled | Use `AF_INET`/`AF_INET6` available on host |
| `EPROTONOSUPPORT` | Type/protocol mismatch | Match `SOCK_STREAM`↔TCP, `SOCK_DGRAM`↔UDP |
| Works on Linux, fails on BSD | Linux-only option | Gate `epoll`/`SO_*` behind `#ifdef` |
| Can’t find peer via Unix socket | Path / permissions | Same FS path; check directory execute bits |

## Gotchas

> [!WARNING]
> **API ≠ complete stack** — sockets need a transport (TCP/UDP) and routing; the API alone sends nothing.

> [!WARNING]
> **“BSD sockets” in embedded docs** — often means “Berkeley-style API”, not that you run FreeBSD.

> [!WARNING]
> **Client/server is a pattern, not a hard rule of the API** — UDP and some IPC designs are peer-to-peer with the same calls.

## When NOT to use

- **New application protocols in C sockets by default** — use mature libraries (TLS, HTTP/2, QUIC) unless you must own bytes.
- **Confusing BSD-the-OS hardening docs with the socket API** — OpenBSD ≠ `socket(2)` man page on Linux.
- **Teaching only “mandatory client/server”** — datagram and Unix sockets break that mental trap.

## Related

[[Networking]] [[POSIX Socket]] [[TCP]] [[UDP]] [[Inter Process Communication]] [[address port]]
