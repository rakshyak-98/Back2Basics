[[Networking]] [[TCP]] [[UDP]] [[BSD Socket]] [[POSIX Socket]] [[outbound ip]] [[localhost]]

# address port

> An address:port pair is one endpoint — local is your socket; peer is the other side.





## Interview Relevance
Interviewers check that you can read `ss` Local vs Peer columns, explain ephemeral vs well-known ports, and define a TCP 5-tuple — common failure talk includes `EADDRINUSE` and port exhaustion.

## Sources
- [IANA — Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) — deep-dive
- [RFC 6335 — Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry](https://www.rfc-editor.org/rfc/rfc6335) — overview
- [man 7 ip (Linux)](https://man7.org/linux/man-pages/man7/ip.7.html) — overview

## Key Concepts
- **Local address:port:** this host’s side of the socket → after `connect`, the OS shows our ephemeral port.
- **Peer / remote address:port:** the other endpoint → peer port is usually the service (80, 443, 5432).
- **Well-known port:** 0–1023 (needs privilege to bind) → listeners for standard services.
- **Ephemeral / dynamic:** high ports the OS assigns to clients → outbound clients rarely bind; OS picks.
- **5-tuple:** protocol + local IP:port + peer IP:port → uniquely identifies a [[TCP]] (or [[UDP]]) flow.

### Typical ranges (Linux)

| Range | Role |
|-------|------|
| 0–1023 | System / privileged |
| 1024–49151 | Registered / app servers |
| 49152–65535 | Ephemeral (often; see `ip_local_port_range`) |

## Technical Details
```txt
Your app                          Remote service
local 192.168.1.10:54321  ←→  peer 203.0.113.5:443
     (ephemeral)                      (well-known)
```

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

| Symptom | Check | Fix |
|---------|-------|-----|
| `EADDRINUSE` | `ss -tlnp \| grep :port` | Kill old process or pick another port |
| Connect works, reply fails | NAT / asymmetric path | Check peer sees correct return IP ([[outbound ip]]) |
| Exhausted outbound ports | Many short connections | Pool connections; raise range; reuse |
| Wrong peer in logs | Looking at local not remote | `ss` Local Address vs Peer Address columns |
| Permission denied bind | Port < 1024 as non-root | Use ≥1024 or grant `CAP_NET_BIND_SERVICE` |

## Real-World Applications
Every socket bind/connect chooses an address:port; load balancers, containers, and firewalls all key off these pairs.

**Example:** A client storm of short HTTPS connections exhausts ephemeral ports — raise `ip_local_port_range`, enable connection pooling, or reuse keep-alive.

## Pros/Cons or Trade-offs
- **Pro:** Simple demultiplexing key for millions of concurrent flows on one host.
- **Con:** Port space is finite — high churn without pooling causes exhaustion.
- **Con:** Privileged ports (<1024) complicate least-privilege deploys unless you use capabilities or higher ports.

## Comparison
- vs hostname: DNS names resolve to addresses; the port still selects the service.
- vs [[localhost]] / bind IP: `127.0.0.1:8080` is not the same socket as `0.0.0.0:8080` or a LAN IP on the same port.
- Related APIs: [[BSD Socket]], [[POSIX Socket]].

## Mistakes to Avoid
- Treating port alone as unique — same port on different IPs (or IPv4 vs IPv6) are different sockets.
- Hard-coding client ports — let the OS assign ephemeral ports unless a firewall demands otherwise.
- Using port as authentication — security groups help; they are not credentials.
- Assuming peer port is stable behind CGNAT — mappings churn; identify users at the application layer.
- Forgetting containers/NAT — host port ≠ container port; map explicitly (`-p 8080:80`).
- Ignoring TIME_WAIT — after close, the 4-tuple can be held briefly and block immediate rebind.
