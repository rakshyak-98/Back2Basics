[[Security]] [[SOP (Same-Origin Policy)]] [[CORS (Cross Origin Request Sharing)]] [[JWT authentication]] [[JWT]] [[content security policy]] [[Authentication terms]]

# XSRF (cross-site request forgery)

> CSRF/XSRF — evil.com tricks the browser into sending your bank.com cookies on a forged request; the bank thinks it’s you.





## Interview Relevance
Browser auth: CSRF abuses ambient cookies; SameSite, CSRF tokens, and why Bearer tokens in headers change the threat.

## Sources
- [OWASP — CSRF](https://owasp.org/www-community/attacks/csrf) — overview
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — deep-dive

## Core Definition
CSRF/XSRF tricks a victim's browser into sending authenticated requests to a site using the victim's cookies without the victim's intent.

## Key Concepts
```txt
You logged into bank.com (session cookie)
        │
evil.com form ──POST──► bank.com/transfer
        │                 Cookie: session=…  (auto-attached)
        └─ bank executes action as you
```

Defense: something evil.com **cannot** read or guess — synchronizer token, or `SameSite` cookies, or both.

| Defense | How it helps |
|---------|----------------|
| **CSRF token** | Hidden field / header bound to session; attacker can’t read it |
| **`SameSite=Lax/Strict`** | Cookie not sent on most cross-site requests |
| **Custom header + CORS** | Simple form POST can’t set `X-CSRF-Token`; preflight required |
| **Re-auth for money moves** | Password/2FA on sensitive actions |

## Technical Details
```js
// Express + csurf-style pattern (concept)
app.use(csrfProtection)
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() })
})
app.post('/transfer', (req, res) => {
  // middleware rejects missing/invalid _csrf
})
```

```http
Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax
```

| Knob | Why it matters |
|------|----------------|
| Token in header (`X-CSRF-Token`) | SPA-friendly; pairs with cookie session |
| Double-submit cookie | Token cookie + matching header/body |
| `SameSite=None; Secure` | Needed for true cross-site iframes — **raises** CSRF risk; compensate with tokens |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Legit form `403 CSRF` | Token missing/stale; session rotated | Render fresh token; fix cookie domain/path |
| SPA POST fails CSRF | Token not in header | Read meta/cookie token; send header |
| Cross-subdomain breaks | Cookie `Domain` / SameSite | Align cookie scope; prefer host-only |
| “Works in Postman” | No browser cookie auto-send | Expected — test with real browser |
| Payment forged via img/form | No CSRF on state-changing GET | **Never** mutate on GET; require token |
| Mobile WebView oddities | Third-party cookie blocked | Prefer Bearer token auth over cookie |

## Real-World Applications
Cookie-session form posts need CSRF tokens or SameSite=Lax/Strict; Bearer-header APIs are largely CSRF-immune.

## Pros/Cons or Trade-offs
- **Pro:** Well-understood defenses (tokens, SameSite) for cookie-session apps.
- **Con:** Pure Bearer-token APIs (no cookies) — CSRF tokens usually unnecessary; still guard XSS.
- **Con:** Server-to-server webhooks — use signatures ([[HMAC (Hash based Message Authentication Codes)]]), not CSRF tokens.
- **Con:** Public read-only GETs — no session mutation → nothing to forge.

## Comparison
- vs [[cross-site scripting]]: CSRF needs the victim's browser + cookies; XSS runs code as the site.
- vs [[CORS (Cross Origin Request Sharing)]]: CORS does not prevent cookie-based CSRF on simple requests.

## Mistakes to Avoid
- CORS does not stop CSRF — CSRF is about the browser *sending* cookies; CORS controls *reading* responses.
- Bearer JWT in `Authorization` header — generally CSRF-resistant (evil page can’t set that header on your API from a simple form). Cookie sessions need CSRF defenses.
- `SameSite=Lax` still allows top-level GET — don’t put state changes on GET links.
