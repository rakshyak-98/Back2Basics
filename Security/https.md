[[TLS (Transport Layer Security)]] [[HTTP Strict Transport Security]] [[Root certificate]] [[response header]]

# HTTPS

> HTTP over TLS — encrypts and authenticates web traffic; browsers require valid PKI chain for padlock, APIs should pin or trust store consciously.

---

## Mental model

```txt
Client                          Server
  │── TCP connect ───────────────►│
  │── TLS ClientHello ───────────►│
  │◄─ cert chain + key exchange ──│
  │── Finished (encrypted) ──────►│
  │◄─ HTTP request/response ─────►│  (confidential + integrity)
```

HTTPS provides:
- **Confidentiality** — eavesdropper can't read body/headers (mostly)
- **Integrity** — tampering detected
- **Authentication** — server cert proves name (if PKI trusted)

Not provided: **authorization**, **XSS protection**, **DDoS immunity**.

HTTP/1.1 vs HTTP/2 vs HTTP/3: TLS is still the security layer; HTTP/2 adds **binary framing** and **multiplexing** on one connection.

---

## Standard config / commands

### Nginx TLS baseline

```nginx
listen 443 ssl http2;
ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Certbot obtain/renew

```bash
sudo certbot certonly --nginx -d example.com -d www.example.com
sudo certbot renew --dry-run
```

### Test chain and protocol

```bash
curl -vI https://example.com
openssl s_client -connect example.com:443 -servername example.com </dev/null
# ssllabs.com or testssl.sh for audit
```

### Redirect HTTP → HTTPS

```nginx
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

**Why fullchain.pem:** serve leaf + intermediates — clients without AIA fetch may fail on missing intermediate.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Certificate expired | `openssl s_client` dates | `certbot renew`; automate reload |
| `NET::ERR_CERT_AUTHORITY_INVALID` | Wrong chain; self-signed | Install intermediate; public CA |
| Mixed content blocked | HTTP assets on HTTPS page | Upgrade URLs; CSP upgrade-insecure |
| TLS handshake timeout | Firewall 443; SNI missing | Open port; correct vhost cert |
| HTTP/2 errors behind old proxy | ALPN not forwarded | Enable HTTP/2 on edge; proxy_protocol |

---

## Gotchas

> [!WARNING]
> **TLS terminates at LB** — backend HTTP is plaintext on network — use mTLS or private network.

> [!WARNING]
> **`ssl_certificate` without full chain** — Android/old clients fail intermittently.

> [!WARNING]
> **HSTS before HTTPS stable** — locks users out if cert breaks.

> [!WARNING]
> **Binary bodies fine on HTTP/1.1** — `Content-Type: application/octet-stream` over TLS is normal.

---

## When NOT to use

Don't deploy HTTPS everywhere then **disable cert verification** in clients (`NODE_TLS_REJECT_UNAUTHORIZED=0`) — fix trust store or use proper private CA.

---

## Related

[[TLS (Transport Layer Security)]] [[HTTP Strict Transport Security]] [[Root certificate]] [[certbot (letsencrypt)]] [[response header]]
