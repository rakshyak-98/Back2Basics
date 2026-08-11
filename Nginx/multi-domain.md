[[Nginx]]

# Optional: redirects HTTP -> HTTPS

> Optional: redirects HTTP -> HTTPS — you can ping api.localhost and it'll look back to your machine.

---

## Mental model

**Say it in one breath:** Optional: redirects HTTP -> HTTPS is infra/security tooling — least privilege, clear config, observable failures.


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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Optional: redirects HTTP -> HTTPS** | Core idea of this note | “I can explain Optional: redirects HTTP -> HTTPS without jargon.” |
| **least privilege** | Only needed access | “Grant the smallest role that works.” |
| **secret** | Password/key/token | “Secrets out of git; rotate them.” |
| **observability** | metrics/logs/traces | “You can’t fix what you can’t see.” |

---

## Standard config / commands

```bash
# status
# check version, auth, and recent changes
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail | clock / creds / IAM | Sync time; fix policy |
| TLS error | cert chain / SNI | Fix certs and CA bundle |
| Deploy down | rollback / health | Roll back; check probes |

---

## Gotchas

> [!WARNING]
> Never commit long-lived secrets.

---

## When NOT to use

- Don’t build custom infra when managed services meet the SLO.

---

## Related

[[Nginx]]
