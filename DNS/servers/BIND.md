[[DNS server]] [[DNS zone]] [[name server]] [[Unbound]] [[dnsmasq]] [[CoreDNS]]

# BIND

> BIND (Berkeley Internet Name Domain) is the reference implementation for authoritative DNS on the Internet — it serves zones, supports DNSSEC, and can recurse (though many deployments split authoritative and recursive r…

```txt
        BIND ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers expect zone-file literacy, SOA serial discipline, `named-checkzo…

## Sources
- [BIND 9 Administrator Reference Manual](https://bind9.readthedocs.io/) — deep-dive
- [ISC — BIND](https://www.isc.org/bind/) — overview

## Key Concepts
- **Authoritative master/slave:** zone files + AXFR/IXFR distribution.
- **Optional recursion:** powerful and dangerous if `allow-recursion` is wide open.
- **DNSSEC tooling:** keygen/signzone plus DS at the registrar.
- **Views / RPZ / RRL:** split-horizon answers, malware blocking, reflection mitigation.

## Technical Details
| Mode | Use |
|------|-----|
| **Authoritative** | Host [[DNS zone]] files; answer for domains you own |
| **Recursive** | Resolver for clients (lock down `allow-recursion`) |
| **Secondary** | AXFR/IXFR slave from primary |

- ISC BIND 9 is current; BIND 8 is obsolete.

```bind
; /etc/bind/db.example.com
$TTL 300
@  IN  SOA  ns1.example.com. admin.example.com. (
        2026081301 ; serial
        7200       ; refresh
        3600       ; retry
        1209600    ; expire
        300 )      ; minimum
     IN  NS   ns1.example.com.
     IN  A    203.0.113.10
www  IN  A    203.0.113.10
```

```bind
zone "example.com" {
    type master;
    file "/etc/bind/db.example.com";
};
```

```bash
named-checkzone example.com /etc/bind/db.example.com
named-checkconf
rndc reload
dnssec-keygen -a ECDSAP256SHA256 example.com
dnssec-signzone -o example.com db.example.com
```

- Publish DS record at registrar after signing.

- **Security:** RPZ for bad domains

## Mistakes to Avoid
- **Mistake:** Forgetting SOA serial increments — secondaries stall on old data
- **Mistake:** Combining public authoritative service with world-open recursion
- **Mistake:** Skipping `named-checkzone` / `named-checkconf` before reload

## Pros/Cons or Trade-offs
- **Pro:** Battle-tested authoritative feature set (DNSSEC, views, catalog zones, RPZ).
- **Con:** Operational complexity vs managed DNS or DB-backed [[PoserDNS]].
- **Con:** Misconfigured recursion turns you into an open amplifier.

## Comparison
- vs [[Unbound]]: BIND for authoritative Internet zones; Unbound for validating recursion.
- vs [[CoreDNS]]: CoreDNS fits Kubernetes service discovery plugins, not classic public zone master…


### Use cases
- ISP and enterprise authoritative hosting

- **Example:** Edit zone file → bump SOA serial → `named-checkzone` → `rndc rel…
