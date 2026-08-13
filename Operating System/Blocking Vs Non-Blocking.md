[[Operating System]] [[Blocking]] [[non-blocking]] [[Epoll]] [[system call]] [[CPU IO Bound Task]]

# Blocking Vs Non-Blocking

> Blocking waits inside the kernel until I/O is ready; non-blocking returns immediately and pushes the wait into your event loop — choose based on concurrency shape, not ideology.

Both modes are properties of **how a file descriptor (or socket) is configured**, combined with how the [[Thread]] model uses them. They are not separate “kinds” of network stack.

## Comparison

| Aspect | Blocking | Non-blocking |
|--------|----------|--------------|
| Call behavior | Thread sleeps until ready | Returns `EAGAIN` / `EWOULDBLOCK` if not ready |
| Code style | Linear, one thread per flow | State machine or callback / async |
| Scalability | Thread count ≈ concurrent waits | Few threads + [[Epoll]] / kqueue |
| Latency under load | Scheduler and stack overhead | Lower thread overhead; complex app logic |
| Error handling | Simple return codes | Must retry on `EINTR` and `EAGAIN` |

## Typical architectures

```txt
Blocking model:
  Thread 1 ── accept ── read ── write ── close
  Thread 2 ── accept ── read ── write ── close
  (N threads for N idle clients)

Non-blocking model:
  Event loop ── epoll_wait ── dispatch read/write on ready fds
  (few threads, many connections)
```

## Hybrid patterns

Thread pools handle **blocking** disk or database calls while the accept loop stays non-blocking. Runtimes (Node.js, Go) multiplex many logical tasks onto fewer OS threads — know which layer is blocking ([[CPU IO Bound Task]]).

Setting non-blocking mode:

```c
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);
```

## Sources

- Kerrisk, *The Linux Programming Interface* — non-blocking I/O, `select`, `poll`, `epoll`
- Linux `fcntl(2)`, `epoll(7)` manual pages
- Wikipedia: [C10k problem](https://en.wikipedia.org/wiki/C10k_problem)
