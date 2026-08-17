[[How does directive work]] [[Configuration]] [[nginx SPA deployment]] [[nginx fastcgi]]

# directives

> Named settings inside Nginx context blocks — `server`, `listen`, `location`, `proxy_pass`, and friends — that decide how each request is handled.

```txt
        directives ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers expect you to name the core directives and what each does (virtu…

## Sources
- [nginx.org — Alphabetical index of directives](https://nginx.org/en/docs/dirindex.html) — overview
- [nginx.org — ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html) — deep-dive
- [nginx.org — ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) — deep-dive

## Key Concepts
- **`server`:** Virtual server — groups config for a domain/port.
- **`listen`:** IP/port (and SSL/http2 flags) this server accepts.
- **`server_name`:** Which `server {}` wins for an incoming `Host` / SNI name.
- **`root` / `index`:** Base directory for static files; default file for directory requests.
- **`location`:** Path-based handler (static, proxy, FastCGI, rewrite).
- **`proxy_pass` / `proxy_set_header`:** Forward to an upstream; pass `Host`, `X-Real-IP`, `X-Forwarded-For`.
- **`error_page`:** Custom page for specific status codes (e.g
- **`upstream`:** Named backend pool for load balancing.
- **`gzip` / `gzip_types`:** Response compression for selected MIME types.
- **`auth_basic` / `auth_basic_user_file`:** HTTP Basic authentication.

## Technical Details
```nginx
server {
	gzip on;
	gzip_types text/plain application/json;
}
```

- Minimal server block (see [[Configuration]] for fuller examples):

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong server block chosen | `server_name` mismatch; `default_server` | Check `nginx -T`; SNI and listen order |
| 404 on existing file | `root`/`alias` path wrong | `namei -l /path`; permissions for `www-data` |
| Proxy returns 502 | upstream down; bad `proxy_pass` URL | `curl` backend; trailing slash rules |
| Config test fails | typo in directive name | `nginx -t` shows file:line |

## Mistakes to Avoid
- **Mistake:** Treating `alias` like `root`
- **Mistake:** Putting TLS certificates only on `default_server` when you serve…
- **Mistake:** Relying on directive order folklore instead of documented locati…

## Pros/Cons or Trade-offs
- **Pro:** Small set of directives covers reverse proxy + static + TLS for most sites.
- **Con:** Inheritance and merge rules across nested blocks surprise people — last-wins and context limits matter.

## Comparison
- vs [[How does directive work]]: this note is a directive cheat sheet
- vs Apache `mod_*` directives: different names and merge model


### Use cases
- Define one `server` per hostname, `location /` for static or SPA fallback, an…
