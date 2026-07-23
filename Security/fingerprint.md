[[TLS (Transport Layer Security)]] [[PKI]] [[openssl]] [[ssh allow local system with key]]

# Fingerprint

> Short hash of a public key or certificate — human-verifiable identity for trust-on-first-use (TOFU) and MITM detection.

---

## Mental model

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| SSH "REMOTE HOST IDENTIFICATION CHANGED" | Server rebuild; MITM | Verify new fingerprint OOB; update known_hosts |
| TLS pin failure in app | Cert renewed; new CA | Rotate pins with overlap; use SPKI hash |
| Different fingerprint same host | Multiple keys (RSA+Ed25519) | Compare correct key type |
| CI deploy fails SSH | Known_hosts stale | Automate fingerprint inject from vault |

---

## Gotchas

> [!WARNING]
> **Fingerprint ≠ trust anchor** — still need provenance (CA, OOB verify).

> [!WARNING]
> **Cert pinning breaks on renewal** — pin SPKI or plan rotation.

> [!WARNING]
> **MD5 fingerprints** — collision resistance weak; display SHA256 in new systems.

---

## When NOT to use

Don't fingerprint **session keys** — ephemeral per connection. Fingerprint **long-lived public keys/certs** only.

---

## Related

[[TLS (Transport Layer Security)]] [[Root certificate]] [[PKI]] [[read pem file]] [[DER]]
