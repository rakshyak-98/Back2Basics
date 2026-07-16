[[Operating system]] [[Networking]] [[FIB (Forwarding Information Base)]] [[PBR (Policy Based Routing)]]

routing table -> is a data structure that stores routes for network traffic, mapping destination IP ranges (CIDR blocks) to next hops (targets).
Structure -> Each entry contains a destination CIDR and a target (where to send matching traffic).
Matching rule -> Most specific match winds. A `/32` route takes precedence over a `/24`, which takes precedence over `/0`.

> [!INFO]
> In AWS, every subnet is associated with a route table (explicit or the VPC's main route table). Route tables determine whether a subnet is public (route to IGW) or private (route to NAT Gateway or none).

view DNS server configurations

```shell
cat /etc/resolv.conf;
resolvectl status;
ip route show;
route -n;
netstat -nr;
```

```shell
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE;
```

## Linux Kernel Routing

Linux Kernel Routing uses the Forwarding Information Base (FIB) and is managed via the `iproute2` suite

The Kernel resolves paths using longest prefix match. When prefix lengths tie, the route with the lowest metric wins. By default, traffic uses the `main` routing table.

Policy-Based Routing (PBR) decouples routing  from the destination IP. Using `ip rule`, you can route packets based on source address, TOS, or firewall marks (`fwmark` from iptables/nftables) by directing them to custom routing tables.

Configuration happens in two tiers: ephemeral kernel state via `ip` CLI, and persistent state managed by a network daemon (systemd-networkd, NetworkManager, or Netplan). Direct CLI changes take effect instantly but vanish or reboot or interface link-state changes.

> [!WARNING]
> Persistence Daemon Overwrites: Manually inserting routes via `ip route add` while systemd-netword or Networkmanager controls the link. A DHCP lease renewal or carrier flap triggers the daemon to synchronize state, wiping your manual kernel routes and causing silent failures.