[[web server]] [[directives]] [[How does directive work]] [[nginx SPA deployment]] [[nginx fastcgi]] [[nginx config structure]] [[nginx using unix socket]] [[nginx stream]] [[static file]] [[Nginx internals]]

# Nginx Configuration

> Reverse proxy and static file front door — match a `location`, then `root`/`alias`, `proxy_pass`, or `fastcgi_pass`; always `nginx -t` before reload.

```txt
        Nginx Configuratio ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you pick `location` precedence, when `root` vs `alias` d…

## Sources
- [nginx.org — Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html) — overview
- [nginx.org — ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html) — deep-dive
- [nginx.org — ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) — deep-dive

## Key Concepts
- **Location match order:** `=` exact → `^~` prefix (stops regex) → `~`/`~*` first matching regex → longe…
- **`root` vs `alias`:** `root` appends the URI under the root; `alias` replaces the location prefix
- **Graceful reload:** `nginx -t` then `nginx -s reload` starts new workers and drains old ones
- **Upstream health (passive):** `max_fails` / `fail_timeout` mark peers down temporarily


- **Core:** Nginx configuration is a tree of contexts (`main` → `http` → `server` → `loca…

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

## Mistakes to Avoid
- **Forgetting `proxy_pass` trailing slash::** → `http://b/` strips prefix; without slash, full URI forwards
- **Mistake:** Mismatched `alias` trailing slashes
- **Mistake:** Reloading without `nginx -t` — bad config can block new workers
- **Mistake:** Putting application business logic or DB pooling in Nginx

## Pros/Cons or Trade-offs
- **Pro:** One process family can terminate TLS, serve static, and proxy — low ops surface.
- **Con:** Business logic and WAF depth belong elsewhere — `limit_req` is not SQLi protection.
- **Con:** URI rewriting via `proxy_pass` slash rules is easy to get wrong under time pressure.

## Comparison
- vs application server alone: Nginx handles TLS, static, and connection fan-in better
- vs [[nginx stream]]: HTTP config lives in `http {}`
- vs [[Nginx ingress]]: host Nginx config vs Kubernetes Ingress controller CRDs.


### Use cases
- Terminate TLS and reverse-proxy a Node/Next app

- **Example:** Deploy changes with `nginx -t && systemctl reload nginx` so in-f…
