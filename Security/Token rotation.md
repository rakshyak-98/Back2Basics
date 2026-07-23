[[JWT authentication]] [[KMS]] [[Security]] [[single-sign-on (SSO)]]

# Token rotation

> **Limit blast radius of leaked credentials** — refresh/access tokens, API keys, session ids, and signing keys expire and are replaced on a schedule or after use. **RFC 6819 (OAuth 2.0 Threat Model)** + prod incidents from never-rotated JWT signing keys.

## Mental model

Long-lived secrets **will** leak (logs, git, browser, support tickets). Rotation means: **short TTL** + **refresh path** + **revocation/list** + **key versioning** so old material stops working without hard-downtime if done right.

```
Access token (15m) ──► API
       │
       └── refresh token (rotating, bound to client) ──► new pair
Signing keys (JWKS kid) ──► verify old + new during overlap window
```

OAuth **refresh token rotation** (RFC 6819 §5.2.2.3): each refresh issues new refresh token; reuse of old refresh = breach signal → revoke family.

## Standard config / commands

### JWT signing keys (asymmetric preferred)

```json
// JWKS — publish two keys during rotation
{
  "keys": [
    { "kid": "2026-03", "kty": "RSA", "use": "sig", ... },
    { "kid": "2025-11", "kty": "RSA", "use": "sig", ... }
  ]
}
```

- Issue with `kid` in header; verifiers accept both keys for **overlap period** (e.g. 7 days).
- Stop signing with old `kid`; remove from JWKS after max access token TTL elapsed.

### OAuth2 refresh rotation (server)

1. Client stores refresh token securely (httpOnly cookie or OS vault).
2. On refresh: validate refresh → issue **new** access + **new** refresh → **invalidate** old refresh hash in DB.
3. Detect **reuse** of invalidated refresh → revoke all sessions for user/client.

### API keys (machine)

| Pattern | Rotation |
|---------|----------|
| Dual-key grace | Key A active, add Key B, deploy clients, retire A |
| STS-style | Prefer [[aws STS (Security Token Service)]] roles over static keys |
| Hash at rest | Store bcrypt/sha256 of key; compare on use |

```bash
# Example: rotate with overlap (pseudo)
vault write -force auth/approle/role/myrole/secret-id
# deploy new secret-id; after 24h revoke old accessor
```

### Session cookies

- Rolling session: extend expiry on activity; rotate session id on privilege change (login, password reset) to prevent fixation.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Mass logout after deploy | JWKS old key removed too early | Re-add key; lengthen overlap |
| Refresh loop / 401 storm | Clock skew; rotated refresh not persisted client-side | Sync NTP; fix client to store new refresh |
| "Invalid signature" intermittent | Multiple issuers/kids; cached JWKS stale | CDN cache JWKS short TTL; verify `kid` |
| One leaked refresh compromises all | No rotation/reuse detection | Enable refresh rotation + family revoke |
| KMS decrypt fail after key delete | Data encrypted with deleted CMK | Restore key from deletion pending; re-encrypt data |
| Mobile apps break on rotation | Hard-coded old public key | Pin to JWKS URL with update mechanism |

## Gotchas

> [!WARNING]
> **Rotating signing key without overlap** — all in-flight access tokens die instantly → global 401.

> [!WARNING]
> **Refresh token in localStorage** — XSS steals long-lived credential; httpOnly cookie + rotation + short access token.

> [!WARNING]
> **Logging tokens** — rotation useless if every refresh logs bearer token at INFO.

> [!WARNING]
> **Symmetric JWT secret in 12 microservices** — rotation requires coordinated deploy; use asymmetric + JWKS.

## When NOT to use

- **Rotate on every API request** — unnecessary overhead; match risk (15m access / 7d refresh typical for web).
- **Rotation without revocation store** — stolen refresh works until natural expiry if you can't invalidate server-side.

## Related

[[JWT authentication]] · [[KMS]] · [[single-sign-on (SSO)]] · [[Security]] · [[response header]]
