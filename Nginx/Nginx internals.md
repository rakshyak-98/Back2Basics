[[Configuration]] [[nginx using unix socket]] [[Epoll]] [[half-open connections]] [[ss]] [[TLS (Transport Layer Security)]] [[nginx core functionality]]

# Nginx internals

> Master manages workers; each worker runs a non-blocking event loop — parse HTTP, run phase handlers, then static / upstream / FastCGI.

## Interview Relevance

Deep systems interviews probe event-driven architecture, HTTP phases, upstream keepalive, and why reload is graceful — distinguishes “used Nginx” from “read the source map.”

## Sources

- [nginx.org — Development guide](https://nginx.org/en/docs/dev/development_guide.html) — deep-dive
- [nginx.com — Inside NGINX](https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/) — overview
- [nginx.org — ngx_http_upstream_module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html) — deep-dive

## Core Definition

Nginx internals are a master/worker process model plus an event module ([[Epoll]] on Linux): workers accept connections, run HTTP request phases, and invoke content handlers (proxy, static, FastCGI) without a thread per request.

## Key Concepts

- **One worker per core (typical):** Fixed memory, high concurrency via non-blocking I/O.
- **Master vs workers:** Master binds ports, reads configuration, manages workers; workers handle connections. `reload` swaps configuration gracefully.
- **HTTP phases:** post-read → server rewrite → find configuration → rewrite → pre-access → access → content → log — modules hook phases.
- **Upstream subsystem:** Connect, retry, load balance, keepalive pool to backends.

## Technical Details

```txt
                         │
           ┌─────────────┼─────────────┐
           ▼             ▼             ▼
        worker 1      worker 2      worker N   (non-root, event loop each)

Client TCP → worker accept → HTTP parse → phase handlers → content handler
                                                      ↓
                                            upstream / static file / FastCGI
```

| Subsystem | Role |
|-----------|------|
| `ngx_http_core_module` | Request struct, phases, variables |
| `ngx_http_upstream` | Backend connection, retries, keepalive pool |
| `ngx_http_proxy_module` | Reverse proxy headers, buffering |
| `ngx_stream_*` | L4 TCP/UDP proxy |
| `ngx_event` | accept, read/write timers |

### Source map (when reading C code)

```txt
http/ngx_http_proxy_module.c    — proxy_pass implementation
http/ngx_http_upstream.c        — upstream connect, failover, lb
http/ngx_http_core_module.c     — location tree, variables
event/ngx_event.c               — event loop
os/unix/ngx_process.c           — master/worker lifecycle
stream/ngx_stream_proxy_module.c — TCP proxy
```

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

```nginx
error_log /var/log/nginx/error.log debug;  # verbose — never prod default
rewrite_log on;
```

```bash
sudo nginx -t
sudo nginx -s reload
curl -v http://127.0.0.1/ -o /dev/null
curl http://127.0.0.1/nginx_status    # stub_status module
ss -tnp | grep nginx
ls -l /proc/$(pgrep -o nginx)/fd | wc -l
```

```nginx
proxy_connect_timeout 5s;
proxy_read_timeout 60s;
proxy_next_upstream error timeout http_502 http_503;
proxy_next_upstream_tries 2;
```

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

## Real-World Applications

Tune workers and upstream keepalive for a busy API gateway; debug 502s with phase-aware reading of `error.log`; enable `stub_status` in lab to watch active connections.

## Pros/Cons or Trade-offs

- **Pro:** Predictable memory and huge concurrency for proxy/static workloads.
- **Con:** Not an application runtime — complex auth often needs OpenResty/Lua or an auth service.
- **Con:** gRPC / HTTP/2 and streaming need careful buffering (`proxy_buffering off` for SSE).

## Comparison

- vs [[nginx core functionality]]: product roles vs module/phase/source-level detail.
- vs thread-per-request servers: event loop avoids per-connection thread stacks.

## Mistakes to Avoid

- Using `if` as general programming in `location` — prefer `map` / `try_files`.
- Ignoring unix socket backlog — app must accept fast enough or 502 under burst.
- Leaving `proxy_buffering` on for SSE/event streams.
- Duplicate upstream names across includes — last definition wins.
- Raising `worker_connections` without `worker_rlimit_nofile` and OS ulimits.
