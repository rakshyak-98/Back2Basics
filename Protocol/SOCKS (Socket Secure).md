[[TCP]] [[UDP]] [[SSH]] [[Egress traffic]] [[webSocket]]

# SOCKS (Socket Secure)

> SOCKS is a client-side proxy protocol that tunnels arbitrary TCP (and UDP in v5) through a proxy — useful for debug egress and jump-host paths (RFC 1928).

```txt
        SOCKS (Socket Secu ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers distinguish SOCKS from HTTP proxies, `socks5` versus `socks5h` D…

## Sources
- [RFC 1928 — SOCKS Protocol Version 5](https://datatracker.ietf.org/doc/html/rfc1928) — deep-dive
- [Wikipedia — SOCKS](https://en.wikipedia.org/wiki/SOCKS) — overview

## Key Concepts
- **Tunnel after handshake:** unlike HTTP proxies (URL-level), SOCKS bridges a raw byte stream to the targe…
- **SOCKS4 vs SOCKS5:** v4 is TCP/IPv4 only; v5 adds UDP, auth, IPv6, and domain names.
- **Remote DNS (`socks5h`):** resolve on the proxy — avoids local leak and reaches internal-only names.
- **Not encryption:** payload is visible unless the inner protocol is TLS/SSH.

## Technical Details
```
App ──SOCKS handshake──► Proxy (:1080) ──TCP connect──► target:443
     ◄──── byte stream bridged both ways ────►
```

| Version | Features |
|---------|----------|
| **SOCKS4** | TCP only, no auth, no hostname (IPv4 only) |
| **SOCKS5** | TCP + UDP, username/password or GSSAPI, IPv4/IPv6/domain |

- Common uses: corporate egress (`ALL_PROXY`), [[SSH]] dynamic forward (`-D 108…

```shell
# SSH local SOCKS proxy (dynamic port forward)
ssh -N -D 1080 -q user@jump-host

# curl through SOCKS (DNS resolved on proxy — avoids local leak)
curl --socks5-hostname 127.0.0.1:1080 https://ifconfig.me
curl -v --proxy socks5h://127.0.0.1:1080 https://internal.service.local

# Test TCP reachability via tunnel
nc -X 5 -x 127.0.0.1:1080 target.host 443

export ALL_PROXY=socks5://127.0.0.1:1080
export NO_PROXY=localhost,127.0.0.1,10.0.0.0/8

chrome --proxy-server="socks5://127.0.0.1:1080"
ss -tlnp | grep 1080
```

- Minimal Dante snippet (`/etc/sockd.conf`):

```
internal: eth0 port = 1080
external: eth0
clientmethod: none
socksmethod: username
user.privileged: root
user.unprivileged: nobody
client pass { from: 10.0.0.0/8 to: 0.0.0.0/0 }
socks pass { from: 10.0.0.0/8 to: 0.0.0.0/0 }
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` to SOCKS port | `ss -tlnp`; SSH `-D` running? | Start tunnel; open firewall to jump host |
| Works for IP, fails for hostname | SOCKS4 vs SOCKS5; DNS local vs remote | Use `socks5h://` (remote resolve) not `socks5://` |
| Auth failure | Username/password required | `curl -U user:pass --socks5-hostname ...` |
| Tunnel up, target timeout | Proxy can't reach destination | SG on target; routing from jump host; wrong VPC |
| HTTPS cert errors through tunnel | Expected if MITM corporate proxy | Use corporate CA; not a SOCKS bug |
| Intermittent drops | Idle NAT timeout on jump path | Enable SSH `ServerAliveInterval 60` |
| UDP apps fail | SOCKS4 or no UDP associate | SOCKS5 with UDP relay; many tools TCP-only |

## Mistakes to Avoid
- **Mistake:** Using `socks5://` when you need remote DNS
- **Mistake:** Assuming SOCKS encrypts traffic
- **Mistake:** Open-relay Dante/microsocks configs without `from:` ACLs
- **Mistake:** Forcing UDP apps through SOCKS4

## Pros/Cons or Trade-offs
- **Pro:** Protocol-agnostic TCP tunnel — SSH, HTTPS, databases all work.
- **Con:** Manual `-D` tunnels are not a service mesh; chaining multiplies failure points.
- **Con:** Browser SOCKS may not cover system DNS or QUIC/HTTP3 bypass paths.

## Comparison
- vs HTTP CONNECT / forward proxy: use those when you must terminate or inspect HTTP
- vs permanent mesh routing: sidecar/iptables beats ad-hoc SOCKS for production service paths.


### Use cases
- Developer access through a bastion, browser debugging of internal hostnames, …

- **Example:** `ssh -N -D 1080 user@jump` plus `curl --socks5-hostname 127.0.0.…
