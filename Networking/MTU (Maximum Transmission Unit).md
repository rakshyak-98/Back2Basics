[[Networking]] [[Packet Fragment]] [[TCP]] [[UDP]]

# MTU (Maximum Transmission Unit)

> MTU is the largest IP packet a link will take without splitting — exceed it and you fragment or drop.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Each hop has a max frame/payload size; your path MTU is the smallest MTU along the route.

```txt
App payload 4000 B, Ethernet MTU 1500
    │
    ├── frame ≤ 1500   (or fragment)
    ├── frame ≤ 1500
    └── remainder
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MTU** | Max packet size on a link | “Ethernet classic is 1500 bytes.” |
| **Path MTU** | Min MTU across the whole path | “VPN/tunnels often shrink it.” |
| **DF bit** | Don’t Fragment | “If DF set and too big → drop + ICMP needfrag.” |
| **MSS** | TCP max segment size | “MSS ≈ MTU − IP/TCP headers.” |
| **Jumbo frames** | MTU > 1500 (e.g. 9000) | “Only if every hop agrees.” |

### Common values

| Link | Typical MTU |
|------|-------------|
| Ethernet | 1500 |
| PPPoE | 1492 |
| WireGuard / many VPNs | ~1420 (varies) |
| Jumbo LAN | 9000 (must be end-to-end) |

---

## Standard config / commands

```bash
# Interface MTU
ip link show eth0
ip link set dev eth0 mtu 1500

# Path MTU discovery probe (Linux)
ping -M do -s 1472 8.8.8.8    # 1472 + 28 = 1500; lower -s until it works

# Trace where size fails
tracepath <host>              # or traceroute --mtu
```

| Knob | Why it matters |
|------|----------------|
| Interface MTU | Local send size before kernel fragments / fails |
| TCP MSS clamp | Routers/firewalls rewrite MSS so TCP never exceeds path |
| VPN MTU | Tunnel headers eat bytes — lower inner MTU or clamp MSS |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Small packets work, large hang | `ping -M do -s …` | Lower MTU / enable PMTUD; fix ICMP blackhole |
| VPN OK for SSH, not for HTTPS uploads | Path MTU vs tunnel overhead | Set tunnel MTU ~1280–1420; MSS clamp |
| Jumbo “works” then random peers fail | One hop still 1500 | Use 1500 unless full path is jumbo |
| Blackhole (silent drop) | ICMP “frag needed” blocked | Allow ICMP type 3 code 4; or clamp MSS |

---

## Gotchas

> [!WARNING]
> **PMTUD needs ICMP** — block “unreachable” and DF packets die with no useful error.

> [!WARNING]
> **MTU is not payload size** — 1500 includes IP header; TCP data is smaller (MSS).

> [!WARNING]
> **Cloud + overlay** — VXLAN/Geneve/WireGuard add headers; copy-paste 1500 from bare metal and wonder why transfers stall.

---

## When NOT to use

- **Jumbo frames on mixed internet paths** — internet is not 9000 end-to-end.
- **Raising MTU to “go faster” without measuring** — fix loss/congestion first; MTU is rarely the first lever.
- **Ignoring MSS when TCP is the workload** — clamp MSS at the edge instead of hoping fragments work.

---

## Related

[[Networking]] [[Packet Fragment]] [[ICMP]] [[TCP]] [[UDP]]
