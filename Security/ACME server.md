[[Security]] [[certbot (letsencrypt)]] [[TLS (Transport Layer Security)]] [[PKI]] [[certbot error]] [[https]]

# ACME server

> The CA’s API that ACME clients (Certbot, Caddy, Traefik) call to prove domain control and get certificates.

```txt
        ACME server ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how automated certificate issuance works end-to-end

## Sources
- [RFC 8555 — Automatic Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555) — deep-dive
- [Let's Encrypt — How It Works](https://letsencrypt.org/how-it-works/) — overview

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


- **Core:** An ACME server is the Certificate Authority API that ACME clients call to pro…

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

## Mistakes to Avoid
- **Mistake:** Staging vs prod directories are different
- **Mistake:** ACME proves domain control, not company legal identity
- **Mistake:** Self-hosted ACME still needs a trust story

## Pros/Cons or Trade-offs
- **Pro:** Automates certificate issuance and renewal with a standard API.
- **Con:** Air-gapped hosts — no outbound ACME; issue offline and ship PEMs.
- **Con:** Non-DNS identities — email/code-signing may use other PKI flows.
- **Con:** One static internal cert for years — long-lived private CA certs without ACME may be simpler (with your own rotation process).

## Comparison
- vs [[certbot (letsencrypt)]]: ACME is the CA protocol/API; Certbot is one client.
- vs manual [[PKI]]: ACME automates issuance and renewal with domain-control challenges.


### Use cases
- Let's Encrypt and private ACME CAs (step-ca, Smallstep) issue short-lived cer…
