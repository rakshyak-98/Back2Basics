[[Configuration]] [[How does directive work]] [[nginx SPA deployment]] [[https]] [[static file]]

# web server

> HTTP server maps a URL path to a handler — today the path is usually a resource id, not a literal filename on disk.

```txt
        web server ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Baseline web review: how URL paths relate to files, SPA fallback, reverse-…

## Sources
- [MDN — What is a web server?](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_web_server) — overview
- [nginx.org — Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html) — overview
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — deep-dive

## Key Concepts
- **URL ≠ file:** `https://example.com/api/users/1` is a route/resource id, not necessarily `/u…
- **Static mapping:** `root` + `try_files` for real files.
- **SPA mapping:** fall back to `index.html` for client routes.
- **Proxy mapping:** forward path (or rewritten URI) to an application.


- **Core:** A web server accepts HTTP requests and produces responses by mapping host + p…

## Technical Details
```
https://example.com/api/users/1
         │      │    └── route / resource id (not necessarily a file)
         host   path
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on client route refresh | No SPA fallback | `try_files … /index.html` |
| Static file exposed | Path traversal | Normalize paths; deny `..` |
| Wrong MIME | `mime.types` | `include mime.types; default_type` |
| `/api` hits static | Location order | Specific `location /api/` before `/` |
| Case sensitivity | Linux FS case-sensitive | Match exact filename case |

## Mistakes to Avoid
- **Mistake:** Assuming URL path always equals filesystem path
- **Mistake:** Mixed content
- **Mistake:** `autoindex on` in production — leaks directory structure
- **Mistake:** Mapping user-upload directories under an executable web root
- **Mistake:** Relying on `.html` suffix for security

## Pros/Cons or Trade-offs
- **Pro:** Clear separation — edge handles TLS/static; app handles business logic.
- **Con:** Misunderstanding path→file mapping causes SPA and REST 404s.

## Comparison
- vs pure static host: no dynamic routes or auth beyond what the edge provides.
- vs app-only listen on :443: edge web server still useful for TLS, buffering, and static offload.
- vs [[nginx SPA deployment]]: general web-server path model vs SPA-specific fallback checklist.


### Use cases
- Nginx (or Apache/Caddy) terminating TLS, serving a marketing site’s static fi…
