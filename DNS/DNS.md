[[TCP]] [[UDP]] [[DNS zone]] [[name server]] [[mDNS]] [[dig]]

# DNS

> One-line: distributed naming that maps names → records (A, AAAA, CNAME, …) via a resolver chain — **Kleppmann, DDIA** + RFC 1035.

## Mental model

DNS is a hierarchical, cached lookup system. Your stub resolver doesn't talk to root directly for every query — it follows referrals or uses a recursive resolver (ISP, 8.8.8.8, corporate [[Unbound]]).

**Resolution chain (recursive lookup):**

```
App → stub resolver (/etc/resolv.conf, systemd-resolved)
         → recursive resolver (recursive mode)
              → root (. )           → TLD (.com)
              → TLD nameserver      → authoritative NS for example.com
              → authoritative NS    → A/AAAA/CNAME answer
         ← cached TTL ←──────────────
```

Transport:
- **UDP/53** default (single query/response, 512-byte traditional limit).
- **TCP/53** for truncated responses (TC bit set) or zone transfers (AXFR).
- **DNS-over-HTTPS/TLS** on recursive path (browser/OS dependent).

**Key record types for ops:**

| Type | Use |
|------|-----|
| A / AAAA | Name → IPv4 / IPv6 |
| CNAME | Alias → another name (no other records at same name) |
| NS | Delegates zone to authoritative servers |
| MX | Mail routing |
| TXT | SPF, DKIM, DMARC, verification tokens |
| SRV | Service location |
| PTR | Reverse (IP → name) |

## Standard config / commands

```shell
# What resolver am I using?
cat /etc/resolv.conf
resolvectl status
systemd-resolve --status 2>/dev/null || true

# Simple lookup
dig example.com A +short
dig example.com AAAA +short
dig example.com MX +short

# Specific resolver (bypass local stub)
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Full answer with TTL and flags
dig example.com ANY +noall +answer +authority +additional

# Reverse lookup
dig -x 93.184.216.34 +short

# Trace from root — shows delegation chain (debug propagation)
dig +trace example.com
dig +trace example.com A @8.8.8.8    # trace via specific recursive

# Compare authoritative vs cached
dig example.com @ns1.example.com +norecurse
dig example.com @8.8.8.8

# DNSSEC validation (if enabled locally)
dig example.com +dnssec +multi

# TCP fallback when UDP truncated
dig example.com +bufsize=4096
dig example.com +tcp
```

**`/etc/resolv.conf` minimal:**

```
nameserver 10.0.0.2          # VPC resolver / corporate
search ec2.internal example.com
options edns0 trust-ad
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NXDOMAIN everywhere for one name | `dig +trace` stops where? | Fix NS delegation or missing zone at authoritative |
| Works with `@8.8.8.8`, fails with corporate DNS | Compare `dig @corp-dns` vs public | Internal split-horizon; add private zone or conditional forwarder |
| Intermittent wrong IP | TTL + multiple A records; geo DNS | Lower TTL during migration; verify all authoritative NS agree (`dig @each-ns`) |
| Slow first query, fast after | `dig` twice; check `+stats` query time | Resolver cold cache normal; fix upstream if always slow |
| `SERVFAIL` | `dig +dnssec`; check authoritative logs | Broken DNSSEC chain; DS/DNSKEY mismatch |
| Large response fails | `dig +ignore` vs `+bufsize=512` shows TC bit | Enable EDNS0 or TCP on resolver/firewall |
| Pod resolves, host doesn't (or reverse) | `resolvectl`; CoreDNS vs host resolv | K8s `ndots` / `search` suffix issue — use FQDN with trailing dot |
| After zone cutover, stale answers | TTL on old records (300–86400 common) | Wait TTL or flush resolver cache; don't assume instant global update |

### Reading `dig +trace` output

1. **Root referral** — lists `.com` TLD servers → proves path started.
2. **TLD referral** — lists `example.com` NS → delegation correct.
3. **Authoritative answer** — final A/AAAA from zone → if missing here, fix zone file / registrar glue.
4. **Stops early with lame delegation** — NS exists but target doesn't answer → fix glue A/AAAA at parent.

## Gotchas

> [!WARNING]
> **`search` domain suffix** causes surprise lookups. `curl api` may query `api.ec2.internal` before `api` — always use FQDN (`api.example.com.`) in automation.

- **CNAME at apex** (example.com) is invalid in traditional DNS — use ALIAS/ANAME at provider or flatten.
- **Negative caching** (NXDOMAIN) respects SOA minimum TTL — typo domains stay "broken" for minutes.
- **Split-horizon**: same name, different answer inside vs outside — debug from both vantage points.
- **systemd-resolved stub** on 127.0.0.53 — tools may show different path than `dig @127.0.0.53`.

## When NOT to use

- Service-to-service naming inside a cluster → platform DNS (K8s, Consul) is faster to iterate.
- Storing non-DNS data in TXT beyond reasonable size — use a real config store.

## Related

[[DNS zone]] · [[mDNS]] · [[name server]] · [[DNS rebinding]] · [[Unbound]] · [[CoreDNS]] · [[dig]]
