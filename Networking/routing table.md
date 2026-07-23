[[Operating system]] [[Networking]] [[FIB (Forwarding Information Base)]] [[PBR (Policy Based Routing)]] [[CIDR (Classless Inter-Domain Routing)]]

# Routing table

> One-line: kernel data structure mapping destination CIDR → next hop; longest-prefix match wins — **Kerrisk, Linux Programming Interface**.

## Mental model

Each entry stores a **destination prefix** and a **target** (gateway, interface, or local delivery). The kernel picks the **most specific** matching route; on tie, lowest **metric** wins.

```
Destination        Gateway         Iface   Metric
10.0.1.0/24        0.0.0.0         eth0    100   ← wins for 10.0.1.5
10.0.0.0/8         10.0.0.1        eth0    100
0.0.0.0/0          192.168.1.1     eth0    100   ← default route
```

Default traffic uses the `main` table. [[PBR (Policy Based Routing)]] via `ip rule` can redirect packets by source IP, TOS, or `fwmark` (from iptables/nftables) into custom tables.

Configuration is two-tier: ephemeral kernel state (`ip route`) and persistent state (systemd-networkd, NetworkManager, Netplan). CLI changes apply instantly but may vanish on reboot or link flap.

> [!INFO]
> In AWS, every subnet associates with a route table (explicit or VPC main). Public subnets route `0.0.0.0/0` → IGW; private subnets route to NAT Gateway or VPC endpoints.

## Standard config / commands

View routes and DNS resolver (often confused during triage):

```shell
ip route show
ip route show table all          # custom PBR tables
ip rule list
route -n
resolvectl status
cat /etc/resolv.conf
```

Add ephemeral routes:

```shell
# Host route via gateway
sudo ip route add 10.50.0.0/16 via 10.0.0.1 dev eth0

# Policy: traffic from this source uses table 100
sudo ip rule add from 10.0.2.0/24 table 100
sudo ip route add default via 10.0.2.1 dev eth1 table 100

# NAT masquerade for forwarding (requires ip_forward=1)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

Capture routing decisions with tcpdump:

```shell
# Confirm which interface carries traffic to a destination
ip route get 203.0.113.50

# Watch packets leave the expected interface (replace eth0)
sudo tcpdump -ni eth0 host 203.0.113.50 -c 20

# ICMP unreachable / no route (blackhole detection)
sudo tcpdump -ni any 'icmp[icmptype] == 3' -v

# Asymmetric routing hint: SYN on eth0, SYN-ACK on eth1
sudo tcpdump -ni any 'tcp[tcpflags] & tcp-syn != 0' and host <peer-ip>

# Trace path MTU issues (Fragmentation Needed)
sudo tcpdump -ni any 'icmp[icmptype] == 3 and icmp[3] == 4' -v
```

## Cloud route table mapping

| Concept | AWS VPC | GCP | Azure |
|---------|---------|-----|-------|
| Route table | Per-subnet association | Subnet ↔ route table | Route table ↔ subnet |
| Internet egress | `0.0.0.0/0` → IGW (public) | default route → default internet gateway | `0.0.0.0/0` → Internet |
| Private egress | `0.0.0.0/0` → NAT GW | Cloud NAT | NAT Gateway |
| VPC/VNet internal | Local routes auto | Subnet CIDR local | VNet address space |
| Peering / hybrid | Peering CIDR, TGW, VPN | VPC peering, Cloud VPN | VNet peering, VPN GW |
| Endpoint shortcut | Gateway / Interface VPCE | Private Google Access | Service endpoints |
| CLI inspect | `aws ec2 describe-route-tables` | `gcloud compute routes list` | `az network route-table show` |

**Mental map:** cloud route table = Linux `main` table per subnet; NACLs/security groups are **not** routing — they filter after routing decision.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Host unreachable to one subnet | `ip route get <dst>` | Missing or wrong route; add via correct gateway |
| Works from host A, not host B | Compare `ip route` + security groups/NACLs | Asymmetric routing or SG blocking return path |
| Route "disappeared" after DHCP renew | `journalctl -u systemd-networkd` / NM logs | Daemon overwrote manual route → make persistent in net config |
| Ping works, TCP fails | `tcpdump` both directions; check MTU / [[MTU (Maximum Transmission Unit)]] | PMTU blackhole; lower MSS or fix middlebox |
| Traffic exits wrong interface | `ip route get <dst>` shows unexpected `dev` | Metric conflict or PBR rule; `ip rule list` |
| New pod/VM can't reach metadata or DNS | Cloud route table + `/etc/resolv.conf` | Missing VPC endpoint route or wrong subnet association |
| Intermittent 5–30s delays | `ip route show cache` / conntrack | Stale nexthop cache; check gateway ARP |
| `RTNETLINK answers: File exists` | Duplicate route entry | `ip route replace` or delete first |

> [!WARNING]
> **Persistence daemon overwrites:** Manually inserting routes via `ip route add` while systemd-networkd or NetworkManager controls the link — a DHCP lease renewal or carrier flap triggers the daemon to sync state, wiping manual kernel routes and causing **silent failures**.

## Gotchas

- **Longest prefix wins**, not "first match" — `/32` beats `/24` beats `0.0.0.0/0`.
- **`ip route get`** is the fastest sanity check; don't guess from `ip route show` alone.
- **Source-based routing** bites during SNAT: reply may leave a different interface than request arrived on.
- **Docker/K8s** inject routes into `main` or custom tables; CNI plugins can clobber manual entries on restart.

## When NOT to use

- Don't hand-edit routes on managed instances (EKS nodes, GKE nodes) — fix the CNI/cloud route table instead.
- Don't add static routes for every microservice; use service mesh or DNS-based discovery for app-level routing.

## Related

[[FIB (Forwarding Information Base)]] · [[PBR (Policy Based Routing)]] · [[NAT (Network Address Translation)]] · [[CIDR (Classless Inter-Domain Routing)]] · [[ip]] · [[route]]
