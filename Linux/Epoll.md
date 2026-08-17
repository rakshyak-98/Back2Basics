[[process]] [[Linux Process Theory]] [[eBPF]]

# Epoll

> `epoll` is Linux's scalable I/O readiness API — one thread can watch thousands of sockets without scanning every file descriptor each wait.

```txt
        Epoll ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Backend / systems staple: contrast `select`/`poll` O(n) scans with `epoll`'s …

## Sources
- `man 7 epoll` — deep-dive
- [epoll(7) — man7.org](https://man7.org/linux/man-pages/man7/epoll.7.html) — deep-dive

## Key Concepts
- **epoll instance:** Interest set you add/mod/delete with `epoll_ctl`.
- **Level-triggered (default):** Keep reporting while the condition remains true.
- **Edge-triggered (`EPOLLET`):** Notify on state change — you must drain the fd.
- **EPOLLONESHOT:** Disable after one event until re-armed.
- **Scales readiness, not fd limits:** `ulimit -n` still caps open files.


- **Core:** The `epoll` family (`epoll_create1`, `epoll_ctl`, `epoll_wait`) registers man…

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

- Nginx, Node.js (libuv), Redis, and systemd use epoll (or newer io_uring) unde…

| Symptom | Check |
|---------|-------|
| CPU spin on idle server | Edge-triggered without full read — drain or use level |
| Missed connections | `somaxconn`; accept loop not registered |
| High latency under load | `strace -e epoll_wait`; compare with `ss -s` |

## Mistakes to Avoid
- **Mistake:** Using `EPOLLET` without non-blocking I/O and a drain-until-EAGAI…
- **Mistake:** Assuming epoll raises `ulimit -n` automatically
- **Mistake:** Confusing “socket in epoll” with “connection accepted”

## Pros/Cons or Trade-offs
- **Pro:** Scales to huge connection counts with constant-time waits on active events.
- **Con:** Edge-triggered bugs are subtle; incorrect draining causes spins or stalled clients. Portability differs (`kqueue` on BSD, IOCP on Windows).

## Comparison
- vs `select`/`poll`: those rescan the whole set each call


### Use cases
- A reverse proxy accepts tens of thousands of keep-alive clients on a few work…
