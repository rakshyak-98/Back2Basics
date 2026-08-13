[[Nginx/Configuration]] [[Nginx/How does directive work]] [[Security/https]]

# Web server (URL path vs filesystem)

> HTTP server maps URL path to handler — today "file" in the path is usually a **resource identifier**, not a literal on-disk filename.

---

## Index

- [[#Decision context]]
- [[#Comparison matrix]]
- [[#Selection guide]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#When NOT to use]]
- [[#Gotchas]]
- [[#Related]]

## Decision context

…

## Comparison matrix

| Criterion | Option A | Option B |
|-----------|----------|----------|
| … | … | … |

## Selection guide

- Choose **A** when …
- Choose **B** when …

## Mental model

**Say it in one breath:** Browser sends `GET /blog/post-1 HTTP/1.1`. Server matches **Host** + **path** to virtual host and location. Static servers map path → filesystem (`root` + URI). application servers (Node, PHP-FPM.


```
https://example.com/api/users/1
         │      │    └── route / resource id (not necessarily /users/1.txt on disk)
         host   path
```

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on client route refresh | No SPA fallback | `try_files … /index.html` |
| Static file exposed | Path traversal | Normalize paths; deny `..` |
| Wrong MIME | `mime.types` | `include mime.types; default_type` |
| `/api` hits static | Location order | Specific `location /api/` before `/` |
| Case sensitivity | Linux FS case-sensitive | Match exact filename case |

## When NOT to use

- Don't map user-upload dir under web root executable — serve from object storage or separate domain.
- Don't rely on `.html` extension hiding — content-type and authentication matter, not suffix.

## Gotchas

> [!WARNING]
> **Assuming URL path = file path** — breaks for REST, Next.js, and reverse proxies.
>
> **Mixed content** — HTTPS page loading HTTP assets blocked by browser.
>
> **Directory listing** — `autoindex on` leaks structure; off in prod.

## Related

[[Nginx/nginx SPA deployment]] [[Nginx/How does directive work]] [[Security/https]]
