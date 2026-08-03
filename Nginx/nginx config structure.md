[[Nginx/Configuration]] [[nginx files]] [[nginx fastcgi]] [[/etc files]] [[Linux]]

# nginx config structure

> One-line: **`/etc/nginx/` layout on Debian/Ubuntu** — how `nginx.conf` includes sites, snippets, and param files into one effective config tree. **Package `nginx` + `nginx-common`.**

## Mental model

Nginx does not run "one big file." The **master config** (`nginx.conf`) sets global defaults, then **`include`** pulls in everything else at parse time. Debian/Ubuntu split **reusable fragments** (params, mime types, snippets) from **virtual hosts** (`sites-available` → `sites-enabled`).

```
/etc/nginx/nginx.conf          ← entry point (main + events + http { … includes … })
        │
        ├── mime.types
        ├── modules-enabled/*.conf   ← load_module directives
        ├── conf.d/*.conf            ← optional drop-ins (often empty on Debian)
        ├── snippets/*.conf          ← reusable location/server fragments
        └── sites-enabled/*  ──symlink──► sites-available/*
                    │
                    └── include fastcgi_params / proxy_params / uwsgi_params
```

| Pattern | Directory / file | Edit for… |
|---------|------------------|-----------|
| Global defaults | `nginx.conf` | Workers, gzip, logging, default `server` |
| Enable a vhost | `sites-available` + `sites-enabled` symlink | Per-domain `server { }` blocks |
| Shared fragment | `snippets/` | PHP FastCGI block, SSL params, security headers |
| Backend param sets | `*_params`, `fastcgi.conf` | FastCGI / proxy / uWSGI / SCGI headers |
| MIME map | `mime.types` | New file extensions → `Content-Type` |
| Dynamic modules | `modules/` + `modules-enabled/` | Optional `.so` modules (image filter, geoip, …) |

**Effective config truth:** `sudo nginx -T` (merged, with comments stripped). **Syntax only:** `sudo nginx -t`.

## Standard config / commands

### Directory map (`ls /etc/nginx/`)

| Name | Type | Purpose |
|------|------|---------|
| `nginx.conf` | file | Root config — `user`, `worker_processes`, `events`, `http` block with includes |
| `conf.d/` | dir | Drop-in `*.conf` files included from `http { }` — common on RHEL; on Debian often unused or for package snippets |
| `sites-available/` | dir | Full `server { }` definitions — **source of truth** for vhosts |
| `sites-enabled/` | dir | Symlinks to enabled sites — only these are loaded |
| `snippets/` | dir | Small reusable includes (`fastcgi-php.conf`, `ssl-params.conf`, …) |
| `mime.types` | file | Extension → MIME type table (`types { … }`) |
| `fastcgi_params` | file | Default CGI environment variables for `fastcgi_pass` |
| `fastcgi.conf` | file | `include fastcgi_params;` + `SCRIPT_FILENAME` preset |
| `proxy_params` | file | Common `proxy_set_header` lines for `proxy_pass` |
| `scgi_params` | file | Parameter set for SCGI backends |
| `uwsgi_params` | file | Parameter set for uWSGI backends |
| `modules/` | dir | Installed dynamic module `.so` binaries (Debian `libnginx-mod-*` packages) |
| `modules-enabled/` | dir | Symlinks to `modules/*.conf` — each file is a `load_module` directive |
| `koi-utf` / `koi-win` / `win-utf` | file | Legacy charset conversion maps (KOI8-R / Windows-1251) — rarely touched today |

### `nginx.conf` — what the main file owns

Typical Debian skeleton:

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
    # multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

| Section | Scope | Typical edits |
|---------|-------|---------------|
| Top-level | Master process | `user`, `worker_processes`, `pid` |
| `events { }` | Connection model | `worker_connections`, `multi_accept` |
| `http { }` | All HTTP servers | Logging, gzip, SSL defaults, `include` sites |

> [!NOTE]
> Some installs also define a **default `server`** block directly in `nginx.conf` or `sites-available/default` — remove/disable the default site if it captures traffic unexpectedly.

### `sites-available` vs `sites-enabled`

Debian convention: **define once, enable with symlink** (same idea as systemd `wants`).

```bash
# Create vhost
sudoedit /etc/nginx/sites-available/myapp.conf

# Enable
sudo ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/

# Disable (keeps file, stops loading)
sudo unlink /etc/nginx/sites-enabled/myapp.conf

sudo nginx -t && sudo systemctl reload nginx
```

