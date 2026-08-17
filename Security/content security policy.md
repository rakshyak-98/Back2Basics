[[cross-site scripting]] [[response header]] [[SOP (Same-Origin Policy)]] [[XSRF (cross-site request forgery)]] [[https]]

# Content Security Policy

> HTTP header that whitelists where scripts, styles, connections, and frames may load from — primary defense-in-depth against XSS and data exfiltration.

```txt
        Content Security P ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Web security interviews ask how CSP reduces XSS impact, what default-src/scri…

## Sources
- [MDN — Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) — overview
- [CSP Level 3 W3C](https://www.w3.org/TR/CSP3/) — deep-dive

## Key Concepts
- **Note:** **CSP** replaces "browser trusts all inline script" with an explicit **allowl…

```http
- **Note:** Content-Security-Policy: default-src 'self'
```

Directives (common):
| Directive | Controls |
|-----------|----------|
| `default-src` | Fallback for unspecified fetch types |
| `script-src` | JS (`<script>`, workers) |
| `style-src` | CSS |
| `img-src` | Images |
| `connect-src` | `fetch`, XHR, WebSocket |
| `frame-ancestors` | Who can embed you (clickjacking) |
| `upgrade-insecure-requests` | HTTP→HTTPS |

- **Note:** Violations report to `report-uri` / `report-to`

- **Note:** Works **with** [[SOP (Same-Origin Policy)]]


- **Core:** Content Security Policy is an HTTP response header that whitelists allowed so…

## Technical Details
### Report-only rollout

```http
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

### Production baseline (no inline JS)

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

### Nginx

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; object-src 'none'" always;
```

### Nonce pattern (inline scripts you control)

```http
Content-Security-Policy: script-src 'self' 'nonce-random123'
```

```html
<script nonce="random123">...</script>
```

- **Why avoid `'unsafe-inline'`:** any injected `<script>` runs

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank page / JS errors | DevTools Console CSP violations | Widen specific directive; nonce/hash inline |
| API calls blocked | `connect-src` | Add API origin explicitly |
| CDN assets blocked | `script-src`/`style-src` | Add CDN host; use Subresource Integrity |
| Can't embed in iframe | `frame-ancestors` | Set parent allowlist or `'none'` intentionally |
| Third-party widgets break | Multiple directives | Isolate widget subdomain; strict default-src |

## Mistakes to Avoid
- **Mistake:** CSP is not input sanitization
- **Mistake:** `unsafe-eval` opens `eval` — some bundlers need it in dev only
- **Mistake:** Meta tag CSP — can't set `frame-ancestors` — must be HTTP header
- **Mistake:** Report-only forever — ship enforce mode after burn-in

## Pros/Cons or Trade-offs
- **Pro:** Limits XSS blast radius even when markup encoding fails.
- **Con:** Don't deploy `'unsafe-inline' 'unsafe-eval' *` — that's theater. Fix asset pipeline instead.

## Comparison
- vs [[cross-site scripting]]: CSP mitigates XSS impact; encoding/escaping prevents XSS.
- vs [[CORS (Cross Origin Request Sharing)]]: CORS governs JS read of responses


### Use cases
- Lock down script sources on a marketing site or SPA to contain XSS blast radi…
