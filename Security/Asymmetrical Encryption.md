[[RSA]] [[symmetrical encryption]] [[TLS (Transport Layer Security)]] [[PKI]]

# Asymmetrical encryption

> Public-key cryptography — encrypt or verify with public key; decrypt or sign with private key; solves key distribution at cost of CPU and size limits.

---

## Mental model

**Asymmetric** = key pair per party:

```txt
Alice public key  → anyone encrypts to Alice
Alice private key → only Alice decrypts

Sign: private key creates signature → public key verifies (not decrypt message)
```

Common uses:
| Operation | Keys used |
|-----------|-----------|
| Confidentiality to one recipient | Encrypt with **recipient public** |
| Digital signature | Sign with **sender private**; verify with **sender public** |
| Key exchange (TLS) | ECDHE ephemeral + cert public key |

Algorithms: **RSA**, **ECDSA**, **Ed25519** (sign), **ECIES** (encrypt). Hybrid systems encrypt a random **symmetric** key asymmetrically, then bulk data with AES — see [[TLS (Transport Layer Security)]].

---

## Standard config / commands

### Generate Ed25519 signing key (modern default)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C 'deploy@example'
```

### RSA key (legacy interop)

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
openssl rsa -in private.pem -pubout -out public.pem
```

### Sign / verify (OpenSSL)

```bash
openssl dgst -sha256 -sign private.pem -out sig.bin message.txt
openssl dgst -sha256 -verify public.pem -signature sig.bin message.txt
```

### Encrypt small secret (RSA-OAEP)

```bash
openssl pkeyutl -encrypt -pubin -inkey public.pem -in secret.bin -out secret.enc
openssl pkeyutl -decrypt -inkey private.pem -in secret.enc -out secret.bin
```

**Why hybrid:** RSA can't encrypt large payloads; AES-GCM carries bulk data.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `decryption failed` | Wrong key; OAEP vs PKCS#1 v1.5 | Match padding; use OAEP for new systems |
| Signature verify fail | Message altered; wrong hash alg | Canonical JSON; specify SHA-256 |
| TLS handshake fail | Cert/key mismatch; expired | Renew cert; full chain |
| Performance bottleneck | RSA sign every request | Move to ECDSA/Ed25519; session tickets |

---

## Gotchas

> [!WARNING]
> **Encrypting with private key is NOT signing** — use proper sign API (`RSA_sign`, Ed25519).

> [!WARNING]
> **Private key in repo** — use KMS/HSM — see [[KMS]].

> [!WARNING]
> **RSA 1024 deprecated** — minimum 2048, prefer 4096 or Ed25519.

---

## When NOT to use

Don't encrypt large blobs directly with RSA. Don't use asymmetric crypto where **[[symmetrical encryption]]** + pre-shared key (already distributed via KMS) suffices.

---

## Related

[[RSA]] [[symmetrical encryption]] [[TLS (Transport Layer Security)]] [[PKI]] [[Root certificate]] [[code signing]]
