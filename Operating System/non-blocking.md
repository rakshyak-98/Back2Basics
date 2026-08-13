[[Operating System]] [[Blocking]] [[Blocking Vs Non-Blocking]] [[Epoll]] [[system call]]

# Non-blocking

> Non-blocking I/O returns immediately when data is not ready — the caller must retry or wait via an event multiplexer instead of sleeping inside the kernel.

Set with `fcntl(O_NONBLOCK)` on [[file descriptors]]. `read()` / `write()` / `accept()` fail with **`EAGAIN`** or **`EWOULDBLOCK`** until the fd is ready.

## Event-driven pattern

```txt
epoll_wait(fds ready) → read/write each ready fd → repeat
```

Pairs with [[Epoll]], `kqueue`, or `io_uring` for many connections and few [[Thread]]s.

Contrast [[Blocking]] simplicity — choose using [[Blocking Vs Non-Blocking]] criteria.

## Sources

- Kerrisk, *The Linux Programming Interface*
- Linux `fcntl(2)`, `epoll(7)` manual pages
