[[DNS]] [[DNS zone]] [[TLS (Transport Layer Security)]] [[Route53]] [[CORS (Cross Origin Request Sharing)]]

# Cloudflare

> **Authoritative DNS + reverse proxy (orange cloud) + WAF/CDN/DDoS** — changes where traffic terminates and who sees origin IP. **Cloudflare docs** + migration incidents when proxy hid real client IP or broke TLS.

## Mental model

Cloudflare sits between users and origin: as **DNS provider** (nameservers → Cloudflare) and optionally **HTTP proxy** (proxied records). Proxied traffic: client → Cloudflare edge → your origin. **OID** identifies objects in Cloudflare API (zones, records, rulesets).

```
User ──► CF edge (TLS, cache, WAF) ──► origin (ALB, nginx, Vercel)
              │
              └── DNS only (grey cloud) = CF DNS, direct to origin IP
```

**Orange cloud (proxied)** hides origin IP, enables CDN/WAF; **grey cloud (DNS only)** is just DNS — origin must handle TLS and DDoS alone.

## Standard config / commands

### Zone setup

1. Add site in Cloudflare dashboard → import/copy DNS records.
2. Change registrar **NS** to Cloudflare-assigned nameservers.
3. Choose proxied vs DNS-only per record (A/AAAA/CNAME).

### SSL/TLS modes (critical)

| Mode | Origin cert | When |
|------|-------------|------|
| **Full (strict)** | Valid cert on origin (Let's Encrypt, ACM) | **Prod default** |
| Full | Self-signed OK on origin | Lab only |
| Flexible | Origin can be HTTP | **Avoid** — CF→origin unencrypted |

### Origin real IP (when proxied)

```nginx
# nginx — trust CF connecting IPs + header
set_real_ip_from 173.245.48.0/20;  # + all CF ranges from https://www.cloudflare.com/ips/
real_ip_header CF-Connecting-IP;
```

App logs: use `CF-Connecting-IP`, not `$remote_addr` (which is CF edge).

### Wrangler CLI (Workers, Pages, R2)

```bash
npm i -g wrangler
wrangler login
wrangler whoami
wrangler pages deploy ./dist
wrangler r2 object put my-bucket/key --file=./local
```

**OID** in API responses = stable id for `zone_id`, `dns_record_id`, etc. — use in Terraform/API, not hostname.

### Page Rules / Cache (basics)

- Cache static assets aggressively (`Cache-Control: public, max-age=31536000`).
- Bypass cache on `/api/*` (Cache Level: Bypass).
- **Always Use HTTPS** + HSTS after validating origin.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Too many redirects | SSL mode vs origin HTTP/HTTPS | Full (strict) + HTTPS origin; or fix origin redirect loop |
| 522 / 523 connection to origin | Origin down; SG/firewall blocks CF IPs | Open firewall to [CF IP ranges](https://www.cloudflare.com/ips/); health check origin |
| 525 SSL handshake failed | Origin cert expired/wrong name | Renew cert; match hostname |
| Wrong client IP in logs | Not reading CF header | `CF-Connecting-IP` / `True-Client-IP` (Enterprise) |
| API CORS breaks after CF | Transform rules; cached OPTIONS | Bypass cache; preserve headers ([[CORS (Cross Origin Request Sharing)]]) |
| DNS propagates but site wrong | Orange vs grey cloud; old A record | Toggle proxy; purge DNS cache |
| Webhook HMAC fail | Body buffered/transformed | Disable buffering on webhook path |

```bash
dig +short NS example.com
curl -I https://example.com --resolve example.com:443:ORIGIN_IP  # bypass CF test
```

## Gotchas

> [!WARNING]
> **Flexible SSL** — users see HTTPS, CF→origin may be plain HTTP. Compliance fail and session hijack on that leg.

> [!WARNING]
> **Proxied records expose only CF IPs** — lock origin to CF IP allowlist; otherwise attackers bypass WAF via direct IP.

> [!WARNING]
> **Caching POST/GraphQL** — default doesn't cache POST, but misconfigured Cache Rules can break mutations.

> [!WARNING]
> **Let's Encrypt HTTP-01 behind proxy** — use DNS-01 or CF origin cert; HTTP-01 needs temporary grey cloud or token path.

## When NOT to use

- **Internal-only services** — no public DNS/proxy needed; use private DNS ([[Route53]] private zone, [[mDNS]]).
- **WebSockets/long polling without config** — works on CF but verify timeout/cache rules.
- **Replacing WAF on complex custom protocols** — CF is HTTP-centric; raw TCP needs Spectrum (paid).

## Related

[[DNS]] · [[DNS zone]] · [[Route53]] · [[TLS (Transport Layer Security)]] · [[CORS (Cross Origin Request Sharing)]] · [[top-level Domain]]
