[[DNS server]] · [[DNS zone]] · [[name server]] · [[Unbound]] · [[dnsmasq]]

# BIND

> BIND (Berkeley Internet Name Domain) is the reference implementation for authoritative DNS on the Internet — it serves zones, supports DNSSEC, and can recurse (though many deployments split authoritative and recursive roles).

---

## Roles

| Mode | Use |
|------|-----|
| **Authoritative** | Host [[DNS zone]] files; answer for domains you own |
| **Recursive** | Resolver for clients (lock down `allow-recursion`) |
| **Secondary** | AXFR/IXFR slave from primary |

ISC BIND 9 is current; BIND 8 is obsolete.

## Minimal authoritative zone

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

## Validate and reload

```bash
named-checkzone example.com /etc/bind/db.example.com
named-checkconf
rndc reload
```

## DNSSEC

```bash
dnssec-keygen -a ECDSAP256SHA256 example.com
dnssec-signzone -o example.com db.example.com
```

Publish DS record at registrar after signing.

## Security

- **RPZ** — block known bad domains
- **Response rate limiting** — mitigate reflection attacks
- **Views** — split internal/external answers ([[DNS zone]] split horizon)

## vs [[Unbound]] / [[CoreDNS]]

BIND excels at **authoritative** Internet zones. Run **Unbound** for validating recursion on clients. **CoreDNS** fits Kubernetes service discovery.

## Recall

- What SOA field must increment on every zone edit?
- Why separate authoritative BIND from public recursive resolvers?

## Sources

- [BIND 9 Administrator Reference Manual](https://bind9.readthedocs.io/)
- [ISC — BIND](https://www.isc.org/bind/)
