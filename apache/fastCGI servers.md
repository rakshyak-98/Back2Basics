[[CGI]] [[PHP-FPM]] [[apache modules]] [[Nginx]] [[Proxy/Reverse Proxy]]

# FastCGI

> Binary protocol between a web server and long-lived application workers — reuse processes instead of forking per request like classic CGI.

```txt
        FastCGI ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want the contrast with CGI, where PHP-FPM fits, and how Nginx/Ap…

## Sources
- [FastCGI specification](https://fastcgi-archives.github.io/) — deep-dive
- [Wikipedia — FastCGI](https://en.wikipedia.org/wiki/FastCGI) — overview

## Key Concepts
- **Persistent workers:** handle many requests → amortize interpreter startup.
- **Language agnostic:** PHP, Python, etc. speak FastCGI to the front door.
- **Socket or TCP:** `unix:/run/php/php-fpm.sock` or `127.0.0.1:9000`.
- **Process manager:** pool sizing (static/dynamic/ondemand) → latency vs memory.

## Technical Details
```
Client → Nginx/Apache → FastCGI (socket) → worker → response
```

- Apache often uses `proxy_fcgi`; Nginx uses `fastcgi_pass`.
- PHP’s common server-side is [[PHP-FPM]].

| Symptom | Check | Fix |
|---------|-------|-----|
| 502/504 | Socket path / pool up? | Start FPM; match path in vhost |
| Spiky latency | Pool too small | Raise `pm.max_children` carefully |
| Memory blowup | Too many workers | Lower children; fix leaks |

## Mistakes to Avoid
- **Mistake:** World-writable FastCGI sockets
- **Mistake:** Sizing `max_children` above what RAM can hold (`memory_limit × c…
- **Mistake:** Mixing leftover `mod_php` with FPM on the same vhost accidentally

## Pros/Cons or Trade-offs
- **Pro:** Far better throughput than classic [[CGI]].
- **Con:** Another daemon to monitor (pool, socket permissions, versions).

## Comparison
- vs CGI: persistent vs process-per-request.
- vs HTTP reverse proxy to Node/Java: FastCGI is a specialized app protocol


### Use cases
- Almost every PHP site behind Nginx/Apache today: front server serves static f…

- **Example:** Deploy moves socket path from `/run/php/php8.2-fpm.sock` to `8.3`
