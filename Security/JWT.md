[[Security]] [[JWT authentication]] [[Token rotation]] [[single-sign-on (SSO)]] [[HMAC (Hash based Message Authentication Codes)]] [[Asymmetrical Encryption]] [[Authentication terms]]

# JWT

> Signed blob of claims the client carries — the server verifies the signature instead of looking up a session (until you add revocation).

## Interview Relevance

Structure of JWT (header.payload.signature), when to use HS* vs RS*/ES*, and access vs refresh token roles.

## Sources

- [RFC 7519 — JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519) — deep-dive
- [RFC 7515 — JSON Web Signature](https://www.rfc-editor.org/rfc/rfc7515) — deep-dive
- [jwt.io introduction](https://jwt.io/introduction) — overview

## Core Definition

A JWT is three Base64url parts (header, payload, signature) carrying claims the client presents and the server verifies without a session lookup (until revocation is added).

## Key Concepts

```txt
Client                         Server
  │  POST /login (creds)         │
  │◄──── access JWT (+ refresh) ─┤
  │                              │
  │  GET /api  Authorization: Bearer <jwt>
  │──────────────────────────────►│
  │                    verify sig → accept claims
```

| Part | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Header** | `alg` + `typ` | “Which algorithm signed this?” |
| **Payload** | Claims (`sub`, `exp`, roles) | “Assertions — trusted only after verify.” |
| **Signature** | HMAC or RSA/ECDSA over header+payload | “Tamper seal.” |

**Access versus refresh:** short-lived access JWT in memory/`Authorization`; longer refresh in HttpOnly cookie → `POST /refresh` mints a new pair. Stateless until you add a denylist or rotate keys.

## Technical Details

```js
const jwt = require('jsonwebtoken')

// Prefer RS256/ES256 in multi-service; HS256 only if one shared secret
const access = jwt.sign(
  { sub: userId, role: 'editor' },
  process.env.JWT_PRIVATE_KEY, // or HS secret
  { algorithm: 'RS256', expiresIn: '10m', issuer: 'api.example.com', audience: 'app' }
)

const claims = jwt.verify(token, process.env.JWT_PUBLIC_KEY, {
  algorithms: ['RS256'], // never allow "none"
  issuer: 'api.example.com',
  audience: 'app',
})
```

| Knob | Why it matters |
|------|----------------|
| `expiresIn` / `exp` | Bound blast radius if stolen |
| `algorithms: [...]` | Blocks alg-confusion (`HS256` with public key as secret) |
| `iss` / `aud` | Stops tokens from other apps being accepted |
| Key rotation | Dual-verify old+new kid; see [[Token rotation]] |

Decode only for debug: `jwt.decode(t)` — **never** authorize from decode alone.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `invalid signature` | Wrong secret/key; HS vs RS mismatch | Match `alg` and key material; check env per env |
| `jwt expired` | Clock skew; too-short TTL | NTP sync; widen skew tolerance slightly; refresh flow |
| `jwt malformed` | Truncated header; wrong encoding | Don't URL-encode mid-token; trim whitespace |
| Works locally, fails in prod | Different JWT secret; wrong `iss`/`aud` | Align env; log verify error code only |
| Logout still authorized | Stateless JWT until `exp` | Short TTL + refresh revoke / denylist `jti` |
| `alg: none` accepted | Library default too loose | Explicit `algorithms` allowlist |
| Role claim ignored / wrong | Custom claim name collision | Namespace claims; verify before use |

## Real-World Applications

OIDC ID tokens and API access tokens are JWTs — parse claims only after signature and `alg` verification.

## Pros/Cons or Trade-offs

- **Pro:** Portable, inspectable claims format widely supported across languages.
- **Con:** Need instant server-side logout / session kill — opaque session IDs in Redis/DB.
- **Con:** Huge authorization graphs in every request — keep JWT thin; fetch permissions server-side.
- **Con:** Broadcast / manage connected clients — JWT is not a messaging channel; use WebSockets + sessions.

## Comparison

- vs opaque session ids: JWT is self-contained claims; opaque ids need a lookup.
- vs [[Token rotation]]: rotation policy sits on top of JWT access/refresh pairs.

## Mistakes to Avoid

- Payload is not secret — Base64 ≠ encryption. Put secrets in the server, not in JWT claims.
- Verify before trust — never branch on `decode()` claims; always `verify()` first.
- One leaked HS256 secret = forge any user — prefer asymmetric keys across services.
- Cannot push-revoke easily — until expiry, stolen tokens work unless you track `jti` or rotate keys.
