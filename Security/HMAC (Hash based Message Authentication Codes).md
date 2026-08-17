[[JWT authentication]] [[Token rotation]] [[openssl]] [[symmetrical encryption]] [[Securing a hash key authentication]] [[RSA]]

# HMAC

> Hash-based Message Authentication Code — proves integrity and shared-secret authenticity of a message without encryption.

```txt
        HMAC ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Crypto/API interviews: HMAC proves integrity and authenticity with a shared s…

## Sources
- [RFC 2104 — HMAC](https://www.rfc-editor.org/rfc/rfc2104) — deep-dive
- [NIST FIPS 198-1 — HMAC](https://csrc.nist.gov/publications/detail/fips/198/1/final) — deep-dive

## Key Concepts
**HMAC** = hash function (SHA-256) keyed with a secret:

```txt
HMAC-SHA256(key, message) → fixed-length tag
Verifier recomputes with same key → constant-time compare
```

Properties:
- **Integrity:** — bit flip detected
- **Authentication:** — without key, tag not forgeable (given proper key size)
- **Not confidentiality:** — message sent in clear unless also encrypted

- **Note:** Used in: JWT `HS256`, webhook signatures (Stripe, GitHub), API request signin…

- **Note:** Contrast **[[Asymmetrical Encryption]]** signatures


- **Core:** HMAC combines a cryptographic hash with a secret key to produce a tag that ve…

## Technical Details
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

- **Why `timingSafeEqual`:** naive `===` leaks tag bytes via timing side channe…

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Signature mismatch | Encoding (hex vs base64); body raw bytes | Sign exact bytes received; no JSON re-serialize |
| Intermittent fail | Clock skew on timestamped HMAC | Tolerance window; NTP |
| Key rotation pain | Single global secret | Dual-key verify window — see [[Token rotation]] |
| Weak forgery resistance | SHA1 HMAC | Upgrade to SHA-256 minimum |

## Mistakes to Avoid
- **Mistake:** Never use plain `SHA256(secret + msg)`
- **Mistake:** Short secrets
- **Mistake:** JWT `none` alg

## Pros/Cons or Trade-offs
- **Pro:** Fast integrity+authenticity with a shared secret — ideal for webhooks.
- **Con:** Prefer **asymmetric signatures** (Ed25519, RSA-PSS) when many verifiers, untrusted clients, or public webhook endpoints — avoids sharing one MAC key with every consumer.

## Comparison
- vs [[Asymmetrical Encryption]] signatures: HMAC needs shared secret
- vs plain hash: hash alone does not prove who held a secret.


### Use cases
- Webhook providers and internal APIs sign payloads with HMAC-SHA256 so receive…
