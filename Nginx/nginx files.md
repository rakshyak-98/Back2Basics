[[Configuration]] [[nginx config structure]] [[How does directive work]] [[Linux/loggging]]

# nginx files

> Package paths and log rotation — where configs, PIDs, and access/error logs live, and how logrotate signals Nginx to reopen files.





## Interview Relevance
Ops interviews ask where to look when “my edit did nothing,” why disks fill from logs, and what `USR1` after logrotate does.

## Sources
- [nginx.org — Logging](https://nginx.org/en/docs/ngx_core_module.html#error_log) — deep-dive
- [Debian — nginx package layout](https://wiki.debian.org/Nginx) — overview
- [logrotate man page](https://linux.die.net/man/8/logrotate) — overview

## Key Concepts
- **Config tree:** `/etc/nginx/nginx.conf` includes `sites-enabled` / `conf.d` — see [[nginx config structure]].
- **Logs:** `/var/log/nginx/access.log` and `error.log` (override with `error_log` / `access_log` directives).
- **PID:** `/run/nginx.pid` — master process id for signals.
- **logrotate + USR1:** After rename/compress, send `USR1` so Nginx reopens log file descriptors (avoids writing to deleted inodes).

## Technical Details
```
/etc/nginx/nginx.conf → sites-enabled/* → access.log / error.log
         ↓ logrotate (daily)
/var/log/nginx/*.log.1.gz
```

### Common paths (Debian/Ubuntu)

| Path                          | Purpose                   |
| ----------------------------- | ------------------------- |
| `/etc/nginx/nginx.conf`       | Main include tree         |
| `/etc/nginx/sites-available/` | Site defs                 |
| `/etc/nginx/sites-enabled/`   | Symlinks to enabled sites |
| `/etc/nginx/conf.d/*.conf`    | Drop-in snippets          |
| `/var/log/nginx/access.log`   | Request log               |
| `/var/log/nginx/error.log`    | Errors, upstream failures |
| `/etc/logrotate.d/nginx`      | Rotation policy           |
| `/run/nginx.pid`              | Master PID                |

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

Typical logrotate snippet:

```
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    sharedscripts
    postrotate
        [ -f /run/nginx.pid ] && kill -USR1 `cat /run/nginx.pid`
    endscript
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Edit has no effect | Which file included? | `nginx -T`; enable correct site symlink |
| Disk full | `/var/log/nginx` size | Force rotate; lower retention; fix log flood |
| Empty error log | `error_log` path override | Grep `error_log` in `nginx -T` |
| Permission denied on log | nginx user | `www-data` ownership on log dir |
| Site enabled twice | Duplicate server_name | One conf per `server_name`:port |
| PID file stale | Crash | `systemctl restart nginx` |

## Real-World Applications
Enable a site via symlink, watch `error.log` for upstream 502s during deploy, rely on daily logrotate with USR1 postrotate.

## Pros/Cons or Trade-offs
- **Pro:** Standard Debian layout is familiar across hosts.
- **Con:** JSON access logs on the same disk as app data can cause IO contention — ship logs centrally when busy.

## Comparison
- vs journald-only logging: Nginx file logs remain common; can also log to syslog.
- vs [[nginx config structure]]: structure is the include tree; this note is paths + rotation lifecycle.

## Mistakes to Avoid
- Reloading without `nginx -t` — bad config fails reload if you skip the test.
- Broken `sites-enabled` symlink to a deleted file — `nginx -t` fails on boot.
- Hand-editing `.log.1.gz` — use `zgrep` instead.
- Disabling logrotate postrotate USR1 — Nginx keeps writing to the old inode → full disk.
