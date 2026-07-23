[[JWT authentication]] [[TLS (Transport Layer Security)]] [[IDOR]]

# Single-sign-on (SSO)

> One-line: one identity provider (IdP) login federates access to many apps via signed assertions — **SAML 2.0** or **OIDC/OAuth 2.0**.

## Mental model

SSO separates **authentication** (who you are) from **app sessions**. User authenticates once at the IdP (Okta, Azure AD, Google Workspace, Keycloak); the app receives a **signed token or assertion** and creates a local session.

```
User ──► App (SP) ──redirect──► IdP login
         ◄── SAML Response / OIDC id_token + code ──
App validates signature ──► session cookie / [[JWT authentication]]
```

| Term | SAML | OIDC |
|------|------|------|
| Identity Provider | IdP | IdP (same) |
| App | Service Provider (SP) | Relying Party (RP) / OAuth client |
| Wire format | XML assertion | JWT id_token (+ access_token) |
| Transport | HTTP-Redirect / POST binding | Authorization Code + PKCE |
| Metadata | `/metadata.xml` | `/.well-known/openid-configuration` |
| Logout | SLO (often brittle) | RP-initiated end_session (varies) |

**OAuth 2.0 alone** is authorization ("can this app access my Google Drive?"). **OIDC** adds identity (`id_token` with `sub`, `email`). Enterprise SSO integrations are almost always **OIDC** (greenfield) or **SAML** (legacy SaaS).

## Standard config / commands

### OIDC integration checklist (SE integrating SSO)

1. **Register app** at IdP → get `client_id`, `client_secret` (or public client + PKCE).
2. **Redirect URIs** — exact match required: `https://app.example.com/auth/callback` (no wildcards on most IdPs).
3. **Fetch discovery doc:** `curl https://idp.example.com/.well-known/openid-configuration`
4. **Validate id_token:** signature (JWKS from `jwks_uri`), `iss`, `aud`, `exp`, `nonce`.
5. **Map claims** → local user: `sub` (stable), `email`, groups → RBAC.
6. **Session strategy:** HTTP-only secure cookie after exchange; don't expose id_token to JS.
7. **SCIM** (optional) — IdP provisions/deprovisions users into app DB.

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

## Triage (when things break)

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

## Gotchas

> [!WARNING]
> **Never trust the id_token from the front channel without signature verification** against JWKS. Always validate server-side.

> [!WARNING]
> **SAML XML is easy to misconfigure** — one wrong ACS URL or cert = opaque 500s. Keep metadata under version control.

- **Just-in-time (JIT) provisioning** creates users on first login — plan default role; disable open signup.
- **SLO / global logout** rarely works across all SPs — document "logout clears this app only".
- **Multiple IdPs** (M&A) → account linking by email is fragile; prefer immutable `sub`.
- **Mobile / SPA** must use **Authorization Code + PKCE**, not implicit flow (deprecated).

## When NOT to use

- Machine-to-machine APIs → client credentials grant or mTLS, not interactive SSO.
- Single small app with local users → SSO adds IdP dependency without ROI.
- Long-lived CLI tools → API keys or device code flow, not browser SSO redirect.

## Related

[[JWT authentication]] · [[TLS (Transport Layer Security)]] · [[CORS (Cross Origin Request Sharing)]] · [[IDOR]]
