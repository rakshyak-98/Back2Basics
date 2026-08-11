[[localhost]] [[DNS]] [[DNS rebinding]] [[TCP]]

# Loopback

> Logical network interface (`lo`) whose addresses (`127.0.0.1`, `::1`) route traffic back to the same host — no physical NIC involved.

---

## Mental model

**Loopback** shortcuts the stack:

```txt
App connects to 127.0.0.1:5432
  └─ packet never leaves host ──► postgres on same machine
```

Uses:
- Local services (DB, Redis, dev servers)
- Health checks bound to localhost only
- **DNS resolving to loopback** — `/etc/hosts` dev entries (`127.0.0.1 myapp.local`)

Distinct from **[[localhost]]** hostname convention — loopback is the interface/address family.

**Security angle:** remote attacker can't reach `127.0.0.1` on your machine directly, but **DNS rebinding** and **SSRF** can trick *your browser or app* into hitting local services.

---

## Standard config / commands

### Interface status

```bash
ip addr show lo
ping -c1 127.0.0.1
ping6 -c1 ::1
```

### Bind service to loopback only

```bash
# postgres pg_hba + listen_addresses = 'localhost'
ss -tlnp | grep 127.0.0.1
```

### /etc/hosts dev mapping

```txt
127.0.0.1   api.local.test
127.0.0.1   app.local.test
```

```bash
getent hosts api.local.test
curl -v http://127.0.0.1:8080/health
```

**Why bind localhost:** expose admin/metrics only to local reverse proxy or SSH tunnel — not the LAN.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused on 127.0.0.1 | `ss -tlnp` listener address | App listening on 0.0.0.0 vs 127.0.0.1 |
| Works by IP, fails by hostname | `/etc/hosts`; DNS | Fix hosts entry; nsswitch `files dns` |
| Browser hits wrong local service | Host header + port | Multiple dev servers; check port |
| SSRF to metadata | App fetches user URL → 169.254/127 | Block link-local and loopback in fetcher |

---

## Gotchas

> [!WARNING]
> **Loopback is not encrypted by default** — traffic stays on host but other local users/processes may connect if permissions weak.

> [!WARNING]
> **Malicious domain → 127.0.0.1** in public DNS is attack surface for clients that fetch attacker URLs.

> [!WARNING]
> **IPv6 `::1` vs IPv4 `127.0.0.1`** — apps listening on only one family fail `localhost` resolution order.

---

## When NOT to use

Don't rely on loopback binding alone in **multi-tenant hosts** — containers share kernel; use network namespaces and auth.

---

## Related

[[localhost]] [[DNS rebinding]] [[TCP]] [[UDP]] [[Network error]]
