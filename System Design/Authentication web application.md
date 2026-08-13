[[JWT authentication]] [[single-sign-on (SSO)]] [[TOTP (Time based One Time Password)]] [[XSRF (cross-site request forgery)]] [[API design]] [[IDOR]]

# Authentication web application

> Web authentication proves who the user is on each request; authorization decides what they may do — sessions, tokens, and identity providers are transport mechanisms, not substitutes for object-level checks.

---

## Authentication versus authorization

| Term | Question |
|------|----------|
| **Authentication** | Who are you? |
| **Authorization** | What may you do on this resource? |

Logging in successfully does not imply access to another user's invoice ([[IDOR]]) — enforce authorization on every handler.

## Common patterns

```txt
Browser ──HTTPS──► Application
   │ login form / OpenID Connect redirect
   ▼
Identity provider or local user store → session or JSON Web Token → APIs
```

| Pattern | Fit |
|---------|-----|
| Server-side session cookie | Classic server-rendered applications |
| Bearer JSON Web Token | Mobile and single-page application APIs |
| Backend-for-frontend | Single-page application with httpOnly cookie |
| OpenID Connect | Workforce or social login via [[single-sign-on (SSO)]] |
| WebAuthn passkeys | Phishing-resistant public-key authentication |
| Time-based one-time password | Second factor ([[TOTP (Time based One Time Password)]]) |

### Session cookie attributes

```http
Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax; Path=/
```

- **HttpOnly** — JavaScript cannot read (reduces cross-site scripting token theft).
- **Secure** — Transport Layer Security only.
- **SameSite** — reduces [[XSRF (cross-site request forgery)]] on cross-site posts.

## Login flow (local credentials)

1. Serve form (include cross-site request forgery token for cookie sessions).
2. Post credentials over Transport Layer Security.
3. Verify password hash (Argon2, bcrypt) — never store plaintext.
4. Optional multi-factor authentication step.
5. Create session; **regenerate session identifier** after login (prevents session fixation).
6. Subsequent requests send cookie or `Authorization` header.

## JSON Web Token cautions

Short-lived access tokens, refresh rotation, and revocation strategy for stolen tokens. Storing tokens in `localStorage` is vulnerable to cross-site scripting — prefer httpOnly cookies or strict Content Security Policy.

See [[JWT authentication]] for claim design and validation.

## Threat model highlights

| Threat | Mitigation |
|--------|------------|
| Credential stuffing | Rate limit, breached-password checks, multi-factor |
| Phishing | WebAuthn, identity provider hardening |
| Man-in-the-middle | Transport Layer Security everywhere |
| Cross-site scripting | Content Security Policy, output encoding |
| Cross-site request forgery | SameSite cookies, anti-forgery tokens |

## Symptom → direction

| Symptom | Check |
|---------|-------|
| Login works, API returns 401 | Cookie domain, `Secure`, `SameSite`, proxy `X-Forwarded-Proto` |
| Single sign-on redirect loop | Redirect URI mismatch, clock skew |
| Multi-factor codes fail | Network Time Protocol on server |
| Token valid forever | Missing `exp`, no revocation list |

Service-to-service calls use mutual Transport Layer Security or signed tokens — not human login forms.

## Sources

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
- [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) — OAuth 2.0.
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html).
- NIST SP 800-63B — digital identity guidelines.
