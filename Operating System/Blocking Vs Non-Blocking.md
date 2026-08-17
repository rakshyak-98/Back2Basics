[[Operating System]] [[Blocking]] [[Epoll]] [[system call]] [[CPU IO Bound Task]] [[Thread]] [[thread pool]] [[file descriptors]]

# Blocking Vs Non-Blocking

> Blocking I/O suspends the calling thread inside the kernel until data is ready; non-blocking I/O returns immediately with `EAGAIN` and delegates waiting to an event multiplexer like epoll — choose based on concurrency shape, not ideology.

---

## Why It Matters

This is a foundational systems interview and architecture question. A blocking HTTP server with one thread per connection works until you have thousands of idle keep-alive connections — then thread stacks and scheduler overhead dominate. A non-blocking server with epoll handles many connections on few threads but demands state machines for partial reads and writes. Production systems are hybrid: event loop for network I/O, thread pool for blocking disk and database calls.

---

## Sources

- Kerrisk, *The Linux Programming Interface* — Definitive treatment of non-blocking I/O, `select`, `poll`, `epoll`, and signal-driven I/O in Chapters 44 and 63.
- [fcntl(2) — Linux manual page](https://man7.org/linux/man-pages/man2/fcntl.2.html) — How to set `O_NONBLOCK` on a file descriptor and what errors to expect.
- [epoll(7) — Linux manual page](https://man7.org/linux/man-pages/man7/epoll.7.html) — Edge-triggered vs level-triggered epoll semantics and scalability properties.
- [Wikipedia — C10k problem](https://en.wikipedia.org/wiki/C10k_problem) — Historical context for why event-driven servers replaced thread-per-connection models.

---

## Key Concepts

| Aspect | Blocking | Non-blocking |
|--------|----------|--------------|
| Call behavior | Thread sleeps in kernel until ready | Returns immediately; `EAGAIN` if not ready |
| Code style | Linear, one thread per flow | State machine, callback, or async/await |
| Scalability | Thread count ≈ concurrent waits | Few threads + epoll/kqueue/io_uring |
| Latency under load | Scheduler and stack overhead grows | Lower thread overhead; complex app logic |
| Error handling | Simple return codes | Must retry on `EINTR` and `EAGAIN` |

### Blocking model

```txt
Thread 1 ── accept() ── read() ── write() ── close()
Thread 2 ── accept() ── read() ── write() ── close()
(N threads for N concurrent idle connections)
```

Each blocked thread consumes stack memory (~8 MB default on Linux) and a scheduler slot.

### Non-blocking model

```txt
Event loop:
  epoll_wait() → dispatch read/write on ready fds → repeat
(Few threads, many connections)
```

The application must handle partial reads (`read` returns fewer bytes than requested), partial writes, and `EAGAIN` by registering interest with epoll and trying again when the fd becomes ready.

### Setting non-blocking mode

```c
#include <fcntl.h>
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);
```

After this, `read()`, `write()`, `accept()`, and `connect()` return `-1` with `errno == EAGAIN` or `EWOULDBLOCK` when the operation would block.

### Event multiplexers

| API | Scalability | Notes |
|-----|-------------|-------|
| `select` / `poll` | O(n) per call | Fine for dozens of fds; degrades with thousands |
| `epoll` (Linux) | O(ready) | Default for Nginx, Node.js libuv, Go netpoller |
| `kqueue` (BSD/macOS) | O(ready) | Same role as epoll on Apple platforms |
| `io_uring` (Linux 5.1+) | Batch submission | Emerging; reduces syscall overhead further |

### Hybrid pattern (production norm)

```txt
Main thread:  epoll loop for TCP sockets (non-blocking)
Worker pool:  blocking PostgreSQL queries, disk I/O, CPU work
```

Never run blocking disk or database calls on the same thread that must accept thousands of connections.

---

## Technical Details

### Minimal epoll read loop (conceptual)

```c
int epfd = epoll_create1(0);
struct epoll_event ev = { .events = EPOLLIN, .data.fd = listen_fd };
epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);

while (1) {
    struct epoll_event events[MAX_EVENTS];
    int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (int i = 0; i < n; i++) {
        if (events[i].events & EPOLLIN) {
            ssize_t nread = read(events[i].data.fd, buf, sizeof buf);
            if (nread == -1 && errno == EAGAIN) continue;
            // handle data or connection close
        }
    }
}
```

### Language/runtime mapping

| Runtime | Model |
|---------|-------|
| Node.js | libuv epoll/kqueue + thread pool for blocking fs/crypto |
| Go | netpoller (epoll/kqueue) + goroutines — blocking syscalls in goroutines |
| Nginx | epoll edge-triggered + worker processes |
| Java NIO | `Selector` over epoll/kqueue |
| Rust Tokio | async/await over mio (epoll/kqueue) |

`async/await` in high-level languages is syntactic sugar over the same readiness model — the runtime still waits for `EPOLLIN`/`EPOLLOUT` under the hood.

---

## Mistakes to Avoid

- Treating "non-blocking" as "faster for a single request" — overhead is in concurrency, not single-request latency.
- Setting `O_NONBLOCK` then busy-spinning on `EAGAIN` without `epoll_wait` — burns CPU.
- Mixing blocking disk calls on the event-loop thread — stalls all connections.
- Ignoring `EINTR` — syscalls interrupted by signals must be retried.
- Ignoring short writes — `write()` may accept only part of the buffer; track offset and retry.
- Edge-triggered epoll without draining the fd completely — misses events until next edge.

---

## Pros/Cons or Trade-offs

| Model | Pro | Con |
|-------|-----|-----|
| Blocking | Easiest correctness; linear code | Poor fit for 10k+ idle connections |
| Non-blocking | High connection density on few cores | State machines; partial I/O; harder debugging |
| Hybrid | Practical production balance | Two concurrency models to reason about |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[Blocking]] | Deep dive on sleep-until-ready syscall behavior |
| [[Epoll]] | Linux-specific multiplexer implementation details |
| [[CPU IO Bound Task]] | Whether work is CPU- or I/O-bound drives thread count |
| async/await (JavaScript, Rust) | Language sugar over readiness polling |

---

## Use cases

- Nginx/Envoy reverse proxy: non-blocking sockets + epoll for millions of idle keep-alive connections.
- Node.js HTTP server: single-threaded event loop for I/O; `worker_threads` for CPU-heavy work.
- Traditional blocking JDBC in a servlet container: thread-per-request — simple but needs large thread pools at scale.
