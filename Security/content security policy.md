[[cross-site scripting]] [[response header]] [[SOP (Same-Origin Policy)]]

# Content Security Policy

> HTTP header that whitelists where scripts, styles, connections, and frames may load from — primary defense-in-depth against XSS and data exfiltration.

---

## Mental model

**CSP** replaces "browser trusts all inline script" with an explicit **allowlist**:

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
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

Violations report to `report-uri` / `report-to` — use for rollout, not sole monitoring.

Works **with** [[SOP (Same-Origin Policy)]] — CSP is finer-grained fetch control.

---

## Standard config / commands

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

**Why avoid `'unsafe-inline'`:** any injected `<script>` runs — defeats XSS mitigation.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank page / JS errors | DevTools Console CSP violations | Widen specific directive; nonce/hash inline |
| API calls blocked | `connect-src` | Add API origin explicitly |
| CDN assets blocked | `script-src`/`style-src` | Add CDN host; use Subresource Integrity |
| Can't embed in iframe | `frame-ancestors` | Set parent allowlist or `'none'` intentionally |
| Third-party widgets break | Multiple directives | Isolate widget subdomain; strict default-src |

---

## Gotchas

> [!WARNING]
> **CSP is not input sanitization** — still escape/stored XSS in HTML contexts.

> [!WARNING]
> **`unsafe-eval` opens `eval`** — some bundlers need it in dev only.

> [!WARNING]
> **Meta tag CSP** can't set `frame-ancestors` — must be HTTP header.

> [!WARNING]
> **Report-only forever** — ship enforce mode after burn-in.

---

## When NOT to use

Don't deploy `'unsafe-inline' 'unsafe-eval' *` — that's theater. Fix asset pipeline instead.

---

## Related

[[cross-site scripting]] [[response header]] [[SOP (Same-Origin Policy)]] [[XSRF (cross-site request forgery)]] [[https]]
