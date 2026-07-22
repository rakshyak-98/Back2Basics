[[php error]] [[PHP-FPM]] [[Linux/commands/Services commands]]

# PHP

> Server-side language runtime — install extensions, pair with FPM, tune for web workloads.

## Mental model

PHP executes per request (FPM worker pool) or CLI (cron, Composer). The **SAPI** (FPM, CLI, Apache module) loads `php.ini` + conf.d snippets. Composer manages dependencies; autoload maps classes. Production = FPM behind Nginx/Apache, opcache on, errors to log not browser.

## Standard config / commands

### Debian/Ubuntu install

```bash
sudo apt update
sudo apt install php8.2-fpm php8.2-cli php8.2-mysql php8.2-curl php8.2-xml php8.2-mbstring
php -v
php -m                    # loaded extensions
```

### Composer (project)

```bash
curl -sS https://getcomposer.org/installer | php
php composer.phar install --no-dev --optimize-autoloader
```

### Key paths

| Path | Purpose |
|------|---------|
| `/etc/php/8.2/fpm/php.ini` | FPM php.ini |
| `/etc/php/8.2/cli/php.ini` | CLI (cron/composer) |
| `/etc/php/8.2/fpm/pool.d/www.conf` | FPM pool |
| `vendor/autoload.php` | App entry autoload |

### Production php.ini knobs

```ini
display_errors = Off
log_errors = On
error_log = /var/log/php/error.log
opcache.enable = 1
opcache.validate_timestamps = 0   ; restart FPM on deploy
memory_limit = 256M
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Extension missing | `php -m` | `apt install php8.2-<ext>`; restart FPM |
| CLI vs FPM different behavior | Compare `php -i` vs FPM | Align ini files |
| Composer memory exhausted | `memory_limit` | `COMPOSER_MEMORY_LIMIT=-1 composer install` |
| Version mismatch | `php -v` on nginx vs cli | Point nginx to correct FPM socket version |

## Gotchas

> [!WARNING]
> **Editing wrong php.ini** — cron uses CLI ini; website uses FPM ini.
>
> **World-writable upload dir** — RCE via uploaded `.php` if webroot includes uploads.
>
> **Deprecated `mysql_*`** — use PDO/mysqli.

## When NOT to use

- Don't use built-in PHP dev server (`php -S`) in production — no FPM isolation or robustness.
- Don't install every extension "just in case" — attack surface and memory.

## Related

[[php error]] [[PHP-FPM]] [[apache/apache modules]] [[Nginx/Configuration]]
