[[Networking]] [[localhost]] [[address port]] [[non-Routable address]] [[network gateway]] [[NAT (Network Address Translation)]]

# Internal routing

> Internal routing is same-LAN reachability — private IP to private IP with no internet hairpin required.

```txt
        Internal routing ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers check whether you debug LAN reachability (bind address, subnet/V…

## Sources
- [RFC 1918 — Address Allocation for Private Internets](https://www.rfc-editor.org/rfc/rfc1918) — overview
- [Wikipedia — Private network](https://en.wikipedia.org/wiki/Private_network) — overview
- [ip-address(8) — Linux manual page](https://man7.org/linux/man-pages/man8/ip-address.8.html) — deep-dive

## Key Concepts
| Word | Plain meaning | Interview phrasing |
|------|---------------|--------------------|
| **Same L2/L3 segment** | Shared broadcast / subnet | “ARP resolves MAC; IP stays private.” |
| **Private IP** | RFC1918 address | “`10/8`, `172.16/12`, `192.168/16`.” |
| **Hairpin / NAT loopback** | LAN host → public IP → back in | “Often broken; prefer private IP on LAN.” |
| **Host firewall** | ufw/iptables on the target | “Port open on process ≠ open on firewall.” |

## Technical Details
```txt
Laptop 192.168.1.10 ── switch ──► Pi 192.168.1.50:5000
                 (no NAT, no public IP needed)
```

```bash
# Target’s private IP
ip -4 addr show
hostname -I

# Is the service listening where you think?
ss -tlnp | grep 5000
# Prefer 0.0.0.0 or LAN IP — not only 127.0.0.1

# Connect from another LAN host
curl http://192.168.1.50:5000

# Allow inbound (example)
sudo ufw allow 5000/tcp
sudo ufw status
```

| Knob | Why it matters |
|------|----------------|
| Bind address | `127.0.0.1` blocks LAN clients |
| Subnet / VLAN | Different VLAN ⇒ need a router between them |
| mDNS / DHCP names | `hostname.local` helps; IP is the reliable debug target |

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `ss -tlnp` on target | Start service; fix bind host/port |
| Timeout | `ping` / `traceroute`; ufw/SG | Same subnet? Allow port; fix Wi‑Fi AP isolation |
| Works via localhost only | Bound to loopback | Bind `0.0.0.0` or LAN IP |
| Phone can’t see laptop | AP client isolation | Disable isolation or use a travel router/VLAN that allows peer traffic |
| Used public IP from LAN | Hairpin NAT | Use private IP on LAN instead |

## Mistakes to Avoid
- **Mistake:** AP / “guest Wi‑Fi” isolation
- **Mistake:** Wrong private IP after DHCP renew
- **Mistake:** VPN split tunnel
- **Mistake:** Assuming same Wi‑Fi = same network — guest networks and VLANs lie
- **Mistake:** Exposing a service to the internet via forever port-forward

## Pros/Cons or Trade-offs
- **Pro:** Low latency, no NAT, no public exposure required for same-LAN clients.
- **Con:** DHCP churn and AP isolation make “same Wi‑Fi” unreliable as a trust or reachability assumption.
- **Con:** LAN is not a security boundary on shared Wi‑Fi — still authenticate.

## Comparison
- vs [[localhost]]: loopback never leaves the host; internal routing is host-to-host on the LAN/VPC.
- vs [[network gateway]] / internet path: off-subnet or public destinations need a gateway
- vs hairpin via public IP: prefer private IP on LAN — hairpin NAT is often broken.


### Use cases
- Homelab services, office printers, IoT devices, and VPC private subnet east-w…

- **Example:** Flask app bound to `127.0.0.1:5000` works on the Pi but times ou…
