[[Security]] [[certbot (letsencrypt)]] [[TLS (Transport Layer Security)]] [[PKI]] [[certbot error]] [[https]]

# ACME server

> The CA’s API that ACME clients (Certbot, Caddy, Traefik) call to prove domain control and get certificates.

## Interview Relevance

Interviewers ask how automated certificate issuance works end-to-end — ACME challenges, account keys, and how clients like Certbot talk to the CA API.

## Sources

- [RFC 8555 — Automatic Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555) — deep-dive
- [Let's Encrypt — How It Works](https://letsencrypt.org/how-it-works/) — overview

## Core Definition

An ACME server is the Certificate Authority API that ACME clients call to prove domain control and receive X.509 certificates.

## Key Concepts

```txt
ACME client                    ACME server (CA)
     │  newAccount / newOrder        │
     │◄──── challenges ──────────────┤
     │  fulfill HTTP-01 / DNS-01     │
     │  finalize + download cert     │
```

| Role | Who |
|------|-----|
| **ACME client** | Certbot, lego, Caddy, cert-manager |
| **ACME server** | Let’s Encrypt, ZeroSSL, Google Trust, step-ca |

## Technical Details

```bash
# Certbot: production (default) vs staging
sudo certbot certonly --nginx -d example.com
sudo certbot certonly --staging --nginx -d example.com

# Point at another ACME directory
sudo certbot certonly --server https://acme.zerossl.com/v2/DV90 ...
# Private CA example
sudo certbot certonly --server https://ca.internal/acme/directory ...
```

### ACME endpoints

| ACME server | Operator | Free? | Browser trusted? | Certbot |
|-------------|----------|-------|------------------|---------|
| Let’s Encrypt prod | ISRG | Yes | Yes | Default |
| Let’s Encrypt staging | ISRG | Yes | No | `--staging` |
| ZeroSSL | ZeroSSL | Limited | Yes | `--server` |
| Google Trust Services | Google | Yes | Yes | `--server` |
| step-ca / Boulder | You | Self-hosted | Only if you trust the root | `--server` |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| `urn:ietf:params:acme:error:rateLimited` | Prod hammering | Staging for tests; back off |
| Challenge pending forever | Public HTTP/DNS not visible | Fix firewall/DNS; see [[certbot (letsencrypt)]] |
| Client talks to wrong directory | `--server` / staging flag | Match intended CA URL |
| Private CA untrusted externally | Root not in public stores | Distribute root only inside org |
| Account key lost | New account = fine; certs independent | Recreate account; keep backup of account key if required by CA |

## Real-World Applications

Let's Encrypt and private ACME CAs (step-ca, Smallstep) issue short-lived certs to Certbot, Caddy, and Traefik for public and internal TLS.

## Pros/Cons or Trade-offs

- **Pro:** Automates certificate issuance and renewal with a standard API.
- **Con:** Air-gapped hosts — no outbound ACME; issue offline and ship PEMs.
- **Con:** Non-DNS identities — email/code-signing may use other PKI flows.
- **Con:** One static internal cert for years — long-lived private CA certs without ACME may be simpler (with your own rotation process).

## Comparison

- vs [[certbot (letsencrypt)]]: ACME is the CA protocol/API; Certbot is one client.
- vs manual [[PKI]]: ACME automates issuance and renewal with domain-control challenges.

## Mistakes to Avoid

- Staging vs prod directories are different — mixing them confuses rate-limit and trust expectations.
- ACME proves domain control, not company legal identity — DV certs only; EV/OV are out of band.
- Self-hosted ACME still needs a trust story — browsers won’t trust your CA unless you install the root.
