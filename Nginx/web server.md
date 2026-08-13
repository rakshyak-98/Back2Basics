[[Nginx/Configuration]] [[Nginx/How does directive work]] [[Security/https]]

# Web server (URL path vs filesystem)

> HTTP server maps URL path to handler — today "file" in the path is usually a **resource identifier**, not a literal on-disk filename.

---

## How it works


```
https://example.com/api/users/1
         │      │    └── route / resource id (not necessarily /users/1.txt on disk)
         host   path
```


## Configuration and commands

### Static files

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    root /var/www/html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### SPA fallback

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### App reverse proxy (path preserved)

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:3000;   # URI forwarded as /api/...
}
```


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on client route refresh | No SPA fallback | `try_files … /index.html` |
| Static file exposed | Path traversal | Normalize paths; deny `..` |
| Wrong MIME | `mime.types` | `include mime.types; default_type` |
| `/api` hits static | Location order | Specific `location /api/` before `/` |
| Case sensitivity | Linux FS case-sensitive | Match exact filename case |


## Comparison

| Criterion | Option A | Option B |
|-----------|----------|----------|
| … | … | … |


## How to choose

- Choose **A** when …
- Choose **B** when …


## Gotchas

> [!WARNING]
> **Assuming URL path = file path** — breaks for REST, Next.js, and reverse proxies.
>
> **Mixed content** — HTTPS page loading HTTP assets blocked by browser.
>
> **Directory listing** — `autoindex on` leaks structure; off in prod.


## When not to use

- Don't map user-upload dir under web root executable — serve from object storage or separate domain.
- Don't rely on `.html` extension hiding — content-type and authentication matter, not suffix.


## Related

[[Nginx/nginx SPA deployment]] [[Nginx/How does directive work]] [[Security/https]]

## Sources

- [Wikipedia — web server](https://en.wikipedia.org/wiki/web_server)
