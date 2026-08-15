[[read pem file]] [[Base64]] [[PKI]] [[openssl]] [[Root certificate]] [[fingerprint]] [[RSA]]

# DER

> Distinguished Encoding Rules — canonical binary ASN.1 encoding for X.509 certs, keys, and CSRs; PEM is Base64-wrapped DER with headers.

## Interview Relevance

PKI tooling interviews: PEM vs DER, when wire formats need binary ASN.1, and how to convert with OpenSSL.

## Sources

- [ITU-T X.690 — DER](https://www.itu.int/rec/T-REC-X.690/) — deep-dive
- [Wikipedia — X.690](https://en.wikipedia.org/wiki/X.690) — overview

## Core Definition

DER (Distinguished Encoding Rules) is the canonical binary ASN.1 encoding used for X.509 certificates, keys, and CSRs; PEM is Base64-wrapped DER.

## Key Concepts

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

## Technical Details

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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to load certificate` | File is PEM with `.der` name | Convert or fix `-inform pem` |
| `bad decrypt` on PKCS#8 | Encrypted PEM vs raw DER | Provide passphrase; export unencrypted for HSM import (careful) |
| Signature verify fail | Re-encoded PEM altered whitespace | Sign/compare DER bytes |
| Java keystore import fail | Wrong format | `keytool -importcert -file cert.der` |

## Real-World Applications

Java keystores, Windows cert stores, and some ACME payloads expect DER; convert with OpenSSL when tooling rejects PEM.

## Pros/Cons or Trade-offs

- **Pro:** Canonical binary encoding for certs/keys in wire and keystore formats.
- **Con:** Humans editing certs → **PEM**. Wire protocols and some embedded parsers → **DER**. Don't hand-edit DER bytes.

## Comparison

- vs PEM ([[read pem file]]): DER is binary; PEM is Base64 text with `BEGIN`/`END` markers.
- vs [[Base64]]: Base64 is the encoding layer inside PEM, not the ASN.1 rules themselves.

## Mistakes to Avoid

- PEM is not "more secure" — same key material; PEM is encoding only.
- Double Base64 — some APIs want PEM string, others raw DER — read API docs.
- Copy/paste corruption — PEM needs exact line wraps; use files not Slack.
