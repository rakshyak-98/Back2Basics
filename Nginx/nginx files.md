[[Nginx/Configuration]] [[Linux/loggging]] [[Linux/commands/journalctl]]

# Nginx files (paths and log rotation)

> Where config, logs, and runtime state live on disk — first stop when nginx -t passes but site wrong or logs vanish.

## Mental model

Package layout varies Debian (`/etc/nginx/`) vs RHEL (`/etc/nginx/` similar) but patterns hold: **main config** includes **snippets** and **sites-enabled**. Logs go to `/var/log/nginx/` unless redirected. **logrotate** truncates logs without dropping open FDs if postrotate sends `USR1` to nginx.

```
/etc/nginx/nginx.conf → sites-enabled/* → access.log / error.log
         ↓ logrotate (daily)
/var/log/nginx/*.log.1.gz
```

## Standard config / commands

### Common paths (Debian/Ubuntu)

| Path | Purpose |
|------|---------|
| `/etc/nginx/nginx.conf` | Main include tree |
| `/etc/nginx/sites-available/` | Site defs |
| `/etc/nginx/sites-enabled/` | Symlinks to enabled sites |
| `/etc/nginx/conf.d/*.conf` | Drop-in snippets |
| `/var/log/nginx/access.log` | Request log |
| `/var/log/nginx/error.log` | Errors, upstream failures |
| `/etc/logrotate.d/nginx` | Rotation policy |
| `/run/nginx.pid` | Master PID |

### Enable site

```bash
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Tail logs

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### logrotate snippet (typical)

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Edit has no effect | Which file included? | `nginx -T`; enable correct site symlink |
| Disk full | `/var/log/nginx` size | Force rotate; lower retention; fix log flood |
| Empty error log | `error_log` path override | Grep `error_log` in `nginx -T` |
| Permission denied on log | nginx user | `www-data` ownership on log dir |
| Site enabled twice | Duplicate server_name | One conf per `server_name`:port |
| PID file stale | Crash | `systemctl restart nginx` |

## Gotchas

> [!WARNING]
> **Reload vs restart** — bad config fails reload silently if you skip `-t`.
>
> **Symlink broken** — sites-enabled points to deleted file → nginx -t fail on boot.
>
> **JSON access log to same disk as app data** — IO contention; ship to centralized logging.

## When NOT to use

- Don't hand-edit `.log.1.gz` — use `zgrep`/`zgrep error`.
- Don't disable logrotate postrotate USR1 — nginx keeps writing to old inode → full disk.

## Related

[[Nginx/Configuration]] [[Nginx/How does directive work]] [[Linux/loggging]]
