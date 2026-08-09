[[Security]] [[Asymmetrical Encryption]] [[TLS (Transport Layer Security)]] [[SSH]]

# symmetrical encryption

> Symmetric encryption — same secret key encrypts and decrypts; fast bulk crypto once both sides share the key.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** AES-GCM (or ChaCha20-Poly1305) with a shared key turns plaintext into ciphertext + auth tag. Key distribution is the hard part — often done via asymmetric key exchange, then symmetric for the session.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Decrypt auth tag fail | Wrong key/IV; truncated ciphertext | Verify key id; send IV+tag+ciphertext |
| Intermittent garbage | Nonce reuse | Unique IV per message; counter/XChaCha |
| “Works in Java, fails in Go” | Padding / encoding | Prefer AEAD; agree on byte layout |
| Key leaked in logs | Debug printed key | Rotate; redact; use KMS |
| Slow bulk encrypt | Soft AES / tiny buffer loops | Hardware AES-NI; larger chunks |

---

## Gotchas

> [!WARNING]
> **ECB mode** — identical blocks leak patterns; never for real data.

> [!WARNING]
> **Homegrown CBC without MAC** — padding oracles; use AEAD.

> [!WARNING]
> **Symmetric alone doesn’t authenticate the peer** — combine with proper handshake / signatures.

---

## When NOT to use

- **First contact with no shared secret** — need asymmetric ([[Asymmetrical Encryption]]) or pre-provisioned keys.
- **Password storage** — use password hashes (Argon2/yescrypt), not reversible AES.
- **Long-term identity** — certificates/signatures, not a static AES key.

---

## Related

[[Asymmetrical Encryption]] [[TLS (Transport Layer Security)]] [[KMS]] [[HMAC (Hash based Message Authentication Codes)]] [[SSH]]
