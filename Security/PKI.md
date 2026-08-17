[[Security]] [[TLS (Transport Layer Security)]] [[Root certificate]] [[certbot (letsencrypt)]] [[read pem file]] [[ACME server]] [[Asymmetrical Encryption]]

# PKI

> PKI (Public Key Infrastructure) — the factory and phone book for certificates: who issues them, who trusts them, how you revoke them.





## Interview Relevance
Trust model interviews: roots, intermediates, leaf certs, revocation, and how browsers decide a site is trusted.

## Sources
- [RFC 5280 — Internet X.509 PKI](https://www.rfc-editor.org/rfc/rfc5280) — deep-dive
- [Wikipedia — Public key infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure) — overview

## Core Definition
PKI is the system of CAs, certificates, and trust stores that bind public keys to identities and enable verification and revocation.

## Key Concepts
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

## Technical Details
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

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `unable to get local issuer` | Missing intermediate | Serve `fullchain.pem`, not leaf alone |
| Name mismatch | SAN vs hostname | Reissue with correct `-d` / SAN list |
| Untrusted / self-signed in prod | Not in public trust store | Use public CA or distribute private root |
| Revoked still accepted | OCSP/CRL not checked | Enable OCSP stapling; fix AIA URL |
| Internal mTLS fail | Wrong CA / expired client cert | Rotate; align trust anchors on both sides |
| Corporate MITM “cert errors” | Proxy TLS inspection | Install corp root or exclude break-glass hosts |

## Real-World Applications
Public web trust (browser roots) and private corporate CAs for mTLS both are PKI deployments with different trust stores.

## Pros/Cons or Trade-offs
- **Pro:** Scalable trust for millions of sites via public CA hierarchies.
- **Con:** One-off local HTTPS demo — self-signed or `mkcert` is enough; full PKI is overhead.
- **Con:** Encrypting application payloads at rest — use [[KMS]] / envelope encryption, not X.509 PKI.
- **Con:** API keys between trusted backends on private net — mTLS is stronger, but HMAC/API keys may be simpler if threat model allows.

## Comparison
- vs raw [[Asymmetrical Encryption]]: PKI adds names, issuance, and revocation around keys.
- vs [[ACME server]]: ACME is one automated issuance method inside a PKI.

## Mistakes to Avoid
- Root ≠ what you deploy — servers send leaf + intermediates; clients already have roots.
- CN-only certs — many clients ignore CN if SAN is present/absent; always set SANs.
- Private CA in public internet — browsers will reject; use only inside your fleet with your root distributed.
