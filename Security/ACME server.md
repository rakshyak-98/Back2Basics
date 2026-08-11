[[Security]] [[certbot (letsencrypt)]] [[TLS (Transport Layer Security)]] [[PKI]]

# ACME server

> ACME server — the CA’s API that ACME clients (Certbot, Caddy, Traefik) call to prove domain control and get certificates.

---

## Mental model

**Say it in one breath:** Client creates an account key → requests an order for names → server issues challenges → client completes HTTP-01/DNS-01/TLS-ALPN-01 → server issues the cert (and later renewals/revocation).

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

---

## Standard config / commands

```bash
# Certbot: production (default) vs staging
sudo certbot certonly --nginx -d example.com
sudo certbot certonly --staging --nginx -d example.com

# Point at another ACME directory
sudo certbot certonly --server https://acme.zerossl.com/v2/DV90 ...
# Private CA example
sudo certbot certonly --server https://ca.internal/acme/directory ...
```

## ACME endpoints

| ACME server | Operator | Free? | Browser trusted? | Certbot |
|-------------|----------|-------|------------------|---------|
| Let’s Encrypt prod | ISRG | Yes | Yes | Default |
| Let’s Encrypt staging | ISRG | Yes | No | `--staging` |
| ZeroSSL | ZeroSSL | Limited | Yes | `--server` |
| Google Trust Services | Google | Yes | Yes | `--server` |
| step-ca / Boulder | You | Self-hosted | Only if you trust the root | `--server` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `urn:ietf:params:acme:error:rateLimited` | Prod hammering | Staging for tests; back off |
| Challenge pending forever | Public HTTP/DNS not visible | Fix firewall/DNS; see [[certbot (letsencrypt)]] |
| Client talks to wrong directory | `--server` / staging flag | Match intended CA URL |
| Private CA untrusted externally | Root not in public stores | Distribute root only inside org |
| Account key lost | New account = fine; certs independent | Recreate account; keep backup of account key if required by CA |

---

## Gotchas

> [!WARNING]
> **Staging vs prod directories are different** — mixing them confuses rate-limit and trust expectations.

> [!WARNING]
> **ACME proves domain control, not company legal identity** — DV certs only; EV/OV are out of band.

> [!WARNING]
> **Self-hosted ACME still needs a trust story** — browsers won’t trust your CA unless you install the root.

---

## When NOT to use

- **Air-gapped hosts** — no outbound ACME; issue offline and ship PEMs.
- **Non-DNS identities** — email/code-signing may use other PKI flows.
- **One static internal cert for years** — long-lived private CA certs without ACME may be simpler (with your own rotation process).

---

## Related

[[certbot (letsencrypt)]] [[certbot error]] [[PKI]] [[TLS (Transport Layer Security)]] [[https]]
