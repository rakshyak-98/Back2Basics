[[Networking]] [[NAT Traversal]] [[UDP]] [[TCP]]

# NAT (Network Address Translation)

> NAT rewrites packet IPs (and often ports) at the edge — many private devices share one public address.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Your laptop has a private IP. The router swaps that for a public IP on the way out, and swaps back on the way in using a mapping table.

```txt
LAN 192.168.1.10:54321
        │
   NAT rewrite  →  Public 203.0.113.10:40000
        │
      Internet
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Private IP** | Address only valid inside the LAN | “Private IPs are not reachable from the internet.” |
| **Public IP** | Address the internet sees | “NAT hides many hosts behind one public IP.” |
| **Mapping / session** | Table entry: private ↔ public:port | “Return traffic must match an existing mapping.” |
| **SNAT / masquerade** | Rewrite source on egress | “Outbound traffic gets the router’s public face.” |
| **DNAT / port forward** | Rewrite dest on ingress | “Port forward opens one public port to an inside host.” |
| **Symmetric NAT** | Mapping depends on remote IP:port | “Symmetric NAT breaks simple hole punching — need TURN.” |

### How packets move (outbound)

1. **Lookup** — does this flow already have a mapping?
2. **Allocate** — if not, pick an ephemeral public port.
3. **Rewrite** — replace source IP/port; fix checksums.
4. **Remember** — store mapping so replies can come back.

Inbound without a mapping (or port forward) is dropped — that is why peers behind NATs need [[NAT Traversal]] / [[ICE (Interactive Connectivity Establishment)]].

---

## Standard config / commands

```bash
# See NAT mappings (Linux nftables/iptables environments vary)
sudo iptables -t nat -L -n -v
sudo nft list ruleset | head

# Who am I on the public internet? (STUN-style check from a host)
curl -4 ifconfig.me
```

Cloud: security groups + private subnets + NAT gateway = same idea at VPC scale.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Outbound OK, inbound fails | No port forward / no mapping | DNAT or use outbound-initiated session |
| WebRTC “connecting” forever | NAT type / UDP blocked | Deploy [[TURN server (Traversal Using Relays around NAT)]] |
| Intermittent drop after idle | Mapping timeout too short | Keepalives; raise UDP timeout |
| Wrong client hit behind CGNAT | Shared public IP | App-level auth; don’t trust IP alone |
| Hairpin / LAN→public→LAN fails | Router lacks NAT loopback | Use private DNS / split horizon |

---

## Gotchas

> [!WARNING]
> **NAT is not a firewall** — it hides topology but default-deny inbound is a side effect, not a policy engine.

> [!WARNING]
> **Carrier-grade NAT (CGNAT)** — your “public” IP may be shared by many subscribers; port forwards often impossible.

> [!WARNING]
> **Checksums** — every IP/port rewrite must recalculate IP and TCP/UDP checksums or packets die silently.

---

## When NOT to use

- **End-to-end public addressing** — IPv6 can remove the conservation reason for NAT (firewalls still apply).
- **Protocols that embed IPs in payloads** — SIP/FTP helpers needed; prefer modern designs that don’t.

---

## Related

[[NAT Traversal]] [[ICE (Interactive Connectivity Establishment)]] [[STUN (Session Traversal Utilities for NAT)]] [[TURN server (Traversal Using Relays around NAT)]] [[UDP]] [[TCP]] [[non-Routable address]]
