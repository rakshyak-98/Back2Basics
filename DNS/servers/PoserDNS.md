[[DNS server]] [[DNS zone]] [[BIND]] [[dns record]] [[Unbound]]

# PoserDNS

> PowerDNS Authoritative serves DNS zones from SQL, LDAP, or BIND-style zone files with a modular architecture — the vault filename `PoserDNS` is a historical typo for PowerDNS.

```txt
        PoserDNS ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast DB-backed authoritative DNS with BIND zone files, and w…

## Sources
- [PowerDNS Authoritative Server documentation](https://doc.powerdns.com/authoritative/) — deep-dive
- [PowerDNS — dnsdist](https://doc.powerdns.com/dnsdist/) — overview

## Key Concepts
- **Authoritative vs Recursor:** separate binaries — this note focuses on Authoritative hosting.
- **Backends:** BIND files, generic SQL, LDAP — pick based on change rate and ops model.
- **dnsdist:** load balancer / DDoS shield in front of authoritative servers.
- **API automation:** JSON API for dynamic rrsets without editing flat files.

## Technical Details
| Server | Role |
|--------|------|
| **Authoritative** | Answers from backend database |
| **Recursor** | Separate recursive resolver (like [[Unbound]]) |
| **dnsdist** | Load balancer / DDoS shield in front |

- **Backends:** 

- **BIND zone file:** (`bind` backend) — migrate existing zones
- **Generic SQL:** (MySQL, PostgreSQL, SQLite) — API-driven record management
- **LDAP:** — enterprise directory integration

```ini
launch=gsql3
gsql3-host=127.0.0.1
gsql3-dbname=pdns
gsql3-user=pdns
local-address=0.0.0.0
local-port=53
```

- Records managed via SQL or **PowerDNS Admin** UI.

```bash
curl -X PATCH --data '{"rrsets": [...]}' \
  -H "X-API-Key: $PDNS_API_KEY" \
  http://127.0.0.1:8081/api/v1/servers/localhost/zones/example.com
```

- Suits large dynamic zones where flat files are painful.
- Native signing with `pdnsutil secure-zone example.com` and DS upload to regis…

| PowerDNS | BIND |
|----------|------|
| Database-native zones | Text zone files standard |
| dnsdist scaling | Long heritage on root/TLD |
| Flexible backends | RPZ, catalog zones mature |

- Many operators run PowerDNS authoritative + **Unbound** or **Recursor** for c…

## Mistakes to Avoid
- **Mistake:** Running Recursor wide-open on the same public IP as Authoritativ…
- **Mistake:** Forgetting DS upload after `pdnsutil secure-zone`
- **Mistake:** Treating the vault name `PoserDNS` as a different product

## Pros/Cons or Trade-offs
- **Pro:** SQL/API backends fit automation and large dynamic zones.
- **Con:** Database availability becomes part of DNS availability.
- **Pro:** dnsdist adds front-door scaling that classic single BIND hosts lack.

## Comparison
- vs [[BIND]]: PowerDNS favors DB backends and APIs
- vs [[Unbound]]: Unbound is recursive/validating


### Use cases
- Multi-tenant DNS hosting, API-driven record platforms, and high-churn zones t…

- **Example:** Provisioning system inserts A/AAAA rows into PostgreSQL; PowerDN…
