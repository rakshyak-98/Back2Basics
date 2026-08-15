[[php]] [[php error]] [[fastCGI servers]] [[Nginx]]

# PHP-FPM

> FastCGI Process Manager for PHP — a master supervises a worker pool; Nginx/Apache proxy requests to a Unix socket or TCP port.

## Interview Relevance

Interviewers ask pool modes (`static`/`dynamic`/`ondemand`), how you size `max_children` from RAM, and why 502 ≠ PHP stack trace.

## Sources

- [PHP — FPM configuration](https://www.php.net/manual/en/install.fpm.configuration.php) — deep-dive
- [Nginx — fastcgi_pass](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html) — overview

## Key Concepts

- **Master vs worker:** master manages; workers execute `index.php`.
- **Pool:** named section (`www.conf`) — user, listen socket, pm settings.
- **`pm.max_requests`:** recycle workers to contain extension leaks.
- **Slowlog / terminate timeout:** find stuck requests; kill runaway ones.

## Technical Details

```txt
Client ──► Nginx ──► [FPM master] ──► worker pool ──► PHP ──► DB
```

```ini
[www]
listen = /run/php/php8.3-fpm.sock
listen.owner = www-data
listen.group = www-data
listen.mode = 0660
pm = dynamic
pm.max_children = 50
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 500
request_slowlog_timeout = 5s
request_terminate_timeout = 60s
```

| Symptom | Meaning |
|---------|---------|
| 502 | No valid FastCGI response (down/mismatch) |
| 500 | PHP ran and failed |
| Max children reached | Undersized pool or slow app |

## Real-World Applications

One pool per app/site for isolation; status page (`pm.status_path`) scraped internally for capacity.

**Example:** Workers at ~80MB and host has 8GB for PHP — oversized `max_children` risks OOM; size from memory, not wishful QPS.

## Pros/Cons or Trade-offs

- **Pro:** Stable, observable, works with Nginx/Apache FastCGI.
- **Con:** Blocking workers need horizontal sizing; not magic concurrency.

## Comparison

- vs classic [[CGI]]: persistent workers vs process-per-request.
- vs `mod_php`: FPM isolates PHP from the web server process model.

## Mistakes to Avoid

- World-writable sockets.
- `max_children` larger than RAM allows.
- Exposing `/fpm-status` to the public internet.
