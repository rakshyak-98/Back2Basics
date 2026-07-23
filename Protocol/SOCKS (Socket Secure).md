[[TCP]] [[UDP]] [[SSH]]

# SOCKS (Socket Secure)

> One-line: client-side proxy protocol that tunnels arbitrary TCP (and UDP in v5) through a proxy — debug egress and bypass paths — **RFC 1928**.

## Mental model

Unlike HTTP proxies (URL-level), SOCKS hands the client a **tunnel** after authentication. The client then speaks the target protocol raw — SSH, HTTPS, DB, anything TCP.

```
App ──SOCKS handshake──► Proxy (:1080) ──TCP connect──► target:443
     ◄──── byte stream bridged both ways ────►
```

| Version | Features |
|---------|----------|
| **SOCKS4** | TCP only, no auth, no hostname (IPv4 only) |
| **SOCKS5** | TCP + UDP, username/password or GSSAPI, IPv4/IPv6/domain |

Common uses: corporate egress (`ALL_PROXY`), [[SSH]] dynamic forward (`-D 1080`), browser `--proxy-server`, tooling (`curl --socks5-hostname`).

## Standard config / commands

```shell
# SSH local SOCKS proxy (dynamic port forward)
ssh -N -D 1080 -q user@jump-host

# curl through SOCKS (DNS resolved on proxy — avoids local leak)
curl --socks5-hostname 127.0.0.1:1080 https://ifconfig.me
curl -v --proxy socks5h://127.0.0.1:1080 https://internal.service.local

# Test TCP reachability via tunnel
nc -X 5 -x 127.0.0.1:1080 target.host 443

# Environment (many CLI tools honor these)
export ALL_PROXY=socks5://127.0.0.1:1080
export NO_PROXY=localhost,127.0.0.1,10.0.0.0/8

# Browser debug (WebSocket through SOCKS)
chrome --proxy-server="socks5://127.0.0.1:1080"

# Listen check
ss -tlnp | grep 1080
```

### Minimal Dante server snippet (`/etc/sockd.conf`)

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Connection refused` to SOCKS port | `ss -tlnp`; SSH `-D` running? | Start tunnel; open firewall to jump host |
| Works for IP, fails for hostname | SOCKS4 vs SOCKS5; DNS local vs remote | Use `socks5h://` (remote resolve) not `socks5://` |
| Auth failure | Username/password required | `curl -U user:pass --socks5-hostname ...` |
| Tunnel up, target timeout | Proxy can't reach destination | SG on target; routing from jump host; wrong VPC |
| HTTPS cert errors through tunnel | Expected if MITM corporate proxy | Use corporate CA; not a SOCKS bug |
| Intermittent drops | Idle NAT timeout on jump path | Enable SSH `ServerAliveInterval 60` |
| UDP apps fail | SOCKS4 or no UDP associate | SOCKS5 with UDP relay; many tools TCP-only |

## Gotchas

> [!WARNING]
> **`socks5` vs `socks5h`:** Without `h`, DNS resolves **locally** — leaks intent and breaks internal-only names. Prefer `-hostname` / `socks5h://` for tunnel debugging.

- **SOCKS is not encryption** — payload visible unless inner protocol is TLS (HTTPS, SSH).
- **Browser SOCKS** doesn't cover all traffic (system DNS, QUIC/HTTP3 may bypass).
- **Chaining** (SOCKS → SOCKS) multiplies failure points — document one canonical jump host.
- **Dante / microsocks** misconfig → open relay; restrict `from:` ACLs.

## When NOT to use

- Terminate TLS and inspect HTTP → HTTP CONNECT or explicit forward proxy, not raw SOCKS.
- Permanent service mesh routing → use sidecar/iptables, not manual `-D` tunnels.

## Related

[[SSH]] · [[TCP]] · [[webSocket]] · [[Egress traffic]]
