[[nginx fastcgi]] [[nginx using unix socket]] [[Nginx internals]] [[file descriptors]] [[half-open connections]]

# PHP-FPM

> FastCGI Process Manager: the worker pool between Nginx/Apache and PHP — **production default for PHP on Linux**.

---

## Mental model

Nginx terminates TLS and forwards requests to **PHP-FPM** over TCP or a **Unix socket**. FPM maintains a pool of worker processes; each worker handles one request at a time (unless you use async frameworks, which is rare in PHP).

```txt
Client ──► Nginx ──► [FPM master] ──► worker pool ──► PHP script ──► DB
              │            │
              │            └── pm=dynamic: spawn/kill workers by load
              └── fastcgi_pass unix:/run/php/php8.3-fpm.sock
```

| Component | Role |
|-----------|------|
| **Master** | Reads config, manages workers, never serves requests |
| **Worker** | Executes `index.php`; dies after `pm.max_requests` (leak mitigation) |
| **Pool** | Named section in `www.conf` — one pool per app or socket |
| **Slowlog** | Stack trace when request exceeds `request_slowlog_timeout` |

**502 Bad Gateway** almost always means Nginx could not get a valid FastCGI response — not a PHP syntax error (those are usually 500 from FPM).

---

## Standard config / commands

### Pool snippet (`/etc/php/8.3/fpm/pool.d/www.conf`)

```ini
[www]
user = www-data
group = www-data

; Unix socket — lower latency than TCP on same host
listen = /run/php/php8.3-fpm.sock
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

; dynamic = default for web traffic
pm = dynamic
pm.max_children = 50          ; hard ceiling — tune from RAM (≈50–80MB/worker)
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 500         ; recycle workers — prevents extension leaks

; Observability
slowlog = /var/log/php8.3-fpm-slow.log
request_slowlog_timeout = 5s
request_terminate_timeout = 60s

; Status page (restrict in Nginx!)
pm.status_path = /fpm-status
ping.path = /fpm-ping
```

### Nginx upstream

```nginx
upstream php_fpm {
    server unix:/run/php/php8.3-fpm.sock;
}

location ~ \.php$ {
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass php_fpm;
    fastcgi_read_timeout 60s;
    fastcgi_buffers 16 16k;
    fastcgi_buffer_size 32k;
}

# Lock down status — never public
location = /fpm-status {
    allow 127.0.0.1;
    deny all;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass unix:/run/php/php8.3-fpm.sock;
}
```

### pm modes

| Mode | Behavior | When |
|------|----------|------|
| **dynamic** | Keeps spare workers between min/max | General web — default |
| **static** | Fixed `pm.max_children` always running | Predictable load, latency-sensitive |
| **ondemand** | Spawns on request, idle timeout kill | Low-traffic / dev — cold-start latency |

### Ops commands

```shell
sudo systemctl status php8.3-fpm
sudo php-fpm8.3 -t                    # config test
sudo systemctl reload php8.3-fpm

# Live pool stats (if status enabled)
curl -s 'http://127.0.0.1/fpm-status?json' | jq .

# Slow requests
sudo tail -f /var/log/php8.3-fpm-slow.log

# Socket perms
ls -la /run/php/php8.3-fpm.sock
# Expected: srw-rw---- www-data www-data
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| **502** on all PHP routes | `ls -la /run/php/*.sock`; `systemctl status php-fpm` | FPM down; socket path mismatch vs Nginx `fastcgi_pass` |
| **502** intermittent | `curl fpm-status`; check `listen queue` | Pool exhausted — raise `pm.max_children` or fix slow queries |
| **502** after deploy | Nginx error log: `connect() to unix:... failed (13: Permission denied)` | `listen.owner/group/mode` — Nginx user must be in socket group |
| **504** gateway timeout | Nginx `fastcgi_read_timeout`; FPM `request_terminate_timeout` | Long-running script; async job queue instead |
| **500** with blank body | FPM `/var/log/php8.3-fpm.log`, app `error_log` | PHP fatal; `display_errors=Off` in prod hides from client |
| Memory climb over days | `pm.max_requests = 0` | Enable recycling; audit extension leaks (imagick, etc.) |
| All workers busy, low CPU | DB lock / external API | Slowlog pinpoints line; not a pool sizing problem |

```shell
# Nginx side
sudo tail -f /var/log/nginx/error.log | grep -i fastcgi

# FPM side
sudo journalctl -u php8.3-fpm -f
```

---

## Gotchas

> [!WARNING]
> **Socket path drift** — distro upgrades rename `/run/php/php7.4-fpm.sock` → `php8.3`. Nginx still points at old path → instant 502 after apt upgrade.

> [!WARNING]
> **`pm.max_children` vs RAM** — 50 workers × 128MB = 6.4GB. OOM killer takes FPM first; Nginx returns 502 for everyone.

> [!WARNING]
> **Opcache + deploy** — stale bytecode after deploy unless `opcache.revalidate_freq=0` in dev or graceful reload strategy in prod.

> [!WARNING]
> **Status page exposed** — `/fpm-status` public = attacker maps your capacity. IP-restrict or internal-only.

> [!WARNING]
> **TCP `127.0.0.1:9000`** — works but adds overhead; Unix socket is same-host best practice. If TCP, ensure not bound `0.0.0.0`.

---

## When NOT to use

- **CLI/cron scripts** — invoke `php` directly, not FPM.
- **Long-lived WebSockets in PHP** — wrong tool; use Node/Go or a dedicated WS gateway.
- **ondemand in prod** — first-request latency after idle spikes; use dynamic.

---

## Related

[[nginx fastcgi]] [[nginx using unix socket]] [[Nginx internals]] [[file descriptors]] [[OOM (Linux Out Of Memory)]]
