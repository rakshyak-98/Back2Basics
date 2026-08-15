[[TLS (Transport Layer Security)]] [[PKI]] [[openssl]] [[ssh allow local system with key]] [[Root certificate]] [[read pem file]] [[DER]]

# Fingerprint

> Short hash of a public key or certificate — human-verifiable identity for trust-on-first-use (TOFU) and MITM detection.

## Interview Relevance

SSH/TLS interviews: fingerprints enable TOFU and MITM detection — know hash algorithms and what a mismatch means.

## Sources

- [RFC 7469 — Public Key Pinning (historical context)](https://www.rfc-editor.org/rfc/rfc7469) — overview
- [OpenSSH — key fingerprints](https://man.openbsd.org/ssh-keygen.1) — deep-dive

## Core Definition

A fingerprint is a short hash of a public key or certificate used for human verification and trust-on-first-use.

## Key Concepts

Full public keys are long; **fingerprints** compress identity:

```txt
SHA256:abc123...  ← hash of DER-encoded public key or cert
```

Contexts:
| Context | What you fingerprint |
|---------|---------------------|
| **SSH host key** | Server public key on first connect |
| **TLS cert** | SPKI or whole cert (pinning) |
| **Code signing** | Developer cert fingerprint in allowlist |
| **API client pinning** | Mobile app embeds expected pin |

Mismatch on reconnect → possible **MITM**, wrong host, or key rotation.

## Technical Details

### SSH host key fingerprint

```bash
ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
ssh-keygen -E sha256 -l -f ~/.ssh/known_hosts
ssh -o FingerprintHash=sha256 user@host
```

### TLS certificate fingerprint

```bash
openssl x509 -in cert.pem -noout -fingerprint -sha256
openssl s_client -connect example.com:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -fingerprint -sha256
```

### Compare out-of-band

```bash
# Publish fingerprint on separate channel (DNS TXT, docs, sticker)
# User verifies matches on first ssh/https
```

**Why SHA256 over MD5:** MD5 ssh fingerprints still shown legacy — prefer `-E sha256`.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| SSH "REMOTE HOST IDENTIFICATION CHANGED" | Server rebuild; MITM | Verify new fingerprint OOB; update known_hosts |
| TLS pin failure in app | Cert renewed; new CA | Rotate pins with overlap; use SPKI hash |
| Different fingerprint same host | Multiple keys (RSA+Ed25519) | Compare correct key type |
| CI deploy fails SSH | Known_hosts stale | Automate fingerprint inject from vault |

## Real-World Applications

SSH TOFU and certificate pinning workflows show fingerprints so operators can detect MITM on first connect.

## Pros/Cons or Trade-offs

- **Pro:** Human-scale check for TOFU and MITM detection.
- **Con:** Don't fingerprint **session keys** — ephemeral per connection. Fingerprint **long-lived public keys/certs** only.

## Comparison

- vs full [[PKI]] chain verify: fingerprints are TOFU/out-of-band checks when you lack a trusted CA path.
- vs [[code signing]]: related integrity ideas; fingerprints are usually hashes of keys/certs.

## Mistakes to Avoid

- Fingerprint ≠ trust anchor — still need provenance (CA, OOB verify).
- Cert pinning breaks on renewal — pin SPKI or plan rotation.
- MD5 fingerprints — collision resistance weak; display SHA256 in new systems.
