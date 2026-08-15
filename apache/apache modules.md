[[apache command]] [[PHP-FPM]] [[Proxy/Reverse Proxy]] [[Security/TLS (Transport Layer Security)]]

# Apache modules

> Features loaded into httpd — static (compiled in) or shared (`LoadModule`) so you toggle capability without rebuilding Apache.

## Interview Relevance

Interviewers want MPM choice (event vs prefork), why fewer modules are safer, and how `rewrite`/`ssl`/`proxy` show up in production vhosts.

## Sources

- [Apache — Dynamic Shared Object (DSO) Support](https://httpd.apache.org/docs/current/dso.html) — deep-dive
- [Apache — MPM](https://httpd.apache.org/docs/current/mpm.html) — overview

## Key Concepts

- **Static vs shared:** baked-in vs `.so` via `LoadModule`.
- **MPM:** prefork/worker/event → concurrency model; PHP-FPM pairs with event/worker, not classic `mod_php`+prefork.
- **Least modules:** smaller memory and attack surface.
- **Distro packaging:** `a2enmod` / `libapache2-mod-*` on Debian.

## Technical Details

```bash
apache2ctl -M
sudo a2enmod rewrite ssl headers proxy proxy_http
sudo a2dismod mpm_prefork   # switch carefully
sudo apachectl configtest && sudo systemctl reload apache2
```

```apache
LoadModule rewrite_module modules/mod_rewrite.so
```

| Module | Purpose |
|--------|---------|
| `mpm_event` | Concurrent connections |
| `ssl` | TLS |
| `rewrite` | URL rewriting |
| `headers` | Security headers |
| `proxy` + `proxy_http` / `proxy_fcgi` | Reverse proxy / FastCGI |

## Real-World Applications

TLS terminator + reverse proxy to an app, or `proxy_fcgi` to PHP-FPM, with `rewrite` for front-controller frameworks.

**Example:** `Invalid command 'RewriteRule'` after deploy — `mod_rewrite` not loaded.

## Pros/Cons or Trade-offs

- **Pro:** Enable only what you need; swap MPM for workload.
- **Con:** Wrong MPM + `mod_php` combinations cause mysterious instability.

## Comparison

- vs Nginx modules: Nginx often needs rebuild for third-party modules; Apache DSO is more dynamic on distros.
- vs [[PHP-FPM]]: modules are httpd features; FPM is the PHP worker pool.

## Mistakes to Avoid

- Loading `mod_info`/`mod_status` publicly without IP allowlists.
- Dual `LoadModule` lines for the same module.
- New stacks still enabling `mod_php` instead of FPM.
