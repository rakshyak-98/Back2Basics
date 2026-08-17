[[Security]] [[CORS (Cross Origin Request Sharing)]] [[XSRF (cross-site request forgery)]] [[cross-site scripting]] [[content security policy]] [[response header]]

# SOP (Same-Origin Policy)

> Origin Policy) — the browser wall: page JS on one origin cannot read another origin’s responses or DOM.





## Interview Relevance
Browser security foundation: what counts as an origin, what SOP blocks, and how CORS/CSP/CSRF relate.

## Sources
- [MDN — Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) — overview
- [HTML Living Standard — Origin](https://html.spec.whatwg.org/multipage/origin.html) — deep-dive

## Core Definition
The Same-Origin Policy is the browser rule that script on one origin cannot read another origin's responses or DOM by default.

## Key Concepts
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

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `Blocked by CORS policy` | Network → response headers | Server ACAO / preflight — [[CORS (Cross Origin Request Sharing)]] |
| Works in curl, fails in browser | SOP/CORS only in browsers | Fix API CORS or same-origin proxy |
| `SecurityError` on iframe | Cross-origin frame | `postMessage` + `event.origin` check |
| Localhost vs 127.0.0.1 “CORS” | Different hosts | Pick one hostname everywhere |
| Cookie missing cross-site | `SameSite` + credentials | Cookie flags + CORS credentials (not SOP alone) |
| Subdomain can't share storage | Different origins | Explicit shared auth via tokens / SSO |

## Real-World Applications
Browser isolation that makes XSS and CSRF design constraints — CORS is the deliberate SOP escape hatch.

## Pros/Cons or Trade-offs
- **Pro:** Foundational browser isolation that makes the web's multi-tenant model viable.
- **Con:** Server-side HTTP clients — no SOP; secure with authz and network policy.
- **Con:** Native mobile apps — different trust model; not browser SOP.
- **Con:** Relaxing SOP in the browser — you can’t; only the *target* server can grant CORS.

## Comparison
- vs [[CORS (Cross Origin Request Sharing)]]: CORS relaxes SOP for chosen origins.
- vs [[XSRF (cross-site request forgery)]]: SOP does not stop cookie-bearing cross-site *writes*; CSRF defenses do.

## Mistakes to Avoid
- SOP ≠ CSRF protection — browsers still *send* cookies on cross-site form POSTs; use CSRF tokens / SameSite ([[XSRF (cross-site request forgery)]]).
- `<script>` and `<img>` still load cross-origin — SOP blocks *reading* them; XSS via injected script is a different bug ([[cross-site scripting]]).
- Port and scheme count — `http://localhost:3000` ≠ `https://localhost:3000`.
