[[Configuration]] [[nginx SPA deployment]] [[How does directive work]] [[mime type]]

# static file

> Serve files from disk with `root`/`alias` and `try_files` — check `$uri`, then `$uri/`, then 404 (or SPA/app fallback) without hitting the app.

```txt
        static file ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Checks whether you can configure efficient static serving, explain `try_files…

## Sources
- [nginx.org — Serving static content](https://nginx.org/en/docs/beginners_guide.html) — overview
- [nginx.org — try_files](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files) — deep-dive
- [nginx.org — ngx_http_headers_module (expires)](https://nginx.org/en/docs/http/ngx_http_headers_module.html) — overview

## Key Concepts
- **`try_files $uri $uri/ =404`:** Exact file → directory (with `index`) → hard 404.
- **`$uri`:** Request path mapped under `root` (e.g
- **Avoid backend calls:** Static locations keep CSS/JS/images off PHP/Node unless another location matc…
- **Caching headers:** `expires` + `Cache-Control` for fingerprinted assets.

## Technical Details
```nginx
location / {
    try_files $uri $uri/ =404;
}
```

- What it means:

- If `/style.css` exists under `root` → serve it.
- If `/blog/` is a directory with `index.html` → serve that (per `index`).
- If neither exists → `404 Not Found` (no PHP fallback in this example).

```nginx
location /assets/ {
    alias /var/www/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 Forbidden | directory listing off; perms | `chmod` for nginx user; `index` directive |
| Stale asset after deploy | browser cache | Cache-bust filenames; shorten `expires` on HTML |
| Wrong MIME type | missing types block | `include mime.types;` |

## Mistakes to Avoid
- **Mistake:** `alias` trailing-slash mismatches with the `location` prefix
- **Mistake:** Serving user uploads from a path that can execute scripts
- **Mistake:** Omitting `mime.types` so browsers mis-handle assets

## Pros/Cons or Trade-offs
- **Pro:** Extremely efficient with `sendfile`; keeps app servers free.
- **Con:** User uploads next to executable scripts under the same root is a security footgun.

## Comparison
- vs [[nginx SPA deployment]]: static `=404` vs fallback to `index.html` for client routes.
- vs `proxy_pass` everything: proxying static assets wastes app capacity.


### Use cases
- CDN-origin or edge Nginx serving built frontend assets
