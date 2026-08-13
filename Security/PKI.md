[[Security]] [[TLS (Transport Layer Security)]] [[Root certificate]] [[certbot (letsencrypt)]]

# PKI

> PKI (Public Key Infrastructure) — the factory and phone book for certificates: who issues them, who trusts them, how you revoke them.

---

## How it works

```txt
Root CA (offline, trusted store)
   │ signs
Intermediate CA
   │ signs
Leaf cert (example.com) + private key on server
```

| Piece | Job |
|-------|-----|
| **CA** (Certificate Authority) | Issues and revokes certs |
| **RA** (Registration Authority) | Validates identity before issue |
| **Certificate** | Public key + subject + issuer + validity + SANs |
| **CRL / OCSP** | “Is this cert revoked?” |
| **Trust store** | Roots your OS/browser believes |

TLS uses PKI for **server identity**; mTLS extends it to clients.

---


## Configuration and commands

```bash
# Inspect leaf + chain
openssl x509 -in fullchain.pem -noout -subject -issuer -dates -ext subjectAltName
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt -untrusted intermediate.pem leaf.pem

# What browsers need on the server
# fullchain.pem = leaf + intermediates (not the root)
```

| Knob | Why it matters |
|------|----------------|
| **SAN** (Subject Alternative Name) | Modern clients match hostname here, not only CN |
| Chain order | Leaf first, then intermediates |
| Private key protection | HSM/KMS or locked file perms; never in git |
| Short lifetime | Let's Encrypt ~90d — automate renew ([[certbot (letsencrypt)]]) |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to get local issuer` | Missing intermediate | Serve `fullchain.pem`, not leaf alone |
| Name mismatch | SAN vs hostname | Reissue with correct `-d` / SAN list |
| Untrusted / self-signed in prod | Not in public trust store | Use public CA or distribute private root |
| Revoked still accepted | OCSP/CRL not checked | Enable OCSP stapling; fix AIA URL |
| Internal mTLS fail | Wrong CA / expired client cert | Rotate; align trust anchors on both sides |
| Corporate MITM “cert errors” | Proxy TLS inspection | Install corp root or exclude break-glass hosts |

---


## Gotchas

> [!WARNING]
> **Root ≠ what you deploy** — servers send leaf + intermediates; clients already have roots.

> [!WARNING]
> **CN-only certs** — many clients ignore CN if SAN is present/absent; always set SANs.

> [!WARNING]
> **Private CA in public internet** — browsers will reject; use only inside your fleet with your root distributed.

---


## When not to use

- **One-off local HTTPS demo** — self-signed or `mkcert` is enough; full PKI is overhead.
- **Encrypting application payloads at rest** — use [[KMS]] / envelope encryption, not X.509 PKI.
- **API keys between trusted backends on private net** — mTLS is stronger, but HMAC/API keys may be simpler if threat model allows.

---


## Related

[[TLS (Transport Layer Security)]] [[Root certificate]] [[read pem file]] [[ACME server]] [[certbot (letsencrypt)]] [[Asymmetrical Encryption]]

## Sources

- [Wikipedia — PKI](https://en.wikipedia.org/wiki/PKI)
