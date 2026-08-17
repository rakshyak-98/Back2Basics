[[CORS (Cross Origin Request Sharing)]] [[TLS (Transport Layer Security)]] [[cross-site scripting]] [[cookies configuration]] [[cloudflare]]

# HTTP Response Headers (Security & Caching)

> Server metadata that controls caching, framing, MIME sniffing, and browser security policy — mis-set headers cause stale content or clickjacking.

```txt
        HTTP Response Head ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Web hardening: security and caching headers

## Sources
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) — overview
- [MDN — HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) — deep-dive

## Key Concepts
- **Note:** Response headers are **out-of-band instructions** to browsers, proxies, and C…

```
- **Note:** Origin ──► App middleware ──► reverse proxy/CDN ──► browser interprets headers
                                    │
                                    └── may strip/add unless explicitly forwarded
```


- **Core:** HTTP response headers carry caching, framing, MIME-sniffing, and browser secu…

## Technical Details
### Security baseline (production)

```nginx
# nginx — add_security_headers snippet
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; frame-ancestors 'none';" always;
# Permissions-Policy: restrict camera/mic/geolocation as needed
```

| Header | Purpose |
|--------|---------|
| `Strict-Transport-Security` | Force HTTPS after first visit |
| `Content-Security-Policy` | XSS/injection surface reduction |
| `X-Frame-Options` / CSP `frame-ancestors` | Clickjacking |
| `Cross-Origin-Opener-Policy` | Isolate browsing context |
| `Cross-Origin-Resource-Policy` | Limit cross-origin reads |

### CORS (API)

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Vary: Origin
```

- Never `Allow-Origin: *` with credentials ([[CORS (Cross Origin Request Sharin…
- Always **`Vary: Origin`** when origin is dynamic.

### Caching + `Vary`

```http
Cache-Control: public, max-age=3600
Vary: Accept-Encoding, Accept-Language
```

- **`Vary`:** tells CDNs/browsers which **request headers** participate in the c…

```nginx
# Separate cache keys for WebP vs JPEG when content negotiation used
add_header Vary "Accept" always;
```

- Common `Vary` values: `Accept-Encoding` (compression), `Accept` (format), `Or…

### Express (Node)

```javascript
import helmet from 'helmet';
app.use(helmet({ contentSecurityPolicy: { directives: { defaultSrc: ["'self'"] } } }));
app.use((req, res, next) => {
  res.vary('Origin');
  next();
});
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| CDN serves wrong language/format | Missing `Vary: Accept` or `Accept-Language` | Add Vary matching negotiation headers |
| CORS works once, cached wrong origin | No `Vary: Origin` | Add Vary; purge CDN |
| Site won't embed in approved iframe | `X-Frame-Options: DENY` | CSP `frame-ancestors` allowlist |
| Assets stale after deploy | `Cache-Control: immutable` on index.html | Hash filenames; `no-cache` on HTML |
| HSTS lock on bad cert | Preload HSTS before cert valid | Fix cert; careful with preload |
| CSP breaks inline scripts | `script-src` too strict | Nonce/hash or refactor; avoid `unsafe-inline` in prod |
| Security headers missing on 4xx/5xx | nginx `add_header` without `always` | Add `always` flag |

```bash
curl -I https://example.com
curl -I -H 'Accept: image/webp' https://example.com/img
curl -I -H 'Origin: https://app.example.com' https://api.example.com/v1/x
```

## Mistakes to Avoid
- **Mistake:** Multiple `Set-Cookie` + missing `Vary: Cookie`
- **Mistake:** `Access-Control-Allow-Origin: *` + credentials
- **Mistake:** HSTS on dev `.local`
- **Mistake:** CSP report-only forgotten in prod

## Pros/Cons or Trade-offs
- **Pro:** One place to enforce browser security and caching policy.
- **Con:** Spray all helmet defaults on API-only JSON — tune CSP/CORP; some headers irrelevant for non-browser consumers.
- **Con:** `Vary: *` — effectively uncacheable; fix root cause instead.

## Comparison
- vs [[content security policy]] / [[HTTP Strict Transport Security]]: those are specific headers c…
- vs request headers: clients send; security policy is mostly on responses.


### Use cases
- Set security and cache headers at the reverse proxy or app framework for clic…
