[[Nginx/Nginx internals]] [[Nginx/Configuration]] [[Operating System/kernel subsystem]] [[compiler/library file]]

# File structure (NGINX source layout)

> How NGINX organizes its C source tree — where event I/O, core utilities, and modules live — **NGINX internals + reading upstream source under incident pressure**.

## Mental model

NGINX is modular C. The **core** owns memory pools, strings, and config parsing; the **event** layer wraps epoll/kqueue and drives the worker loop; **HTTP/stream modules** plug into that loop.

```
nginx/
├── src/core/       ← ngx_pool, ngx_string, ngx_conf — shared primitives
├── src/event/      ← epoll/kqueue, timers, accept — non-blocking I/O hub
├── src/http/       ← HTTP parser, upstream, proxy, gzip modules
├── src/stream/     ← TCP/UDP proxy (stream {} block)
├── src/os/unix/    ← platform syscalls, sendfile, aio
└── objs/           ← build artifacts after ./configure && make
```

Request path (simplified):

```
accept (event/) → parse HTTP (http/) → upstream (http/) → write (event/)
         ↑________________ core/ alloc + logging ________________|
```

## Standard config / commands

### Build from source (inspect structure locally)

```bash
git clone https://github.com/nginx/nginx.git
cd nginx
./auto/configure --with-debug --with-http_ssl_module
make -j$(nproc)

# Find where a symbol is defined
rg -l "ngx_event_process" src/
rg "ngx_http_upstream" src/http/
```

### Key directories (what to open when debugging)

| Path | Responsibility |
|------|----------------|
| `src/core/ngx_cycle.c` | Master/worker lifecycle, config reload |
| `src/event/ngx_event.c` | Event loop, connection accept |
| `src/http/ngx_http_request.c` | Request state machine |
| `src/http/modules/` | Built-in modules (proxy, gzip, ssl) |
| `src/os/unix/ngx_process_cycle.c` | fork workers, signal handling |

### Custom module placement

Third-party modules typically live under `modules/` or are compiled via `--add-module=` pointing at your module's `config` script — same hook points as built-ins under `src/http/modules/`.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Segfault after module upgrade | Module compiled against wrong NGINX version | Rebuild module against running `nginx -V` headers |
| Worker spins at 100% CPU | `event/` loop stuck in tight read | Enable `--with-debug`; trace `ngx_event_process_events` |
| Reload drops connections | `core/` cycle vs old workers | Expected brief overlap; check `worker_shutdown_timeout` |
| Can't find symbol at link time | Wrong `objs/ngx_modules.c` | Clean `make clean` + reconfigure |

## Gotchas

> [!WARNING]
> NGINX **never** blocks the worker on disk I/O in the hot path — if your custom module calls synchronous `read()` on large files inside the event callback, you stall every connection on that worker.

- **Master vs worker:** only workers run the event loop; master handles signals and re-exec — don't debug worker bugs in master code paths.
- **Memory:** almost everything uses `ngx_pool_t` from `core/` — freeing individual allocations is rare; pool destroy at request end.
- **Version skew:** distro packages (`nginx-extras`) may patch paths — always match headers to the binary you run.

## When NOT to use

- You only need runtime behavior — read [[Nginx/Configuration]] and `nginx -T`, not the full source tree.
- Application-level folder layout (React `src/components`) — different topic; this note is NGINX C source structure.

## Related

[[Nginx/Nginx internals]] [[Nginx/Configuration]] [[Linux/Epoll]] [[Operating System/kernel subsystem]]
