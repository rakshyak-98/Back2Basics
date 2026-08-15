[[php error]] [[PHP-FPM]] [[pma token]]

# PHP

> Server-side language runtime — execute scripts via FPM or CLI, load extensions, and tune `php.ini` for web workloads.

## Interview Relevance

Interviewers expect FPM-behind-Nginx as the modern default, Composer autoload, opcache, and the CLI vs FPM ini split.

## Sources

- [PHP — Manual](https://www.php.net/manual/en/) — deep-dive
- [PHP — OPcache](https://www.php.net/manual/en/book.opcache.php) — overview

## Key Concepts

- **SAPI:** FPM, CLI, (legacy) Apache module → how PHP is hosted.
- **Per-request workers:** typical FPM model → one request at a time per worker.
- **Composer:** dependency manager + PSR autoload → `vendor/autoload.php`.
- **Opcache:** caches compiled bytecode → turn off timestamp validation in production and restart on deploy.

## Technical Details

```bash
sudo apt install php8.2-fpm php8.2-cli php8.2-mysql php8.2-curl php8.2-xml php8.2-mbstring
php -v && php -m
composer install --no-dev --optimize-autoloader
```

| Path | Purpose |
|------|---------|
| `/etc/php/8.2/fpm/php.ini` | Web requests |
| `/etc/php/8.2/cli/php.ini` | Cron/Composer |
| `pool.d/www.conf` | FPM pool |

```ini
display_errors = Off
log_errors = On
opcache.enable = 1
opcache.validate_timestamps = 0
memory_limit = 256M
```

## Real-World Applications

Production API: Nginx → PHP-FPM socket → front controller; cron uses CLI binary with its own ini.

**Example:** Extension missing in web but present in CLI — you edited the wrong ini; align FPM conf.d.

## Pros/Cons or Trade-offs

- **Pro:** Huge web ecosystem; solid FPM hosting model.
- **Con:** Request-bound concurrency needs many workers for parallelism.

## Comparison

- vs Node: PHP workers are usually blocking per request; Node is event-loop by default.
- vs [[PHP-FPM]]: PHP is the language/runtime; FPM is the preferred process manager SAPI.

## Mistakes to Avoid

- `display_errors=On` in production.
- World-writable upload directories inside the web root.
- Using ancient `mysql_*` APIs instead of PDO/mysqli.
