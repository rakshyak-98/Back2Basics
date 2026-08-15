[[Operating system]] [[Networking]] [[FIB (Forwarding Information Base)]] [[PBR (Policy Based Routing)]] [[CIDR (Classless Inter-Domain Routing)]] [[NAT (Network Address Translation)]] [[ip]] [[route]]

# Routing table

> Kernel data structure mapping destination CIDR → next hop; longest-prefix match wins — **Kerrisk, Linux Programming Interface**.

## Interview Relevance

Interviewers use routing tables to check longest-prefix match, default routes, and whether you can debug with `ip route get` — plus how cloud subnet route tables relate to the Linux `main` table.

## Sources

- [man 8 ip-route](https://man7.org/linux/man-pages/man8/ip-route.8.html) — deep-dive
- [Kerrisk — The Linux Programming Interface (networking chapters)](https://man7.org/tlpi/) — deep-dive
- [Wikipedia — Routing table](https://en.wikipedia.org/wiki/Routing_table) — overview

## Core Definition

Each entry stores a destination prefix and a target (gateway, interface, or local delivery). The kernel picks the most specific matching route; on a tie, the lowest metric wins.

## Key Concepts

- **Longest-prefix match:** `/32` beats `/24` beats `0.0.0.0/0` → not “first match.”
- **Default route:** `0.0.0.0/0` (or `::/0`) → where unknown destinations go.
- **Metric:** tie-breaker among equal prefixes → which path is preferred.
- **Main vs custom tables:** default traffic uses `main`; [[PBR (Policy Based Routing)]] via `ip rule` can steer by source, TOS, or `fwmark`.
- **Ephemeral vs persistent:** `ip route` changes apply now but may vanish on reboot/DHCP; daemons (systemd-networkd, NetworkManager, Netplan) own persistence.

## Technical Details

```
Destination        Gateway         Iface   Metric
10.0.1.0/24        0.0.0.0         eth0    100   ← wins for 10.0.1.5
10.0.0.0/8         10.0.0.1        eth0    100
0.0.0.0/0          192.168.1.1     eth0    100   ← default route
```

Default traffic uses the `main` table. [[PBR (Policy Based Routing)]] via `ip rule` can redirect packets by source IP, TOS, or `fwmark` (from iptables/nftables) into custom tables.

In AWS, every subnet associates with a route table (explicit or VPC main). Public subnets route `0.0.0.0/0` → IGW; private subnets route to NAT Gateway or VPC endpoints.

### View and change routes

```shell
ip route show
ip route show table all          # custom PBR tables
ip rule list
route -n
resolvectl status
cat /etc/resolv.conf
```

```shell
# Host route via gateway
sudo ip route add 10.50.0.0/16 via 10.0.0.1 dev eth0

# Policy: traffic from this source uses table 100
sudo ip rule add from 10.0.2.0/24 table 100
sudo ip route add default via 10.0.2.1 dev eth1 table 100

# NAT masquerade for forwarding (requires ip_forward=1)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Capture routing decisions

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

### Cloud route table mapping

| Concept | AWS VPC | GCP | Azure |
|---------|---------|-----|-------|
| Route table | Per-subnet association | Subnet ↔ route table | Route table ↔ subnet |
| Internet egress | `0.0.0.0/0` → IGW (public) | default route → default internet gateway | `0.0.0.0/0` → Internet |
| Private egress | `0.0.0.0/0` → NAT GW | Cloud NAT | NAT Gateway |
| VPC/VNet internal | Local routes auto | Subnet CIDR local | VNet address space |
| Peering / hybrid | Peering CIDR, TGW, VPN | VPC peering, Cloud VPN | VNet peering, VPN GW |
| Endpoint shortcut | Gateway / Interface VPCE | Private Google Access | Service endpoints |
| CLI inspect | `aws ec2 describe-route-tables` | `gcloud compute routes list` | `az network route-table show` |

**Mental map:** cloud route table ≈ Linux `main` table per subnet; NACLs/security groups are **not** routing — they filter after the routing decision. Related: [[FIB (Forwarding Information Base)]].

## Real-World Applications

Hosts, containers, and cloud VPCs all forward by consulting a route table before a packet leaves an interface.

**Example:** A private subnet cannot reach the internet — missing `0.0.0.0/0` → NAT Gateway in the cloud route table (or wrong subnet association).

## Pros/Cons or Trade-offs

- **Pro:** Longest-prefix match is predictable and scales with [[CIDR (Classless Inter-Domain Routing)]].
- **Con:** Manual `ip route add` fights persistence daemons — DHCP renew or carrier flap can wipe routes silently.
- **Con:** Source-based / PBR paths complicate SNAT and asymmetric return traffic.

## Comparison

- vs [[FIB (Forwarding Information Base)]]: FIB is the forwarding plane’s compiled view; the routing table is the control-plane entries that feed it.
- vs [[PBR (Policy Based Routing)]]: main-table LPM is destination-based; PBR selects an alternate table by policy.
- vs security groups / NACLs: those filter; they do not choose next hops.

## Mistakes to Avoid

- Guessing from `ip route show` alone — use `ip route get <dst>` as the sanity check.
- Hand-editing routes on managed nodes (EKS/GKE) — fix the CNI or cloud route table instead.
- Adding static routes for every microservice — use service discovery/DNS for application-level routing.
- Forgetting Docker/Kubernetes inject routes — CNI restarts can clobber manual entries.
