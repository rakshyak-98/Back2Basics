[[TLS (Transport Layer Security)]] [[ACME server]] [[Configuration]]

# Certbot error

> One-line: map Let's Encrypt / Certbot failures to root cause and fix — **operational runbook**, not a log dump.

## Mental model

Certbot talks to an [[ACME server]] (Let's Encrypt by default) through **challenges** to prove domain control. Failures cluster into: **policy**, **DNS**, **HTTP reachability**, **rate limits**, **local misconfig**, and **renewal drift**.

```
certbot → ACME order → challenge (http-01 | dns-01 | tls-alpn-01)
              ↓ pass
         certificate issued → /etc/letsencrypt/live/<name>/
              ↓ fail
         order invalid → read sub-problems in log
```

Always read the **sub-problem** detail — Certbot aggregates multiple SAN failures into one line.

## Standard config / commands

```shell
# Verbose run (first triage step)
sudo certbot certonly --dry-run -v

# Renew test
sudo certbot renew --dry-run -v

# Single domain HTTP-01 (nginx standalone or webroot)
sudo certbot certonly --webroot -w /var/www/html -d example.com -d www.example.com

# DNS-01 (wildcard — needs plugin)
sudo certbot certonly --dns-cloudflare -d example.com -d '*.example.com'

# Inspect cert expiry / SANs
sudo certbot certificates
openssl x509 -in /etc/letsencrypt/live/example.com/fullchain.pem -noout -dates -subject -ext subjectAltName

# Logs
sudo tail -100 /var/log/letsencrypt/letsencrypt.log
journalctl -u certbot.timer
```

## Triage (error → cause → fix)

| Error / symptom | Cause | Fix |
|-----------------|-------|-----|
| `Cannot issue for "x.example.com": forbidden by policy` | Name on LE blocklist (e.g. certain TLDs, `example.com`, typosquats) or reserved | Use a real public domain; remove invalid SANs from `-d` list |
| `DNS problem: NXDOMAIN looking up A/AAAA for ...` | No public DNS record for challenge host | Add A/AAAA (http-01) or fix `_acme-challenge` TXT (dns-01) |
| `Connection refused` / `Timeout during connect` on http-01 | Port 80 closed, wrong server, or LB not routing `/.well-known/acme-challenge/` | Open :80 to internet; nginx location for webroot; cloud SG / firewall |
| `404` on acme-challenge | Wrong webroot `-w`; app catches all routes | `location ^~ /.well-known/acme-challenge/ { root /var/www/html; }` |
| `Invalid response ... 403` | WAF, auth middleware, geo block | Allowlist ACME path; disable basic auth on `/.well-known/` |
| `Too many certificates already issued for exact set of domains` | LE rate limit (5 dupes / 7 days per SAN set) | Wait; use existing cert; avoid delete+reissue loops in CI |
| `too many failed authorizations recently` | Repeated failed orders (5 / hour per account+hostname) | Fix root cause first; use `--dry-run`; wait 1 hour |
| `Error creating new order :: ... sub-problems` | One bad SAN in multi-domain cert | Split certs or fix the failing name (see sub-problem) |
| `Could not bind to port 80` (standalone) | nginx/apache already on :80 | Stop listener temporarily or switch to `--webroot` / `--nginx` plugin |
| `Renewal failure` but manual issue works | Deploy hook broke; nginx still points at old path | `certbot renew --deploy-hook "nginx -s reload"`; verify symlink chain in `live/` |
| `Certificate has expired` | Timer disabled; renew failed silently for weeks | `systemctl enable --now certbot.timer`; fix renew error; `certbot renew --force-renewal` once |
| `DNS problem: SERVFAIL looking up TXT for _acme-challenge` | Authoritative DNS broken or slow | Fix NS; lower TTL before change; verify TXT at all authoritative NS |
| `The server could not connect to validation target` (from LE side) | IPv6 AAAA points wrong; split DNS | Align A and AAAA; test `curl -6 http://[v6]/.well-known/...` |
| `urn:ietf:params:acme:error:malformed` | Bad CSR (empty SAN, bad key) | Regenerate with explicit `-d`; check openssl key match |

### Example: policy rejection (multi-SAN)

```text
Error creating new order :: Cannot issue for "testhotel1.example.com":
The ACME server refuses to issue for this domain name, because it is forbidden by policy
(and 1 more problems. Refer to sub-problems for more information.)
```

**Cause:** At least one `-d` name violates CA policy (fake TLD, internal-only name submitted to public CA, or blocklisted pattern).

**Fix:**
1. `grep -i subproblem /var/log/letsencrypt/letsencrypt.log` — identify each failing SAN.
2. Remove non-public names from the cert request; use internal CA for `.local` / `.internal`.
3. Re-run with only valid FQDNs: `certbot certonly --webroot ... -d valid.example.com`.

## Gotchas

> [!WARNING]
> **`certbot certonly` doesn't install into nginx** — you must point `ssl_certificate` at `/etc/letsencrypt/live/...` and reload.

> [!WARNING]
> **Staging vs production:** Hit `https://acme-staging-v02.api.letsencrypt.org/directory` for tests — avoids rate limits while iterating.

- **Wildcard requires DNS-01** — HTTP-01 cannot prove `*.example.com`.
- **Cloudflare orange-cloud proxy** is fine for http-01 if origin serves challenge; DNS-01 easier for wildcards.
- **Multiple servers** sharing one name need shared webroot or DNS-01 — standalone mode only works on one host.
- **Short cert lifetime (90d)** — monitor expiry externally (uptime check), not only `certbot.timer` locally.

## When NOT to use

- Internal mTLS mesh between services → private CA (step-ca, Vault) not Let's Encrypt.
- Devices without public DNS → don't force public ACME; use DNS-01 with API or internal PKI.

## Related

[[TLS (Transport Layer Security)]] · [[ACME server]] · [[Configuration]] · [[DNS]]
