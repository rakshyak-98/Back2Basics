[[DNS]] [[Name server]] [[BIND]]

> A zone is an administrative boundary containing DNS records that an authoritative DNS system manages.

```txt
api.example.com
stage.example.com
prod.example.com
test.example.com
```
These are subdomains/names. They are not separate DNS zones just because you created them.


```txt
example.com zone
│
├── example.com       A      194.195.119.168
├── www.example.com   A      194.195.119.168
├── api.example.com   A      10.0.0.20
├── mail.example.com  A      10.0.0.30
├── exampel.com       MX     mail.theoterra.com
├── example.com       TXT    ...
└── exampel.com       NS     ns1...
```
These records collectively form the **DNS data of the zone.**

Zone != domain
A **domain** is part of the DNS namespace
A **zone** is the portion of that namespace that is actually administered by a particular DNS authority.

## What makes something a separate zone?
the key concept is **Delegation**

In your single zone one **DNS authority can manage all of the names (subdomain).**

**Noe delegation**
You don't want your existing DNS provider to manage
```txt
api.dev.example.com
git.dev.example.com
jenkins.dev.example.com
```

So you tell DNS:
> "For `dev.example.com` and everything else below it, ask these other nameservers." This is **delegation**.
> - Now there are two zones.
> - `dev.example.com` became a separate zone because authority was delegated to different nameservers.

"`dev.example.com` is managed by these nameservers."

> DNS delegation is when the authoritative servers for a parent zone tell DNS that a child portion of the namespace is authoritative somewhere else.

> A subdomain does not become a child zone merely because the name exists. It becomes a separate child zone when authority for that name is delegated to different authoritative nameservers.

**After delegation**
```txt
example.com.       NS    ns1.example-dns.com.
example.com.       NS    ns2.example-dns.com.

dev.example.com.   NS    ns1.dev-dns.com.
dev.example.com.   NS    ns2.dev-dns.com.
```

**Purpose of delegation and why authoritative DNS uses multiple server.**
```txt
ns1.parent-dns.com  ❌ DOWN
ns2.parent-dns.com  ✅ UP

ns1.child-dns.com   ✅ UP
ns2.child-dns.com   ✅ UP
```
if the resolver has never seen `dev.example.com` before. This is where the parent matters. The resolver needs the **parent delegation** to discover the child nameservers. If **all the authoritative nameserver for the parent zone are unavailable**, a resolver that doesn't already have the delegation cached may not be able to discover the child zone.

"So the child server being health isn't sufficient by itself." This is why you normally have multiple nameservers.

> [!NOTE]
> The child nameserver doesn't depend on the parent nameserver to answer queries. Once the resolver knows `dev.example.com -> ns1.child-dns.com` it can query the child directly.

If **one parent NS dies,** nothing special happens, the resolver uses another authoritative NS for the parent.

If **all parent NS die,** cached delegation may allow existing resolvers to continue reaching the child, but **new resolvers that don't have the delegation cached can have trouble discovering the child.**

"That's one of the fundamental reasons DNS is designed with **redundant authoritative nameservers at every important delegation level.**"

## Zone file
A **zone file is the data file that describes the DNS records for a particular DNS zone.** Traditionally written as a text file. A zone file contains DNS records, it can contain many record types.
The authoritative DNS server **loads/serves the zone data.** When a resolver asks `api.example.com -> ?` then the authoritative server looks at its authoritative zone data and answers `api.example.com -> 194.195.119.168`

**Zone** the administrative/authoritative portion of the DNS namespace.
**Zone file** a traditional text representation of the data belonging to that zone.

> Modern DNS providers don't necessarily use an actual text zone file internally. They may store the records in databases or distributed systems.

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

[[DNS]] · [[Name server]] · [[BIND]] · [[CoreDNS]] · [[DNS rebinding]]
