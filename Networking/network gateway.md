[[Networking]] [[NAT (Network Address Translation)]] [[outbound ip]] [[CIDR (Classless Inter-Domain Routing)]] [[Internal routing]] [[routing table]]

# network gateway

> A gateway is the next hop for traffic that isn’t local — usually your router’s LAN IP, or `0.0.0.0/0` in the route table.

```txt
        network gateway ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe default routes, the dual meaning of `0.0.0.0`, and how you…

## Sources
- [Wikipedia — Gateway (telecommunications)](https://en.wikipedia.org/wiki/Gateway_(telecommunications)) — overview
- [ip-route(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ip-route.8.html) — deep-dive
- [RFC 1812 — Requirements for IP Version 4 Routers](https://www.rfc-editor.org/rfc/rfc1812) — overview

## Key Concepts
| Word | Plain meaning | Interview phrasing |
|------|---------------|--------------------|
| **Default gateway** | Router for “everything else” | “Route `0.0.0.0/0` via that IP.” |
| **`0.0.0.0/0`** | Match any destination | “Default route in the table.” |
| **`0.0.0.0` bind** | Unspecified local address | “Listen on all interfaces — different meaning.” |
| **Port forward** | Map WAN port → LAN IP:port | “Inbound path through the gateway.” |
| **Reverse tunnel / VPN** | Reach private hosts without inbound NAT | “Outbound-initiated path.” |

Reach a private host from the internet:

| Method | When |
|--------|------|
| Port forwarding | You control the router; open one service |
| Reverse SSH / Cloudflare Tunnel / ngrok | No inbound; host dials out |
| VPN / Tailscale / ZeroTier | Whole private net, better than random forwards |

## Technical Details
```txt
Host 192.168.1.10
  │ dest 8.8.8.8 not local
  ▼
Gateway 192.168.1.1 ── NAT / ISP ──► Internet
```

```bash
# Default route / gateway
ip route
# default via 192.168.1.1 dev eth0

# Public face (what internet sees)
curl -4 https://ifconfig.me

# Reverse SSH example (private:3000 published on VPS:8080)
ssh -R 8080:localhost:3000 user@public-server.example
```

| Knob | Why it matters |
|------|----------------|
| Default route | Wrong gateway ⇒ “no internet” with local LAN OK |
| Port forward target | Must be current DHCP lease / reservation |
| Dual WAN / metric | Lower metric wins; failover can surprise you |

| Symptom | Check | Fix |
|---------|-------|-----|
| LAN OK, internet dead | `ip route`; ping gateway then `1.1.1.1` | Fix default via; DHCP gateway; cable/WAN |
| Forward “open” but timeout | Target IP changed; host firewall | Reservation + ufw allow; test from outside |
| Two defaults | `ip route` metrics | Remove stale route; fix NetworkManager |
| Can egress, can’t ingress | CGNAT / ISP blocks inbound | Tunnel/VPN instead of port forward |

## Mistakes to Avoid
- **Mistake:** Conflating `0.0.0.0/0` (default path) with bind `0.0.0.0` (all l…
- **Mistake:** Assuming `ifconfig.me` is your laptop
- **Mistake:** Hairpin NAT surprises
- **Mistake:** Hard-coding gateway IPs in apps

## Pros/Cons or Trade-offs
- **Pro:** One next hop for “everything not local” keeps host routing simple.
- **Con:** Single point of failure for internet reachability.
- **Con:** Port-forwarding hobby services exposes administrator UIs; tunnels/VPN are often safer.
- **Con:** Home gateways are weak policy engines — not a zero-trust boundary.

## Comparison
- vs [[routing table]]: the table holds many routes
- vs [[outbound ip]]: gateway is where you send packets
- vs [[Internal routing]]: same-LAN traffic often needs no gateway; only off-subnet destinations do.


### Use cases
- Home routers, cloud VPC internet/NAT gateways, and edge appliances that own t…

- **Example:** Laptop loses internet but still pings other LAN hosts
