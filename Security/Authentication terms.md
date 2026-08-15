[[JWT authentication]] [[TOTP (Time based One Time Password)]] [[single-sign-on (SSO)]] [[HMAC (Hash based Message Authentication Codes)]] [[Token rotation]] [[digest access authentication]]

# Authentication terms

> Glossary of identity primitives — use consistent vocabulary in design reviews, incident docs, and API specs.

## Interview Relevance

Staff interviews expect precise AuthN vs AuthZ vocabulary — sessions, tokens, MFA, SSO — without conflating identity proof with permissions.

## Sources

- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html) — deep-dive
- [OWASP — Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — overview

## Core Definition

A shared glossary of identity primitives so design reviews, incidents, and API specs use the same words for AuthN, AuthZ, sessions, and tokens.

## Key Concepts

Authentication stack layers:

```txt
Identity proof  →  Session/token  →  Authorization (what you may do)
     │                    │
     └── factors          └── bearer vs proof-of-possession
```

| Term | Meaning |
|------|---------|
| **Authentication (AuthN)** | Proving *who* you are |
| **Authorization (AuthZ)** | What you're *allowed* to do |
| **Identification** | Claiming an identifier (username) — not proof |
| **Credential** | Secret or factor used to prove identity |
| **Factor** | Something you know/have/are (MFA) |
| **Session** | Server-side state keyed by session ID cookie |
| **Token** | Self-contained or opaque bearer (JWT, random UUID) |
| **SSO** | One login → multiple apps — [[single-sign-on (SSO)]] |
| **OAuth 2.0** | *Authorization* delegation framework (often confused with login) |
| **OIDC** | Identity layer on OAuth (ID token = AuthN) |
| **SAML** | XML SSO for enterprise |
| **TOTP** | Time-based OTP — [[TOTP (Time based One Time Password)]] |
| **top_secret / seed** | Shared secret for TOTP/HOTP generator — not the OTP itself |
| **Refresh token** | Long-lived token to obtain new access tokens |
| **Access token** | Short-lived API authorization |
| **API key** | Long-lived identifier + secret — service accounts |
| **mTLS** | Client cert as authentication factor |
| **RBAC / ABAC** | Role vs attribute based authorization |

## Technical Details

### TOTP setup (concept)

```bash
# Server stores base32 secret (the "top_secret" / seed)
# Client: Google Authenticator scans otpauth:// URI
# Verify: window ±1 step (30s) for clock skew
```

### JWT claims (AuthN vs AuthZ)

```json
{
  "sub": "user-123",
  "iss": "https://auth.example.com",
  "aud": "api.example.com",
  "exp": 1710000000,
  "scope": "read:orders"
}
```

### Naming in logs (avoid ambiguity)

```txt
authn_success user_id=... method=oidc
authz_denied  user_id=... resource=... action=delete
```

**Why separate AuthN/AuthZ:** passing login doesn't imply administrator — check permissions every request.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| "Logged in but 403" | AuthZ policy | Fix roles/scopes; not token refresh |
| Token valid forever | Missing `exp` | Short TTL + refresh rotation |
| TOTP drift fail | NTP on server/phone | Widen window temporarily; fix time |
| OAuth confusion | Using access token as ID token | Use OIDC ID token for identity |
| Session fixation | Cookie not rotated on login | Regenerate session ID |

## Real-World Applications

Use this vocabulary in design docs and incident write-ups so AuthN, AuthZ, MFA, and session vs token are not conflated.

## Pros/Cons or Trade-offs

- **Pro:** Shared vocabulary reduces design and incident ambiguity.
- **Con:** Don't roll custom crypto authentication protocols — use OIDC/SAML libraries and proven password KDFs ([[yashcrypt]] / argon2 / bcrypt).

## Comparison

- vs [[JWT authentication]] / [[single-sign-on (SSO)]]: glossary vs concrete mechanisms — use terms consistently when designing those systems.

## Mistakes to Avoid

- OAuth ≠ authentication — unless using OIDC ID token validated properly.
- `top_secret` in TOTP — compromise = forge all future codes; treat like password hash seed.
- Bearer token in URL — logs, Referer leaks — use Authorization header.
- API key in frontend — not secret; use backend proxy.
