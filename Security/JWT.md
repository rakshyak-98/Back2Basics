[[Security]] [[JWT authentication]] [[Token rotation]] [[single-sign-on (SSO)]]

# JWT

> JWT (JSON Web Token) — a signed blob of claims the client carries; the server verifies the signature instead of looking up a session.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Three Base64 segments — header.payload.signature. Anyone can read the payload; only holders of the secret/key can forge a valid signature.

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

**Access vs refresh:** short-lived access JWT in memory/`Authorization`; longer refresh in HttpOnly cookie → `POST /refresh` mints a new pair. Stateless until you add a denylist or rotate keys.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `invalid signature` | Wrong secret/key; HS vs RS mismatch | Match `alg` and key material; check env per env |
| `jwt expired` | Clock skew; too-short TTL | NTP sync; widen skew tolerance slightly; refresh flow |
| `jwt malformed` | Truncated header; wrong encoding | Don't URL-encode mid-token; trim whitespace |
| Works locally, fails in prod | Different JWT secret; wrong `iss`/`aud` | Align env; log verify error code only |
| Logout still authorized | Stateless JWT until `exp` | Short TTL + refresh revoke / denylist `jti` |
| `alg: none` accepted | Library default too loose | Explicit `algorithms` allowlist |
| Role claim ignored / wrong | Custom claim name collision | Namespace claims; verify before use |

---

## Gotchas

> [!WARNING]
> **Payload is not secret** — Base64 ≠ encryption. Put secrets in the server, not in JWT claims.

> [!WARNING]
> **Verify before trust** — never branch on `decode()` claims; always `verify()` first.

> [!WARNING]
> **One leaked HS256 secret = forge any user** — prefer asymmetric keys across services.

> [!WARNING]
> **Cannot push-revoke easily** — until expiry, stolen tokens work unless you track `jti` or rotate keys.

---

## When NOT to use

- **Need instant server-side logout / session kill** — opaque session IDs in Redis/DB.
- **Huge authorization graphs in every request** — keep JWT thin; fetch permissions server-side.
- **Broadcast / manage connected clients** — JWT is not a messaging channel; use WebSockets + sessions.

---

## Related

[[JWT authentication]] [[Token rotation]] [[HMAC (Hash based Message Authentication Codes)]] [[Asymmetrical Encryption]] [[single-sign-on (SSO)]] [[Authentication terms]]
