<!-- note-strategy: operational -->
[[Security]] [[single-sign-on (SSO)]] [[JWT authentication]] [[OAuth]]

# white-label auth-url

> White-label auth URL — users log in on your branded domain while an external IdP still runs the real authentication behind the scenes.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Your application sends the browser to a tenant-specific login URL that *looks* like you (custom domain/theme). The IdP authenticates, then redirects back with a code/token.

```txt
App (partner.example)
  → redirect to auth.partner.example (CNAME → IdP)
  → user enters creds (IdP UI, your skin)
  → redirect back ?code=… → app exchanges code
```

| Term | Meaning |
|------|---------|
| **White-label** | No “Powered by BigIdP” chrome; your domain/branding |
| **Auth URL** | Authorize endpoint (per tenant/client) |
| **Callback / redirect_uri** | Must be exact allowlisted URL |

Common with Auth0/Cognito/Okta custom domains + OIDC.

---

## Standard config / commands

```txt
# Conceptual OIDC authorize URL
https://auth.yourbrand.com/authorize
  ?client_id=…
  &redirect_uri=https://app.yourbrand.com/callback
  &response_type=code
  &scope=openid profile
  &state=…&nonce=…
```

| Knob | Why it matters |
|------|----------------|
| Custom domain TLS | Cert on auth hostname; DNS CNAME to IdP |
| Per-tenant client_id | Isolation between white-label customers |
| Exact `redirect_uri` | Mismatch → IdP hard fail |
| Branding/theme | Logos, CSS — still IdP security pages |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `redirect_uri_mismatch` | Allowlist vs actual URL | Exact match incl. scheme/path/slash |
| Cert error on auth host | Custom domain TLS | Fix cert/CNAME; wait DNS |
| Wrong tenant branding | client_id / org id | Map subdomain → tenant config |
| Loop login ↔ app | Cookie `Secure`/`SameSite`; mixed domains | Align parent domain cookies carefully |
| CORS on token endpoint | Browser calling token URL | Prefer server-side code exchange (BFF) |

---

## Gotchas

> [!WARNING]
> **Branding ≠ trust boundary** — users still type passwords into the IdP; phishing education still matters.

> [!WARNING]
> **Custom domain DNS cutover** — broken CNAME = total login outage for that brand.

> [!WARNING]
> **Shared IdP cookies across brands** — understand session sharing; isolate tenants if required.

---

## When NOT to use

- **First-party simple login** — local sessions may be enough.
- **Workforce SSO already on IdP domain** — white-label mostly for customer-facing multi-tenant brands.
- **Native apps with ASWebAuthenticationSession** — different URL patterns; still OIDC but not “white-label web.”

---

## Related

[[single-sign-on (SSO)]] [[JWT authentication]] [[Authentication terms]] [[TLS (Transport Layer Security)]]
