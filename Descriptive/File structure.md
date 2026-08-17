[[Nginx/Nginx internals]] [[Nginx/Configuration]] [[Operating System/kernel subsystem]] [[compiler/library file]] [[Linux/Epoll]]

# File structure (NGINX source layout)

> File structure (NGINX source layout) — ├── src/core/ ← ngx_pool, ngx_string, ngx_conf — shared primitives

```txt
        File structure (NG ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Project structure questions check modularity and discoverability

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** NGINX is modular C. The **core** owns memory pools, strings, and configuratio…

```
nginx/
- **Note:** ├── src/core/ ← ngx_pool, ngx_string, ngx_conf — shared primitives
- **Note:** ├── src/event/ ← epoll/kqueue, timers, accept — non-blocking I/O hub
- **Note:** ├── src/http/ ← HTTP parser, upstream, proxy, gzip modules
├── src/stream/     ← TCP/UDP proxy (stream {} block)
├── src/os/unix/    ← platform syscalls, sendfile, aio
- **Note:** └── objs/ ← build artifacts after ./configure && make
```

Request path (simplified):

```
- **Note:** accept (event/) → parse HTTP (http/) → upstream (http/) → write (event/)
         ↑________________ core/ alloc + logging ________________|
```

## Technical Details
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

- Third-party modules typically live under `modules/` or are compiled via `--ad…

## Mistakes to Avoid
> [!WARNING]
> NGINX **never** blocks the worker on disk I/O in the hot path — if your custom module calls synchronous `read()` on large files inside the event callback, you stall every connection on that worker.

- **Mistake:** **Master versus worker:** only workers run the event loop
- **Mistake:** **Memory:** almost everything uses `ngx_pool_t` from `core/`
- **Mistake:** **Version skew:** distro packages (`nginx-extras`) may patch pat…

| Symptom | Check | Fix |
|---------|-------|-----|
| Segfault after module upgrade | Module compiled against wrong NGINX version | Rebuild module against running `nginx -V` headers |
| Worker spins at 100% CPU | `event/` loop stuck in tight read | Enable `--with-debug`; trace `ngx_event_process_events` |
| Reload drops connections | `core/` cycle vs old workers | Expected brief overlap; check `worker_shutdown_timeout` |
| Can't find symbol at link time | Wrong `objs/ngx_modules.c` | Clean `make clean` + reconfigure |

## Pros/Cons or Trade-offs
- You only need runtime behavior
- Application-level folder layout (React `src/components`)
