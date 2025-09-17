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