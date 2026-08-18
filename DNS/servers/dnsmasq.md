[[DNS]] [[DNS server]] [[TFTP]] [[Unbound]] [[CoreDNS]] [[BIND]]

# dnsmasq

> dnsmasq — small DNS forwarder/cache plus DHCP (and optional TFTP) — the usual brain of home routers and tiny lab networks.

## Mental model

**Say it in one breath:** Clients use dnsmasq as their DNS; it answers local names / DHCP hostnames from cache and forwards the rest upstream — often the same process that handed out the DHCP lease.

```txt
LAN client → dnsmasq :53
               ├─ local A / DHCP name → answer
               └─ everything else → upstream resolvers (cache on the way back)
             dnsmasq :67 DHCP  (+ optional [[TFTP]] for PXE)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Forwarder + cache** | Not full recursive from root by default | “It asks 1.1.1.1 and remembers.” |
| --- | --- | --- |
| **DHCP integration** | Lease → local DNS name | “phone.lan resolves because DHCP told dnsmasq.” |
| **address= / host-record** | Static local overrides | “Force `foo.test` to 10.0.0.5.” |
| **server=** | Upstream or conditional forward | “Send `*.corp` to 10.1.1.10.” |
| **PXE** | DHCP options + TFTP root | “dnsmasq can boot VMs off the LAN.” |

### When to pick what

| Need | Tool |
| --- | --- |
| Router / homelab / libvirt | **dnsmasq** |
| Validating recursive | [[Unbound]] |
| Kubernetes | [[CoreDNS]] |
| Big authoritative | [[BIND]] / PowerDNS |

## Standard config / commands

```txt
# /etc/dnsmasq.d/lab.conf
domain=lab.local
expand-hosts
interface=eth0
dhcp-range=10.0.0.50,10.0.0.150,12h
dhcp-option=option:router,10.0.0.1
server=1.1.1.1
server=/corp.example/10.1.1.10
address=/whoami.lab.local/10.0.0.20
# enable-tftp
# tftp-root=/srv/tftp
```

```bash
dnsmasq --test
systemctl restart dnsmasq
dig @10.0.0.1 whoami.lab.local
journalctl -u dnsmasq -f
```

| Knob | Why it matters |

| `interface=` / `bind-interfaces` | Avoid answering on the wrong NIC |
| --- | --- |
| `server=` order | Bad upstream = whole LAN “no internet” |
| DHCP range vs static | Overlaps cause duplicate IP fights |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| DHCP works, DNS doesn’t | Listen 53 / conflict with systemd-resolved | Stop conflict; bind dnsmasq correctly |
| Local names NXDOMAIN | `expand-hosts` / domain | Fix domain; check `/etc/hosts` + leases |
| External NX / timeout | Upstream `server=` | Fix forwarders; test `dig @1.1.1.1` |
| Duplicate IP | Range overlap | Shrink DHCP range; reserve MACs |
| PXE file not found | TFTP root / filename options | Align DHCP boot file with [[TFTP]] tree |
| Intermittent wrong answer | Stale cache | Restart or `sighup`; shorten local TTLs |

## Gotchas

> [!WARNING]
> **Fight with NetworkManager / systemd-resolved** — two listeners on :53; only one wins.

> [!WARNING]
> **`.local` and mDNS** — using `.local` as DHCP DNS domain collides with [[mDNS]] on many OSes; prefer `lab.home` / `lan`.

> [!WARNING]
> **dnsmasq is not DNSSEC-validating recursive by default** — don’t pretend it’s [[Unbound]].

## When NOT to use

- **ISP-scale recursion or DNSSEC-heavy resolvers** — [[Unbound]].
- **Multi-tenant authoritative DNS with APIs** — PowerDNS ([[PoserDNS]]).
- **Kubernetes cluster DNS** — [[CoreDNS]].

## Related

[[DNS]] [[DNS server]] [[TFTP]] [[Unbound]] [[CoreDNS]] [[BIND]] [[PoserDNS]] [[mDNS]] [[name server]]
