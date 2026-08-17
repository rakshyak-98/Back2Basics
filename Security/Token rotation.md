[[JWT authentication]] [[KMS]] [[Security]] [[single-sign-on (SSO)]] [[response header]]

# Token rotation

> Expire and replace secrets often so a leak has a short life — especially OAuth refresh tokens with reuse detection.

```txt
        Token rotation ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Session security: short-lived access tokens, refresh rotation, reuse detectio…

## Sources
- [RFC 6819 — OAuth 2.0 Threat Model](https://www.rfc-editor.org/rfc/rfc6819) — deep-dive
- [OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics) — overview

## Key Concepts
- **Core:** Token rotation expires and replaces credentials (access, refresh, or API keys…

## Technical Details
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

- Issue with `kid` in header
- Stop signing with old `kid`

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

- Rolling session: extend expiry on activity

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Mass logout after deploy | JWKS old key removed too early | Re-add key; lengthen overlap |
| Refresh loop / 401 storm | Clock skew; rotated refresh not persisted client-side | Sync NTP; fix client to store new refresh |
| "Invalid signature" intermittent | Multiple issuers/kids; cached JWKS stale | CDN cache JWKS short TTL; verify `kid` |
| One leaked refresh compromises all | No rotation/reuse detection | Enable refresh rotation + family revoke |
| KMS decrypt fail after key delete | Data encrypted with deleted CMK | Restore key from deletion pending; re-encrypt data |
| Mobile apps break on rotation | Hard-coded old public key | Pin to JWKS URL with update mechanism |

## Mistakes to Avoid
- **Rotating signing key without overlap::** → global 401
- **Mistake:** Refresh token in localStorage
- **Mistake:** Logging tokens
- **Mistake:** Symmetric JWT secret in 12 microservices

## Pros/Cons or Trade-offs
- **Pro:** Shrinks leak windows and can detect stolen refresh-token reuse.
- **Con:** Rotate on every API request — unnecessary overhead; match risk (15m access / 7d refresh typical for web).
- **Con:** Rotation without revocation store — stolen refresh works until natural expiry if you can't invalidate server-side.

## Comparison
- vs long-lived API keys: rotation shrinks leak windows and enables reuse detection.
- vs [[JWT authentication]]: rotation applies to refresh/signing keys that mint JWTs.


### Use cases
- OAuth refresh-token rotation with reuse detection limits the window after a s…
