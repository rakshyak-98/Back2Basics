[[routing table]] [[ip]] [[Linux network commands]] [[netstat]]

# route

> One-line: legacy **net-tools** view of the kernel [[routing table]] — use `ip route` on modern systems; keep `route -n` for quick mental mapping and old scripts. **Kerrisk, Linux Programming Interface**.

## Mental model

The kernel holds one or more **routing tables** (main table by default). Each route maps a destination prefix to a **next hop** (gateway), **outgoing interface**, or local delivery. `route` reads/writes via the old ioctl API; `ip route` uses **netlink** (same API NetworkManager, systemd-networkd, and Cilium use).

```
                    ┌─────────────────┐
  packet ──────────►│ routing table   │──► longest-prefix match
                    │ (main + PBR)    │──► pick gateway + dev
                    └─────────────────┘
                           ▲
              route (net-tools)  │  ip route (iproute2)
```

| Tool | Package | Status on modern distros |
|------|---------|--------------------------|
| `route`, `netstat`, `ifconfig` | net-tools | Deprecated; may be absent |
| `ip`, `ss` | iproute2 | Default; full feature set |

**Translation cheat sheet:**

| net-tools | iproute2 |
|-----------|----------|
| `route -n` | `ip route show` |
| `route add default gw 192.168.1.1` | `ip route add default via 192.168.1.1` |
| `route add -net 10.0.0.0/8 gw 10.0.0.1` | `ip route add 10.0.0.0/8 via 10.0.0.1` |
| `route del default` | `ip route del default` |

## Standard config / commands

```bash
# Quick numeric view (no DNS — always -n under pressure)
route -n

# Same truth, modern tool (preferred)
ip route show
ip -d route show                    # details: mtu, proto, metric

# Which path would a packet take?
ip route get 8.8.8.8
# via 192.168.1.1 dev eth0 src 192.168.1.50 uid 1000

# Default gateway
ip route add default via 192.168.1.1 dev eth0
ip route replace default via 192.168.1.1    # idempotent update

# Static route to a subnet
ip route add 10.20.0.0/16 via 10.0.0.1 dev eth0

# Delete a route
ip route del 10.20.0.0/16
ip route del default

# All tables (PBR)
ip route show table all
ip rule list
```

**Legacy `route` (when net-tools is installed):**

```bash
route -n                              # kernel routing table
route add default gw 192.168.1.1      # ephemeral — lost on reboot
route add -net 172.16.0.0/12 gw 10.0.0.254
```

Persistent routes belong in **NetworkManager**, Netplan, `/etc/systemd/network/`, or cloud-init — not bare CLI on production hosts unless you know they won't reboot.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Network is unreachable" | `ip route show`; `ip route get <dst>` | Add default route or more-specific route |
| Wrong interface used | `ip route get <dst>` | Fix metric; remove conflicting route; check PBR (`ip rule`) |
| Route vanishes after reboot | Was CLI-only | Add to Netplan/NM/systemd-networkd config |
| `route: command not found` | net-tools not installed | Use `ip route`; or `apt install net-tools` if legacy scripts need it |
| Two default routes | `ip route \| grep default` | Remove duplicate; lower metric wins on tie |
| Can ping gateway, not internet | Default route missing/wrong | `ip route replace default via <gw> dev <iface>` |
| Asymmetric routing | `ip route get` from both hosts | Align forward + reverse paths; check [[routing table]] PBR |

## Gotchas

> [!WARNING]
> **`route` and `ip route` changes are ephemeral** — survive until reboot or network manager rewrite. Always trace persistence layer on the host.

> [!WARNING]
> **`-n` on `route` disables DNS for gateway names** — without it, a broken resolver makes `route` hang or mislead during outages.

> [!WARNING]
> **Default route on wrong interface** — common after VPN connect/disconnect or docker0 appearing. Compare `ip route get 1.1.1.1` before and after.

> [!WARNING]
> **`route -n` shows main table only** — policy routing (`ip rule`, custom tables) invisible here. Use [[ip]] `route show table all`.

## When NOT to use

- **New automation or playbooks** → [[ip]] exclusively.
- **Socket/port debugging** → [[ss]], not route.
- **DNS resolution issues** → `resolvectl`, `/etc/resolv.conf` — routing is L3, not name lookup.
- **Cloud VPC routing** → AWS route tables / GCP routes — host table is only one layer.

## Related

[[routing table]] [[ip]] [[Linux network commands]] [[netstat]] [[ss]] [[BGP]]
