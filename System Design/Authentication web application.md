[[System Design]] [[JWT]] [[single-sign-on (SSO)]] [[TOTP (Time based One Time Password)]] [[XSRF (cross-site request forgery)]]

# Authentication web application

> Web authentication — prove who the user is (session, token, or IdP), then enforce authz on every request.

---

## Mental model

**Say it in one breath:** Credentials → server verifies → issues session cookie or tokens → browser sends them → server checks on each call. MFA adds a second factor; SSO moves verify to an IdP.

```txt
Browser ──HTTPS──► App
   │ login form / OIDC redirect
   ▼
IdP or local user store → session / JWT → APIs
```

| Term | Plain |
|------|-------|
| AuthN | Who are you? |
| AuthZ | What may you do? |
| Session cookie | Server-side session id |
| JWT | Signed claims client carries |
| OAuth/OIDC | Delegate login to IdP |
| Passkey/WebAuthn | Phishing-resistant public-key auth |
| TOTP/MFA | Second factor |

Threats: MITM (use HTTPS), phishing, credential stuffing, XSS stealing tokens, CSRF on cookie sessions.

---

## Standard config / commands

```txt
Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax; Path=/
```

```js
// Sketch: local session
app.post('/login', async (req, res) => {
  const user = await verifyPassword(req.body)
  req.session.userId = user.id
  res.redirect('/app')
})
```

| Pattern | Use |
|---------|-----|
| Cookie session | Classic SSR apps |
| Bearer JWT | APIs / mobile |
| BFF | SPA + httpOnly cookies |
| OIDC | Workforce / social login |

## Login form flow

1. GET form (CSRF token if cookie session).
2. POST credentials over HTTPS.
3. Verify hash ([[yashcrypt]] / argon2); optional MFA.
4. Establish session; regenerate session id.
5. Subsequent requests carry cookie or `Authorization`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Login works, API 401 | Cookie domain/Secure/SameSite | Align site + HTTPS |
| CSRF on state change | Missing token / SameSite | [[XSRF (cross-site request forgery)]] |
| SSO redirect loop | `redirect_uri`, clock | Fix IdP app config |
| JWT forever valid | No `exp` / no revoke | Short TTL + refresh rotation |
| MFA codes fail | NTP skew | Sync time; widen window slightly |
| Session fixation | Id not rotated at login | Regenerate session id |

---

## Gotchas

> [!WARNING]
> **HTTPS terminates elsewhere** — app must still set `Secure` cookies correctly behind proxy (`X-Forwarded-Proto`).

> [!WARNING]
> **XSS + localStorage JWT** — prefer httpOnly cookies or strict CSP.

> [!WARNING]
> **AuthN ≠ AuthZ** — logged-in user still needs object-level checks ([[IDOR]]).

---

## When NOT to use

- **Public read-only content** — no auth tax.
- **Service-to-service** — mTLS or signed tokens, not human login forms.
- **Building your own crypto password protocol** — use vetted libs + IdP when possible.

---

## Related

[[JWT]] [[single-sign-on (SSO)]] [[TOTP (Time based One Time Password)]] [[XSRF (cross-site request forgery)]] [[Authentication terms]]
