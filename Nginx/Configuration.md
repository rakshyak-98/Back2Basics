[[Nginx]] [[web server]] [[directives]] [[nginx SPA deployment]] [[nginx fastcgi]]

# Nginx Configuration

> One-line: reverse proxy + static file server — configure locations correctly, validate with `nginx -t`, reload without dropping connections.

## Mental model

Nginx is **not** an app server. It terminates HTTP, serves static files from disk, and forwards dynamic work to upstreams (Node, PHP-FPM, uWSGI) via `proxy_pass` or `fastcgi_pass`. One **master** (root) owns listen sockets; **workers** (unprivileged) handle requests concurrently.

Location matching priority: `=` exact → `^~` prefix (stops regex) → `~`/`~*` regex → plain prefix (longest wins).

| Directive | Config | Request | Resolved path |
|-----------|--------|---------|---------------|
| `root` | `location /images/ { root /var/www/static; }` | `/images/cat.png` | `/var/www/static/images/cat.png` |
| `alias` | `location /images/ { alias /var/www/static/; }` | `/images/cat.png` | `/var/www/static/cat.png` |

> [!WARNING]
> Nginx does not expand `~` in `include` paths — no shell expansion. Use absolute paths or generate configs via Ansible/Jinja/envsubst.
> Variables are **not** allowed in `alias`.

---

## Standard config / commands

### Validate and reload

```bash
sudo nginx -t
sudo nginx -t -c /path/to/custom/nginx.conf
sudo nginx -c /path/to/custom/nginx.conf -g "daemon off"   # foreground debug
sudo nginx -s reload
sudo truncate -s 0 /var/log/nginx/access.log
```

Use `-c` when testing configs outside `/etc/nginx/nginx.conf`.

### Reverse proxy + static (Next.js pattern)

```nginx
http {
  server {
    listen 8080;
    server_name localhost;

    location /_next/static/ {
      alias /home/app/.next/static/;
      access_log off;
    }

    location /public/ {
      alias /home/app/public/img/;
    }

    location / {
      proxy_pass http://127.0.0.1:3000;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
}
events {}
```

### Upstream health + failover

```nginx
upstream api_backend {
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3002 max_fails=3 fail_timeout=30s;
    keepalive 32;   # reuse connections to upstream — big win under load
}

server {
    location /api/ {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        proxy_next_upstream error timeout http_502 http_503 http_504;
    }

    # Active health check (nginx-plus) OR passive via max_fails above (OSS)
    location /health {
        access_log off;
        proxy_pass http://api_backend/health;
    }
}
```

Passive health: after `max_fails` errors within `fail_timeout`, upstream is marked down. No OSS active probe without third-party modules or external health checker + dynamic upstream API.

### Rate limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn:10m;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;   # burst absorbs spikes
            limit_conn conn 10;
            proxy_pass http://127.0.0.1:3000;
        }
    }
}
```

`$binary_remote_addr` = 4 bytes per IPv4 — efficient zone key. Tune `rate` and `burst` from real traffic; too aggressive → 503 for legit users.

### open_file_cache (static-heavy sites)

```nginx
http {
    open_file_cache          max=10000 inactive=60s;
    open_file_cache_valid    30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors   on;
}
```

Caches file descriptors + metadata for static serving. **Disable or shrink** if content changes frequently without reload — stale FDs until `inactive` expires.

### Worker tuning

```nginx
worker_processes auto;   # 1 per CPU core is the common default

