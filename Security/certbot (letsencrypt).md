[[Security]] [[ACME server]] [[TLS (Transport Layer Security)]] [[certbot error]] [[https]]

# certbot (letsencrypt)

> Certbot — ACME client that proves you own a domain, then installs a Let’s Encrypt cert and renews it before expiry.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Renew certificate]]
- [[#Webroot]]
- [[#HTTP-01 Challenge]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Certbot talks to an [[ACME server]], completes HTTP-01 or DNS-01, writes certs under `/etc/letsencrypt/live/<name>/`, and a timer runs `certbot renew`.

```txt
certbot ──ACME──► Let's Encrypt
   │                  │
   │◄── challenge ────┤
   │ serve token :80 or TXT DNS
   │◄── leaf + chain ─┤
   └── fullchain.pem + privkey.pem → nginx/apache
```

| Path | Role |
|------|------|
| `/var/log/letsencrypt/letsencrypt.log` | Debug log |
| `/etc/letsencrypt/cli.ini` | Global config |
| `~/.config/letsencrypt/cli.ini` | Per-user config |
| `/etc/letsencrypt/live/…/fullchain.pem` | What TLS servers should use |

Use **`--staging`** while debugging — avoids production rate limits; staging certs are untrusted.

---

## Standard config / commands

```bash
certbot plugins
certbot certificates
sudo apt install certbot python3-certbot-nginx

# Issue + rewrite nginx
sudo certbot --nginx -d example.com -d www.example.com

# Cert only
sudo certbot certonly --nginx -d example.com

# Standalone (temp server on :80 — nothing else bound)
sudo certbot certonly --staging --standalone \
  -d testhotel1.example.com --email you@example.com --agree-tos --non-interactive
```

| Plugin | When |
|--------|------|
| `--nginx` / `--apache` | Autoconfigure vhost |
| `--webroot -w` | Existing server already serves docroot |
| `--standalone` | No web server, or stop it briefly |
| `--dns-<provider>` | Wildcards / blocked port 80 |

## Renew certificate

```bash
sudo certbot renew
sudo certbot renew --dry-run
sudo certbot renew --deploy-hook "systemctl reload nginx"
sudo certbot renew --quiet   # cron/systemd timer
```

## Webroot

Writes challenge files into your docroot so the running server serves them:

```bash
sudo certbot certonly --webroot -w /var/www/html -d example.com -d www.example.com
```

## HTTP-01 Challenge

Prove control by serving `http://<domain>/.well-known/acme-challenge/<token>` on **port 80**. DNS-01 instead sets a TXT record (wildcards).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection timeout from LE | Port 80/firewall/SG | Open 80 from internet; fix NAT |
| `404` on challenge | Wrong webroot / nginx location | Align `-w` with served path; allow `/.well-known/` |
| Rate limited | Too many failed prod attempts | Use `--staging`; wait; see [[certbot error]] |
| Renew dry-run fails | Auth path changed | Fix plugin config before expiry |
| nginx still old cert | Wrong `ssl_certificate` path | Point to `live/…/fullchain.pem`; reload |
| Wildcard fail | HTTP-01 used | Switch to DNS-01 plugin |

---

## Gotchas

> [!WARNING]
> **Staging certs look “broken” in browsers** — expected; switch off `--staging` for real trust.

> [!WARNING]
> **Standalone steals :80** — fails if nginx already listens; use webroot or stop nginx briefly.

> [!WARNING]
> **IPv6 AAAA wrong** — LE may prefer v6; align A/AAAA or remove bad AAAA.

---

## When NOT to use

- **Internal-only hostnames** — public LE can’t validate private DNS; use private CA / step-ca.
- **Devices without inbound 80/DNS API** — pre-provision or use DNS-01 with automation.
- **One-hour lab on localhost** — `mkcert` / self-signed OpenSSL is faster.

---

## Related

[[ACME server]] [[certbot error]] [[TLS (Transport Layer Security)]] [[https]] [[openssl]] [[PKI]]
