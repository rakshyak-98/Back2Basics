[[read pem file]] [[Base64]] [[PKI]] [[openssl]]

# DER

> Distinguished Encoding Rules — canonical binary ASN.1 encoding for X.509 certs, keys, and CSRs; PEM is Base64-wrapped DER with headers.

---

## Mental model

```txt
Logical cert (ASN.1 structure)
        │
        ▼ DER encode (binary, canonical)
   cert.der
        │
        ▼ Base64 + -----BEGIN CERTIFICATE----- 
   cert.pem  (human portable)
```

**DER** properties:
- **Binary** — not safe to paste in chat/logs without encoding
- **Canonical** — one valid encoding per value (good for signatures)
- **What TLS sends** on the wire (inside records)

Formats engineers confuse:
| Format | Encoding |
|--------|----------|
| **DER** | Binary ASN.1 |
| **PEM** | Base64 DER + labels |
| **PKCS#12 (.p12)** | Encrypted bundle of key+cert |

---

## Standard config / commands

### PEM ↔ DER conversion

```bash
# PEM → DER
openssl x509 -in cert.pem -outform der -out cert.der

# DER → PEM
openssl x509 -inform der -in cert.der -out cert.pem

# Private key
openssl pkey -in key.pem -outform der -out key.der
openssl rsa -inform der -in key.der -out key.pem
```

### Inspect DER without converting

```bash
openssl x509 -inform der -in cert.der -noout -text
openssl asn1parse -inform der -i -in cert.der | head
```

### Fingerprint (hashes DER or SPKI — tool-dependent)

```bash
openssl x509 -in cert.der -inform der -noout -fingerprint -sha256
```

**Why DER in Java/Android:** `CertificateFactory.generateCertificate(InputStream)` expects DER by default.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to load certificate` | File is PEM with `.der` name | Convert or fix `-inform pem` |
| `bad decrypt` on PKCS#8 | Encrypted PEM vs raw DER | Provide passphrase; export unencrypted for HSM import (careful) |
| Signature verify fail | Re-encoded PEM altered whitespace | Sign/compare DER bytes |
| Java keystore import fail | Wrong format | `keytool -importcert -file cert.der` |

---

## Gotchas

> [!WARNING]
> **PEM is not "more secure"** — same key material; PEM is encoding only.

> [!WARNING]
> **Double Base64** — some APIs want PEM string, others raw DER — read API docs.

> [!WARNING]
> **Copy/paste corruption** — PEM needs exact line wraps; use files not Slack.

---

## When NOT to use

Humans editing certs → **PEM**. Wire protocols and some embedded parsers → **DER**. Don't hand-edit DER bytes.

---

## Related

[[read pem file]] [[Base64]] [[Root certificate]] [[fingerprint]] [[RSA]] [[openssl]]
