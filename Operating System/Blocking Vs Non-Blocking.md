[[Blocking]] [[non-blocking]] [[Event Loop]] [[libuv]] [[Callback]] [[context switching]]

# Blocking vs Non-Blocking

> Two axes engineers conflate: **thread blocking** (scheduler) vs **I/O readiness** (fd returns `EAGAIN`) — **Node docs + Stevens**.

---

## Mental model

| Term | Meaning | Who waits |
|------|---------|-----------|
| **Blocking I/O** | Syscall doesn't return until data ready / buffer space | Thread sleeps → [[context switching]] |
| **Non-blocking I/O** | Syscall returns immediately; may get `EAGAIN` | Thread continues → poll/epoll [[non-blocking]] |
| **Blocking API (JS)** | Callback/promise not invoked until operation completes | Event loop free for other work |
| **Sync API (JS)** | Entire **main thread** stuck until syscall returns | Starves [[Event Loop]] |

```txt
Blocking thread model:     [Thread]──read(block)──sleep──►wake──►work
Non-blocking + reactor:    [Event loop]──read(EAGAIN)──epoll──►read──►work
                           (few threads, many connections)
```

**Node canonical rule:** only the main JavaScript thread must never do **long blocking** work (sync fs, `bcrypt` sync, huge JSON parse). libuv hides **non-blocking** network/disk behind a thread pool for some ops.

**Go:** goroutine blocking on `conn.Read` blocks an OS thread from the pool — cheap until GOMAXPROCS threads all block.

**Java:** thread-per-request **blocking** servlets vs Netty **non-blocking** — thread count vs complexity tradeoff.

---

## Decision table

| Workload | Prefer | Why |
|----------|--------|-----|
| High fan-in HTTP/WebSocket | Non-blocking + event loop | Few [[file descriptors]] threads, many conns |
| CRUD API moderate QPS | Blocking + thread pool | Simpler code; pool size tuned to cores |
| Disk-heavy batch ETL | Blocking threads or async IO | Throughput over latency |
| CPU-bound (hash, ML) | Worker threads/processes | I/O model irrelevant — avoid blocking event loop |
| Postgres client | Blocking JDBC common | Pool limits connections; pgbouncer |

---

## Standard config / commands

### Spot blocking on event-loop runtimes

```shell
# Node: event loop delay (built-in or clinic.js)
node --trace-sync-io server.js    # warns on sync I/O

# strace: long blocking read on main thread PID
strace -p PID -e read,write,fsync -T

# Go: goroutine dump if all threads blocked
curl localhost:6060/debug/pprof/goroutine?debug=2

# Java: thread dump
jcmd PID Thread.print | grep -A5 BLOCKED
```

### Move from blocking to non-blocking (patterns)

**Node:** `fs.readFile` → `fs.promises.readFile`; never `fs.readFileSync` in request path. CPU work → `worker_threads`.

**Go:** `net/http` is goroutine-per-connection (blocking reads) — fine at moderate scale; switch to `netpoll` tuning or fewer handlers if thread count explodes.

**Java:** Tomcat `maxThreads` caps blocking workers; reactive stack (WebFlux) for non-blocking end-to-end **only if** DB/driver also async.

See [[non-blocking]] for `fcntl O_NONBLOCK`, epoll, and `EAGAIN` handling.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Node API freezes under load | sync fs/crypto; CPU on main thread | Remove sync APIs; offload workers |
| Timeouts cascade | thread pool exhausted (Java/Go) | Pool size; circuit breakers; faster downstream |
| Low CPU, requests queue | blocked on external I/O | Timeouts; async client; non-blocking [[non-blocking]] |
| p99 fine, p999 awful | occasional sync path | `--trace-sync-io`; audit deps |
| Works in dev, stalls prod | larger files / slower disk | Don't sync read logs on request path |
| "Non-blocking" still slow | thread pool saturation (libuv) | UV_THREADPOOL_SIZE; separate disk ops |

---

## Gotchas

> [!WARNING]
> **Async API ≠ non-blocking I/O.** Some "async" DB drivers block a thread pool thread — end-to-end latency still tied to pool size.

> [!WARNING]
> **libuv thread pool** — `fs` operations and DNS often block **worker threads**, not the main loop — default pool size 4.

> [!WARNING]
> **Blocking in callback** blocks the event loop even after non-blocking I/O delivered data.

> [!WARNING]
> **False comfort from `setImmediate`** — doesn't parallelize CPU; still one JS thread.

> [!WARNING]
> **Mixed model deadlocks** — async code calling sync wrapper that waits on future — classic Java/Python/Node bridge bugs.

---

## When NOT to use

- Don't rewrite blocking CRUD app to epoll for ideology — measure connection count and team expertise.
- Don't use non-blocking disk patterns without [[fsync]] / durability design for stateful writes.

---

## Related

[[non-blocking]] [[Blocking]] [[Event Loop]] [[libuv]] [[Callback]] [[thread pool]] [[context switching]] [[file descriptors]] [[CPU IO Bound Task]]
