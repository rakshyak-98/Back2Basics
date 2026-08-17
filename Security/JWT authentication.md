[[single-sign-on (SSO)]] [[TLS (Transport Layer Security)]] [[IDOR]] [[KMS]]

# JWT authentication

> signed (or encrypted) JSON claims for stateless auth — verify **algorithm, signature, and claims** server-side every request — **RFC 7519**.

```txt
        JWT authentication ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** API reviews: verify algorithm, signature, and claims every request

## Sources
- [RFC 7519 — JWT](https://www.rfc-editor.org/rfc/rfc7519) — deep-dive
- [OWASP — JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) — overview

## Key Concepts
- **Note:** JWT = `header.payload.signature` (JWS) or nested JWE. Server trusts token onl…

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


- **Core:** JWT authentication uses signed (or encrypted) JSON claims as bearer credentia…

## Technical Details
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

- Use **`jti`** (unique token ID) for blacklist keys

- when user logs in and receives an access token or refresh token, multiple tok…

### Failure signals

| Symptom                               | Check                                                      | Fix                                                                    |
| ------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- |
| `invalid signature` after IdP change  | JWKS `kid`; cached old key                                 | Refresh JWKS; support multiple `kid`; reduce cache TTL during rotation |
| `jwt expired` sporadic                | NTP on API nodes vs IdP                                    | Sync time (chrony); set `clockTolerance: 30`                           |
| `jwt not active` (`nbf`)              | Clock ahead on client                                      | Fix skew; avoid `nbf` unless needed                                    |
| Auth bypass reports (pen test)        | Accept `alg: none`? HS256 with public key?                 | **Allowlist algorithms**; use asymmetric RS256/ES256 for multi-service |
| `kid` header attack                   | App fetches key from attacker URL via `kid` path traversal | Map `kid` to known JWKS only — never filesystem paths from header      |
| Logged-out user still works until exp | No revocation                                              | Blacklist `jti`; or short access token (5–15m) + refresh               |
| Refresh token reuse detected          | Rotation not enforced                                      | Issue new refresh on use; invalidate family on reuse                   |
| `aud` mismatch                        | Token for wrong client                                     | Validate `aud` matches your API identifier                             |

## Mistakes to Avoid
- **Mistake:** `alg: none` attack:
- **Mistake:** `kid` injection:
- **Mistake:** **Don't store secrets in JWT payload**
- **Mistake:** ### Key rotation playbook
- **Mistake:** 1

## Pros/Cons or Trade-offs
- **Pro:** Scales horizontally without a central session store (until revocation needs appear).
- **Con:** Session-heavy monolith with server-side session store already → JWT adds complexity without benefit.
- **Con:** Long-lived credentials in mobile apps without secure storage → use platform keystore + refresh rotation.
- **Con:** Passing JWT in URL query strings → leaks via logs and Referer.

## Comparison
- vs server sessions: JWT is typically stateless until denylist/rotation; sessions need a store.
- vs [[single-sign-on (SSO)]]: SSO issues identity; JWT is a common token format afterward.


### Use cases
- Stateless API access tokens verified at each service
