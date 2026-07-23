[[Linux]] [[process]] [[ss]] [[half-open connections]]

# epoll

> One-line: Linux’s **scalable FD readiness notification** — O(1) wait on thousands of sockets instead of scanning all FDs every wake. **Stevens / Kerrisk.**

## Mental model

`select` / `poll`: every wake, kernel scans **all** watched FDs → O(n).

`epoll`: register FDs once (`epoll_ctl ADD`); `epoll_wait` returns **only ready FDs** → O(ready).

```
                    epoll_create1
                          │
    socket FDs ──► epoll_ctl(ADD, events) ──► epoll kernel wait queue
                          │
              epoll_wait ─┴─► [fd3 readable, fd7 writable, …]
                          │
                   app read/write on ready FDs only
```

| API | Scale | FD limit | Typical stack |
|-----|-------|----------|---------------|
| `select` | O(n) scan | `FD_SETSIZE` (~1024) | legacy, portable |
| `poll` | O(n) scan | ulimit | portable middle ground |
| `epoll` | O(ready) | millions (mem bound) | nginx, Node libuv, Go netpoller |

**Who uses it:** nginx worker, Node.js (libuv `uv__io_poll`), Go runtime netpoller, Redis, most Linux-native async servers. They all share the same contract: **non-blocking sockets + epoll edge/level trigger + careful accept/read loops.**

## Standard config / commands

Operators rarely tune epoll directly — you debug **misuse** in apps and proxies.

```bash
# How many FDs can this process open? (epoll watches FDs, not separate limit)
ulimit -n
cat /proc/<pid>/limits | grep "open files"

# Count open sockets for a service
ls /proc/<pid>/fd | wc -l
ss -tp | grep <pid>

# Rare but decisive: see epoll_wait behavior under load
strace -f -e epoll_wait,epoll_ctl,poll,read,write -p <pid> 2>&1 | head -200
# Expect: epoll_wait blocks → returns N ready → read/write loops → epoll_wait again
# Bad: epoll_wait returns → no read → immediate epoll_wait (spin or missed edge)
```

**Trigger modes (the part that breaks prod):**

| Mode | Behavior | Correct usage |
|------|----------|-----------------|
| **Level (default)** | Ready as long as condition true (data in buffer) | Safer; may wake repeatedly until drained |
| **Edge (`EPOLLET`)** | Notify only on **transition** (idle→ready) | Must **drain to EAGAIN** on every wake; nginx default |

```c
// Edge-triggered contract (pseudocode)
while (true) {
    n = epoll_wait(...);
    for each ready fd:
        while ((r = read(fd, buf, sizeof buf)) > 0) { handle(r); }
        if (r == -1 && errno == EAGAIN) break;  // fully drained
}
```

**Useful flags:**

| Flag | Effect |
|------|--------|
| `EPOLLONESHOT` | One event per `epoll_ctl` re-arm — serializes FD handling across threads (nginx multi-accept patterns) |
| `EPOLLEXCLUSIVE` | Wake one epoll set member on accept thundering herd (Linux 4.5+, listen sockets) |
| `EPOLLRDHUP` | Peer closed write half — detect half-close without read returning 0 yet |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CPU spin at idle, one core hot | `strace -c -p <pid>` → high `epoll_wait` + `read` EAGAIN loop | Edge trigger without drain; or busy-loop on accept |
| Connections stall under load | `ss -ti` Recv-Q/Send-Q; `ss -s` | Event loop blocked on sync work — offload to thread pool |
| Accept storm melts workers | `ss -s`; nginx `worker_connections` | `EPOLLEXCLUSIVE` on listen fd; SO_REUSEPORT; more workers |
| Mystery hung clients | `ss -o state established '( timer=(keepalive))'` | App not reading → kernel recv buffer full → backpressure |
| `EMFILE` / too many open files | `ulimit -n`; `lsof -p <pid> \| wc -l` | Raise limit in systemd `LimitNOFILE`; fix FD leak |
| Half-open / RST after idle LB timeout | [[half-open connections]]; tcpdump FIN/RST | Enable TCP keepalive or app heartbeat; align LB idle timeout |

**Thundering herd:** many threads blocked in `epoll_wait` on the **same listen FD**; one incoming connection wakes **all** → wasted context switches. Fixes: `EPOLLEXCLUSIVE`, single acceptor thread, or `SO_REUSEPORT` with per-process listen sockets.

**Connection to runtimes:**

- **nginx:** edge-triggered; `worker_connections` caps registered FDs; `multi_accept on` batches accepts.
- **Node:** libuv epoll backend; one thread runs the loop — blocking the loop blocks all I/O (don’t sync CPU on hot path).
- **Go:** netpoller in separate threads; goroutines block on net without blocking OS thread — still epoll under the hood on Linux.

## Gotchas

> [!WARNING]
> **Edge trigger + partial read = silent stall.** If you read once and stop while data remains, you may never get another edge until new data arrives.

> [!WARNING]
> **Level trigger + slow consumer = repeated wakes.** Not wrong, but can inflate CPU if you don’t drain aggressively.

- **`EPOLLHUP` on write side:** peer gone; many apps forget to close and leak FDs.
- **LT + EPOLLONESHOT confusion:** ONESHOT disables until re-arm — combine deliberately, not by copy-paste.
- **strace volume:** full `-e epoll_wait` on high-QPS prod can itself distort timing — use short captures or `strace -c` aggregates.

## When NOT to use

- **Cross-platform abstraction layer** — use libuv / asio / Go net; they pick epoll/kqueue/IOCP.
- **File I/O readiness on Linux** — epoll works on pipes/sockets/timers; for **disk files** prefer thread pool + blocking I/O or `io_uring`.
- **“Fix” TCP churn with epoll tuning** — [[connection chrun]] is keepalive/LB/TIME_WAIT policy, not epoll flags.

## Related

[[ss]] [[half-open connections]] [[connection chrun]] [[process]] [[Linux network commands]]
