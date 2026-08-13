[[process]] [[Linux Process Theory]] [[eBPF]]

# Epoll

> `epoll` is Linux's edge-triggered / level-triggered readiness notification API — the scalable replacement for `select`/`poll` when one thread must watch thousands of sockets.

The `epoll` family (`epoll_create1`, `epoll_ctl`, `epoll_wait`) lets a process register many file descriptors on one **epoll instance**. The kernel returns only descriptors that became readable/writable since the last wait — O(active events) instead of O(total fds).

## Mental picture

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
| `EPOLLET` | Edge-triggered — must drain fd after event |
| `EPOLLONESHOT` | Disable after one event until re-armed |

## Minimal C-shaped pseudocode

```c
int epfd = epoll_create1(0);
struct epoll_event ev = { .events = EPOLLIN, .data.fd = sock };
epoll_ctl(epfd, EPOLL_CTL_ADD, sock, &ev);

struct epoll_event events[64];
int n = epoll_wait(epfd, events, 64, -1);
for (int i = 0; i < n; i++)
    handle(events[i].data.fd);
```

## Operator relevance

You rarely call `epoll` directly unless writing high-performance servers. You *do* see its effects when tuning:

- **Nginx**, **Node.js** (libuv), **Redis**, **systemd** use epoll (or io_uring on newer stacks).
- `ulimit -n` (open files) still matters — epoll scales readiness, not fd table size.

## Debugging event-loop stalls

| Symptom | Check |
|---------|-------|
| CPU spin on idle server | Edge-triggered without full read — switch to level or drain buffer |
| Missed connections | `somaxconn`, accept loop not registered |
| High latency under load | `strace -e epoll_wait` on process; compare with `ss -s` |

## Related

[[process]] · [[Linux Process Theory]] · [[eBPF]]

## Sources

- `man 7 epoll`
- [epoll(7) — man7.org](https://man7.org/linux/man-pages/man7/epoll.7.html)
