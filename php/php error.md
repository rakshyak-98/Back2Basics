[[PHP-FPM]] [[apache/apache modules]] [[Nginx/Configuration]]

# PHP errors

> Apache/PHP-FPM startup and runtime failures — read the error log line, fix the socket/port/config mismatch.

## Mental model

PHP in production usually sits behind **Apache** (`mod_php` rare now) or **Nginx → PHP-FPM** (Unix socket or TCP). "No listening sockets" means the web server couldn't bind its port — often Apache still running or port 80/443 taken. PHP errors also surface in `error_log`, FPM pool logs, and HTTP 502 from Nginx when FPM is down.

## Standard config / commands

### Find what's on port 80/443

```bash
sudo ss -tlnp | grep -E ':80|:443'
sudo systemctl status apache2 nginx php*-fpm
```

### Apache graceful restart

```bash
sudo apachectl configtest
sudo systemctl restart apache2
sudo tail -f /var/log/apache2/error.log
```

### PHP-FPM (with Nginx)

```bash
sudo php-fpm8.2 -t                    # or php-fpm -t
sudo systemctl restart php8.2-fpm
sudo tail -f /var/log/php8.2-fpm.log
```

### Nginx ↔ FPM socket must match

```nginx
# nginx site
fastcgi_pass unix:/run/php/php8.2-fpm.sock;
```

```ini
; /etc/php/8.2/fpm/pool.d/www.conf
listen = /run/php/php8.2-fpm.sock
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `no listening sockets available, shutting down` | `ss -tlnp`, Apache already up | Stop duplicate Apache; free port 80 |
| `Address already in use` | Conflicting nginx/apache | One listener per port; disable unused service |
| 502 Bad Gateway | FPM running? socket path | Restart FPM; align socket in nginx + pool |
| Blank page, no log | `display_errors` off | Check FPM/Apache error log; enable log in dev only |
| `Permission denied` on socket | www-data group | `listen.owner/group/mode` in pool config |
| Max children reached | FPM slow log | Raise `pm.max_children`; fix slow queries |

## Gotchas

> [!WARNING]
> **`apachectl` vs `apache2ctl`** — wrong binary on Debian/Ubuntu = confusing paths.
>
> **Editing php.ini but FPM uses pool ini** — `php_admin_value` in pool overrides.
>
> **Opcache stale after deploy** — restart FPM on deploy or tune `validate_timestamps`.

## When NOT to use

- Don't enable `display_errors=On` in production — leaks paths and logic.
- Don't run Apache and Nginx both binding :80 without intentional reverse-proxy setup.

## Related

[[PHP-FPM]] [[apache/apache modules]] [[Nginx/Configuration]] [[Linux/commands/journalctl]]

## PHP timezone error
```
Fatal error: date(): Timezone database is corrupt - this should *never* happen!
in /home/mihir/GitHub/TheOterraWebsite/TheOtium/Website-Admin/system/core/Log.php
on line 185

```
- it means PHP reached its date/time subsystem and encountered an internal inconsistency in the timezone data/state. It is not simply saying: "You forgot to set `date.timezone`"

`date()` is a **built-in PHP function.** Your MVC framework didn't create it. Its job is to convert the current time into a human-readable format.

> PHP timezone support is based on timezone data that is compiled/included with PHP, depending on how PHP was build and packaged. On common Linux distributions, the PHP package may be built/uploaded alongside the system timezone data, but PHP does not simply read `/usr/share/zoneinfo/Asia/Kolkata` every time `date()` executes.