[[JWT authentication]] [[Token rotation]] [[openssl]] [[symmetrical encryption]]

# HMAC

> Hash-based Message Authentication Code — proves integrity and shared-secret authenticity of a message without encryption.

---

## Mental model

**HMAC** = hash function (SHA-256) keyed with a secret:

```txt
HMAC-SHA256(key, message) → fixed-length tag
Verifier recomputes with same key → constant-time compare
```

Properties:
- **Integrity** — bit flip detected
- **Authentication** — without key, tag not forgeable (given proper key size)
- **Not confidentiality** — message sent in clear unless also encrypted

Used in: JWT `HS256`, webhook signatures (Stripe, GitHub), API request signing, TLS 1.2 PRF building blocks.

Contrast **[[Asymmetrical Encryption]]** signatures — public verify, private sign; no shared secret distribution problem at scale.

---

## Standard config / commands

### OpenSSL CLI

```bash
echo -n 'payload' | openssl dgst -sha256 -hmac 'secret-key'
```

### Node.js

```javascript
import crypto from 'crypto';
const tag = crypto.createHmac('sha256', secret).update(body).digest('hex');
crypto.timingSafeEqual(Buffer.from(tag, 'hex'), Buffer.from(expected, 'hex'));
```

### Python

```python
import hmac, hashlib
hmac.new(key, msg, hashlib.sha256).hexdigest()
```

### Webhook verify pattern

```bash
# Stripe-style: signed payload header
sig = HMAC-SHA256(webhook_secret, timestamp + '.' + raw_body)
```

**Why `timingSafeEqual`:** naive `===` leaks tag bytes via timing side channel.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Signature mismatch | Encoding (hex vs base64); body raw bytes | Sign exact bytes received; no JSON re-serialize |
| Intermittent fail | Clock skew on timestamped HMAC | Tolerance window; NTP |
| Key rotation pain | Single global secret | Dual-key verify window — see [[Token rotation]] |
| Weak forgery resistance | SHA1 HMAC | Upgrade to SHA-256 minimum |

---

## Gotchas

> [!WARNING]
> **Never use plain `SHA256(secret + msg)`** — vulnerable to length-extension; use HMAC or KDF.

> [!WARNING]
> **Short secrets** — brute-force HMAC on offline captures; use ≥256-bit random keys.

> [!WARNING]
> **JWT `none` alg** — separate issue, but HMAC JWTs need strong secret and alg allowlist.

---

## When NOT to use

Prefer **asymmetric signatures** (Ed25519, RSA-PSS) when many verifiers, untrusted clients, or public webhook endpoints — avoids sharing one MAC key with every consumer.

---

## Related

[[JWT authentication]] [[Securing a hash key authentication]] [[Token rotation]] [[RSA]] [[openssl]]
