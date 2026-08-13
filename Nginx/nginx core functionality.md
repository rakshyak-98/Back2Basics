[[Nginx]]

# nginx core functionality

> nginx core functionality — all workers processes get simultaneously notified about a new incoming connection.

---

## How it works

`accept_mutex`
When `accept_mutex` disabled
- All workers processes get simultaneously notified about a new incoming connection.
- the race to call `accept()` on the shared listen socket.
- Only one of them actually gets the connection.
- The others get `EAGAIN` (or similar) and go back to sleep.
This is called **thundering herd** problem (or wake-up storm).


## Configuration and commands

Roles: reverse proxy, static file server, TLS termination, load balancer (`upstream`).

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| High worker CPU | SSL renegotiation; gzip on huge files | Tune `worker_connections`; offload TLS |
| Slow static files | disk IO; sendfile off | Enable `sendfile`; check filesystem |
| Upstream flapping | health checks missing | `max_fails` and `fail_timeout` in upstream |

---


## Gotchas

> [!WARNING]
> Nginx handles many connections with **few worker processes** — mis-tuned `worker_connections` causes 502 storms.

---


## When not to use

- Do not use Nginx alone for WebSocket-heavy apps without proper `proxy_read_timeout` tuning.


---


## Related

[[Nginx]]

## Sources

- [Wikipedia — nginx core functionality](https://en.wikipedia.org/wiki/nginx_core_functionality)
