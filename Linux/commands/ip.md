[[routing table]] [[route]] [[Linux network commands]] [[ss]] [[netstat]]

# ip

> One-line: **iproute2** Swiss army knife — links, addresses, routes, neighbors, tunnels. **Modern replacement for ifconfig/route/netstat.** Kerrisk.

## Mental model

Network config is objects: **link** (interface), **address** (IP on link), **route** (forwarding decision), **rule** (PBR). `ip` talks netlink to the kernel — same API NetworkManager and Cilium use. Changes are **immediate** and often **ephemeral** unless persisted in Netplan/NM/systemd-networkd.

```
ip link ──► iface up/down, mtu, master (bond/bridge)
ip addr ──► IPv4/IPv6 on link
ip route ──► [[routing table]] entries
ip rule ──► policy routing
ip neigh ──► ARP/NDP cache
```

| Legacy (net-tools) | iproute2 |
|--------------------|----------|
| `ifconfig eth0` | `ip addr show dev eth0` |
| `ifconfig eth0 up` | `ip link set eth0 up` |
| `route -n` | `ip route show` |
| `arp -n` | `ip neigh show` |
| `netstat -rn` | `ip route` + [[ss]] |

## Standard config / commands

**Links:**

```bash
ip link show
ip link show ens5
ip link set dev ens5 up
ip link set dev ens5 down
ip link set dev ens5 mtu 9000          # jumbo frames — switch must match
ip -s link show ens5                   # RX/TX stats (drops, errors)
```

**Addresses:**

```bash
ip addr show dev ens5
ip addr add 10.0.0.5/24 dev ens5
ip addr del 10.0.0.5/24 dev ens5
```

**Routing:**

```bash
ip route show
ip -d route show                      # proto, metric, mtu detail
ip route show table all
ip rule list

# Which path for this destination? — best debug command
ip route get 8.8.8.8
# 8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.50 uid 1000

# Default gateway
ip route add default via 192.168.1.1 dev eth0
ip route replace default via 192.168.1.1

# Static subnet route
ip route add 10.20.0.0/16 via 10.0.0.1 dev eth0
ip route del 10.20.0.0/16
```

**Neighbors (ARP):**

```bash
ip neigh show
ip neigh flush dev eth0               # careful — brief connectivity blip
```

**Bridge/VLAN (common in servers):**

```bash
ip link add link eth0 name eth0.100 type vlan id 100
ip link set dev eth0.100 up
```

**Monitor traffic counters:**

```bash
watch -n1 'ip -s link show ens5'
sar -n DEV 1 5                        # needs sysstat
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Interface down | `ip link` `state DOWN` | `ip link set dev X up`; check NM/cloud config |
| No route to host | `ip route get <dst>` | Add route or default gw; check link local |
| Wrong source IP chosen | `ip route get` shows `src` | More specific route; policy rule |
| MTU black hole | Large ping fails, small ok | `ip link set mtu 1500`; path MTU discovery |
| ARP failures | `ip neigh` INCOMPLETE | Cable/gw down; stale neigh flush |
| Config lost on reboot | Only `ip` CLI used | Persist in Netplan/NM/systemd-networkd |
| Stats show drops/errors | `ip -s link` | Driver/firmware; ring buffer; [[ss]] for app backlog |

## Gotchas

> [!WARNING]
> **`ip route add` without `replace`** — duplicate routes error or coexist confusingly. Use `replace` for idempotent scripts.

> [!WARNING]
> **Cloud ENI naming** — `ens5`, `eth0` varies. Scripts must discover via `ip route get $(dig +short example.com)` not hardcoded names.

> [!WARNING]
> **Policy routing invisible in `ip route` alone** — check `ip rule list` and `table all`.

> [!WARNING]
> **Changing MTU on live TCP** — can reset connections. Maintenance window for production NICs.

## When NOT to use

- **Socket/process ownership** → [[ss]] `-lntp`.
- **DNS resolution** → `resolvectl`, `dig` — `ip` is L3.
- **Firewall** → nftables/iptables — routes don't filter packets.
- **Persistent prod networking** → config management, not ad-hoc CLI only.

## Related

[[routing table]] [[route]] [[Linux network commands]] [[ss]] [[netstat]] [[BGP]]
