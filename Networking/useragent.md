[[response header]] [[HTTP]] [[cross-site scripting]] [[Network error]]

# User-Agent

> Client-declared software identity string on HTTP requests — used for compatibility, analytics, and bot detection; easily spoofed.





## Interview Relevance
Interviewers ask about User-Agent to see if you treat it as **untrusted metadata** — useful for logs and rough telemetry, never as authorization — and whether you know UA reduction / Client Hints.

## Sources
- [RFC 9110 — User-Agent](https://www.rfc-editor.org/rfc/rfc9110#name-user-agent) — deep-dive
- [MDN — User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) — overview
- [MDN — User-Agent Client Hints](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints) — overview
- [Chromium — User-Agent Reduction](https://www.chromium.org/updates/ua-reduction/) — overview

## Core Definition
`User-Agent` is an optional HTTP request header where the client names its software stack; servers may adapt, log, or rate-limit from it, but any client can send any string.

## Key Concepts
- **Identity claim:** browser/app/library string → not cryptographic proof of who is calling.
- **Adaptation / analytics:** mobile vs desktop templates, market share → declining for layout; still common in logs.
- **Bot / scraper signals:** empty or script UAs → rate limits, CAPTCHA (verify bots via DNS/IP ranges too).
- **Client Hints (`Sec-CH-UA-*`):** structured alternative → less brittle than parsing frozen UA strings.
- **API client fingerprints:** `okhttp`, `curl`, custom app tokens → useful forensics, not auth.

## Technical Details
```http
User-Agent: Mozilla/5.0 (...) Chrome/120.0.0.0 Safari/537.36
```

Common mobile/API fingerprints:

```txt
okhttp/4.12.0          → Kotlin/Java Android (OkHttp stack)
Dalvik/...             → older Android
MyApp/1.2.3 (iOS)      → custom app token
curl/8.5.0             → scripts, health checks
```

```bash
curl -v https://httpbin.org/user-agent
curl -A 'MyBot/1.0 (+https://example.com/bot)' https://example.com/
```

```nginx
log_format combined '$remote_addr - $http_user_agent';
# Block empty UA (noisy bots)
if ($http_user_agent = "") { return 403; }

proxy_set_header User-Agent $http_user_agent;
```

```javascript
const ua = req.headers['user-agent'] ?? '';
if (ua.includes('okhttp')) { /* likely Android app */ }
```

**Why log UA:** incident forensics (“was this curl or Chrome?”) — correlate with [[Network error]] patterns.

| Symptom | Check | Fix |
|---------|-------|-----|
| Mobile app blocked by WAF | Default okhttp UA | Allowlist pattern; custom UA header + auth |
| Feature gate wrong | UA sniffing | Replace with Client Hints or capability detection |
| Rate limit hits scripts | Shared datacenter UA | Per-API-key limits, not UA alone |
| SEO/bot traffic | Search bot UA spoof | Verify bot via reverse DNS + IP ranges |

## Real-World Applications
CDNs, WAFs, analytics pipelines, and API gateways read User-Agent for triage and rough client classification.

**Example:** An Android app using OkHttp is blocked by a WAF that only allows “browser-like” UAs — allowlist the pattern and authenticate with tokens, not the header alone.

## Pros/Cons or Trade-offs
- **Pro:** Cheap signal for logs, debugging, and coarse bot filtering.
- **Con:** Trivially spoofed — security decisions must not depend on it.
- **Con:** UA reduction freezes detail — sniffing breaks; prefer Client Hints or capability detection.

## Comparison
- vs tokens / mTLS / attestation: those authenticate; User-Agent only names software.
- vs Client Hints: structured, privacy-aware fields instead of one opaque legacy string.
- Related: [[response header]], [[mime type]], [[cross-site scripting]].

## Mistakes to Avoid
- Branching **authorization** on User-Agent — use tokens, mTLS, or attestation for API clients.
- Fragile UA sniffing for features — Chrome frozen UA reduction; use Client Hints where needed.
- Treating search-bot UA strings as proof — verify via reverse DNS and published IP ranges.
- Ignoring privacy retention — UA in logs can be personal data under some policies.