```nginx
# /etc/nginx/sites-available/myapp.conf
server {
    listen 80;
    server_name app.example.com;
    root /var/www/myapp;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**`conf.d/` vs `sites-enabled/`:** both are just `include` targets. Pick **one convention** per host — mixing is fine but confusing. Many teams use `sites-*` for vhosts and `conf.d/` for global HTTP snippets (rate-limit zones, upstream blocks).

### `snippets/` — DRY includes

Packaged examples (names vary by version):

```nginx
# snippets/fastcgi-php.conf — typical contents
fastcgi_split_path_info ^(.+\.php)(/.+)$;
fastcgi_pass unix:/run/php/php8.2-fpm.sock;
fastcgi_index index.php;
include fastcgi.conf;
```

```nginx
# In a server block
location ~ \.php$ {
    include snippets/fastcgi-php.conf;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

Use `snippets/` for: SSL ciphers, security headers, ACME challenges, repeated `proxy_set_header` sets.

### Param files — FastCGI, proxy, uWSGI, SCGI

These files only define **`fastcgi_param`**, **`proxy_set_header`**, or **`uwsgi_param`** lines. They do **not** start servers or open sockets — you still need `fastcgi_pass`, `proxy_pass`, or `uwsgi_pass` in your `location`.

| File | Include when | Sets |
|------|--------------|------|
| `fastcgi_params` | `fastcgi_pass` to PHP-FPM, etc. | `QUERY_STRING`, `REQUEST_METHOD`, `REMOTE_ADDR`, … |
| `fastcgi.conf` | Same, shortcut | `include fastcgi_params;` + `SCRIPT_FILENAME` |
| `proxy_params` | `proxy_pass` to HTTP upstream | `Host`, `X-Real-IP`, `X-Forwarded-For`, … |
| `uwsgi_params` | `uwsgi_pass` | uWSGI protocol variables |
| `scgi_params` | `scgi_pass` | SCGI protocol variables |

```nginx
# Minimal PHP location
location ~ \.php$ {
    include snippets/fastcgi-php.conf;
}

# Reverse proxy (modern apps often set headers inline instead)
location / {
    include proxy_params;
    proxy_pass http://127.0.0.1:3000;
}
```

**`fastcgi_params` vs `fastcgi.conf`:** `fastcgi.conf` is a superset — it includes `fastcgi_params` and adds `SCRIPT_FILENAME`. Use one pattern consistently; duplicating `SCRIPT_FILENAME` causes subtle bugs.

→ Deeper FastCGI routing: [[nginx fastcgi]]

### `mime.types`

Maps file extensions to `Content-Type`. Included once in `http { }`:

```nginx
include /etc/nginx/mime.types;
default_type application/octet-stream;
```

```nginx
# Add a custom type in conf.d or http block
types {
    application/vnd.app+json  appjson;
}
```

Wrong MIME → browser downloads instead of rendering, or breaks JS modules (`application/javascript` vs `text/javascript` legacy).

### `modules/` and `modules-enabled/`

Debian ships optional modules as packages (`libnginx-mod-http-geoip`, etc.). Each enabled module is a tiny `.conf`:

```nginx
# modules-enabled/50-mod-http-geoip.conf
load_module modules/ngx_http_geoip_module.so;
```

```bash
ls -la /etc/nginx/modules-enabled/
# enable: ln -s ../modules-available/50-mod-http-geoip.conf modules-enabled/
```

Dynamic modules load **before** `events { }` — syntax errors here prevent nginx from starting at all.

### Charset maps (`koi-utf`, `koi-win`, `win-utf`)

Legacy **character recoding** tables for Cyrillic encodings. Modern UTF-8 sites rarely reference them. If present in old configs:

```nginx
charset koi8-r;
source_charset koi8-r;
```

Prefer UTF-8 end-to-end; treat these files as package defaults you normally leave alone.

### Inspect and validate

```bash
sudo nginx -t                           # syntax
sudo nginx -T | less                    # full merged config
sudo nginx -T | grep -E 'server_name|root|proxy_pass'
readlink -f /etc/nginx/sites-enabled/*  # which vhosts are active
grep -r include /etc/nginx/nginx.conf /etc/nginx/sites-enabled/
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| New site not loaded | Symlink missing | `ln -s sites-available/foo sites-enabled/`; `nginx -t` |
| Wrong site answers | Default server / duplicate `server_name` | `nginx -T \| grep server_name`; disable `default` site |
| `unknown directive` after package install | Module not loaded | Enable module in `modules-enabled/` |
| PHP 404 / empty response | Wrong param file | Use `fastcgi.conf` or set `SCRIPT_FILENAME`; see [[nginx fastcgi]] |
| JS/CSS served as download | MIME missing | `mime.types`; `default_type`; custom `types { }` |
| Config edit ignored | Edited `sites-available` but not enabled | Check `sites-enabled` symlink |
| `nginx -t` fails on include | Broken symlink | `readlink -f` each enabled site |
| Duplicate upstream / limit zone | Same zone name in `conf.d` + site | One definition per `limit_req_zone` name |

## Gotchas

> [!WARNING]
> **`include` does not shell-expand** — no `~`, `$VAR`, or globs beyond what nginx supports (`*.conf` only). Generate absolute paths in CI/templates.

> [!WARNING]
> **Two enabled files, same `listen` + `server_name`** — nginx may warn; unpredictable default server selection.

> [!WARNING]
> **Editing `sites-available` without reload** — running workers keep old config until `systemctl reload nginx` (after `nginx -t`).

- **`conf.d/default.conf` on some distros** — conflicts with `sites-enabled/default`; know which include wins (order in `nginx.conf`).
- **`proxy_params` is dated** — many configs set `X-Forwarded-Proto` inline; copy from snippets or modern reference configs.
- **Package upgrades** — `nginx-common` may add new files under `snippets/`; diff after `apt upgrade`.
- **`modules-enabled` out of sync** — removing a package leaves broken `load_module` symlinks.

## When NOT to use

- **Don't put secrets in world-readable conf** — TLS keys need `root:www-data` + `640` or systemd credentials; prefer certbot paths under `/etc/letsencrypt/`.
- **Don't duplicate full `server` blocks** — extract shared SSL and headers to `snippets/`.
- **Don't use `sites-available` on minimal containers** — single `nginx.conf` or one `default.conf` is fine when orchestration replaces symlinks.
- **Don't edit `mime.types` for one app** — use `types { }` in that vhost or a `conf.d` snippet.

## Related

[[Nginx/Configuration]] [[nginx files]] [[nginx fastcgi]] [[nginx auto file configuration]] [[How does directive work]] [[/etc files]] [[PHP-FPM]]
