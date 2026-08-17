[[TLS (Transport Layer Security)]] [[TCP]] [[SSH]] [[DNS]]

# LDAP (Lightweight Directory Access Protocol)

> LDAP queries and updates a hierarchical directory (users, groups, devices) over the network — usually the source of truth for “who is this user?”

```txt
        LDAP (Lightweight  ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want DN/bind/filter fluency, LDAPS versus StartTLS, and why gree…

## Sources
- [RFC 4511 — LDAP](https://datatracker.ietf.org/doc/html/rfc4511) — deep-dive
- [OpenLDAP Administrator's Guide](https://www.openldap.org/doc/admin26/) — overview
- [Wikipedia — LDAP](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) — overview

## Technical Details
```txt
App / IdP / login shell
        │  bind + search (ldap://:389 or ldaps://:636)
        ▼
Directory (OpenLDAP, Active Directory, 389-ds)
   dc=example,dc=com
     └─ ou=people
          └─ uid=alice  (attributes: mail, memberOf, …)
```

1. Client connects (389 + StartTLS, or 636 LDAPS).
2. Bind as service account or end user.
3. Search with base, scope, filter; read attributes.
4. Apps map groups → roles; IdPs sync or proxy LDAP.

```bash
ldapsearch -H ldap://ldap.example.com -x -D 'cn=admin,dc=example,dc=com' -W \
  -b 'dc=example,dc=com' '(uid=alice)' mail memberOf

# StartTLS
ldapsearch -H ldap://ldap.example.com -ZZ -x ...

# LDAPS
ldapsearch -H ldaps://ldap.example.com -x ...
```

```txt
# /etc/nslcd.conf or sssd sketch — OS login via LDAP
uri ldap://ldap.example.com
base dc=example,dc=com
tls_reqcert demand
```

| Knob | Why it matters |
|------|----------------|
| Bind DN privileges | Over-privileged binds = directory takeover |
| Size/time limits | Huge subtree searches melt the DSA |
| Referral chasing | Multi-master / AD trees need correct chase policy |

| Symptom | Check | Fix |
|---------|-------|-----|
| `Can't contact LDAP server` | DNS, 389/636, TLS | Fix SRV/A; open ports; trust CA |
| Invalid credentials | Wrong DN / password / expired | Confirm DN form; unlock AD account |
| Search returns nothing | Bad base DN / filter / ACLs | Widen filter; check ACI/ACL deny |
| TLS handshake fails | Hostname vs cert SAN | Fix cert; `TLS_REQCERT` not `never` in production |
| Slow logins | Unindexed filter | Add indexes for uid/mail/member |
| Intermittent AD auth | DC failover / site awareness | Point to VIP or correct site DCs |

## Mistakes to Avoid
- **Mistake:** Cleartext simple bind
- **Mistake:** Treating DN string equality casually
- **Mistake:** Using LDAP as a general application database
- **Mistake:** `TLS_REQCERT never` in production

## Pros/Cons or Trade-offs
- **Pro:** Hierarchical identity and group data with mature tooling (AD, OpenLDAP).
- **Con:** Wrong model for session stores, catalogs, or high-churn documents — use Redis/SQL.
- **Con:** Direct app-to-LDAP couples every service to directory quirks; prefer OIDC/SAML in front.

## Comparison
- vs OIDC/SAML IdP: hide LDAP behind the IdP for consumer SaaS and modern apps.
- vs SQL user tables: directory wins for org hierarchy and centralized OS login


### Use cases
- Active Directory / OpenLDAP for enterprise login, SSH key distribution via at…

- **Example:** A Linux fleet uses SSSD against LDAP so `uid=alice` resolves to …
