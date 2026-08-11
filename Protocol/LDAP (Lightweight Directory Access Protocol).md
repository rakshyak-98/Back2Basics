[[Protocol]] [[TLS (Transport Layer Security)]] [[TCP]]

# LDAP (Lightweight Directory Access Protocol)

> LDAP (Lightweight Directory Access Protocol) — query and update a hierarchical directory (users, groups, devices) over the network — usually the source of truth for “who is this user?”

---

## Mental model

**Say it in one breath:** Clients bind (authenticate) to a directory server (DSA), then search/modify entries addressed by DN (distinguished name) in a tree — think “phone book + authentication,” not a general SQL database.

```txt
App / IdP / login shell
        │  bind + search (ldap://:389 or ldaps://:636)
        ▼
Directory (OpenLDAP, Active Directory, 389-ds)
   dc=example,dc=com
     └─ ou=people
          └─ uid=alice  (attributes: mail, memberOf, …)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **DN** | Full path to an entry | “uid=alice,ou=people,dc=example,dc=com.” |
| **Bind** | Authenticate the LDAP session | “Simple bind is user+password; prefer SASL/GSSAPI.” |
| **Base DN + filter** | Where to search + who matches | “Subtree search with `(uid=alice)`.” |
| **Attribute** | Field on an entry | “memberOf / mail / sshPublicKey live as attrs.” |
| **LDAPS / StartTLS** | Encrypt LDAP | “Never bind with passwords on cleartext 389.” |

### How the story goes

1. Client connects (389 + StartTLS, or 636 LDAPS).
2. Bind as service account or end user.
3. Search with base, scope, filter; read attributes.
4. Apps map groups → roles; IdPs sync or proxy LDAP.

---

## Standard config / commands

```bash
# Anonymous or simple bind search (lab only)
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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Can't contact LDAP server` | DNS, 389/636, TLS | Fix SRV/A; open ports; trust CA |
| Invalid credentials | Wrong DN / password / expired | Confirm DN form; unlock AD account |
| Search returns nothing | Bad base DN / filter / ACLs | Widen filter; check ACI/ACL deny |
| TLS handshake fails | Hostname vs cert SAN | Fix cert; `TLS_REQCERT` not `never` in prod |
| Slow logins | Unindexed filter | Add indexes for uid/mail/member |
| Intermittent AD auth | DC failover / site awareness | Point to VIP or correct site DCs |

---

## Gotchas

> [!WARNING]
> **Cleartext simple bind** — password on the wire if you skip StartTLS/LDAPS.

> [!WARNING]
> **DN string equality is picky** — escaping, case, and attribute order confuse apps.

> [!WARNING]
> **LDAP is not your app DB** — wide writes and complex joins belong in a real database; directory is for identity and org data.

---

## When NOT to use

- **Session store or product catalog** — use Redis/SQL.
- **Greenfield consumer SaaS authentication** — OIDC/SAML to an IdP; hide LDAP behind it.
- **High-churn document storage** — wrong consistency and query model.

---

## Related

[[TLS (Transport Layer Security)]] [[TCP]] [[SSH]] [[DNS]] [[Protocol]]
