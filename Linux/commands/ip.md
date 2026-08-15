[[routing table]] [[route]] [[Linux network commands]] [[ss]] [[netstat]] [[BGP]]

# ip

> ip (iproute2) configures links, addresses, routes, and neighbors via netlink — the modern replacement for ifconfig/route.

## Interview Relevance
Core networking: `ip route get`, ephemeral vs persisted config, and mapping legacy net-tools to iproute2.

## Sources
- [ip(8)](https://man7.org/linux/man-pages/man8/ip.8.html) — deep-dive
- [iproute2 documentation](https://wiki.linuxfoundation.org/networking/iproute2) — overview

## Core Definition
Network configuration is objects: **link** (interface), **address** (IP on link), **route** (forwarding), **rule** (policy routing). `ip` talks netlink to the kernel. Changes are immediate and often ephemeral unless persisted in Netplan/NM/systemd-networkd.

## Key Concepts
- **link / addr / route / neigh / rule:** Main object families.
- **`ip route get`:** Best debug — shows path and source IP chosen.
- **Ephemeral CLI:** Lost on reboot without a network manager.
- **Policy routing:** Extra tables via `ip rule` — invisible in default `ip route` alone.
- **netns:** Containers = network namespaces + veth.

## Technical Details

| Legacy | iproute2 |
|--------|----------|
| `ifconfig eth0` | `ip addr show dev eth0` |
| `ifconfig eth0 up` | `ip link set eth0 up` |
| `route -n` | `ip route show` |
| `arp -n` | `ip neigh show` |

```bash
ip link show
ip link set dev ens5 up
ip link set dev ens5 mtu 9000
ip -s link show ens5

ip addr show dev ens5
ip addr add 10.0.0.5/24 dev ens5
ip addr del 10.0.0.5/24 dev ens5

ip route show
ip -d route show
ip route show table all
ip rule list
ip route get 8.8.8.8
ip route replace default via 192.168.1.1
ip route add 10.20.0.0/16 via 10.0.0.1 dev eth0

ip neigh show
ip neigh flush dev eth0

ip link add link eth0 name eth0.100 type vlan id 100
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Interface down | `ip link` state | `ip link set up`; check NM/cloud |
| No route to host | `ip route get <dst>` | Add route/default; check link |
| Wrong source IP | `ip route get` `src` | Specific route / policy rule |
| MTU black hole | Large ping fails | Lower MTU; PMTUD |
| Config lost on reboot | Only CLI used | Persist in Netplan/NM/networkd |

## Real-World Applications
Debugging “no route to host,” adding a temporary static route during an incident, and checking RX drops with `ip -s link`.

## Pros/Cons or Trade-offs
- **Pro:** Precise, scriptable, complete netlink surface.
- **Con:** Easy to strand a remote host; changes vanish without persistence.
- **Trade-off:** `add` vs `replace` for idempotent automation.

## Comparison
vs [[ss]]: sockets/process ownership, not L3 config. vs [[route]]: older net-tools; prefer `ip route`. vs firewall/nftables: routes don’t filter.

## Mistakes to Avoid
- Hard-coding `eth0` on cloud images (`ens5`, etc.).
- Ignoring `ip rule` / alternate tables when routes “look right.”
- Changing MTU on live production TCP without a window.
