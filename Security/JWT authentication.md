[[single-sign-on (SSO)]] [[TLS (Transport Layer Security)]] [[IDOR]]

# JWT authentication

> One-line: signed (or encrypted) JSON claims for stateless auth — verify **algorithm, signature, and claims** server-side every request — **RFC 7519**.

## Mental model

JWT = `header.payload.signature` (JWS) or nested JWE. Server trusts token only after **cryptographic verification** + **claim checks**. Stateless by default — revocation requires blocklist or short TTL + refresh rotation.

```
Client ── Authorization: Bearer eyJ... ──► API
              verify sig (JWKS / shared secret)
              check exp, iss, aud, nbf
              authorize sub + scopes
```

| Part | Contents |
|------|----------|
| Header | `alg`, `typ`, optional `kid` |
| Payload | `sub`, `exp`, `iss`, `aud`, custom claims |
| Signature | HMAC or asymmetric over `header.payload` |

## Standard config / commands

### Verify safely (Node — jsonwebtoken + jwks-rsa)

```javascript
const jwt = require('jsonwebtoken');
const jwks = require('jwks-rsa');

const client = jwks({
  jwksUri: 'https://idp.example.com/.well-known/jwks.json',
  cache: true,
  rateLimit: true,
});

function getKey(header, cb) {
  client.getSigningKey(header.kid, (err, key) => {
    cb(err, key?.getPublicKey());
  });
}

function verifyToken(token) {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getKey,
      {
        algorithms: ['RS256'],           // explicit allowlist — blocks alg:none
        issuer: 'https://idp.example.com',
        audience: 'my-api',
        clockTolerance: 30,              // seconds — clock skew
      },
      (err, decoded) => (err ? reject(err) : resolve(decoded))
    );
  });
}
```

### Key rotation (asymmetric)

```shell
# IdP publishes multiple keys in JWKS — old + new during rotation
curl -s https://idp/.well-known/jwks.json | jq '.keys[].kid'

# Your verifier must fetch JWKS periodically (cache 5–15 min max)
# Accept tokens signed by any key in set matching kid
```

### Token blacklisting (logout / compromise)

```javascript
// On logout: TTL = remaining exp
const ttl = decoded.exp - Math.floor(Date.now() / 1000);
if (ttl > 0) await redis.setEx(`bl:${jti}`, ttl, '1');

// Middleware: reject if jti in blacklist (requires jti claim in token)
```

Use **`jti`** (unique token ID) for blacklist keys — not the full token string (memory heavy).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `invalid signature` after IdP change | JWKS `kid`; cached old key | Refresh JWKS; support multiple `kid`; reduce cache TTL during rotation |
| `jwt expired` sporadic | NTP on API nodes vs IdP | Sync time (chrony); set `clockTolerance: 30` |
| `jwt not active` (`nbf`) | Clock ahead on client | Fix skew; avoid `nbf` unless needed |
| Auth bypass reports (pen test) | Accept `alg: none`? HS256 with public key? | **Allowlist algorithms**; use asymmetric RS256/ES256 for multi-service |
| `kid` header attack | App fetches key from attacker URL via `kid` path traversal | Map `kid` to known JWKS only — never filesystem paths from header |
| Logged-out user still works until exp | No revocation | Blacklist `jti`; or short access token (5–15m) + refresh |
| Refresh token reuse detected | Rotation not enforced | Issue new refresh on use; invalidate family on reuse |
| `aud` mismatch | Token for wrong client | Validate `aud` matches your API identifier |

## Gotchas

> [!WARNING]
> **`alg: none` attack:** Libraries that honor the header algorithm can accept unsigned tokens if `algorithms` isn't restricted. Always pass explicit `algorithms: ['RS256']`.

> [!WARNING]
> **`kid` injection:** If server does `fs.readFile('/keys/' + header.kid)` an attacker sets `kid` to `../../etc/passwd`. Use JWKS lookup table only.

- **Don't store secrets in JWT payload** — base64 is not encryption; anyone can read claims.
- **HS256 with shared secret** leaks if any service discloses secret — prefer RS256 + JWKS for microservices.
- **`jwt.decode()` without verify** is for debugging only — never authorize on it.
- **Long-lived JWTs** can't be revoked without infrastructure — pair 15m access + refresh with rotation.
- **Clock skew:** validate `exp` and `nbf` with small tolerance; IdP and all API nodes on UTC/NTP.

### Key rotation playbook

1. IdP adds new key to JWKS (`kid-new`), still signs with old.
2. Deploy verifiers that accept both keys (JWKS poll).
3. IdP switches signing to `kid-new`.
4. After max token TTL elapsed, remove old key from JWKS.

## When NOT to use

- Session-heavy monolith with server-side session store already → JWT adds complexity without benefit.
- Long-lived credentials in mobile apps without secure storage → use platform keystore + refresh rotation.
- Passing JWT in URL query strings → leaks via logs and Referer.

## Related

[[single-sign-on (SSO)]] · [[TLS (Transport Layer Security)]] · [[IDOR]] · [[KMS]]
