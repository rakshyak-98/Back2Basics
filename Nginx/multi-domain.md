[[Configuration]] [[nginx files]] [[openssl]] [[certbot (letsencrypt)]] [[https]]

# multi-domain

> Several hostnames on one Nginx — separate `server` blocks (or SAN/wildcard certs) so `server_name` and TLS pick the right site.

```txt
        multi-domain ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how virtual hosts and SNI work: wrong `default_server`, cert…

## Sources
- [nginx.org — Server names](https://nginx.org/en/docs/http/server_names.html) — deep-dive
- [nginx.org — Configuring HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html) — deep-dive
- [Let’s Encrypt — Challenge Types](https://letsencrypt.org/docs/challenge-types/) — overview

## Key Concepts
- **`server_name` selection:** Exact, wildcard, then regex names; unmatched Host hits `default_server`.
- **Local `/etc/hosts`:** Map fake names (`api.localhost`) to `127.0.0.1` for local multi-vhost testing.
- **TLS per name:** Each name needs a matching certificate unless you use a SAN or wildcard cert.
- **HTTP→HTTPS:** Optional separate `listen 80` servers that `return 301 https://$host$request_…


- **Core:** Multi-domain hosting means multiple `server {}` blocks on the same `listen` p…

## Technical Details
- Add fake domains to `/etc/hosts`:

```
127.0.0.1   api.localhost
127.0.0.1   shop.localhost
127.0.0.1   blog.localhost
```

- Create roots and separate server blocks (e.g.
- under `sites-available`):

```bash
sudo mkdir -p /var/www/api /var/www/shop /var/www/blog
```

```nginx
server {
    listen 80;
    server_name api.localhost;
    root /var/www/api;
    index index.html;
}
server {
    listen 80;
    server_name shop.localhost;
    root /var/www/shop;
    index index.html;
}
server {
    listen 80;
    server_name blog.localhost;
    root /var/www/blog;
    index index.html;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/multidomain /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

- Shared cert for multiple names (SAN):

```nginx
server {
    listen 443 ssl;
    server_name a.example.com b.example.com;
    ssl_certificate     /etc/letsencrypt/live/a.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/a.example.com/privkey.pem;
}
```

- Self-signed for local TLS: see [[openssl]].

| Symptom | Check | Fix |
|---------|-------|-----|
| Certificate name mismatch | SNI; wrong cert on default | Separate `server` per cert or SAN cert |
| Wrong site content | `default_server` catches unknown Host | Set explicit `server_name` on each vhost |
| ACME challenge fails | `.well-known` not reachable | Dedicated location for `/.well-known/acme-challenge/` |

## Mistakes to Avoid
- **Mistake:** Assuming one certificate covers all `server_name`s without SAN/w…
- **Mistake:** Leaving the package `default` site as `default_server` so unknow…
- **Mistake:** Typoing `sites-available` / `sites-enabled` paths so the symlink…

## Pros/Cons or Trade-offs
- **Pro:** One Nginx instance, many hostnames — cheap and standard.
- **Con:** Certificate and `default_server` mistakes leak content or break TLS for unknown hosts.
- **Con:** Crowding unrelated tenants into one `server` without strict `server_name` lists is fragile.

## Comparison
- vs one `server` with many `location`s: host-based split is clearer when roots, TLS, or apps diffe…
- vs [[Nginx ingress]]: Kubernetes Ingress uses Host/path rules in CRDs instead of host filesystem …


### Use cases
- Local multi-tenant demos with `*.localhost` in `/etc/hosts`
