[[Configuration]] [[nginx files]] [[php error]] [[How does directive work]]

# nginx fastcgi

> Hand PHP (and other FastCGI apps) to a pool — Nginx speaks FastCGI to php-fpm over a unix socket or TCP, not by embedding the language.

```txt
        nginx fastcgi ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Classic ops review: why `.php` downloads instead of runs, what `SCRIPT_FIL…

## Sources
- [nginx.org — ngx_http_fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html) — deep-dive
- [PHP-FPM documentation](https://www.php.net/manual/en/install.fpm.php) — overview

## Key Concepts
- **Two routes for “other languages”:** reverse proxy (HTTP upstream) or FastCGI (`fastcgi_pass`)
- **`SCRIPT_FILENAME`:** Must be the real filesystem path PHP can open
- **`fastcgi_params` / `fastcgi.conf`:** Parameter templates; `fastcgi.conf` typically sets `SCRIPT_FILENAME`.
- **Socket vs TCP:** `unix:/run/php/php8.2-fpm.sock` vs `127.0.0.1:9000`


- **Core:** FastCGI is a binary protocol between a web server and an application process …

## Technical Details
```nginx
location ~ \.php$ {
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

- See also `fastcgi_split_path_info` for PATH_INFO-style frameworks: [ngx_http_…

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | php-fpm socket down | `systemctl status php8.2-fpm`; socket path |
| File download instead of execute | missing `fastcgi_pass` | PHP must pass to FPM not bare `root` |
| PATH_INFO broken | split path info rules | Use documented `try_files` + fastcgi pattern |

## Mistakes to Avoid
- **Mistake:** Leaving `SCRIPT_FILENAME` unset or wrong so PHP cannot open the …
- **Mistake:** Serving `.php` as static files when the FastCGI location does no…
- **Mistake:** Hard-coding an old socket path after a PHP version upgrade

## Pros/Cons or Trade-offs
- **Pro:** Isolates PHP in FPM pools (user, memory limits) separate from Nginx workers.
- **Con:** More moving parts than a pure static/`proxy_pass` stack — socket and param bugs are common.

## Comparison
- vs Apache `mod_php`: prefer php-fpm + Nginx (or Apache proxy) for isolation.
- vs HTTP `proxy_pass` to Node/Go: FastCGI is specific to FastCGI apps


### Use cases
- WordPress/Laravel on Debian: `try_files` front controller plus `location ~ \.…
