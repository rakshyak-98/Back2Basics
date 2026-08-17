[[Operating System]] [[Blocking]] [[Blocking Vs Non-Blocking]] [[Epoll]] [[system call]] [[file descriptors]] [[Thread]]

# Non-blocking

> Non-blocking I/O returns immediately when data is not ready — retry or wait via an event multiplexer instead of sleeping inside the kernel.





## Interview Relevance
`O_NONBLOCK` + `EAGAIN` + `epoll_wait` loop; when it beats thread-per-connection.

## Sources
- Kerrisk, *The Linux Programming Interface* — deep-dive
- Linux `fcntl(2)`, `epoll(7)` manual pages — deep-dive

## Key Concepts
- **Immediate return:** `EAGAIN` / `EWOULDBLOCK` if not ready.
- **Set via:** `fcntl(O_NONBLOCK)` on [[file descriptors]].
- **Multiplex:** [[Epoll]] / kqueue / `io_uring`.
- **Few threads:** many connections without one [[Thread]] per wait.

## Technical Details
```txt
epoll_wait(fds ready) → read/write each ready fd → repeat
```

Contrast [[Blocking]] simplicity — decision criteria in [[Blocking Vs Non-Blocking]].

## Real-World Applications
Nginx/Envoy-style proxies, Node event loop, and Go netpoller under the hood.

## Pros/Cons or Trade-offs
- **Pro:** High connection density; low thread overhead.
- **Con:** State machines; partial reads; careful retries.
- **Trade-off:** complexity vs scalability.

## Comparison
- vs [[Blocking]]: sleep in kernel vs return + reactor.
- vs async/await: language sugar over the same readiness model.

## Mistakes to Avoid
- Busy-spinning on `EAGAIN` without waiting for readiness.
- Mixing blocking disk calls on the event-loop thread.
- Ignoring `EINTR` and short writes.
