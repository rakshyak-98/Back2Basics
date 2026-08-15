[[Configuration]] [[static file]] [[nginx URL rewrite]] [[URL Rewriting]] [[How does directive work]]

# Nginx SPA Deployment

> Client-side routers own URLs that are not on disk — `try_files` falls back to `index.html` without breaking API routes or hashed assets.

## Interview Relevance

Frontend/platform interviews ask why refresh on `/dashboard` 404s, how to split `/api` from SPA fallback, and why `index.html` must not be cached like hashed assets.

## Sources

- [nginx.org — try_files](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files) — deep-dive
- [MDN — SPA / client-side routing](https://developer.mozilla.org/en-US/docs/Glossary/SPA) — overview

## Core Definition

An SPA deploy serves one HTML shell plus JS/CSS bundles; deep links must return that shell so the client router can render, while real files and API paths must not fall through to HTML.

## Key Concepts

- **History mode needs fallback:** HTML5 routes have no files on disk; hash mode (`/#/…`) does not need server fallback.
- **`try_files` order:** Prefer `$uri $uri/ /index.html` so real directories still work.
- **API before catch-all:** `/api/` (or `^~ /api/`) must win before the SPA `location /`.
- **Cache policy:** Long-cache hashed `/assets/`; never long-cache `index.html`.

## Technical Details

```
Browser GET /dashboard
    → Nginx looks for /usr/share/nginx/html/dashboard  (missing)
    → Without fallback: 404
    → With try_files: serve index.html → JS router renders /dashboard
```

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

    location /assets/ {
        try_files $uri =404;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Typical Vite/React `dist/`: `index.html` + `assets/index-*.js|css`. Point `root` at `dist/`, not the repository root.

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on refresh at `/dashboard` | Missing or wrong `try_files` | Add `try_files $uri $uri/ /index.html` in `/` |
| API returns HTML | API location missing or after catch-all | Put `/api/` **before** `/`; use `^~ /api/` if needed |
| Blank page, 200 on `/` | Wrong `root`; JS 404 | Verify `root`; Network tab for `/assets/*.js` |
| Infinite redirect loop | `try_files` + `error_page 404 /index.html` | Prefer `try_files` alone |
| `/index.html` cached forever | Cache-Control on HTML | Cache hashed assets only |

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://mysite.com/dashboard
curl -sS https://mysite.com/ | head -5
curl -sS -H "Accept: text/html" https://mysite.com/dashboard | grep -o '<title>.*</title>'
```

## Real-World Applications

React/Vue/Angular static hosting behind Nginx with a separate Node API on `/api/`.

## Pros/Cons or Trade-offs

- **Pro:** Cheap, cacheable static hosting with simple Nginx config.
- **Con:** Pure SPA fallback is wrong for SSR/SSG (Next.js/Nuxt SSR) — need server routing or hybrid proxy.
- **Con:** Multiple SPAs on one host need careful prefixes, not one global catch-all.

## Comparison

- vs [[static file]]: static serving without HTML fallback returns 404 for deep links.
- vs [[URL Rewriting]]: SPA fallback is usually `try_files`, not a long `rewrite` chain.
- vs SSR: server must understand routes; Nginx alone is not enough.

## Mistakes to Avoid

- Two-arg `try_files $uri /index.html` when real directories exist — use three-arg form.
- Mixing `try_files` with `alias` casually — prefer `root` for SPA deploys.
- Subpath deploy (`base: '/app/'`) without matching `location` / router `basename`.
- Using `error_page 404 /index.html` — returns 200 HTML and breaks missing-asset monitoring.
