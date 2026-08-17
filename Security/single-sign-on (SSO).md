[[JWT authentication]] [[TLS (Transport Layer Security)]] [[IDOR]] [[CORS (Cross Origin Request Sharing)]]

# Single-sign-on (SSO)

> One IdP login unlocks many apps — the Service Provider redirects to the Identity Provider, then back with an assertion or code.





## Interview Relevance
Identity interviews: IdP vs SP, OIDC/SAML flows, redirect_uri exactness, and when SSO is overkill.

## Sources
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) — deep-dive
- [Wikipedia — Single sign-on](https://en.wikipedia.org/wiki/Single_sign-on) — overview

## Core Definition
SSO lets a user authenticate once at an Identity Provider and access multiple Service Providers without separate passwords per app.

## Technical Details
### OIDC integration checklist (SE integrating SSO)

1. **Register application** at IdP → get `client_id`, `client_secret` (or public client + PKCE).
2. **Redirect URIs** — exact match required: `https://app.example.com/auth/callback` (no wildcards on most IdPs).
3. **Fetch discovery document:** `curl https://idp.example.com/.well-known/openid-configuration`
4. **Validate id_token:** signature (JWKS from `jwks_uri`), `iss`, `aud`, `exp`, `nonce`.
5. **Map claims** → local user: `sub` (stable), `email`, groups → RBAC.
6. **Session strategy:** HTTP-only secure cookie after exchange; don't expose id_token to JS.
7. **SCIM** (optional) — IdP provisions/deprovisions users into application DB.

### SAML integration checklist

1. Exchange **metadata XML** (SP ↔ IdP).
2. Configure **Assertion Consumer Service (ACS)** URL — POST binding most common.
3. **NameID format** — usually `emailAddress` or `persistent`.
4. **Attribute mapping** — `givenName`, `sn`, `memberOf`.
5. **Sign requests / encrypt assertions** per IdP policy; clock skew ≤ 5 min.
6. **SP Entity ID** must match metadata exactly.

### Debug commands

```shell
# OIDC discovery
curl -s https://login.microsoftonline.com/<tenant>/v2.0/.well-known/openid-configuration | jq .

# JWKS (verify JWT locally)
curl -s https://idp/.well-known/jwks.json | jq .

# Decode JWT payload (signature NOT verified — triage only)
echo "$ID_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | jq .

# SAML trace — browser devtools → POST to ACS, base64 InResponseTo
# openssl verify signature with IdP cert from metadata
```

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `redirect_uri_mismatch` | IdP app config vs actual callback URL | Exact match scheme/host/path; trailing slash matters |
| `invalid_client` | Secret rotated; wrong tenant | Update client secret; verify tenant ID in issuer URL |
| Login works, instant logout | Cookie `Secure`/`SameSite`; proxy HTTPS | Terminate TLS at edge; set `SameSite=None; Secure` if cross-site |
| `Invalid signature` on SAML | IdP cert rotated; stale metadata | Refresh IdP metadata; update SP cert fingerprint |
| `Audience restriction invalid` | Entity ID mismatch | Align SP Entity ID with assertion `Audience` |
| `AuthnStatement too old` / skew | NTP drift on SP or IdP | Sync chrony; allow ±300s in validator |
| Groups not mapped to roles | Missing attribute release | IdP attribute statement / OIDC groups claim |
| Works in dev, fails prod | Different client IDs; HTTP vs HTTPS | Separate IdP apps per env; never HTTP callbacks in prod |
| Infinite redirect loop | Session not persisted; cookie domain | Fix cookie domain; check middleware order |

## Real-World Applications
Employees open many internal apps after one IdP login via OIDC or SAML.

## Pros/Cons or Trade-offs
- **Pro:** One strong login UX across many apps; central MFA and offboarding.
- **Con:** Machine-to-machine APIs → client credentials grant or mTLS, not interactive SSO.
- **Con:** Single small application with local users → SSO adds IdP dependency without ROI.
- **Con:** Long-lived CLI tools → API keys or device code flow, not browser SSO redirect.

## Comparison
- vs local username/password per app: SSO centralizes AuthN at an IdP.
- vs [[JWT authentication]]: SSO protocols (OIDC/SAML) often deliver JWTs or assertions afterward.

## Mistakes to Avoid
- Never trust the id_token from the front channel without signature verification — against JWKS. Always validate server-side.
- SAML XML is easy to misconfigure — one wrong ACS URL or cert = opaque 500s. Keep metadata under version control.
- **Just-in-time (JIT) provisioning** creates users on first login — plan default role; disable open signup.
- **SLO / global logout** rarely works across all SPs — document "logout clears this application only".
- **Multiple IdPs** (M&A) → account linking by email is fragile; prefer immutable `sub`.
- **Mobile / SPA** must use **Authorization Code + PKCE**, not implicit flow (deprecated).
