[[Security]] [[Asymmetrical Encryption]] [[TLS (Transport Layer Security)]] [[SSH]] [[KMS]] [[HMAC (Hash based Message Authentication Codes)]]

# symmetrical encryption

> Symmetric encryption — same secret key encrypts and decrypts; fast bulk crypto once both sides share the key.

```txt
        symmetrical encryp ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Crypto basics: same key both ways, AES-GCM preferred, key distribution proble…

## Sources
- [NIST SP 800-38D — GCM](https://csrc.nist.gov/publications/detail/sp/800-38d/final) — deep-dive
- [Wikipedia — Symmetric-key algorithm](https://en.wikipedia.org/wiki/Symmetric-key_algorithm) — overview

## Key Concepts
```txt
Key exchange (ECDHE / RSA wrap)
        │
        ▼
Shared session key ──AES-GCM──► encrypted bytes on the wire
```

| Use | Example |
|-----|---------|
| TLS record layer | After handshake, symmetric protects HTTP |
| Disk / DB fields | Data key from [[KMS]] |
| SSH session | Symmetric after kex |


- **Core:** Symmetric encryption uses the same secret key to encrypt and decrypt

## Technical Details
```bash
# Illustrative OpenSSL enc (prefer libsodium/age for new tools)
openssl enc -aes-256-gcm -in plain.bin -out cipher.bin -K <hexkey> -iv <hexiv>
```

```js
// Node: AES-256-GCM
const key = crypto.randomBytes(32)
const iv = crypto.randomBytes(12)
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv)
const enc = Buffer.concat([cipher.update(plain), cipher.final()])
const tag = cipher.getAuthTag()
```

| Knob | Why it matters |
|------|----------------|
| **AEAD** (GCM/Poly1305) | Encrypt + integrity; avoid raw CBC+HMAC DIY |
| Random IV/nonce | Never reuse nonce with same key (GCM) |
| Key length | AES-256 common; manage keys in KMS/HSM |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Decrypt auth tag fail | Wrong key/IV; truncated ciphertext | Verify key id; send IV+tag+ciphertext |
| Intermittent garbage | Nonce reuse | Unique IV per message; counter/XChaCha |
| “Works in Java, fails in Go” | Padding / encoding | Prefer AEAD; agree on byte layout |
| Key leaked in logs | Debug printed key | Rotate; redact; use KMS |
| Slow bulk encrypt | Soft AES / tiny buffer loops | Hardware AES-NI; larger chunks |

## Mistakes to Avoid
- **Mistake:** ECB mode — identical blocks leak patterns; never for real data
- **Mistake:** Homegrown CBC without MAC — padding oracles; use AEAD
- **Mistake:** Symmetric alone doesn’t authenticate the peer

## Pros/Cons or Trade-offs
- **Pro:** High throughput for bulk data once keys are established.
- **Con:** First contact with no shared secret — need asymmetric ([[Asymmetrical Encryption]]) or pre-provisioned keys.
- **Con:** Password storage — use password hashes (Argon2/yescrypt), not reversible AES.
- **Con:** Long-term identity — certificates/signatures, not a static AES key.

## Comparison
- vs [[Asymmetrical Encryption]]: shared secret vs key pair — TLS uses both (handshake then bulk).
- vs [[HMAC (Hash based Message Authentication Codes)]]: encryption hides plaintext


### Use cases
- TLS record protection and disk/volume encryption use AES-GCM (or similar) wit…
