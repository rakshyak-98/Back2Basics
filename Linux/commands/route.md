[[routing table]] [[ip]] [[Linux network commands]] [[netstat]] [[ss]] [[BGP]]

# route

> Legacy net-tools view of the kernel [[routing table]] — prefer `ip route` on modern systems.

```txt
        route ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Shows you know longest-prefix match, default routes, and that `route` is depr…

## Sources
- [man ip-route](https://man7.org/linux/man-pages/man8/ip-route.8.html) — deep-dive
- [Wikipedia — route (command)](https://en.wikipedia.org/wiki/Route_(command)) — overview

## Key Concepts
- **Default route:** `0.0.0.0/0` — no default usually means no internet.
- **Metric:** lower metric wins among equal prefixes.
- **Ephemeral CLI changes:** lost on reboot unless Netplan/NM/systemd-networkd persists them.
- **Policy routing:** `ip rule` + extra tables — invisible to plain `route -n`.


- **Core:** The kernel holds routing tables (main by default). Each route maps a destinat…

## Technical Details
```
                    ┌─────────────────┐
  packet ──────────►│ routing table   │──► longest-prefix match
                    │ (main + PBR)    │──► pick gateway + dev
                    └─────────────────┘
                           ▲
              route (net-tools)  │  ip route (iproute2)
```

| net-tools | iproute2 |
|-----------|----------|
| `route -n` | `ip route show` |
| `route add default gw 192.168.1.1` | `ip route add default via 192.168.1.1` |
| `route add -net 10.0.0.0/8 gw 10.0.0.1` | `ip route add 10.0.0.0/8 via 10.0.0.1` |
| `route del default` | `ip route del default` |

```bash
route -n
ip route show
ip -d route show
ip route get 8.8.8.8
ip route add default via 192.168.1.1 dev eth0
ip route replace default via 192.168.1.1
ip route add 10.20.0.0/16 via 10.0.0.1 dev eth0
ip route del 10.20.0.0/16
ip route show table all
ip rule list
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Network is unreachable | `ip route show`; `ip route get <dst>` | Add default or more-specific route |
| Wrong interface used | `ip route get <dst>` | Fix metric; remove conflict; check `ip rule` |
| Route vanishes after reboot | Was CLI-only | Persist in Netplan/NM/systemd-networkd |
| `route: command not found` | net-tools missing | Use `ip route` |
| Two default routes | `ip route \| grep default` | Remove duplicate; lower metric wins |

## Mistakes to Avoid
- **Mistake:** Changing routes only on the CLI and expecting them to survive re…
- **Mistake:** Omitting `-n` so a broken resolver hangs `route`
- **Mistake:** Believing `route -n` shows all tables when policy routing is in …

## Pros/Cons or Trade-offs
- **Pro:** Short mental model (`route -n`) on ancient hosts.
- **Con:** Incomplete for policy routing; often not installed; wrong tool for new automation.

## Comparison
- vs [[ip]]: full feature set and persistence story — use for all new work.
- vs [[routing table]]: the kernel data structure; `route`/`ip route` are the CLI.


### Use cases
- Debugging “can ping gateway but not internet,” VPN leftover defaults, and tra…

- **Example:** After Docker or VPN churn, `ip route get 1.1.1.1` shows traffic …
