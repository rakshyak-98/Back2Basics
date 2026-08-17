[[process]] [[Linux Process Theory]] [[eBPF]]

# Epoll

> `epoll` is Linux's scalable I/O readiness API — one thread can watch thousands of sockets without scanning every file descriptor each wait.





## Interview Relevance
Backend / systems staple: contrast `select`/`poll` O(n) scans with `epoll`'s O(ready) waits, explain edge-triggered vs level-triggered, and name who uses it (Nginx, Node/libuv, Redis).

## Sources
- `man 7 epoll` — deep-dive
- [epoll(7) — man7.org](https://man7.org/linux/man-pages/man7/epoll.7.html) — deep-dive

## Core Definition
The `epoll` family (`epoll_create1`, `epoll_ctl`, `epoll_wait`) registers many file descriptors on one **epoll instance**. The kernel returns only descriptors that became ready — not a full walk of every watched fd.

## Key Concepts
- **epoll instance:** Interest set you add/mod/delete with `epoll_ctl`.
- **Level-triggered (default):** Keep reporting while the condition remains true.
- **Edge-triggered (`EPOLLET`):** Notify on state change — you must drain the fd.
- **EPOLLONESHOT:** Disable after one event until re-armed.
- **Scales readiness, not fd limits:** `ulimit -n` still caps open files.

## Technical Details
```
epoll instance
  ├─ fd: socket A  (EPOLLIN)
  ├─ fd: socket B  (EPOLLOUT | EPOLLET)
  └─ fd: timerfd
         │
         ▼
   epoll_wait() ──► ready fd list ──► handler
```

| Flag | Meaning |
|------|---------|
| `EPOLLIN` | Readable |
| `EPOLLOUT` | Writable |
| `EPOLLET` | Edge-triggered — drain after event |
| `EPOLLONESHOT` | One shot until re-armed |

```c
int epfd = epoll_create1(0);
struct epoll_event ev = { .events = EPOLLIN, .data.fd = sock };
epoll_ctl(epfd, EPOLL_CTL_ADD, sock, &ev);

struct epoll_event events[64];
int n = epoll_wait(epfd, events, 64, -1);
for (int i = 0; i < n; i++)
    handle(events[i].data.fd);
```

Nginx, Node.js (libuv), Redis, and systemd use epoll (or newer io_uring) under the hood.

| Symptom | Check |
|---------|-------|
| CPU spin on idle server | Edge-triggered without full read — drain or use level |
| Missed connections | `somaxconn`; accept loop not registered |
| High latency under load | `strace -e epoll_wait`; compare with `ss -s` |

## Real-World Applications
A reverse proxy accepts tens of thousands of keep-alive clients on a few worker threads because each worker’s event loop is epoll-based, not `select`.

## Pros/Cons or Trade-offs
- **Pro:** Scales to huge connection counts with constant-time waits on active events.
- **Con:** Edge-triggered bugs are subtle; incorrect draining causes spins or stalled clients. Portability differs (`kqueue` on BSD, IOCP on Windows).

## Comparison
vs `select`/`poll`: those rescan the whole set each call; epoll does not. vs io_uring: newer async submission/completion model that can reduce syscalls further. vs [[eBPF]]: epoll is userspace readiness; eBPF observes inside the kernel.

## Mistakes to Avoid
- Using `EPOLLET` without non-blocking I/O and a drain-until-EAGAIN loop.
- Assuming epoll raises `ulimit -n` automatically.
- Confusing “socket in epoll” with “connection accepted” — you still need an accept loop on the listen fd.
