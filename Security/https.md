[[TLS (Transport Layer Security)]] [[HTTP Strict Transport Security]] [[Root certificate]] [[response header]] [[certbot (letsencrypt)]]

# HTTPS

> HTTP over TLS — encrypts and authenticates web traffic; browsers require valid PKI chain for padlock, APIs should pin or trust store consciously.

```txt
        HTTPS ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Baseline: HTTPS = HTTP over TLS

## Sources
- [MDN — HTTPS](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS) — overview
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — deep-dive

## Key Concepts
```txt
Client                          Server
  │── TCP connect ───────────────►│
  │── TLS ClientHello ───────────►│
  │◄─ cert chain + key exchange ──│
  │── Finished (encrypted) ──────►│
- **Note:** │◄─ HTTP request/response ─────►│ (confidential + integrity)
```

HTTPS provides:
- **Confidentiality:** — eavesdropper can't read body/headers (mostly)
- **Integrity:** — tampering detected
- **Authentication:** — server cert proves name (if PKI trusted)

- **Note:** Not provided: **authorization**, **XSS protection**, **DDoS immunity**.

- **Note:** HTTP/1.1 versus HTTP/2 versus HTTP/3: TLS is still the security layer


- **Core:** HTTPS is HTTP carried over TLS so browsers and APIs get confidentiality, inte…

## Technical Details
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

- **Why fullchain.pem:** serve leaf + intermediates

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Certificate expired | `openssl s_client` dates | `certbot renew`; automate reload |
| `NET::ERR_CERT_AUTHORITY_INVALID` | Wrong chain; self-signed | Install intermediate; public CA |
| Mixed content blocked | HTTP assets on HTTPS page | Upgrade URLs; CSP upgrade-insecure |
| TLS handshake timeout | Firewall 443; SNI missing | Open port; correct vhost cert |
| HTTP/2 errors behind old proxy | ALPN not forwarded | Enable HTTP/2 on edge; proxy_protocol |

## Mistakes to Avoid
- **Mistake:** TLS terminates at LB
- **Mistake:** `ssl_certificate` without full chain
- **Mistake:** HSTS before HTTPS stable — locks users out if cert breaks
- **Mistake:** Binary bodies fine on HTTP/1.1

## Pros/Cons or Trade-offs
- **Pro:** Confidentiality and server auth for web traffic users expect by default.
- **Con:** Don't deploy HTTPS everywhere then **disable cert verification** in clients (`NODE_TLS_REJECT_UNAUTHORIZED=0`) — fix trust store or use proper private CA.

## Comparison
- vs [[TLS (Transport Layer Security)]]: HTTPS is HTTP-over-TLS
- vs [[HTTP Strict Transport Security]]: HSTS forces browsers to stick to HTTPS after first visit.


### Use cases
- Every public web app terminates HTTPS at the edge, redirects HTTP, and serves…
