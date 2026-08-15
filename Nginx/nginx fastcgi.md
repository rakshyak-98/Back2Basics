[[Configuration]] [[nginx files]] [[php error]] [[How does directive work]]

# nginx fastcgi

> Hand PHP (and other FastCGI apps) to a pool — Nginx speaks FastCGI to php-fpm over a unix socket or TCP, not by embedding the language.

## Interview Relevance

Classic ops interview: why `.php` downloads instead of runs, what `SCRIPT_FILENAME` must be, and how php-fpm socket paths relate to 502s.

## Sources

- [nginx.org — ngx_http_fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html) — deep-dive
- [PHP-FPM documentation](https://www.php.net/manual/en/install.fpm.php) — overview

## Core Definition

FastCGI is a binary protocol between a web server and an application process manager; Nginx’s `fastcgi_pass` sends the request to php-fpm (or another FastCGI server) instead of executing code in-process.

## Key Concepts

- **Two routes for “other languages”:** reverse proxy (HTTP upstream) or FastCGI (`fastcgi_pass`) — PHP usually uses the latter via FPM.
- **`SCRIPT_FILENAME`:** Must be the real filesystem path PHP can open — often `$document_root$fastcgi_script_name`.
- **`fastcgi_params` / `fastcgi.conf`:** Parameter templates; `fastcgi.conf` typically sets `SCRIPT_FILENAME`.
- **Socket vs TCP:** `unix:/run/php/php8.2-fpm.sock` vs `127.0.0.1:9000` — permissions and path must match the pool.

## Technical Details

```nginx
location ~ \.php$ {
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

See also `fastcgi_split_path_info` for PATH_INFO-style frameworks: [ngx_http_fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_split_path_info).

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | php-fpm socket down | `systemctl status php8.2-fpm`; socket path |
| File download instead of execute | missing `fastcgi_pass` | PHP must pass to FPM not bare `root` |
| PATH_INFO broken | split path info rules | Use documented `try_files` + fastcgi pattern |

## Real-World Applications

WordPress/Laravel on Debian: `try_files` front controller plus `location ~ \.php$` to the distro php-fpm socket.

## Pros/Cons or Trade-offs

- **Pro:** Isolates PHP in FPM pools (user, memory limits) separate from Nginx workers.
- **Con:** More moving parts than a pure static/`proxy_pass` stack — socket and param bugs are common.

## Comparison

- vs Apache `mod_php`: prefer php-fpm + Nginx (or Apache proxy) for isolation.
- vs HTTP `proxy_pass` to Node/Go: FastCGI is specific to FastCGI apps; most modern apps use HTTP reverse proxy instead.

## Mistakes to Avoid

- Leaving `SCRIPT_FILENAME` unset or wrong so PHP cannot open the script.
- Serving `.php` as static files when the FastCGI location does not match.
- Hard-coding an old socket path after a PHP version upgrade.
