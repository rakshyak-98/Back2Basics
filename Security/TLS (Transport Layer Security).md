[[Security]] [[Nginx]] [[Configuration]] [[Node.js security flaws in architecture]]

# TLS (Transport Layer Security)

> Encrypt and authenticate bytes on the wire — terminate at the edge, prefer modern suites, automate certificate renewal, verify the full chain.

```txt
        TLS (Transport Lay ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Core networking/security: handshake, certificates, cipher suites, termination…

## Sources
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) — deep-dive
- [RFC 5246 — TLS 1.2](https://www.rfc-editor.org/rfc/rfc5246) — deep-dive
- [MDN — TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) — overview

## Key Concepts
- **Note:** TLS sits above TCP

```
Client                         Server
  │──── ClientHello ────────────►│
  │◄─── ServerHello + cert ─────│
  │──── verify cert chain ──────►│  (client checks CA trust)
  │──── Finished (session keys) ─►│
  │◄══ encrypted HTTP ══════════►│
```

- **Note:** **Certificate** binds public key to DNS name (SAN). **Private key** stays on …

SSL is obsolete terminology — say TLS 1.2/1.3.


- **Core:** TLS encrypts and authenticates a byte stream above TCP (or QUIC)

## Technical Details
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

- application behind proxy must trust `X-Forwarded-Proto` only from known hop

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `SSL certificate problem: unable to get local issuer` | Missing intermediate in `fullchain.pem` | Use `fullchain.pem` not `cert.pem` only |
| Browser "not secure" / name mismatch | SAN vs hostname | Reissue cert with correct `-d` names |
| `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` | Old client vs TLS 1.3-only | Enable TLSv1.2 temporarily; fix client |
| Cert expired | `openssl x509 -dates` | `certbot renew`; check timer |
| Mixed content warnings | HTTP assets on HTTPS page | Upgrade URLs or CSP upgrade-insecure-requests |
| Works in browser, fails in app | Custom CA not trusted | Add CA to trust store or use public CA |
| Handshake OK, then 502 | Backend issue, not TLS | See [[Configuration]] 502 playbook |

## Mistakes to Avoid
- **Mistake:** Private key permissions — `chmod 600`; never commit to git
- **Mistake:** TLS renegotiation / client certs
- **Mistake:** HSTS before HTTPS stable
- **Mistake:** Wildcard cert `*.example.com`
- **Mistake:** Certificate transparency + short lifetimes

## Pros/Cons or Trade-offs
- **Pro:** Industry-standard wire security with broad client support.
- **Con:** TLS inside trusted VPC for every microservice hop — mTLS/service mesh when policy requires; otherwise edge termination + private network is common.
- **Con:** Self-signed in production public sites — users can't trust; use public CA.

## Comparison
- vs [[https]]: TLS is the secure channel; HTTPS is HTTP on TLS.
- vs VPN/mTLS mesh: different trust and hop models for east-west traffic.


### Use cases
- Edge Nginx terminates TLS for HTTPS sites
