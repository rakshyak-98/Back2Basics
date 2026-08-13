<!-- note-strategy: operational -->
[[Nginx]]

# static file

> static file — try_files — checks the filesystem for one or more paths in order.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** static file — try_files — checks the filesystem for one or more paths in order.

### Nginx static file serving rule for a location
```nginx
location / {
    try_files $uri $uri/ =404;
}
```
`try_files` -> checks the filesystem for one or more paths in order.
`$uri` -> the exact file path from the request e.g. `/index.html` -> `/var/www/global/index.html`
`$uri/` -> the same but as a directory path e.g. `/docs/` if this exists, nginx can serve `index.html` from inside it (depending on your `index` directive).
`=404` -> if neither a matching file nor a matching directory exists, return HTTP 404 immediately (instead of falling back to a PHP handler).
**What it means in practice**
- If `/style.css` exists in your `root` → serve it.
- If `/blog/` exists as a directory and contains an `index.html` → serve that.
- If neither exists → return `404 Not Found`.
- It **avoids unnecessary backend calls** — Nginx won’t forward these requests to PHP/Python/etc. unless they match a different location.

## Standard config / commands

```nginx
location /assets/ {
    alias /var/www/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 Forbidden | directory listing off; perms | `chmod` for nginx user; `index` directive |
| Stale asset after deploy | browser cache | Cache-bust filenames; shorten `expires` on HTML |
| Wrong MIME type | missing types block | `include mime.types;` |

---

## Gotchas

> [!WARNING]
> Use `alias` for prefix locations — trailing slash on both `location` and `alias` matters.

---

## When NOT to use

- Do not serve user-uploaded files from the same path as executable scripts.


---

## Related

[[Nginx]]
