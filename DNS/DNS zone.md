[[DNS]] [[name server]] [[BIND]]

# DNS zone

> One-line: a contiguous DNS namespace slice served authoritatively by one or more NS — **RFC 1035**.

## Mental model

A **zone** is everything below a **zone apex** (e.g. `example.com`) that one administrative entity controls. The parent zone (`.com`) holds **NS glue** pointing to your nameservers.

```
.com (parent zone)
  └── example.com (child zone apex)
        ├── www.example.com   A
        ├── api.example.com   CNAME
        └── _dmarc.example.com TXT
```

**Delegation:** parent publishes NS records; child zone file holds the actual records. **Subdomain delegation** (`sub.example.com` → different NS) creates a separate zone cut.

| Concept | Meaning |
|---------|---------|
| Zone apex | `@` in zone file = `example.com` itself |
| Authoritative | Server answers from zone data, not cache/recursion |
| Primary (master) | Source of truth; edits happen here |
| Secondary (slave) | AXFR/IXFR from primary |
| SOA | Serial, refresh, retry, expire, minimum TTL |

## Standard config / commands

### Inspect zone (operator view)

```shell
# All records from authoritative NS
dig @ns1.example.com example.com AXFR          # zone transfer (often ACL'd)
dig @ns1.example.com example.com SOA +short
dig @ns1.example.com example.com NS +short

# Compare serial across replicas (should match)
for ns in ns1 ns2; do
  echo -n "$ns: "
  dig @$ns.example.com example.com SOA +short | awk '{print $1}'
done

# Validate delegation from parent
dig example.com NS +trace | tail -20
dig ns1.example.com A +short                   # glue must resolve
```

### Minimal BIND zone snippet (`/etc/bind/db.example.com`)

```bind
$TTL 300
@   IN SOA ns1.example.com. hostmaster.example.com. (
        2025072201  ; serial (YYYYMMDDnn — bump on every change)
        3600        ; refresh
        600         ; retry
        604800      ; expire
        300 )       ; negative cache TTL
    IN NS  ns1.example.com.
    IN NS  ns2.example.com.
    IN A   203.0.113.10

www IN A   203.0.113.10
api IN CNAME www.example.com.
```

After edit:

```shell
sudo named-checkzone example.com /etc/bind/db.example.com
sudo rndc reload example.com
```

### Cloud managed zones (pattern)

```shell
# Route53
aws route53 list-resource-record-sets --hosted-zone-id Z1234567890

# Cloudflare
curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Some resolvers get old IP | SOA serial on all NS; TTL remaining | Bump serial; ensure secondaries synced (`rndc notify` / provider auto-sync) |
| Zone transfer fails | `dig AXFR @primary`; firewall TCP/53 | ACL on primary; allow secondary IP; check TSIG key |
| Subdomain NXDOMAIN | Delegation NS in parent vs child zone | Add NS + glue at parent OR record in parent zone — not both incorrectly |
| Apex MX/TXT broken after adding CNAME | CNAME coexists with nothing else at apex | Remove apex CNAME; use ALIAS or separate name |
| DNSSEC validation fails | `dig +dnssec`; DS at parent matches DNSKEY | Re-sign zone; publish correct DS to registrar |
| Serial not incrementing | Secondary serving stale data | Always increment SOA serial on change (automate in CI) |
| Wildcard surprises | `*.example.com` catches unintended names | Narrow wildcard; explicit records override wildcard |

## Gotchas

> [!WARNING]
> **Forgot to bump SOA serial** → secondaries never pick up changes. Automate serial in dynamic DNS or use provider-managed zones.

- **CNAME at `@`** is invalid in plain DNS — registrars offering "CNAME flattening" hide this; know your provider's behavior.
- **NS at apex must match parent delegation** — mismatch = lame delegation intermittent failures.
- **TTL 86400 during migration** = up to 24h pain; lower TTL **before** cutover, not after.
- **Split-horizon zones** (internal vs external) drift easily — treat as two zones with sync discipline.

## When NOT to use

- Single static host entry on one machine → `/etc/hosts` or local [[dnsmasq]] stub.
- Global anycast without understanding secondary sync → managed DNS (Route53, Cloudflare) reduces ops load.

## Related

[[DNS]] · [[name server]] · [[BIND]] · [[CoreDNS]] · [[DNS rebinding]]
