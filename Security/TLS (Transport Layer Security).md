[[Security]] [[Nginx]] [[Configuration]]

# TLS (Transport Layer Security)

> One-line: encrypt + authenticate bytes on the wire — terminate at the edge (Nginx), use modern cipher suites, automate cert renewal, verify the full chain.

## Mental model

TLS sits above TCP. Handshake negotiates version, ciphers, and (usually) server identity via **X.509 certificate**. After handshake, application data (HTTP → HTTPS) is encrypted and integrity-protected.

```
Client                         Server
  │──── ClientHello ────────────►│
  │◄─── ServerHello + cert ─────│
  │──── verify cert chain ──────►│  (client checks CA trust)
  │──── Finished (session keys) ─►│
  │◄══ encrypted HTTP ══════════►│
```

**Certificate** binds public key to DNS name (SAN). **Private key** stays on server (or HSM). **Chain** = leaf + intermediates; clients trust via OS/browser CA store.

SSL is obsolete terminology — say TLS 1.2/1.3.

---

## Standard config / commands

### Nginx TLS termination

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;   # TLS 1.3 ignores anyway

    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;         # forward secrecy preference

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

App behind proxy must trust `X-Forwarded-Proto` only from known hop — see [[Node.js security flaws in architecture]].

### Let's Encrypt (certbot)

```bash
sudo certbot certonly --nginx -d example.com -d www.example.com
sudo certbot renew --dry-run
# cron/systemd timer: certbot renew
```

### Verify deployment

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject -issuer

curl -vI https://example.com
# testssl.sh or ssllabs.com for external audit
```

### Generate self-signed (lab only)

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
  -subj "/CN=localhost"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `SSL certificate problem: unable to get local issuer` | Missing intermediate in `fullchain.pem` | Use `fullchain.pem` not `cert.pem` only |
| Browser "not secure" / name mismatch | SAN vs hostname | Reissue cert with correct `-d` names |
| `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` | Old client vs TLS 1.3-only | Enable TLSv1.2 temporarily; fix client |
| Cert expired | `openssl x509 -dates` | `certbot renew`; check timer |
| Mixed content warnings | HTTP assets on HTTPS page | Upgrade URLs or CSP upgrade-insecure-requests |
| Works in browser, fails in app | Custom CA not trusted | Add CA to trust store or use public CA |
| Handshake OK, then 502 | Backend issue, not TLS | See [[Configuration]] 502 playbook |

---

## Gotchas

> [!WARNING]
> **Private key permissions** — `chmod 600`; never commit to git.

> [!WARNING]
> **TLS renegotiation / client certs** — rare for public APIs; adds complexity.

> [!WARNING]
> **HSTS before HTTPS stable** — locks users to HTTPS; broken cert becomes hard outage.

> [!WARNING]
> **Wildcard cert `*.example.com`** — does not cover `example.com` bare (needs SAN entry).

> [!WARNING]
> **Certificate transparency + short lifetimes** — Let's Encrypt 90 days; automate renew or pager at T-30.

---

## When NOT to use

- **TLS inside trusted VPC for every microservice hop** — mTLS/service mesh when policy requires; otherwise edge termination + private network is common.
- **Self-signed in production public sites** — users can't trust; use public CA.

---

## Related

[[Configuration]] [[Nginx]] [[Node.js security flaws in architecture]]
