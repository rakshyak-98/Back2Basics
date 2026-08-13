[[Networking]] [[NAT (Network Address Translation)]] [[outbound ip]] [[CIDR (Classless Inter-Domain Routing)]]

# network gateway

> A gateway is the next hop for traffic that isn’t local — usually your router’s LAN IP, or `0.0.0.0/0` in the route table.

---

## How it works

```txt
Host 192.168.1.10
  │ dest 8.8.8.8 not local
  ▼
Gateway 192.168.1.1 ── NAT / ISP ──► Internet
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Default gateway** | Router for “everything else” | “Route `0.0.0.0/0` via that IP.” |
| **`0.0.0.0/0`** | Match any destination | “Default route in the table.” |
| **`0.0.0.0` bind** | Unspecified local address | “Listen on all interfaces — different meaning.” |
| **Port forward** | Map WAN port → LAN IP:port | “Inbound path through the gateway.” |
| **Reverse tunnel / VPN** | Reach private hosts without inbound NAT | “Outbound-initiated path.” |

### Reach a private host from the internet (options)

| Method | When |
|--------|------|
| Port forwarding | You control the router; open one service |
| Reverse SSH / Cloudflare Tunnel / ngrok | No inbound; host dials out |
| VPN / Tailscale / ZeroTier | Whole private net, better than random forwards |

---


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| LAN OK, internet dead | `ip route`; ping gateway then `1.1.1.1` | Fix default via; DHCP gateway; cable/WAN |
| Forward “open” but timeout | Target IP changed; host firewall | Reservation + ufw allow; test from outside |
| Two defaults | `ip route` metrics | Remove stale route; fix NetworkManager |
| Can egress, can’t ingress | CGNAT / ISP blocks inbound | Tunnel/VPN instead of port forward |

---


## Gotchas

> [!WARNING]
> **`0.0.0.0` means two jobs** — route `0.0.0.0/0` = default path; bind `0.0.0.0` = all local IPs. Don’t conflate them.

> [!WARNING]
> **Public IP ≠ your laptop** — `ifconfig.me` shows the NAT’s [[outbound ip]]; port forwards must target the real LAN host.

> [!WARNING]
> **Hairpin NAT** — accessing your public IP from inside the LAN often fails; use the private IP on LAN ([[Internal routing]]).

---


## When not to use

- **Port-forwarding every hobby service** — prefer Tailscale/Cloudflare Tunnel for administrator UIs.
- **Assuming the gateway is a firewall policy engine** — many home routers are weak; don’t rely on them for zero-trust.
- **Hard-coding gateway IPs in apps** — use the OS route table; apps should dial destinations, not next hops.

---


## Related

[[Networking]] [[NAT (Network Address Translation)]] [[outbound ip]] [[Internal routing]] [[CIDR (Classless Inter-Domain Routing)]] [[Egress and Ingress]]

## Sources

- [Wikipedia — network gateway](https://en.wikipedia.org/wiki/network_gateway)
