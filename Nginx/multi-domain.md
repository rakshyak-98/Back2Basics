[[Nginx]]

# Optional: redirects HTTP -> HTTPS

> Optional: redirects HTTP -> HTTPS — you can ping api.localhost and it'll look back to your machine.

## Mental model

**Say it in one breath:** Optional: redirects HTTP -> HTTPS — you can ping api.localhost and it'll look back to your machine.

Add fake domains to `/etc/hosts`
```
127.0.0.1   api.localhost
127.0.0.1   shop.localhost
127.0.0.1   blog.localhost
```
- You can `ping api.localhost` and it'll look back to your machine.
Create local folders
```bash
sudo mkdir -p /var/www/api /var/www/shop /var/www/blog;
```
Configure Nginx
- create separate server blocks `/etc/nginx-sites-available/multidoman`;
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
- enable it
```bash
sudo ln -s /etc/nginx/site-available/multidomain /etc/nginx/sites-enable;
sudo nginx -t; # test config.
sudo systemctl reload nginx;
```
### TLS self-signed certificate
Generate a self signed certificate [[openssl#Generate self signed certificate]]

## Standard config / commands

```nginx
server {
    listen 443 ssl;
    server_name a.example.com b.example.com;
    ssl_certificate     /etc/letsencrypt/live/a.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/a.example.com/privkey.pem;
}
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Certificate name mismatch | SNI; wrong cert on default | Separate `server` per cert or SAN cert |
| Wrong site content | `default_server` catches unknown Host | Set explicit `server_name` on each vhost |
| ACME challenge fails | `.well-known` not reachable | Dedicated location for `/.well-known/acme-challenge/` |

## Gotchas

> [!WARNING]
> Each `server_name` needs a matching certificate unless you use a SAN or wildcard cert.

## When NOT to use

- Do not serve many unrelated tenants from one `server` block without strict `server_name` lists.

## Related

[[Nginx]]