events {
    worker_connections 2048;
    # max concurrent ≈ worker_processes × worker_connections
}
```

```bash
nproc
grep -c ^processor /proc/cpuinfo
watch 'sudo lsof -i :80 | grep nginx | wc -l'
ss -tupn | grep nginx
```

### Location modifiers

| Modifier | Meaning | Stops regex? | Typical use |
|----------|---------|--------------|-------------|
| `=` | Exact match | Yes | `/favicon.ico` |
| `^~` | Prefix, high priority | **Yes** | `/storage/`, static uploads |
| `~` / `~*` | Regex (case sens/insens) | No | `.php$`, rewrite rules |
| (none) | Normal prefix | No | Fallback routes |

`location ^~ /storage/ {` — prefix wins; no regex location can override.

### PHP via FastCGI

```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/html/yourproject;
    index index.php index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

> [!NOTE]
> PHP-FPM typically runs as `www-data`. Project dirs need read (execute on dirs) for PHP; write on `storage/`, uploads, cache.

`fastcgi.conf` — standard params when Nginx forwards to FastCGI; Nginx never executes PHP itself.

`~ \.php$` = case-sensitive regex. `~* \.php$` = case-insensitive.

### sites-available / sites-enabled

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/myapp   # disable without deleting config
sudo nginx -t && sudo systemctl reload nginx
```

### IP allow/deny

```nginx
location /admin {
    deny 192.168.1.0/24;
    allow all;
}
```

Order matters: first matching rule wins.

---

## Triage (when things break)

### 499 / 502 / 504 playbook

| Code | Symptom | Check | Fix |
|------|---------|-------|-----|
| **499** | Client closed before upstream responded; spikes during deploys or slow APIs | `grep " 499 " /var/log/nginx/access.log`; correlate with upstream latency | Increase client timeouts only if needed; fix slow upstream; during deploy use `proxy_next_upstream` + drain connections; 499 is often **client-side** (mobile, tab close) — not always your bug |
| **502** | Bad Gateway — Nginx reached upstream but got invalid/no response | `curl -v http://127.0.0.1:UPSTREAM_PORT/health`; check upstream process (`ss -tlnp`, `systemctl status`); error log: `upstream prematurely closed` | Restart crashed app; fix socket path for unix (`proxy_pass http://unix:/path.sock`); verify `proxy_pass` trailing slash rules; check `keepalive` pool not holding dead connections |
| **504** | Gateway Timeout — upstream too slow | `grep "upstream timed out" /var/log/nginx/error.log`; compare `proxy_read_timeout` vs app p99 | Raise `proxy_read_timeout` / `proxy_connect_timeout` if app is legitimately slow; fix blocking event loop; add upstream health checks; scale workers |

```bash
# Quick upstream probe (bypass Nginx)
curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" http://127.0.0.1:3000/health

# Error log tail during incident
sudo tail -f /var/log/nginx/error.log | grep -E 'upstream|timeout|connect'
```

### General triage

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on static asset | `root` vs `alias` table above; `try_files` order | Fix path mapping; trailing slash on `alias` |
| 403 Forbidden | `namei -l /path/to/file`; SELinux context | Fix ownership (`www-data` read); `chmod`; `chcon` if enforcing |
| Config won't reload | `sudo nginx -t` | Fix syntax; duplicate `server_name`; missing `;` |
| Changes not visible | Wrong `sites-enabled` symlink; browser cache | `nginx -T \| grep server_name`; hard refresh |
| Permission denied on unix socket | `ls -la /var/run/app.sock` | Match user/group between app and Nginx; `chmod 660` + shared group |

---

## Gotchas

> [!WARNING]
> **`proxy_pass` trailing slash:** `location /api/ { proxy_pass http://backend/; }` strips `/api/` prefix. Without trailing slash on URI, full path is forwarded — #1 source of double-prefix bugs.

> [!WARNING]
> **`alias` trailing slash:** `location /images/ { alias /var/www/static/; }` — both must end with `/` or paths misalign silently.

> [!WARNING]
> **Reload ≠ zero-downtime for broken config:** `nginx -t` before every reload. Bad config on reload can leave old workers running but block new ones.

> [!WARNING]
> **Worker count alone doesn't fix saturation:** Also tune `worker_connections`, upstream `keepalive`, and OS `somaxconn` / `file-max`.

---

## Process architecture

```
PID (root)     = Master — owns FD 6 (IPv4 :80), FD 7 (IPv6 :80), manages workers
PID (nginx)    = Workers — handle requests, inherit same listen sockets
```

All processes show in `lsof -i :80` because each worker holds the shared socket. Worker count from config or `ps aux | grep nginx`.

---

## When NOT to use

- **Application logic in Nginx** — use `lua`/`js` modules only when edge logic is truly needed; business rules belong in the app.
- **Nginx as database connection pooler** — use PgBouncer, ProxySQL, or app-side pooling.
- **Replacing WAF entirely with rate limits** — `limit_req` helps abuse; doesn't stop SQLi/XSS.

---

## Related

[[nginx SPA deployment]] [[nginx using unix socket]] [[nginx stream]] [[static file]] [[Nginx internals]] [[TLS (Transport Layer Security)]]
