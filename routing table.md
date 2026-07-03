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