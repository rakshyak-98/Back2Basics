[[web server]] [[directives]] [[How does directive work]] [[nginx SPA deployment]] [[nginx fastcgi]] [[nginx config structure]] [[nginx using unix socket]] [[nginx stream]] [[static file]] [[Nginx internals]]

# Nginx Configuration

> Reverse proxy and static file front door — match a `location`, then `root`/`alias`, `proxy_pass`, or `fastcgi_pass`; always `nginx -t` before reload.

## Interview Relevance

Interviewers ask how you pick `location` precedence, when `root` vs `alias` differs, and how you reload without dropping traffic — signals you have operated Nginx in production, not only pasted configs.

## Sources

- [nginx.org — Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html) — overview
- [nginx.org — ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html) — deep-dive
- [nginx.org — ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) — deep-dive

## Core Definition

Nginx configuration is a tree of contexts (`main` → `http` → `server` → `location`) where directives compose how a request is matched and where bytes come from (disk, upstream, or FastCGI).

## Key Concepts

- **Location match order:** `=` exact → `^~` prefix (stops regex) → `~`/`~*` first matching regex → longest prefix — wrong winner is a common 404/proxy bug.
- **`root` vs `alias`:** `root` appends the URI under the root; `alias` replaces the location prefix — trailing slashes must align.
- **Graceful reload:** `nginx -t` then `nginx -s reload` starts new workers and drains old ones — untested reload can leave workers unable to start.
- **Upstream health (passive):** `max_fails` / `fail_timeout` mark peers down temporarily — not a full active health check in OSS.

## Technical Details

```txt
Client → nginx (location match) → root/alias | proxy_pass | fastcgi_pass
```

| Directive | Path rule |
|-----------|-----------|
| `root` | URI appended under root |
| `alias` | Replaces location prefix |

```bash
sudo nginx -t && sudo nginx -s reload
sudo nginx -T | less          # merged config
```

```nginx
upstream api { server 127.0.0.1:3000; keepalive 32; }

server {
  listen 80;
  location /_next/static/ { alias /var/www/app/.next/static/; }
  location / {
    proxy_pass http://api;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ { limit_req zone=api burst=20 nodelay; proxy_pass http://api; }
```

| Knob | Why it matters |
|------|----------------|
| `proxy_pass` trailing `/` | Strips location prefix |
| `worker_processes auto` | ~1 per CPU |
| `max_fails` / `fail_timeout` | Passive upstream health |

| Symptom | Check | Fix |
|---------|-------|-----|
| 502 Bad Gateway | Upstream up? socket path? | Restart app; fix `unix:` path |
| 504 Gateway Timeout | `proxy_read_timeout` vs p99 | Raise timeout or fix slow app |
| 499 Client Closed | Client left early | Often mobile/tab — check deploy drain |
| 404 static | `root` vs `alias` | Fix mapping + trailing slashes |
| 403 | perms / SELinux | `www-data` read; `namei -l` |
| reload fails | `nginx -t` | Fix syntax before reload |

## Real-World Applications

Terminate TLS and reverse-proxy a Node/Next app; serve hashed static assets from `alias`/`root`; rate-limit public `/api/` with `limit_req`.

**Example:** Deploy changes with `nginx -t && systemctl reload nginx` so in-flight requests finish on old workers while new workers load the new config.

## Pros/Cons or Trade-offs

- **Pro:** One process family can terminate TLS, serve static, and proxy — low ops surface.
- **Con:** Business logic and WAF depth belong elsewhere — `limit_req` is not SQLi protection.
- **Con:** URI rewriting via `proxy_pass` slash rules is easy to get wrong under time pressure.

## Comparison

- vs application server alone: Nginx handles TLS, static, and connection fan-in better; app owns business logic.
- vs [[nginx stream]]: HTTP config lives in `http {}`; L4 TCP/UDP is `stream {}` with no HTTP headers.
- vs [[Nginx ingress]]: host Nginx config vs Kubernetes Ingress controller CRDs.

## Mistakes to Avoid

- Forgetting `proxy_pass` trailing slash — `/api/` → `http://b/` strips prefix; without slash, full URI forwards.
- Mismatched `alias` trailing slashes — location and alias must both end with `/` or paths misalign.
- Reloading without `nginx -t` — bad config can block new workers.
- Putting application business logic or DB pooling in Nginx — use the app / PgBouncer.
