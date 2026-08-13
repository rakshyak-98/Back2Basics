[[DNS server]] · [[DNS zone]] · [[BIND]] · [[dns record]]

# PoserDNS

> PowerDNS Authoritative serves DNS zones from SQL, LDAP, or BIND-style zone files with a modular architecture — the vault filename `PoserDNS` is a historical typo for PowerDNS.

---

## PowerDNS components

| Server | Role |
|--------|------|
| **Authoritative** | Answers from backend database |
| **Recursor** | Separate recursive resolver (like [[Unbound]]) |
| **dnsdist** | Load balancer / DDoS shield in front |

This note focuses on **Authoritative** hosting.

## Backends

- **BIND zone file** (`bind` backend) — migrate existing zones
- **Generic SQL** (MySQL, PostgreSQL, SQLite) — API-driven record management
- **LDAP** — enterprise directory integration

## Example `pdns.conf` snippet

```ini
launch=gsql3
gsql3-host=127.0.0.1
gsql3-dbname=pdns
gsql3-user=pdns
local-address=0.0.0.0
local-port=53
```

Records managed via SQL or **PowerDNS Admin** UI.

## API and automation

```bash
curl -X PATCH --data '{"rrsets": [...]}' \
  -H "X-API-Key: $PDNS_API_KEY" \
  http://127.0.0.1:8081/api/v1/servers/localhost/zones/example.com
```

Suits large dynamic zones where flat files are painful.

## DNSSEC

Native signing with `pdnsutil secure-zone example.com` and DS upload to registrar.

## vs [[BIND]]

| PowerDNS | BIND |
|----------|------|
| Database-native zones | Text zone files standard |
| dnsdist scaling | Long heritage on root/TLD |
| Flexible backends | RPZ, catalog zones mature |

Many operators run PowerDNS authoritative + **Unbound** or **Recursor** for clients.

## Recall

- When is a SQL backend preferable to BIND zone files?
- What does dnsdist add in front of authoritative servers?

## Sources

- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/)
- [PowerDNS — dnsdist](https://doc.powerdns.com/dnsdist/)
