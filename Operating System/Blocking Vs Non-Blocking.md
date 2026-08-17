[[Operating System]] [[Blocking]] [[non-blocking]] [[Epoll]] [[system call]] [[CPU IO Bound Task]] [[Thread]] [[thread pool]]

# Blocking Vs Non-Blocking

> Blocking waits inside the kernel until I/O is ready; non-blocking returns immediately and pushes the wait into your event loop — choose by concurrency shape, not ideology.





## Interview Relevance
A classic systems interview fork: walk both models, name `EAGAIN` / `epoll`, and pick a hybrid (non-blocking accept + blocking worker pool) for a concrete service.

## Sources
- Kerrisk, *The Linux Programming Interface* — non-blocking I/O, `select`, `poll`, `epoll` — deep-dive
- Linux `fcntl(2)`, `epoll(7)` manual pages — deep-dive
- [Wikipedia — C10k problem](https://en.wikipedia.org/wiki/C10k_problem) — overview

## Key Concepts
- **Mode is an fd property:** blocking vs non-blocking is how the descriptor is configured, plus how threads use it — not a different network stack.
- **Scalability lever:** blocking ≈ one thread per wait; non-blocking ≈ few threads + readiness ([[Epoll]] / kqueue).
- **Hybrid is normal:** event loop for sockets; [[thread pool]] for blocking disk/DB.

## Technical Details
| Aspect | Blocking | Non-blocking |
|--------|----------|--------------|
| Call behavior | Thread sleeps until ready | Returns `EAGAIN` / `EWOULDBLOCK` if not ready |
| Code style | Linear, one thread per flow | State machine or callback / async |
| Scalability | Thread count ≈ concurrent waits | Few threads + [[Epoll]] / kqueue |
| Latency under load | Scheduler and stack overhead | Lower thread overhead; complex app logic |
| Error handling | Simple return codes | Must retry on `EINTR` and `EAGAIN` |

```txt
Blocking model:
  Thread 1 ── accept ── read ── write ── close
  Thread 2 ── accept ── read ── write ── close
  (N threads for N idle clients)

Non-blocking model:
  Event loop ── epoll_wait ── dispatch read/write on ready fds
  (few threads, many connections)
```

```c
int flags = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, flags | O_NONBLOCK);
```

## Real-World Applications
Node.js and Go multiplex many logical tasks onto fewer OS threads — know which layer still blocks ([[CPU IO Bound Task]]). Nginx / Envoy style reactors keep the hot path non-blocking.

## Pros/Cons or Trade-offs
- **Blocking pro:** easiest correctness for sequential protocols.
- **Blocking con:** poor fit for tens of thousands of idle connections.
- **Non-blocking pro:** high connection density on few cores.
- **Non-blocking con:** state machines, partial reads, and careful `EAGAIN` handling.

## Comparison
- Detail on sleep-until-ready: [[Blocking]].
- Detail on immediate return + reactor: [[non-blocking]].
- Bound-type sizing: [[CPU IO Bound Task]].

## Mistakes to Avoid
- Treating “non-blocking” as “faster for one request” — it mainly helps concurrency, not single-op latency.
- Setting `O_NONBLOCK` then spinning without `epoll_wait` / `poll`.
- Mixing blocking disk calls on the same thread that must serve many sockets.
