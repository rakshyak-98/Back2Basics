[[Security]] [[CORS (Cross Origin Request Sharing)]] [[XSRF (cross-site request forgery)]] [[cross-site scripting]]

# SOP (Same-Origin Policy)

> SOP (Same-Origin Policy) — the browser wall: page JS on one origin cannot read another origin’s responses or DOM.

---

## Mental model

**Say it in one breath:** Origin = scheme + host + port. Same origin → free access. Different origin → JS cannot read the result unless the other side opts in ([[CORS (Cross Origin Request Sharing)]]).

```txt
https://app.example.com:443
         ≠
https://api.example.com:443   (host differs)
http://app.example.com:80     (scheme differs)
https://app.example.com:8443  (port differs)
```

| Allowed without CORS? | Blocked for JS read? |
|-----------------------|----------------------|
| Same-origin `fetch` / XHR | Cross-origin `fetch` response body |
| Navigation, form POST | Reading cross-origin iframe DOM |
| `<script src>`, `<img>` load | Reading pixels/bytes of those loads |

SOP is **browser-enforced**. curl, Postman, and server-to-server ignore it.

---

## Standard config / commands

```js
// Same origin — no CORS needed (prefer BFF / reverse-proxy same host)
fetch('/api/me')

// Cross origin — server must send ACAO (see CORS note)
fetch('https://api.example.com/me', { credentials: 'include' })
```

```html
<!-- SOP blocks reading iframe document -->
<iframe src="https://other.example.com"></iframe>
<script>
  // throws SecurityError
  document.querySelector('iframe').contentDocument
</script>
```

| Pattern | Why |
|---------|-----|
| App + API same host (`/api`) | Avoid CORS entirely |
| `document.domain` (legacy) | Deprecated — do not use |
| `postMessage` | Safe cross-origin messaging with origin checks |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Blocked by CORS policy` | Network → response headers | Server ACAO / preflight — [[CORS (Cross Origin Request Sharing)]] |
| Works in curl, fails in browser | SOP/CORS only in browsers | Fix API CORS or same-origin proxy |
| `SecurityError` on iframe | Cross-origin frame | `postMessage` + `event.origin` check |
| Localhost vs 127.0.0.1 “CORS” | Different hosts | Pick one hostname everywhere |
| Cookie missing cross-site | `SameSite` + credentials | Cookie flags + CORS credentials (not SOP alone) |
| Subdomain can't share storage | Different origins | Explicit shared auth via tokens / SSO |

---

## Gotchas

> [!WARNING]
> **SOP ≠ CSRF protection** — browsers still *send* cookies on cross-site form POSTs; use CSRF tokens / SameSite ([[XSRF (cross-site request forgery)]]).

> [!WARNING]
> **`<script>` and `<img>` still load cross-origin** — SOP blocks *reading* them; XSS via injected script is a different bug ([[cross-site scripting]]).

> [!WARNING]
> **Port and scheme count** — `http://localhost:3000` ≠ `https://localhost:3000`.

---

## When NOT to use

- **Server-side HTTP clients** — no SOP; secure with authz and network policy.
- **Native mobile apps** — different trust model; not browser SOP.
- **Relaxing SOP in the browser** — you can’t; only the *target* server can grant CORS.

---

## Related

[[CORS (Cross Origin Request Sharing)]] [[XSRF (cross-site request forgery)]] [[cross-site scripting]] [[content security policy]] [[response header]]
