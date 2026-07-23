[[Nginx]] [[Configuration]] [[static file]]

# Nginx SPA Deployment

> One-line: client-side routers own URLs that don't exist on disk — `try_files` must fall back to `index.html` without breaking API routes or static assets.

## Mental model

SPAs (React, Vue, Angular) handle routes like `/dashboard` and `/profile/settings` **in the browser**. Those paths are not files on the server. Nginx only sees HTTP paths.

```
Browser GET /dashboard
    → Nginx looks for /usr/share/nginx/html/dashboard  (missing)
    → Without fallback: 404
    → With try_files: serve index.html → JS router renders /dashboard
```

The server delivers **one shell** (`index.html` + JS bundle); the framework router takes over after load.

---

## Standard config / commands

### Minimal SPA server

```nginx
server {
    listen 80;
    server_name mysite.com;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Production SPA + API split

```nginx
server {
    listen 443 ssl http2;
    server_name mysite.com;
    root /var/www/app/dist;
    index index.html;

    # Hashed assets — long cache (Vite/Webpack emit content hashes)
    location /assets/ {
        try_files $uri =404;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API — never fall through to index.html
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SPA fallback — last resort
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Build output layout (Vite/React typical)

```
dist/
  index.html
  assets/
    index-a1b2c3.js
    index-d4e5f6.css
```

Ensure `root` points at `dist/`, not repo root.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on refresh at `/dashboard` | Missing or wrong `try_files` | Add `try_files $uri $uri/ /index.html` in `/` location |
| 404 on refresh but direct URL works from home | Nested `location` blocks overriding fallback | Single catch-all for SPA; don't duplicate conflicting locations |
| API returns HTML (index.html) instead of JSON | API `location` missing or ordered after catch-all | Put `/api/` **before** `/` fallback; use `^~ /api/` if regex locations interfere |
| Blank page, 200 on `/` | Wrong `root`; JS 404 | Verify `root` path; check Network tab for failed `/assets/*.js` |
| Infinite redirect loop | `try_files` + `error_page 404 /index.html` double fallback | Pick one strategy — prefer `try_files`, not both |
| `/index.html` cached forever | `Cache-Control` on HTML | Never long-cache `index.html`; cache hashed assets only |

```bash
# Verify file exists on disk
curl -sS -o /dev/null -w "%{http_code}\n" https://mysite.com/dashboard
curl -sS https://mysite.com/ | head -5

# Confirm Nginx serves index.html for unknown path
curl -sS -H "Accept: text/html" https://mysite.com/dashboard | grep -o '<title>.*</title>'
```

---

## Gotchas

> [!WARNING]
> **`try_files $uri /index.html` vs `$uri $uri/ /index.html`:** Two-arg form skips directory check. If you have real directories (e.g. `/docs/` static site inside SPA), use three-arg form or they'll 404 instead of serving `index.html`.

> [!WARNING]
> **`try_files` + `alias`:** Don't mix casually. Prefer `root` for SPA deploys. `alias` + fallback is a common footgun.

> [!WARNING]
> **Base path / subpath deploy:** App built with `base: '/app/'` needs `location /app/ { try_files $uri $uri/ /app/index.html; }` and matching router `basename`. Mismatch → assets load from wrong path.

> [!WARNING]
> **History mode vs hash mode:** Hash routing (`/#/dashboard`) doesn't need server fallback — but ugly URLs. HTML5 history mode **requires** Nginx fallback.

> [!WARNING]
> **`error_page 404 /index.html`:** Returns 200 with index.html body — breaks monitoring that expects 404 on missing static files. Prefer explicit `try_files`.

---

## When NOT to use

- **SSR/SSG frameworks (Next.js, Nuxt SSR)** — need server-side routing or hybrid config, not pure SPA fallback. See [[Configuration]] for Next.js proxy pattern.
- **Multiple SPAs on one host** — use separate `root` + `server_name` or careful prefix locations, not one catch-all.

---

## Related

[[Configuration]] [[static file]] [[nginx URL rewrite]] [[URL Rewriting]]
