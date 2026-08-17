[[Asymmetrical Encryption]] [[PKI]] [[TLS (Transport Layer Security)]] [[openssl]] [[DER]] [[read pem file]] [[Root certificate]] [[JWT authentication]]

# RSA

> Public-key algorithm from factoring hardness — historically TLS and signatures; prefer modern curves for new signing when you can.

```txt
        RSA ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Crypto: RSA keygen/sign/encrypt roles, padding (OAEP/PSS), and why new system…

## Sources
- [RFC 8017 — PKCS #1 RSA Cryptography](https://www.rfc-editor.org/rfc/rfc8017) — deep-dive
- [Wikipedia — RSA (cryptosystem)](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) — overview

## Key Concepts
- **Note:** **RSA** uses math on large composites (factorization hardness):

```txt
Keygen → (n, e) public, (d) private
- **Note:** Encrypt: ciphertext = plaintext^e mod n (small messages only)
- **Note:** Sign: signature = hash^d mod n (with PKCS#1 v1.5 or PSS padding)
```

Roles in production:
- **TLS cert keys:** (RSA 2048/4096) — declining versus ECDSA
- **Legacy JWT RS256:** 
- **Key encapsulation:** — wrap AES key (RSA-OAEP)

Limits:
- **Slow:** versus ECDSA/Ed25519 at sign/verify
- **Size:** — 2048-bit keys, ciphertext max ~190 bytes for OAEP-SHA256
- **Padding critical:** — raw RSA malleable


- **Core:** RSA is a public-key algorithm based on the hardness of factoring large compos…

## Technical Details
### Generate key pair

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
openssl rsa -in private.pem -pubout -out public.pem
```

### CSR for public CA

```bash
openssl req -new -key private.pem -out csr.pem -subj "/CN=api.example.com"
openssl req -in csr.pem -noout -text
```

### Sign / verify (PSS preferred)

```bash
openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:-1 \
  -sign private.pem -out sig.bin data.bin
openssl dgst -sha256 -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:-1 \
  -verify public.pem -signature sig.bin data.bin
```

### JWT RS256 (concept)

```javascript
// Use library — never hand-roll RSA
import { SignJWT, jwtVerify, importPKCS8, importSPKI } from 'jose';
```

- **Why OAEP/PSS:** PKCS#1 v1.5 padding classes of attacks in old implementatio…

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| TLS RSA handshake slow | CPU bound | Enable ECDHE + ECDSA cert; session resumption |
| `data too large for key size` | Plain RSA encrypt | Hybrid encrypt AES key only |
| Verification fail cross-lang | Padding mode mismatch | Standardize PSS/OAEP params |
| Weak key detected | <2048 bits | Regenerate; HSM stored keys |

## Mistakes to Avoid
- **Mistake:** Don't use RSA without padding — textbook RSA broken
- **Mistake:** Private key in PEM on disk — chmod 600; prefer [[KMS]]
- **Mistake:** Quantum threat

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous interop for legacy TLS and JWT RS256 ecosystems.
- **Con:** Greenfield **signing** → **Ed25519**. Greenfield **TLS** → **ECDSA P-256** or Ed25519 certs. RSA for legacy interop only.

## Comparison
- vs ECDSA/Ed25519: smaller keys/signatures and often preferred for new signing.
- vs [[symmetrical encryption]]: RSA is not for bulk payload encryption — hybrid crypto uses both.


### Use cases
- Legacy TLS and JWT RS256 still use RSA
