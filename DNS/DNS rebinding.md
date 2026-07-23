[[DNS]] [[SOP (Same-Origin Policy)]] [[CORS (Cross Origin Request Sharing)]]

# DNS rebinding

> One-line: attacker rotates DNS answers to turn the browser into a proxy to internal IPs — bypasses naive same-origin checks — **CWE-350**.

## Mental model

Browser loads attacker page from `evil.example` (legitimate origin at load time). Attacker's DNS TTL is **very short**; on reconnect the name resolves to `127.0.0.1`, `169.254.169.254`, or `10.0.0.5`. Same-origin policy compares **scheme+host+port at request time** — if host string still matches but IP is now internal, fetches may hit services that trust "local" clients.

```
1. Victim opens https://evil.example/attacker.js
2. DNS: evil.example → 1.2.3.4 (attacker server) ✓ SOP ok
3. Attacker JS loops fetch('https://evil.example:8080/admin')
4. DNS TTL expires → evil.example → 127.0.0.1
5. Browser connects to localhost:8080 — same host header, new IP
```

> [!INFO]
> [[SOP (Same-Origin Policy)]] compares origin **names**, not resolved IPs. DNS rebinding exploits the gap between DNS name and routing target.

Targets: admin panels on `127.0.0.1`, Redis/Memcached without auth, cloud metadata (`169.254.169.254`), internal REST APIs, WebSocket servers bound `0.0.0.0`.

## Standard config / commands

### Detect (defender)

```shell
# Short TTL on public name pointing to RFC1918? (passive DNS / registrar audit)
dig suspicious.example A +noall +answer +ttlid

# Services bound to all interfaces (attack surface)
ss -tlnp | grep -E ':(6379|11211|8080|9200)\s'

# Metadata exposure test (from instance — should fail from browser context after fix)
curl -s --max-time 2 http://169.254.169.254/latest/meta-data/
```

### Mitigations (layered — use more than one)

**1. Bind services to specific interfaces**

```yaml
# redis.conf
bind 127.0.0.1 ::1
protected-mode yes
```

**2. Host header validation (apps + reverse proxies)**

```nginx
# Reject requests whose Host doesn't match allowlist
server {
    listen 8080;
    if ($host !~* ^(app\.internal\.example\.com)$) {
        return 444;
    }
}
```

**3. DNS pinning in custom clients** — browsers don't expose this; **don't rely on it in browser-facing apps**.

**4. Block private/reserved IPs at egress (browser isn't enough — server-side outbound too)**

```nginx
# Prevent SSRF-style outbound from your app (also helps rebinding callbacks)
# Use resolver + variable proxy_pass; deny literal private IPs in app code
```

**5. Browser protections (modern)**

- Chrome/Firefox maintain **private network access** checks (formerly CORS-RFC1918): cross-origin requests to private IPs may require preflight approval.
- Still patch services — browser policy isn't universal across engines/versions.

**6. Firewall internal services**

```shell
# Only VPC CIDR can reach admin port
iptables -A INPUT -p tcp --dport 8080 -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -p tcp --dport 8080 -j DROP
```

**7. mTLS / auth on every internal API** — rebinding without credentials yields nothing.

**8. Disable unnecessary HTTP servers** on dev machines; don't run `kubectl proxy` / Docker API exposed.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Internal API hit from "external" referer | Access logs show Host=public name, src=127.0.0.1 | Host allowlist; bind service to internal IP only |
| Metadata stolen from browser chain | IMDS hop limit, metadata service v2 | AWS IMDSv2 required + hop limit 1; firewall 169.254.169.254 from containers |
| Redis/Mongo "random" commands | `MONITOR`; bind address | `bind 127.0.0.1`; require AUTH; SG restrict port |
| Dev laptop compromised via local service | `ss -tlnp` for 0.0.0.0 listeners | Bind localhost; use firewall (ufw) default deny |
| Pen test flags DNS rebinding | PoC resolves to internal IP | Implement mitigations above; document accepted risk only with auth layer |

## Gotchas

> [!WARNING]
> **`0.0.0.0` bind on a laptop** behind a browser = rebinding target. "It's dev only" doesn't matter if you visit the internet on the same machine.

- **WebSocket** is equally vulnerable — origin check without IP pinning doesn't stop rebinding.
- **Long-lived connections** may hold old IP while new DNS queries get new IP — race amplifies attack window.
- **Corporate split DNS** doesn't protect localhost services.
- **IPv6** `:1` and ULA addresses are in scope — block `::1` and fc00::/7 in SSRF guards too.

## When NOT to use

- Offensive testing without written scope — rebinding against third parties is illegal.
- Assuming [[CORS (Cross Origin Request Sharing)]] alone fixes this — CORS governs cross-origin reads, not DNS-to-IP mapping attacks on same host string.

## Related

[[DNS]] · [[SOP (Same-Origin Policy)]] · [[CORS (Cross Origin Request Sharing)]] · [[IDOR]] · [[TLS (Transport Layer Security)]]
