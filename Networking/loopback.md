[[localhost]] [[DNS]] [[DNS rebinding]] [[TCP]] [[UDP]] [[Network error]]

# Loopback

> Logical network interface (`lo`) whose addresses (`127.0.0.1`, `::1`) route traffic back to the same host — no physical NIC involved.

```txt
        Loopback ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers distinguish loopback (interface/addresses) from the `localhost` …

## Sources
- [RFC 1122 — Requirements for Internet Hosts — Communication Layers](https://www.rfc-editor.org/rfc/rfc1122) — deep-dive
- [RFC 4291 — IP Version 6 Addressing Architecture (loopback)](https://www.rfc-editor.org/rfc/rfc4291) — overview
- [Wikipedia — Loopback](https://en.wikipedia.org/wiki/Loopback) — overview

## Key Concepts
- **Interface `lo`:** always-up virtual NIC → no cable, no ARP to the outside.
- **IPv4 / IPv6 addresses:** `127.0.0.1` and `::1` → same-host delivery.
- **Local-only services:** DB, Redis, metrics, health checks bound to loopback → not exposed on the LAN …
- **DNS → loopback:** `/etc/hosts` development entries (`127.0.0.1 myapp.local`) → name resolves wi…
- **Security boundary (partial):** remote attackers cannot reach *your* `127.0.0.1` directly, but SSRF and DNS r…


- **Core:** Loopback shortcuts the stack so packets to `127.0.0.0/8` or `::1` never leave…

## Technical Details
```txt
App connects to 127.0.0.1:5432
  └─ packet never leaves host ──► postgres on same machine
```

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

- **Why bind localhost:** expose administrator/metrics only to a local reverse …

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused on 127.0.0.1 | `ss -tlnp` listener address | App listening on 0.0.0.0 vs 127.0.0.1 |
| Works by IP, fails by hostname | `/etc/hosts`; DNS | Fix hosts entry; nsswitch `files dns` |
| Browser hits wrong local service | Host header + port | Multiple dev servers; check port |
| SSRF to metadata | App fetches user URL → 169.254/127 | Block link-local and loopback in fetcher |

## Mistakes to Avoid
- **Mistake:** Assuming loopback binding alone protects multi-tenant or contain…
- **Mistake:** Ignoring IPv6 `::1` vs IPv4 `127.0.0.1`
- **Mistake:** Allowing unrestricted URL fetchers

## Pros/Cons or Trade-offs
- **Pro:** Simple isolation from the LAN without firewall rules for many single-host setups.
- **Con:** Not encrypted by default — other local users/processes may still connect if permissions are weak.
- **Con:** Multi-tenant hosts and containers share a kernel — loopback alone is not a tenancy boundary; use namespaces and authentication.

## Comparison
- vs [[localhost]]: loopback is the interface/address family
- vs LAN bind (`0.0.0.0` / NIC IP): reachable from other hosts on the network.
- vs link-local (`169.254/16`): same L2 segment, not “this host only.”


### Use cases
- Local databases, reverse proxies fronting admin UIs, and developer `/etc/host…

- **Example:** Metrics bound to `127.0.0.1:9090` are scraped by a local agent o…
