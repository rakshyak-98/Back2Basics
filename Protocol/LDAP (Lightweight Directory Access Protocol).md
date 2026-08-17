[[TLS (Transport Layer Security)]] [[TCP]] [[SSH]] [[DNS]]

# LDAP (Lightweight Directory Access Protocol)

> LDAP queries and updates a hierarchical directory (users, groups, devices) over the network — usually the source of truth for “who is this user?”





## Interview Relevance
Interviewers want DN/bind/filter fluency, LDAPS versus StartTLS, and why greenfield SaaS hides LDAP behind OIDC rather than exposing it to apps.

## Sources
- [RFC 4511 — LDAP](https://datatracker.ietf.org/doc/html/rfc4511) — deep-dive
- [OpenLDAP Administrator's Guide](https://www.openldap.org/doc/admin26/) — overview
- [Wikipedia — LDAP](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) — overview

## Recall Cues
- Why do interviewers care about DN/bind/filter fluency, LDAPS versus StartTLS, and why greenfield SaaS hides LDAP behind OIDC rather than exposing it to apps?
- What is step 1: Client connects (389 + StartTLS, or 636 LDAPS)?
- What is step 2: Bind as service account or end user?
- What is step 3: Search with base, scope, filter; read attributes?
- What is step 4: Apps map groups → roles; IdPs sync or proxy LDAP?
- What mistake is **Cleartext simple bind — password on the wire without StartTLS/LDAPS**?
- What mistake is **Treating DN string equality casually — escaping, case, and attribute order confuse apps**?
- What mistake is **Using LDAP as a general application database**?

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
- Cleartext simple bind — password on the wire without StartTLS/LDAPS.
- Treating DN string equality casually — escaping, case, and attribute order confuse apps.
- Using LDAP as a general application database.
- `TLS_REQCERT never` in production.

## Comparison
- vs OIDC/SAML IdP: hide LDAP behind the IdP for consumer SaaS and modern apps.
- vs SQL user tables: directory wins for org hierarchy and centralized OS login; SQL wins for product data.

## Real-World Applications
Active Directory / OpenLDAP for enterprise login, SSH key distribution via attributes, and IdP backends that sync directory groups into roles.

**Example:** A Linux fleet uses SSSD against LDAP so `uid=alice` resolves to the same POSIX attributes on every host.

## Pros/Cons or Trade-offs
- **Pro:** Hierarchical identity and group data with mature tooling (AD, OpenLDAP).
- **Con:** Wrong model for session stores, catalogs, or high-churn documents — use Redis/SQL.
- **Con:** Direct app-to-LDAP couples every service to directory quirks; prefer OIDC/SAML in front.
