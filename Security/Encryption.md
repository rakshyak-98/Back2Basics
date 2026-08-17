[[Security]] [[TLS (Transport Layer Security)]] [[RSA]] [[PKI]] [[KMS]] [[HMAC (Hash based Message Authentication Codes)]] [[SSH authentication]]

# Encryption

> Cryptography protects data in transit and at rest using either a shared secret (symmetric) or a public/private key pair (asymmetric); production systems almost always combine both.

---

## Why It Matters

Every security review eventually asks how keys are generated, exchanged, rotated, and stored. Symmetric algorithms (AES-GCM, ChaCha20-Poly1305) encrypt bulk data fast once both sides share a key. Asymmetric algorithms (RSA, ECDSA, Ed25519) solve the harder problem of distributing keys and proving identity — but they are slower and cannot encrypt large payloads directly. TLS, SSH, JWT signing, and disk encryption all use a hybrid pattern: asymmetric handshake, then symmetric bulk protection.

---

## Sources

- [NIST SP 800-57 Part 1 — Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final) — NIST guidance on key lifetimes, algorithm selection, and storage requirements for federal and industry systems.
- [NIST SP 800-38D — GCM](https://csrc.nist.gov/publications/detail/sp/800-38d/final) — Official specification for AES-GCM authenticated encryption, including nonce rules and security proofs.
- [Wikipedia — Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) — Accessible overview of asymmetric encryption, digital signatures, and key exchange.
- [Wikipedia — Symmetric-key algorithm](https://en.wikipedia.org/wiki/Symmetric-key_algorithm) — Overview of block ciphers, stream ciphers, and why symmetric crypto dominates bulk throughput.

---

## Key Concepts

### Symmetric encryption (shared secret)

Both sender and receiver use the **same secret key** to encrypt and decrypt. Algorithms are fast — AES-GCM can encrypt gigabytes per second on modern CPUs with AES-NI.

```txt
Alice                          Bob
  │── AES-GCM(key, plaintext) ──►│
  │◄── AES-GCM(key, ciphertext) ──│
         same key both directions
```

| Property | Detail |
|----------|--------|
| Speed | Excellent for bulk data (TLS records, disk volumes, database field encryption) |
| Key distribution | Hard — how does Bob get the key without an attacker listening? |
| Integrity | Use **AEAD** modes (GCM, Poly1305) — never raw CBC without a MAC |
| Nonce/IV | Must be unique per message with the same key; nonce reuse in GCM is catastrophic |

Common algorithms: **AES-256-GCM**, **ChaCha20-Poly1305** (common on mobile and when AES-NI is absent).

### Asymmetric encryption (public-key cryptography)

Each party has a **key pair**: public key (publishable) and private key (secret). What one key encrypts, only the other decrypts.

```txt
Encrypt to Alice:  anyone uses Alice's PUBLIC key  → only Alice's PRIVATE key decrypts
Sign as Alice:       Alice uses her PRIVATE key     → anyone verifies with PUBLIC key
```

| Operation | Keys used | Purpose |
|-----------|-----------|---------|
| Confidentiality to one recipient | Encrypt with recipient **public** | Only recipient can read |
| Digital signature | Sign with sender **private**; verify with sender **public** | Proves origin and integrity |
| Key exchange (TLS, SSH) | Ephemeral ECDHE + certificate public key | Derive shared session secret |

Common algorithms: **RSA** (legacy interop), **ECDSA** / **Ed25519** (signatures), **ECIES** (encrypt). RSA cannot encrypt payloads larger than the key size minus padding overhead — typically a few hundred bytes.

### Hybrid pattern (how TLS actually works)

```txt
Client ──► TLS handshake (asymmetric: certs, ECDHE key exchange)
         ──► Derive session keys (symmetric)
         ──► HTTP records encrypted with AES-GCM (symmetric bulk)
```

This is why you need both models: asymmetric for **identity and key agreement**, symmetric for **throughput**.

---

## Technical Details

### Symmetric: AES-256-GCM in Node.js

```javascript
import crypto from 'node:crypto';

const key = crypto.randomBytes(32);   // 256-bit AES key
const iv  = crypto.randomBytes(12);    // 96-bit nonce for GCM — unique per message

const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
const encrypted = Buffer.concat([cipher.update('secret payload', 'utf8'), cipher.final()]);
const authTag = cipher.getAuthTag();   // 128-bit integrity tag — send with ciphertext

// Decrypt
const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
decipher.setAuthTag(authTag);
const plain = Buffer.concat([decipher.update(encrypted), decipher.final()]);
```

Wire format convention: `iv (12) || authTag (16) || ciphertext` — document this in your API.

### Symmetric: OpenSSL CLI (illustrative)

```bash
# Prefer age, libsodium, or KMS APIs for new tools — shown for debugging only
openssl enc -aes-256-gcm -in plain.bin -out cipher.bin -K <64-hex-chars> -iv <24-hex-chars>
```

### Asymmetric: generate Ed25519 signing key (modern default)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C 'deploy@example.com'
```

### Asymmetric: RSA key pair (legacy interop)

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
openssl rsa -in private.pem -pubout -out public.pem
chmod 600 private.pem
```

### Asymmetric: sign and verify

```bash
openssl dgst -sha256 -sign private.pem -out sig.bin message.txt
openssl dgst -sha256 -verify public.pem -signature sig.bin message.txt && echo OK
```

### Asymmetric: encrypt small secret (RSA-OAEP)

```bash
openssl pkeyutl -encrypt -pubin -inkey public.pem -in secret.bin -out secret.enc -pkeyopt rsa_padding_mode:oaep
openssl pkeyutl -decrypt -inkey private.pem -in secret.enc -out secret.bin -pkeyopt rsa_padding_mode:oaep
```

For payloads larger than ~190 bytes (RSA-2048 OAEP), encrypt a random AES key with RSA, then encrypt data with AES-GCM.

### Failure signals

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| GCM auth tag verification failed | Wrong key, wrong IV, truncated ciphertext | Verify key id; send IV+tag+ciphertext together |
| `decryption failed` (RSA) | Wrong key; OAEP vs PKCS#1 v1.5 mismatch | Standardize on OAEP for new systems |
| Signature verify fail | Message altered; wrong hash algorithm | Canonical serialization; specify SHA-256 |
| TLS handshake fail | Cert/key mismatch; expired chain | Renew cert; install full chain |
| Intermittent garbage after decrypt | GCM nonce reuse | Unique IV per message; use counter or XChaCha20 |
| Performance bottleneck | RSA sign on every request | Move to ECDSA/Ed25519; use session tickets |

---

## Mistakes to Avoid

- **ECB mode** — identical plaintext blocks produce identical ciphertext; never use for real data.
- **CBC without MAC** — padding oracle attacks; use AEAD (GCM) instead of DIY encrypt-then-MAC.
- **Encrypting with private key is not signing** — use proper signature algorithms (RSA-PSS, ECDSA, Ed25519).
- **Private keys in repos** — use [[KMS]], HSM, or sealed secrets; rotate on exposure.
- **RSA 1024** — deprecated; minimum 2048 bits, prefer 4096 or Ed25519 for new keys.
- **Symmetric alone does not authenticate the peer** — you still need certificates, HMAC, or a pre-shared identity mechanism.
- **Password storage** — use Argon2/bcrypt/scrypt hashes, not reversible AES encryption.

---

## Pros/Cons or Trade-offs

| Model | Pros | Cons |
|-------|------|------|
| Symmetric | Fast bulk throughput; simple API once keys exist | Key distribution problem; compromise of one key exposes all traffic |
| Asymmetric | Solves key distribution; enables signatures and PKI | Slow; size limits on direct encryption; more complex key management |
| Hybrid (TLS-style) | Best of both — identity + speed | Operational complexity: cert renewal, cipher suites, HSTS |

---

## Comparison

| Need | Use |
|------|-----|
| TLS record protection after handshake | Symmetric (AES-GCM) |
| SSH host authentication | Asymmetric (Ed25519 host key) |
| JWT RS256 / ES256 signature | Asymmetric (sign with private key) |
| Disk/volume encryption | Symmetric data key wrapped by [[KMS]] |
| Message integrity with shared secret | [[HMAC (Hash based Message Authentication Codes)]] — not encryption |
| First contact with no shared secret | Asymmetric handshake or pre-provisioned keys |

---

## Use cases

- **TLS HTTPS**: ECDHE key exchange (asymmetric) → AES-GCM records (symmetric).
- **SSH login**: host key verification (asymmetric) → session cipher (symmetric).
- **S3 SSE-KMS**: envelope encryption — KMS wraps a data key (asymmetric/hybrid), S3 encrypts objects (symmetric).
- **JWT**: RS256 signs claims with private key; API gateway verifies with public key (asymmetric only — no bulk encryption).
- **Database field encryption**: application generates AES data key per row or per tenant; master key in [[KMS]] (symmetric with KMS-managed wrapping).
