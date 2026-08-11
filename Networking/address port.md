[[Networking]] [[TCP]] [[UDP]] [[BSD Socket]] [[POSIX Socket]]

# address port

> An address:port pair is one endpoint — local is your socket; peer is the other side.

---

## Mental model

**Say it in one breath:** IP picks the host; port picks the process/service on that host. A TCP connection is two endpoints: local and peer.

```txt
Your app                          Remote service
local 192.168.1.10:54321  ←→  peer 203.0.113.5:443
     (ephemeral)                      (well-known)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Local address:port** | This host’s side of the socket | “After connect, OS shows our ephemeral port.” |
| **Peer / remote address:port** | The other endpoint | “Peer port is usually the service (80, 443, 5432).” |
| **Well-known port** | 0–1023 (needs privilege to bind) | “Listeners for standard services.” |
| **Ephemeral / dynamic** | High ports OS assigns to clients | “Outbound clients rarely bind; OS picks.” |
| **5-tuple** | proto + local IP:port + peer IP:port | “Uniquely identifies a TCP flow.” |

### Typical ranges (Linux)

| Range | Role |
|-------|------|
| 0–1023 | System / privileged |
| 1024–49151 | Registered / app servers |
| 49152–65535 | Ephemeral (often; see `ip_local_port_range`) |

---

## Standard config / commands

```bash
# Who is listening / connected?
ss -tlnp                  # listeners
ss -tnp | head            # established + peers

# Ephemeral port range
cat /proc/sys/net/ipv4/ip_local_port_range

# Explicit bind (rare for clients)
# bind 0.0.0.0:8080 → accept on all IPs, port 8080
```

| Knob | Why it matters |
|------|----------------|
| Bind port | Server identity — collide ⇒ `EADDRINUSE` |
| Bind IP | `127.0.0.1` vs LAN vs `0.0.0.0` |
| `SO_REUSEADDR` | Faster rebind after TIME_WAIT |
| Peer port in logs | Debug wrong service / NAT mapping |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep :port` | Kill old process or pick another port |
| Connect works, reply fails | NAT / asymmetric path | Check peer sees correct return IP ([[outbound ip]]) |
| Exhausted outbound ports | Many short connections | Pool connections; raise range; reuse |
| Wrong peer in logs | Looking at local not remote | `ss` Local Address vs Peer Address columns |
| Permission denied bind | Port < 1024 as non-root | Use ≥1024 or grant `CAP_NET_BIND_SERVICE` |

---

## Gotchas

> [!WARNING]
> **Port alone is not unique** — same port on different IPs (or IPv4 vs IPv6) are different sockets.

> [!WARNING]
> **Ephemeral ≠ forever** — after close, TIME_WAIT can hold the 4-tuple briefly.

> [!WARNING]
> **Containers / NAT** — host port ≠ container port; map explicitly (`-p 8080:80`).

---

## When NOT to use

- **Hard-coding client ports** — let the OS assign ephemeral ports unless a firewall demands otherwise.
- **Using port as auth** — security groups help; they are not credentials.
- **Assuming peer port stable behind CGNAT** — mappings churn; identify users at the app layer.

---

## Related

[[Networking]] [[TCP]] [[UDP]] [[BSD Socket]] [[POSIX Socket]] [[outbound ip]] [[localhost]]
