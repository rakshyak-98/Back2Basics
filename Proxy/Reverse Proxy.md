[[Proxy]] [[Nginx]] [[apache modules]] [[Security/TLS (Transport Layer Security)]]

# Reverse Proxy

> Server-side proxy that accepts client requests and forwards them to internal backends — TLS termination, routing, and hiding origin servers.

## Interview Relevance

Interviewers want reverse vs forward proxy, why APIs sit behind Nginx/Enovy, and headers (`X-Forwarded-For`/`Proto`) for real client IP and HTTPS scheme.

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

Preserve client info with forwarded headers — and trust them only from your proxy hop.

## Real-World Applications

Public HTTPS on Nginx/Caddy; Node/PHP-FPM/Java listen on localhost ports.

**Example:** App thinks all users are `127.0.0.1` — configure forwarded headers and app trust settings.

## Pros/Cons or Trade-offs

- **Pro:** Central TLS, routing, and security controls.
- **Con:** Misconfigured headers cause wrong IPs/URLs; extra hop to debug.

## Comparison

- vs forward proxy (corp egress): opposite trust direction.
- vs API gateway: gateway adds auth/rate-limit product features on the same idea.

## Mistakes to Avoid

- Trusting `X-Forwarded-*` from the open internet without hop limits.
- Leaving backends publicly reachable bypassing the proxy.
- Forgetting WebSocket upgrade headers on proxied WS apps.
