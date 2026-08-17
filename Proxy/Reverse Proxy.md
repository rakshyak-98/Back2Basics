[[Proxy]] [[Nginx]] [[apache modules]] [[Security/TLS (Transport Layer Security)]]

# Reverse Proxy

> Server-side proxy that accepts client requests and forwards them to internal backends — TLS termination, routing, and hiding origin servers.

```txt
        Reverse Proxy ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want reverse vs forward proxy, why APIs sit behind Nginx/Enovy, …

## Sources
- [Wikipedia — Reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy) — overview
- [Nginx — Reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) — deep-dive

## Key Concepts
- **Reverse:** clients talk to the proxy; proxy chooses backends.
- **Forward:** clients configure a proxy to reach the outside world.
- **TLS termination:** decrypt at edge; HTTP inside a private network (or re-encrypt).
- **Routing:** path/host to service; load balancing and health checks.

## Technical Details
```txt
Client → Reverse proxy (TLS) → App1 / App2 / Static
```

| Job | Example |
|-----|---------|
| Terminate TLS | Certificates on Nginx |
| Route | `/api` → Node, `/` → static |
| Buffer/upload limits | Protect slow backends |

- Preserve client info with forwarded headers

## Mistakes to Avoid
- **Mistake:** Trusting `X-Forwarded-*` from the open internet without hop limi…
- **Mistake:** Leaving backends publicly reachable bypassing the proxy
- **Mistake:** Forgetting WebSocket upgrade headers on proxied WS apps

## Pros/Cons or Trade-offs
- **Pro:** Central TLS, routing, and security controls.
- **Con:** Misconfigured headers cause wrong IPs/URLs; extra hop to debug.

## Comparison
- vs forward proxy (corp egress): opposite trust direction.
- vs API gateway: gateway adds auth/rate-limit product features on the same idea.


### Use cases
- Public HTTPS on Nginx/Caddy; Node/PHP-FPM/Java listen on localhost ports.

- **Example:** App thinks all users are `127.0.0.1`
