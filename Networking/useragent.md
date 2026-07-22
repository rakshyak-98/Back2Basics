[[response header]] [[HTTP]] [[cross-site scripting]]

# User-Agent

> Client-declared software identity string on HTTP requests — used for compatibility, analytics, and bot detection; easily spoofed.

---

## Mental model

Every HTTP request may include:

```http
User-Agent: Mozilla/5.0 (...) Chrome/120.0.0.0 Safari/537.36
```

Purposes:
- **Server adaptation** — mobile vs desktop templates (declining; prefer responsive CSS)
- **Analytics** — browser/OS market share
- **Bot/scraper detection** — rate limits, CAPTCHA
- **API client identification** — mobile apps often use library defaults

**Not authentication** — any client can send any string.

Common mobile/API fingerprint:

```txt
okhttp/4.12.0          → Kotlin/Java Android (OkHttp stack)
Dalvik/...             → older Android
MyApp/1.2.3 (iOS)      → custom app token
curl/8.5.0             → scripts, health checks
```

---

## Standard config / commands

### Inspect

```bash
curl -v https://httpbin.org/user-agent
curl -A 'MyBot/1.0 (+https://example.com/bot)' https://example.com/
```

### Nginx log and map

```nginx
log_format combined '$remote_addr - $http_user_agent';
# Block empty UA (noisy bots)
if ($http_user_agent = "") { return 403; }
```

### Server-side (Node)

```javascript
const ua = req.headers['user-agent'] ?? '';
if (ua.includes('okhttp')) { /* likely Android app */ }
```

### Reverse proxy pass-through

```nginx
proxy_set_header User-Agent $http_user_agent;
```

**Why log UA:** incident forensics ("was this curl or Chrome?") — correlate with [[Network error]] patterns.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mobile app blocked by WAF | Default okhttp UA | Allowlist pattern; custom UA header + auth |
| Feature gate wrong | UA sniffing | Replace with Client Hints or capability detection |
| Rate limit hits scripts | Shared datacenter UA | Per-API-key limits, not UA alone |
| SEO/bot traffic | Search bot UA spoof | Verify bot via reverse DNS + IP ranges |

---

## Gotchas

> [!WARNING]
> **UA sniffing is fragile** — Chrome frozen UA reduction; use **Client Hints** (`Sec-CH-UA-*`) where needed.

> [!WARNING]
> **Security must not depend on UA** — trivial header forgery.

> [!WARNING]
> **Privacy regulations** — UA can be personal data in logs; retention policy applies.

---

## When NOT to use

Don't branch **authorization** on User-Agent. Use tokens, mTLS, or attestation for API clients.

---

## Related

[[response header]] [[mime type]] [[Network error]] [[cross-site scripting]]
