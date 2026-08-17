[[Nginx internals]] [[Configuration]] [[static file]] [[web server]] [[webSocket]]

# nginx core functionality

> Event-driven reverse proxy and static server — few workers, many connections; roles include TLS termination, load balancing, and FastCGI.

```txt
        nginx core functio ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want the master/worker model, why Nginx scales with events not t…

## Sources
- [nginx.org — Inside NGINX: How We Designed for Performance & Scale](https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/) — overview
- [nginx.org — ngx_core_module (accept_mutex)](https://nginx.org/en/docs/ngx_core_module.html#accept_mutex) — deep-dive
- [Wikipedia — nginx](https://en.wikipedia.org/wiki/Nginx) — overview

## Key Concepts
- **Master / workers:** Master binds and reloads
- **`accept_mutex`:** When disabled, all workers wake on a new connection and race `accept()`
- **Core roles:** reverse proxy, static file server, TLS termination, load balancer (`upstream`…
- **Connection budget:** `worker_connections` × workers ≈ max concurrent connections (also limited by …


- **Core:** Nginx’s core is a master process that manages configuration and worker proces…

## Technical Details
- When `accept_mutex` is off:

- All worker processes are notified about a new incoming connection.
- They race to call `accept()` on the shared listen socket.
- Only one gets the connection

| Symptom | Check | Fix |
|---------|-------|-----|
| High worker CPU | SSL renegotiation; gzip on huge files | Tune `worker_connections`; offload TLS |
| Slow static files | disk IO; sendfile off | Enable `sendfile`; check filesystem |
| Upstream flapping | health checks missing | `max_fails` and `fail_timeout` in upstream |

## Mistakes to Avoid
- **Mistake:** Assuming more workers always help
- **Mistake:** Using Nginx alone for WebSocket-heavy apps without raising idle/…
- **Mistake:** Ignoring thundering herd on very busy listen sockets when diagno…

## Pros/Cons or Trade-offs
- **Pro:** High concurrency with fixed worker count and low memory vs thread-per-connection servers.
- **Con:** Mis-tuned `worker_connections` / ulimits cause 502 storms under load.
- **Con:** WebSocket and long-poll need explicit timeout tuning (`proxy_read_timeout`).

## Comparison
- vs Apache prefork/worker: different concurrency model — Nginx event loop vs process/thread pools.
- vs [[Nginx internals]]: this note is the product roles + accept behavior


### Use cases
- Edge TLS + reverse proxy in front of app servers
