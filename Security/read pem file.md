[[DER]] [[openssl]] [[RSA]] [[Root certificate]] [[fingerprint]] [[https]]

# Read PEM file

> Inspect PEM-encoded certs, keys, and CSRs with OpenSSL — confirm subject, expiry, SANs, and key type before install or debug TLS.

## Interview Relevance

Ops debugging: prove subject, SANs, expiry, and key match before installing a cert — OpenSSL one-liners.

## Sources

- [OpenSSL — x509 command](https://www.openssl.org/docs/manmaster/man1/openssl-x509.html) — deep-dive
- [RFC 7468 — Textual Encodings of PKIX](https://www.rfc-editor.org/rfc/rfc7468) — overview

## Core Definition

Reading a PEM file means decoding the Base64 ASN.1 blob to inspect certificate or key fields before deploy or TLS troubleshooting.

## Key Concepts

**PEM** files are Base64 DER with label lines:

```txt
-----BEGIN CERTIFICATE-----
MIIF...
-----END CERTIFICATE-----
```

Common labels:
| BEGIN line | Contents |
|------------|----------|
| `CERTIFICATE` | X.509 public cert |
| `PRIVATE KEY` / `RSA PRIVATE KEY` | Private key (PKCS#1 or PKCS#8) |
| `ENCRYPTED PRIVATE KEY` | Password-protected key |
| `CERTIFICATE REQUEST` | CSR for CA signing |
| `PUBLIC KEY` | SPKI public key |

Always verify **which file is which** before pasting into servers — installing private key where cert goes breaks TLS silently or exposes key.

## Technical Details

### Certificate

```bash
openssl x509 -in cert.pem -text -noout
openssl x509 -in cert.pem -noout -dates -subject -issuer -ext subjectAltName
```

### Private key (check matches cert)

```bash
openssl rsa -in key.pem -check -noout
openssl pkey -in key.pem -text -noout

# Modulus match (RSA)
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa  -noout -modulus -in key.pem  | openssl md5
# Hashes must match
```

### CSR

```bash
openssl req -in csr.pem -text -noout
```

### Encrypted key decrypt (for import)

```bash
openssl pkey -in encrypted.key -out decrypted.key
# chmod 600 decrypted.key — delete when done
```

### Fix common typo from old notes

```bash
# Correct command (not x500):
openssl x509 -in file.pem -text -noout
openssl rsa  -in file.pem -text -noout
openssl req  -in file.pem -text -noout
```

**Why modulus check:** cert renewal with wrong key → nginx starts but handshake fails.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to load key` | PEM label vs content | Re-export; PKCS#8 convert |
| Cert/key mismatch | Modulus/hash compare | Reissue cert or correct key file |
| Missing SAN | `-ext subjectAltName` | Reissue with DNS names |
| Expired | `-dates` | Renew — [[certbot (letsencrypt)]] |
| Wrong file order in fullchain | leaf vs intermediate | `fullchain`: leaf first, then intermediates |

## Real-World Applications

Before Nginx reload, confirm SANs, dates, and that the private key modulus matches the certificate.

## Pros/Cons or Trade-offs

- **Pro:** Catch SAN/expiry/key-mismatch before a production TLS outage.
- **Con:** Don't `-text -noout` multi-GB PEM bundles in CI repeatedly — parse programmatically. For binary, use [[DER]] `-inform der`.

## Comparison

- vs [[openssl]] general use: this note is the inspect-before-install checklist.
- vs [[DER]]: convert when tools require binary.

## Mistakes to Avoid

- Never commit private PEM to git — scan with gitleaks; rotate if leaked.
- `BEGIN RSA PRIVATE KEY` vs PKCS#8 — some tools picky; convert with `openssl pkcs8`.
- Windows line endings — CRLF can break parsers; `dos2unix file.pem`.
- Certificate is public — but reveals infrastructure names — don't paste prod certs in public tickets casually.
