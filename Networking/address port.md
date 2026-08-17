[[Networking]] [[TCP]] [[UDP]] [[BSD Socket]] [[POSIX Socket]] [[outbound ip]] [[localhost]]

# address port

> An address:port pair is one endpoint — local is your socket; peer is the other side.

```txt
        address port ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check that you can read `ss` Local vs Peer columns, explain ephe…

## Sources
- [IANA — Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) — deep-dive
- [RFC 6335 — Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry](https://www.rfc-editor.org/rfc/rfc6335) — overview
- [man 7 ip (Linux)](https://man7.org/linux/man-pages/man7/ip.7.html) — overview

## Key Concepts
- **Local address:port:** this host’s side of the socket → after `connect`, the OS shows our ephemeral …
- **Peer / remote address:port:** the other endpoint → peer port is usually the service (80, 443, 5432).
- **Well-known port:** 0–1023 (needs privilege to bind) → listeners for standard services.
- **Ephemeral / dynamic:** high ports the OS assigns to clients → outbound clients rarely bind; OS picks.
- **5-tuple:** protocol + local IP:port + peer IP:port → uniquely identifies a [[TCP]] (or […

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

## Mistakes to Avoid
- **Mistake:** Treating port alone as unique
- **Mistake:** Hard-coding client ports
- **Mistake:** Using port as authentication
- **Mistake:** Assuming peer port is stable behind CGNAT
- **Mistake:** Forgetting containers/NAT
- **Mistake:** Ignoring TIME_WAIT

## Pros/Cons or Trade-offs
- **Pro:** Simple demultiplexing key for millions of concurrent flows on one host.
- **Con:** Port space is finite — high churn without pooling causes exhaustion.
- **Con:** Privileged ports (<1024) complicate least-privilege deploys unless you use capabilities or higher ports.

## Comparison
- vs hostname: DNS names resolve to addresses; the port still selects the service.
- vs [[localhost]] / bind IP: `127.0.0.1:8080` is not the same socket as `0.0.0.0:8080` or a LAN IP…
- Related APIs: [[BSD Socket]], [[POSIX Socket]].


### Use cases
- Every socket bind/connect chooses an address:port

- **Example:** A client storm of short HTTPS connections exhausts ephemeral por…
