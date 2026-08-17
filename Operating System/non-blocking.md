[[Operating System]] [[Blocking]] [[Blocking Vs Non-Blocking]] [[Epoll]] [[system call]] [[file descriptors]] [[Thread]]

# Non-blocking

> Non-blocking I/O returns immediately when data is not ready — retry or wait via an event multiplexer instead of sleeping inside the kernel.

```txt
        Non-blocking ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** `O_NONBLOCK` + `EAGAIN` + `epoll_wait` loop

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

- Contrast [[Blocking]] simplicity

## Mistakes to Avoid
- **Mistake:** Busy-spinning on `EAGAIN` without waiting for readiness
- **Mistake:** Mixing blocking disk calls on the event-loop thread
- **Mistake:** Ignoring `EINTR` and short writes

## Pros/Cons or Trade-offs
- **Pro:** High connection density; low thread overhead.
- **Con:** State machines; partial reads; careful retries.
- **Trade-off:** complexity vs scalability.

## Comparison
- vs [[Blocking]]: sleep in kernel vs return + reactor.
- vs async/await: language sugar over the same readiness model.


### Use cases
- Nginx/Envoy-style proxies, Node event loop, and Go netpoller under the hood.
