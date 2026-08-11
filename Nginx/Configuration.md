[[Nginx]] [[web server]] [[directives]] [[nginx SPA deployment]] [[nginx fastcgi]] [[nginx configuration structure]]

# Nginx Configuration

> Reverse proxy + static files — validate with `nginx -t`, reload without dropping connections.

---

## Mental model

**Say it in one breath:** Nginx terminates HTTP, serves static files, and proxies to upstreams — master owns sockets; workers handle requests.

```txt
Client → nginx (location match) → root/alias | proxy_pass | fastcgi_pass
```

Location priority: `=` exact → `^~` prefix (stops regex) → `~`/`~*` regex → longest prefix.

| Directive | Path rule |
|-----------|-----------|
| `root` | URI appended under root |
| `alias` | Replaces location prefix |

---

## Standard config / commands

```bash
sudo nginx -t && sudo nginx -s reload
sudo nginx -T | less          # merged config
```

```nginx
upstream api { server 127.0.0.1:3000; keepalive 32; }

server {
  listen 80;
  location /_next/static/ { alias /var/www/app/.next/static/; }
  location / {
    proxy_pass http://api;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

```nginx
# rate limit
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ { limit_req zone=api burst=20 nodelay; proxy_pass http://api; }
```

| Knob | Why it matters |
|------|----------------|
| `proxy_pass` trailing `/` | Strips location prefix |
| `worker_processes auto` | ~1 per CPU |
| `max_fails` / `fail_timeout` | Passive upstream health |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | Upstream up? socket path? | Restart app; fix `unix:` path |
| 504 Gateway Timeout | `proxy_read_timeout` vs p99 | Raise timeout or fix slow app |
| 499 Client Closed | Client left early | Often mobile/tab — check deploy drain |
| 404 static | `root` vs `alias` | Fix mapping + trailing slashes |
| 403 | perms / SELinux | `www-data` read; `namei -l` |
| reload fails | `nginx -t` | Fix syntax before reload |

---

## Gotchas

> [!WARNING]
> **`proxy_pass` slash** — `/api/` → `http://b/` strips prefix; without slash, full URI forwards.

> [!WARNING]
> **`alias` trailing slash** — location and alias must both end with `/` or paths misalign.

> [!WARNING]
> **Never reload untested config** — `nginx -t` first.

---

## When NOT to use

- **application business logic in Nginx** — keep in the application.
- **DB connection pooling** — use PgBouncer / application pool.
- **Sole WAF** — `limit_req` ≠ SQLi protection.

---

## Related

[[nginx SPA deployment]] [[nginx using unix socket]] [[nginx stream]] [[static file]] [[Nginx internals]]
