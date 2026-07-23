[[DNS]] [[servers]]

# BIND (named) — Operations

> One-line: authoritative/recursive DNS via `named` — edit `named.conf`, validate zones, reload without restart, know recursion vs authority.

## Mental model

BIND 9 runs as **`named`**. Two roles (don't mix blindly on public internet):

```
Authoritative:  "I own example.com" → answers from zone files / DNSSEC
Recursive:      "Look up google.com for client" → queries root → TLD → …
```

Public resolvers open to the world amplify attacks if misconfigured. Authoritative servers answer only zones they host.

Key files (Debian/RHEL layouts vary):

```
/etc/named.conf              # main config
/etc/named.conf.local          # your zones (include)
/var/named/ or /etc/bind/      # zone files
rndc.key                     # admin control key
```

---

## Standard config / commands

### Minimal named.conf skeleton

```named
options {
    directory "/var/cache/bind";
    listen-on port 53 { any; };
    allow-query { any; };           # tighten for authoritative-only public
    recursion no;                   # authoritative server: OFF
    dnssec-validation auto;
};

include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";
```

### Authoritative zone

```named
// named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/db.example.com";
};
```

```dns
; db.example.com
$TTL 300
@   IN SOA  ns1.example.com. admin.example.com. (
        2025072201 ; serial (YYYYMMDDnn)
        3600       ; refresh
        600        ; retry
        86400      ; expire
        300 )      ; negative cache
    IN NS   ns1.example.com.
    IN A    203.0.113.10
www IN A    203.0.113.10
```

**Serial bump rule:** increment on every zone change or secondaries won't transfer.

### Validate and reload

```bash
sudo named-checkconf
sudo named-checkzone example.com /etc/bind/db.example.com
sudo rndc reload                    # reload zones without full restart
sudo rndc reload example.com        # single zone
sudo systemctl reload named
sudo systemctl status named
```

### rndc admin

```bash
sudo rndc status
sudo rndc flush                     # clear cache (resolver)
sudo rndc reconfig                  # reload named.conf only
```

### dig verification

```bash
dig @127.0.0.1 example.com A +short
dig @127.0.0.1 example.com SOA
dig @ns1.example.com example.com AXFR   # zone transfer test (restrict in prod)
```

### Slave/secondary zone

```named
zone "example.com" {
    type slave;
    masters { 203.0.113.1; };
    file "/var/cache/bind/slave/example.com";
};
```

Restrict transfers:

```named
zone "example.com" {
    allow-transfer { 203.0.113.2; };   # secondary IP only
};
```

### TSIG for secure transfer

```bash
rndc-confgen -a   # generates key for rndc
# named.conf: allow-transfer { key "transfer-key"; };
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NXDOMAIN for valid record | Serial not bumped; wrong zone file path | `named-checkzone`; bump SOA serial; `rndc reload` |
| Secondary stale | NOTIFY blocked; serial | Open TCP 53 between prim/sec; increment serial |
| `REFUSED` on query | `allow-query` ACL | Add client network or `any` (careful) |
| SERVFAIL | Config syntax; DNSSEC break | `journalctl -u named`; `named-checkconf` |
| Open resolver abuse | Recursion on for world | `recursion no;` + `allow-recursion { localhost; };` |
| Zone transfer leak | AXFR open | `allow-transfer` restricted; TSIG |
| named won't start | Port 53 in use | `ss -ulnp \| grep :53`; disable systemd-resolved stub if conflict |

```bash
sudo journalctl -u named -n 50 --no-pager
sudo named-checkconf -z
```

### systemd-resolved conflict (common on Ubuntu)

```bash
# If port 53 held by stub resolver
sudo ss -ulnp | grep :53
# Options: disable stub, or configure BIND on different interface
```

---

## Gotchas

> [!WARNING]
> **Forgot serial increment** — #1 secondary drift issue. Automate with `dnssec-signzone` tools or CI check.

> [!WARNING]
> **CNAME at apex** — invalid (RFC); use ALIAS/ANAME at provider or A record at apex.

> [!WARNING]
> **TTL too high during migration** — lower TTL days before IP change.

> [!WARNING]
> **DNSSEC** — broken DS record at registrar = full domain outage. Have rollback plan.

> [!WARNING]
> **Views** — split-horizon (internal vs external) doubles operational complexity; document which view clients hit.

---

## When NOT to use

- **Simple public DNS for a startup** — managed DNS (Route53, Cloudflare) reduces BIND ops burden.
- **Recursive resolver for office** — consider Unbound or dedicated resolver distro; BIND can do it but harden carefully.

---

## Related

[[DNS]] [[TLS (Transport Layer Security)]]
