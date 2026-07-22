[[Configuration]] [[nginx using unix socket]] [[Epoll]] [[half-open connections]] [[ss]]

# Nginx internals

> Event-driven master/worker proxy — how requests flow through phases, upstream pools, and the filesystem — **nginx.org dev docs** + production 502 debugging.

---

## Mental model

```txt
                    master (root, reads config)
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
        worker 1      worker 2      worker N   (non-root, event loop each)

Client TCP → worker accept → HTTP parse → phase handlers → content handler
                                                      ↓
                                            upstream / static file / FastCGI
```

**One worker per core** (typical) — each runs **non-blocking event loop** ([[Epoll]] on Linux). No thread-per-request; high concurrency with fixed memory.

**Master:** bind ports, read config, manage workers. **Workers:** handle connections. `reload` = graceful config swap without dropping established connections (mostly).

**Key subsystems:**

| Subsystem | Role |
|-----------|------|
| `ngx_http_core_module` | Request struct, phases, variables |
| `ngx_http_upstream` | Backend connection, retries, keepalive pool |
| `ngx_http_proxy_module` | Reverse proxy headers, buffering |
| `ngx_stream_*` | L4 TCP/UDP proxy |
| `ngx_event` | accept, read/write timers |

**Request phases (HTTP):** post-read → server rewrite → find config → rewrite → pre-access → access → content → log. Modules hook phases (auth, rate limit, `try_files`, `proxy_pass`).

---

## Standard config / commands

### Source map (when reading C code)

```txt
http/ngx_http_proxy_module.c    — proxy_pass implementation
http/ngx_http_upstream.c        — upstream connect, failover, lb
http/ngx_http_core_module.c     — location tree, variables
event/ngx_event.c               — event loop
os/unix/ngx_process.c           — master/worker lifecycle
stream/ngx_stream_proxy_module.c — TCP proxy
```

### Worker / connection tuning

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
  worker_connections 4096;   # per worker; total ≈ workers × connections
  multi_accept on;
  use epoll;                 # Linux default on modern builds
}

http {
  upstream backend {
    server 127.0.0.1:8080;
    keepalive 32;            # idle connections to upstream — huge win
  }

  server {
    location / {
      proxy_http_version 1.1;
      proxy_set_header Connection "";
      proxy_pass http://backend;
    }
  }
}
```

### Debug config (lab only)

```nginx
error_log /var/log/nginx/error.log debug;  # verbose — never prod default
rewrite_log on;
```

```bash
sudo nginx -t
sudo nginx -s reload
curl -v http://127.0.0.1/ -o /dev/null
```

### Observe live state

```bash
# Stub status (require stub_status module + location)
curl http://127.0.0.1/nginx_status

# Active connections per worker
ss -tnp | grep nginx

# Which worker owns FD (Linux)
ls -l /proc/$(pgrep -o nginx)/fd | wc -l
```

### Upstream failure behavior

```nginx
proxy_connect_timeout 5s;
proxy_read_timeout 60s;
proxy_next_upstream error timeout http_502 http_503;
proxy_next_upstream_tries 2;
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | `error.log` upstream connect/refused | App down; wrong socket; `proxy_pass` URL typo |
| 504 Gateway Timeout | `upstream timed out` | ↑ read timeout; fix slow app; DB lock |
| 499 (client closed) | User/aborted; LB idle | Harmless spike; check client timeouts |
| 413 / 400 large body | `client_max_body_size` | Increase on relevant `location` |
| Static file wrong path | root vs alias ([[Configuration]]) | Test resolved path; trailing slash rules |
| Reload didn't apply | `nginx -t` failed silently? | Fix config; full restart last resort |
| Worker OOM | Huge `proxy_buffer` / many uploads | Tune buffers; limit body; more RAM |
| Uneven CPU | 1 hot worker | `reuseport` on listen; check long-lived connections |
| Upstream connection churn | No keepalive | Enable upstream keepalive + HTTP/1.1 |
| SSL handshake CPU hot | All on workers | Session cache; TLS termination at LB |

---

## Gotchas

> [!WARNING]
> **`if` in nginx** — not a general programming construct; surprising behavior in `location` — prefer `map`/`try_files`.

> [!WARNING]
> **Unix socket backlog** — app must accept fast enough; 502 under burst with silent app queue.

> [!WARNING]
> **`proxy_buffering off` for SSE** — needed for streaming; breaks if enabled for event streams.

> [!WARNING]
> **Same name upstream in multiple files** — last definition wins in include order; name collisions cause ghost routing.

> [!WARNING]
> **Worker_connections vs system ulimit** — bump `worker_rlimit_nofile` **and** `/etc/security/limits.conf`.

---

## When NOT to use

- **Application business logic** — nginx is proxy/static; use app server for code execution.
- **Complex auth without modules** — OpenResty/lua or delegate to auth service.
- **Long-lived bidirectional gRPC without HTTP/2 tuning** — verify grpc module settings or use dedicated proxy.

---

## Related

[[Configuration]] · [[nginx using unix socket]] · [[Epoll]] · [[half-open connections]] · [[ss]] · [[TLS (Transport Layer Security)]]
