[[TLS (Transport Layer Security)]] [[PKI]] [[openssl]] [[ssh allow local system with key]] [[Root certificate]] [[read pem file]] [[DER]]

# Fingerprint

> Short hash of a public key or certificate — human-verifiable identity for trust-on-first-use (TOFU) and MITM detection.

```txt
        Fingerprint ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** SSH/TLS reviews: fingerprints enable TOFU and MITM detection

## Sources
- [RFC 7469 — Public Key Pinning (historical context)](https://www.rfc-editor.org/rfc/rfc7469) — overview
- [OpenSSH — key fingerprints](https://man.openbsd.org/ssh-keygen.1) — deep-dive

## Key Concepts
- **Note:** Full public keys are long; **fingerprints** compress identity:

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

- **Note:** Mismatch on reconnect → possible **MITM**, wrong host, or key rotation.


- **Core:** A fingerprint is a short hash of a public key or certificate used for human v…

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

- **Why SHA256 over MD5:** MD5 ssh fingerprints still shown legacy

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| SSH "REMOTE HOST IDENTIFICATION CHANGED" | Server rebuild; MITM | Verify new fingerprint OOB; update known_hosts |
| TLS pin failure in app | Cert renewed; new CA | Rotate pins with overlap; use SPKI hash |
| Different fingerprint same host | Multiple keys (RSA+Ed25519) | Compare correct key type |
| CI deploy fails SSH | Known_hosts stale | Automate fingerprint inject from vault |

## Mistakes to Avoid
- **Mistake:** Fingerprint ≠ trust anchor
- **Mistake:** Cert pinning breaks on renewal — pin SPKI or plan rotation
- **Mistake:** MD5 fingerprints

## Pros/Cons or Trade-offs
- **Pro:** Human-scale check for TOFU and MITM detection.
- **Con:** Don't fingerprint **session keys** — ephemeral per connection. Fingerprint **long-lived public keys/certs** only.

## Comparison
- vs full [[PKI]] chain verify: fingerprints are TOFU/out-of-band checks when you lack a trusted CA…
- vs [[code signing]]: related integrity ideas; fingerprints are usually hashes of keys/certs.


### Use cases
- SSH TOFU and certificate pinning workflows show fingerprints so operators can…
