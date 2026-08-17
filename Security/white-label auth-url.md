[[Security]] [[single-sign-on (SSO)]] [[JWT authentication]] [[OAuth]] [[Authentication terms]] [[TLS (Transport Layer Security)]]

# white-label auth-url

> White-label auth URL — users log in on your branded domain while an external IdP still runs the real authentication behind the scenes.





## Interview Relevance
B2B SaaS identity: branded login domains while an external IdP still owns credentials — DNS, TLS, and redirect_uri pitfalls.

## Sources
- [OpenID Connect Core — redirect_uri](https://openid.net/specs/openid-connect-core-1_0.html) — deep-dive
- [Auth0 — Custom Domains](https://auth0.com/docs/customize/custom-domains) — overview

## Core Definition
A white-label auth URL lets users sign in on your branded domain while an external Identity Provider still performs authentication behind the scenes.

## Key Concepts
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

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `redirect_uri_mismatch` | Allowlist vs actual URL | Exact match incl. scheme/path/slash |
| Cert error on auth host | Custom domain TLS | Fix cert/CNAME; wait DNS |
| Wrong tenant branding | client_id / org id | Map subdomain → tenant config |
| Loop login ↔ app | Cookie `Secure`/`SameSite`; mixed domains | Align parent domain cookies carefully |
| CORS on token endpoint | Browser calling token URL | Prefer server-side code exchange (BFF) |

## Real-World Applications
SaaS tenants log in at `auth.customer.com` CNAME'd to your IdP while branding stays on the customer domain.

## Pros/Cons or Trade-offs
- **Pro:** Tenant branding without hosting their credential store yourself.
- **Con:** First-party simple login — local sessions may be enough.
- **Con:** Workforce SSO already on IdP domain — white-label mostly for customer-facing multi-tenant brands.
- **Con:** Native apps with ASWebAuthenticationSession — different URL patterns; still OIDC but not “white-label web.”

## Comparison
- vs vanilla [[single-sign-on (SSO)]]: same IdP flows with custom domain/branding and stricter DNS/TLS setup.
- vs embedded login widgets: full redirect to branded auth URL keeps credentials off the app origin.

## Mistakes to Avoid
- Branding ≠ trust boundary — users still type passwords into the IdP; phishing education still matters.
- Custom domain DNS cutover — broken CNAME = total login outage for that brand.
- Shared IdP cookies across brands — understand session sharing; isolate tenants if required.
